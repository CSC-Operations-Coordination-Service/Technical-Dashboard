"""SAR-MPC Quality Disclaimer consolidation"""

from maas_engine.engine.replicate import ReplicatorEngine

from maas_cds.model import CdsQualityDisclaimer


class QualityDisclaimerConsolidatorEngine(ReplicatorEngine):
    """Consolidate raw SAR-MPC Quality Disclaimers into a single consolidated
    document per disclaimer.

    This is a one-to-one copy: every raw field (including the full
    ``impacted_product_names`` list) is replicated into ``CdsQualityDisclaimer``.
    The consolidated document keeps the same id as the raw one (the disclaimer
    number), so a re-collected/modified disclaimer overwrites its consolidation.
    """

    ENGINE_ID = "CONSOLIDATE_QUALITY_DISCLAIMER"

    CONSOLIDATED_MODEL = CdsQualityDisclaimer

    # pylint: disable=R0913
    def __init__(
        self,
        args=None,
        send_reports=True,
        min_doi=None,
        chunk_size=0,
        target_model="CdsQualityDisclaimer",
        exclude_fields=None,
        include_fields=None,
    ):
        super().__init__(
            args,
            send_reports=send_reports,
            min_doi=min_doi,
            chunk_size=chunk_size,
            target_model=target_model,
            exclude_fields=exclude_fields,
            include_fields=include_fields,
        )
