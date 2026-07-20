"""Stamp products impacted by a SAR-MPC Quality Disclaimer with a known_issue reference.

Triggered after a CdsQualityDisclaimer is consolidated: for every product name
listed in the disclaimer, the matching cds-product document(s) get their
``known_issue`` field set to the disclaimer id.
"""
import typing

from maas_engine.engine.rawdata import DataEngine

from maas_cds.model import CdsProduct
from maas_cds.lib.parsing_name.utils import generate_publication_names


class QualityDisclaimerKnownIssueEngine(DataEngine):
    """Propagate a quality-disclaimer id onto the products it lists.

    Input documents are ``CdsQualityDisclaimer`` (resolved from the message).
    Output documents are ``CdsProduct`` (the impacted products), so this engine
    writes to a different index than its input.
    """

    ENGINE_ID = "COMPUTE_QUALITY_DISCLAIMER_KNOWN_ISSUE"

    # terms queries are chunked to stay well under OpenSearch clause limits
    _NAME_QUERY_CHUNK = 1024

    def __init__(self, args=None, send_reports=False, chunk_size=0):
        # send_reports defaults to False: stamping products must not re-trigger the
        # whole product pipeline (completeness, datatake, ...).
        super().__init__(args, send_reports=send_reports, chunk_size=chunk_size)

    def action_iterator(self) -> typing.Iterator[dict]:
        """Yield bulk actions stamping known_issue on the impacted products."""
        # dedup products across disclaimers/variants within a single run
        impacted: dict = {}

        for disclaimer in self.input_documents:
            if disclaimer is None:
                continue

            names = getattr(disclaimer, "impacted_product_names", None) or []
            if not names:
                self.logger.info(
                    "Disclaimer %s has no impacted products", disclaimer.meta.id
                )
                continue

            # the value written on each product: the disclaimer id (== its _id)
            known_issue = disclaimer.meta.id

            # expand every product name into its extension variants so we match
            # cds-product `name` values regardless of .SAFE/.zip suffixes
            variants: set = set()
            for name in names:
                variants |= generate_publication_names(name)

            count = 0
            for product in self._search_products(list(variants)):
                product.known_issue = known_issue
                impacted[(product.meta.index, product.meta.id)] = product
                count += 1

            self.logger.info(
                "Disclaimer %s: matched %s product(s) for %s impacted name(s)",
                known_issue,
                count,
                len(names),
            )

        for product in impacted.values():
            yield product.to_bulk_action()

    def _search_products(self, names: list) -> typing.Iterator[CdsProduct]:
        """Yield cds-product documents whose name matches any of ``names``.

        ``seq_no_primary_term`` is requested so ``to_bulk_action`` emits a
        versioned ``index`` op (optimistic concurrency) instead of a ``create``
        op, which would 409 on the already-existing products.
        """
        for start in range(0, len(names), self._NAME_QUERY_CHUNK):
            chunk = names[start : start + self._NAME_QUERY_CHUNK]
            search = CdsProduct.search().filter("terms", name=chunk)
            yield from search.params(
                size=1000, seq_no_primary_term=True, version=True
            ).scan()
