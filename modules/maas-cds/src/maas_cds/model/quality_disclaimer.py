"""DAO classes for SAR-MPC Quality Disclaimers.

Hand-written (not in generated.py) because the raw model originates from the
maas-collector disclaimer collector. Both classes mirror the OpenSearch index
templates:
    - resources/templates/raw-data-quality-disclaimer_template.json
    - resources/templates/cds-quality-disclaimer_template.json
"""

from opensearchpy import Keyword, Long, Text

from maas_model import MAASDocument, MAASRawDocument, ZuluDate

__all__ = ["QualityDisclaimer", "CdsQualityDisclaimer"]


class QualityDisclaimer(MAASRawDocument):
    """Raw SAR-MPC Quality Disclaimer as collected from https://sar-mpc.eu"""

    class Index:
        "inner class for DSL"

        name = "raw-data-quality-disclaimer"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("raw-data-quality-disclaimer")

    _PARTITION_FIELD = "ingestionTime"

    _PARTITION_FIELD_FORMAT = "%Y-%m"

    disclaimer_id = Long()

    last_modified = ZuluDate()

    mission = Keyword()

    description = Text()

    product_quality_status = Keyword()

    degradation_percentage = Keyword()

    validity_start = ZuluDate()

    validity_stop = ZuluDate()

    product_types = Keyword()

    pdf_filename = Keyword()

    pdf_url = Keyword()

    title = Text()

    cause = Text()

    status = Text()

    degradation_types_selected = Keyword()

    impacted_products_count = Long()

    impacted_product_names = Keyword()

    interface_name = Keyword()


class CdsQualityDisclaimer(MAASDocument):
    """Consolidated SAR-MPC Quality Disclaimer (one document per disclaimer)."""

    class Index:
        "inner class for DSL"

        name = "cds-quality-disclaimer"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("cds-quality-disclaimer")

    _PARTITION_FIELD = "last_modified"

    _PARTITION_FIELD_FORMAT = "%Y-%m"

    disclaimer_id = Long()

    last_modified = ZuluDate()

    mission = Keyword()

    description = Text()

    product_quality_status = Keyword()

    degradation_percentage = Keyword()

    validity_start = ZuluDate()

    validity_stop = ZuluDate()

    product_types = Keyword()

    pdf_filename = Keyword()

    pdf_url = Keyword()

    title = Text()

    cause = Text()

    status = Text()

    degradation_types_selected = Keyword()

    impacted_products_count = Long()

    impacted_product_names = Keyword()

    interface_name = Keyword()
