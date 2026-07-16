"""SAR-MPC Quality Disclaimer collector - v1 implementation.

Walks the paginated disclaimers listing, opens each disclaimer detail page,
downloads its PDF report and yields one combined JSON document per disclaimer.
"""
import datetime
import os
import re
import tempfile
import typing

from bs4 import BeautifulSoup
from requests import RequestException

from maas_collector.rawdata.collector.disclaimer.query_strategy import (
    AbstractDisclaimerQueryStrategy,
)
from maas_collector.rawdata.collector.disclaimer import pdf_extract


_LISTING_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$")


class DisclaimerQueryV1Implementation(AbstractDisclaimerQueryStrategy):
    """Scrape https://sar-mpc.eu/disclaimers/ (v1 site layout)."""

    def __iter__(self):
        """Yield one JSON document per collected disclaimer."""
        if self.disclaimer_ids:
            yield from self._iter_explicit_ids()
            return

        yield from self._iter_listing()

    # ------------------------------------------------------------------ #
    # Iteration modes
    # ------------------------------------------------------------------ #
    def _iter_explicit_ids(self):
        """Collect only the disclaimer ids listed in the configuration."""
        for raw_id in self.disclaimer_ids:
            if self.collector.should_stop_loop:
                break
            try:
                disclaimer_id = int(raw_id)
            except (TypeError, ValueError):
                self.logger.warning("Ignoring invalid disclaimer id: %r", raw_id)
                continue

            document = self._collect_disclaimer(disclaimer_id)
            if document:
                self._current_id = disclaimer_id
                yield document

    def _iter_listing(self):
        """Walk the paginated listing, newest first, honouring incremental limits."""
        start_naive = self._to_naive_utc(self.start_date)
        self.logger.info(
            "[%s] Collecting disclaimers modified after %s",
            self.interface_name,
            start_naive,
        )

        page = 1
        collected = 0
        while True:
            if self.collector.should_stop_loop:
                break
            if self.page_limit and page > self.page_limit:
                self.logger.info("Reached page limit (%s): stopping", self.page_limit)
                break

            rows = self._fetch_listing_rows(page)
            if not rows:
                self.logger.info("No more disclaimers on page %s: stopping", page)
                break

            new_in_page = 0
            for row in rows:
                if self.collector.should_stop_loop:
                    break

                last_modified = row.get("last_modified_dt")
                if (
                    start_naive is not None
                    and last_modified is not None
                    and last_modified <= start_naive
                ):
                    # already collected on a previous run
                    continue

                document = self._collect_disclaimer(
                    row["disclaimer_id"], listing_row=row
                )
                if document:
                    self._current_id = row["disclaimer_id"]
                    new_in_page += 1
                    collected += 1
                    yield document

            if self.stop_on_seen and new_in_page == 0:
                self.logger.info(
                    "No new disclaimers on page %s: stopping pagination", page
                )
                break

            page += 1

        self.logger.info(
            "[%s] Collected %d disclaimer(s)", self.interface_name, collected
        )

    # ------------------------------------------------------------------ #
    # HTTP helpers
    # ------------------------------------------------------------------ #
    def _http_get(self, url: str, *, stream: bool = False):
        """GET a URL with the collector session, raising on non-2xx status."""
        headers = self.authentication.get_headers()
        response = self.http_session.get(
            url,
            headers=headers,
            timeout=self.collector.http_config.timeout,
            stream=stream,
        )
        if not 200 <= response.status_code < 300:
            raise ValueError(f"Error querying {url}: HTTP {response.status_code}")
        return response

    def _fetch_listing_rows(self, page: int) -> typing.List[dict]:
        """Fetch and parse one listing page into a list of row dicts."""
        url = f"{self.product_url}{self.listing_path}"
        params_suffix = f"?page={page}" if page > 1 else ""
        try:
            response = self._http_get(f"{url}{params_suffix}")
        except (RequestException, ValueError) as error:
            self.logger.error("[SKIP] Cannot fetch listing page %s: %s", page, error)
            return []
        return self._parse_listing(response.text)

    # ------------------------------------------------------------------ #
    # Disclaimer collection
    # ------------------------------------------------------------------ #
    def _collect_disclaimer(
        self, disclaimer_id: int, listing_row: dict = None
    ) -> typing.Optional[dict]:
        """Fetch a disclaimer detail page + PDF and build its JSON document."""
        detail_url = f"{self.product_url}{self.listing_path}{disclaimer_id}/"
        self.logger.info("Collecting disclaimer #%s (%s)", disclaimer_id, detail_url)

        try:
            response = self._http_get(detail_url)
        except (RequestException, ValueError) as error:
            self.logger.error(
                "[SKIP] Cannot fetch disclaimer #%s: %s", disclaimer_id, error
            )
            return None

        properties, pdf_href, pdf_name = self._parse_detail(response.text)

        document = {
            # emit as string so the OpenSearch document id is "399" (matching the
            # bulk-response id) and the per-document journal callback fires; the
            # value is still coerced into the Integer model field on indexing
            "disclaimer_id": str(disclaimer_id),
            "detail_url": detail_url,
            "last_modified": self._to_iso(properties.get("last modified")),
            "mission": properties.get("mission"),
            "description": properties.get("description"),
            "product_quality_status": properties.get("product quality status"),
            "degradation_percentage": properties.get("degradation percentage"),
            "validity_start": self._to_iso(properties.get("validity start")),
            "validity_stop": self._to_iso(properties.get("validity stop")),
            "product_types": self._split_product_types(
                properties.get("product types")
            ),
            "pdf_filename": pdf_name,
            "pdf_url": None,
            "pdf_metadata": None,
            "pdf": None,
        }

        if pdf_href:
            pdf_url = self._absolute_url(pdf_href)
            document["pdf_url"] = pdf_url
            pdf_result = self._download_and_extract_pdf(pdf_url, pdf_name, disclaimer_id)
            if pdf_result:
                document["pdf_metadata"] = pdf_result.get("metadata")
                document["pdf"] = pdf_result.get("structured")
        else:
            self.logger.warning(
                "No PDF report found on disclaimer #%s", disclaimer_id
            )

        return document

    def _download_and_extract_pdf(
        self, pdf_url: str, pdf_name: str, disclaimer_id: int
    ) -> typing.Optional[dict]:
        """Download a disclaimer PDF to a temp file and run the MPC parser."""
        try:
            response = self._http_get(pdf_url, stream=True)
        except (RequestException, ValueError) as error:
            self.logger.error(
                "[SKIP] Cannot download PDF for disclaimer #%s: %s",
                disclaimer_id,
                error,
            )
            return None

        working_dir = self.collector.args.working_directory
        os.makedirs(working_dir, exist_ok=True)
        fd, tmp_path = tempfile.mkstemp(
            suffix=".pdf", prefix=f"QD-{disclaimer_id}_", dir=working_dir
        )
        try:
            with os.fdopen(fd, "wb") as tmp_file:
                for chunk in response.iter_content(chunk_size=65536):
                    if chunk:
                        tmp_file.write(chunk)

            return pdf_extract.extract_pdf(tmp_path)
        except Exception as error:  # pylint: disable=broad-except
            self.logger.error(
                "[SKIP] Failed to extract PDF %s for disclaimer #%s: %s",
                pdf_name,
                disclaimer_id,
                error,
            )
            return None
        finally:
            if not self.keep_pdf:
                try:
                    os.remove(tmp_path)
                except OSError:
                    pass
            else:
                self.logger.debug("Kept PDF file %s", tmp_path)

    # ------------------------------------------------------------------ #
    # HTML parsing
    # ------------------------------------------------------------------ #
    def _parse_listing(self, html: str) -> typing.List[dict]:
        """Parse a listing page table into a list of row dicts."""
        soup = BeautifulSoup(html, "html.parser")
        table = soup.find("table")
        if table is None:
            return []

        headers = [th.get_text(strip=True).lower() for th in table.find_all("th")]

        rows: typing.List[dict] = []
        for tr in table.find_all("tr"):
            cells = tr.find_all("td")
            if not cells:
                # header row
                continue

            values = [td.get_text(" ", strip=True) for td in cells]
            row = dict(zip(headers, values)) if headers else {}

            link = cells[0].find("a")
            disclaimer_id = None
            if link and link.get("href"):
                match = re.search(r"(\d+)", link["href"])
                if match:
                    disclaimer_id = int(match.group(1))
            if disclaimer_id is None:
                continue

            row["disclaimer_id"] = disclaimer_id
            row["last_modified_dt"] = self._parse_dt(row.get("last modified"))
            rows.append(row)

        return rows

    def _parse_detail(
        self, html: str
    ) -> typing.Tuple[dict, typing.Optional[str], typing.Optional[str]]:
        """Parse a disclaimer detail page: property/value table + PDF link."""
        soup = BeautifulSoup(html, "html.parser")
        table = soup.find("table")
        properties: dict = {}
        pdf_href = None
        pdf_name = None

        if table is None:
            return properties, pdf_href, pdf_name

        for tr in table.find_all("tr"):
            cells = tr.find_all("td")
            if len(cells) != 2:
                continue
            key = cells[0].get_text(" ", strip=True).lower()
            link = cells[1].find("a")
            if link and link.get("href"):
                pdf_href = link["href"]
                pdf_name = link.get_text(strip=True)
                properties[key] = pdf_name
            else:
                properties[key] = cells[1].get_text(" ", strip=True)

        return properties, pdf_href, pdf_name

    # ------------------------------------------------------------------ #
    # Small utilities
    # ------------------------------------------------------------------ #
    def _absolute_url(self, href: str) -> str:
        """Resolve a possibly-relative href against the site product_url."""
        if href.startswith("http://") or href.startswith("https://"):
            return href
        return f"{self.product_url}{href}"

    @staticmethod
    def _split_product_types(value: typing.Optional[str]) -> typing.Optional[list]:
        if not value:
            return None
        return value.split()

    @staticmethod
    def _to_iso(value: typing.Optional[str]) -> typing.Optional[str]:
        """Convert 'YYYY-MM-DD HH:MM:SS' (UTC on the SAR-MPC site) to ISO 8601.

        The 'Z' suffix marks the value as UTC so ZuluDate does not reinterpret a
        naive timestamp in the host's local timezone. Non-date values are
        returned unchanged.
        """
        if not value:
            return None
        value = value.strip()
        if _LISTING_DATE_RE.match(value):
            return value.replace(" ", "T") + "Z"
        return value

    @staticmethod
    def _parse_dt(value: typing.Optional[str]) -> typing.Optional[datetime.datetime]:
        if not value:
            return None
        try:
            return datetime.datetime.strptime(value.strip(), "%Y-%m-%d %H:%M:%S")
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _to_naive_utc(
        value: typing.Optional[datetime.datetime],
    ) -> typing.Optional[datetime.datetime]:
        """Return a tz-naive UTC datetime for comparison with listing dates."""
        if value is None:
            return None
        if value.tzinfo is not None:
            return value.astimezone(datetime.timezone.utc).replace(tzinfo=None)
        return value
