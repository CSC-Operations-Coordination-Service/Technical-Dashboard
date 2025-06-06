"""Custom consolidated acquisition pass status"""

from datetime import timedelta
from opensearchpy import Keyword

from maas_cds.model import generated

from maas_cds.model.anomaly_mixin import AnomalyMixin

__all__ = ["CdsHktmAcquisitionCompleteness", "CdsHktmProductionCompleteness"]


class CdsHktmAcquisitionCompleteness(
    generated.CdsHktmAcquisitionCompleteness, AnomalyMixin
):
    """overide to add cams_tickets as a multi keyword"""

    cams_tickets = Keyword(multi=True)


class CdsHktmProductionCompleteness(generated.CdsHktmProductionCompleteness):
    """overide to add cams_tickets as a multi keyword"""

    REFERENCE_HKTM_PRODUCT_TYPE = {
        "S1": "HK_RAW__0_",
        "S2": "PRD_HKTM__",
    }

    def count_produced_hktm(self, tolerance_value=0):
        """
        Compute the completeness of production based on products.


        Args:
            tolerance_value (int): The shift of the sensing start date in minutes

        Returns:
            int: The count of document that met the criteria

        """
        tolerance_value = timedelta(minutes=tolerance_value)

        query = (
            generated.CdsProduct.search()
            .filter("term", mission=self.mission)
            .filter("term", satellite_unit=self.satellite_unit)
            .filter("term", product_type=self.REFERENCE_HKTM_PRODUCT_TYPE[self.mission])
            .filter(
                "range",
                sensing_start_date={
                    "lte": self.effective_downlink_start + tolerance_value
                },
            )
            .filter(
                "range",
                sensing_start_date={
                    "gte": self.effective_downlink_start - tolerance_value
                },
            )
        )

        count = query.count()

        return count
