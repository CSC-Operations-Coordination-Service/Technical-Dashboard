"""Collect SAR-MPC Quality Disclaimers by scraping https://sar-mpc.eu/disclaimers/

The collector walks the paginated HTML listing, opens each disclaimer detail
page, extracts every field shown there (the *last modified* date is the database
reference), downloads the attached PDF report and extracts its content with the
MPC PDF parser. Each disclaimer is emitted as a single JSON document mapped to
the raw-data model by a ``JSONExtractor``.
"""

from dataclasses import dataclass, field

from maas_collector.rawdata.collector.httpcollector import (
    HttpCollector,
    HttpCollectorConfiguration,
    HttpConfiguration,
)

from maas_collector.rawdata.collector.httpmixin import HttpMixin

from maas_collector.rawdata.collector.disclaimer.v1_impl import (
    DisclaimerQueryV1Implementation,
)


@dataclass
class DisclaimerCollectorConfiguration(HttpCollectorConfiguration):
    """Configuration for the SAR-MPC Quality Disclaimer collector"""

    # attribute used as database reference / journal date: the disclaimer's
    # "last modified" timestamp shown in the listing and detail page
    date_attr: str = "last_modified"

    # time interval between two refreshes of this interface, in minutes
    refresh_interval: int = 1440

    # offset (minutes) subtracted from the collection end date
    end_date_time_offset: int = 0

    # path (relative to product_url) of the disclaimers listing page
    listing_path: str = "/disclaimers/"

    # maximum number of listing pages to walk per run (0 = no limit)
    page_limit: int = 0

    # when True, stop paginating as soon as a listing page contains only
    # disclaimers already collected (last_modified <= journal date)
    stop_on_seen: bool = True

    # optional explicit list of disclaimer ids to collect (overrides the
    # listing walk); handy for targeted (re)collection and testing
    disclaimer_ids: list = None

    # keep the downloaded PDF files on disk (debug)
    keep_pdf: bool = False

    protocol_version: str = "v1"


@dataclass
class DisclaimerConfiguration(HttpConfiguration):
    """Store Disclaimer runtime (CLI) configuration vars"""


class DisclaimerCollector(HttpCollector, HttpMixin):
    """A collector that scrapes SAR-MPC Quality Disclaimers from the web site."""

    CONFIG_CLASS = DisclaimerCollectorConfiguration

    IMPL_DIR = {"v1": DisclaimerQueryV1Implementation}

    @classmethod
    def build_probe_query(cls, config: DisclaimerCollectorConfiguration):
        """Build the URL used by the health probe to check the site is reachable.

        Args:
            config (DisclaimerCollectorConfiguration): collector configuration

        Returns:
            str: the disclaimers listing URL
        """
        return f"{config.get_config_product_url()}{config.listing_path}"

    @classmethod
    def document(cls, config: DisclaimerCollectorConfiguration):
        information = super().document(config)
        information |= {
            "protocol": "HTTP(S)",
        }
        return information
