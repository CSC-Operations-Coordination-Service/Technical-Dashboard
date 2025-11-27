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

    cams_tickets = Keyword(multi=True)

    REFERENCE_HKTM_PRODUCT_TYPE = {
        "S1": "HK_RAW__0_",
        "S2": "PRD_HKTM__",
    }

    PRODUCT_MAPPING = [
        ["name", "related_document_name"],
        ["fos_pushing_date_backup"],
        ["fos_pushing_date_nominal"],
    ]

    def find_related_document(self, tolerance_value):

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

        proof_documents = list(query.execute())

        return proof_documents

    def evaluated_produced_hktm(self, tolerance_value=0):
        """
        Compute the completeness of production based on products.


        Args:
            tolerance_value (int): The shift of the sensing start date in minutes

        Returns:
            int: The count of document that met the criteria

        """
        timedelta_tolerance_value = timedelta(minutes=tolerance_value)

        proof_documents = self.find_related_document(timedelta_tolerance_value)

        self.set_completeness(proof_documents)

    def set_completeness(self, proof_documents):
        if proof_documents is None or len(proof_documents) == 0:
            self.completeness = 0
        else:
            self.completeness = 1
            proof_document = proof_documents[0]

            for field in self.PRODUCT_MAPPING:
                if hasattr(proof_document, field[0]) and (
                    value := getattr(proof_document, field[0], None)
                ):
                    setattr(
                        self,
                        field[-1],  # Trigs to avoid duplication 🧨
                        value,
                    )
