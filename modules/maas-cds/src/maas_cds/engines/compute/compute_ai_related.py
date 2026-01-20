"""Create / Update AI completeness after related products are ingested"""

from typing import Union
from maas_cds.lib.hash_utils import get_hash
from maas_engine.engine.rawdata import RawDataEngine

from maas_cds.model import CdsAiProductionCompleteness, CdsProductS1


class ComputeAiRelatedEngine(RawDataEngine):
    """Update documents related to hktm creation or update"""

    ENGINE_ID = "COMPUTE_AI_RELATED"

    CONSOLIDATED_MODEL = CdsAiProductionCompleteness

    def __init__(
        self,
        args=None,
        send_reports=False,
    ):
        """constructor

        Args:
            args (namespace, optional): cli options. Defaults to None.
            send_reports (bool, optional): flag. Defaults to False.
        """
        super().__init__(args, send_reports=send_reports)

    def get_consolidated_id(self, product: CdsProductS1):
        """Create the unique identifier for AISAUX and also AI_RAW product

        Args:
            product (CdsProductS1): AISAUX or AI_RAW product

        Returns:
            str: The id of document CdsAiProductionCompleteness related for the product
        """
        return get_hash(
            [
                "sensing_start_date",
                "sensing_end_date",
            ],
            product,
        )

    def _common_consolidation(
        product_doc: CdsProductS1, completeness_doc: CdsAiProductionCompleteness
    ):
        """Set to the completeness doc the common attribuate

        This allow the document creation from both part

        Args:
            product_doc (CdsProductS1): _description_
            completeness_doc (CdsAiProductionCompleteness): _description_
        """

        completeness_doc.mission = product_doc.mission
        completeness_doc.satellite_unit = product_doc.satellite_unit
        completeness_doc.sensing_start_date = product_doc.sensing_start_date
        completeness_doc.sensing_end_date = product_doc.sensing_end_date

    def consolidate(
        self, product_doc: CdsProductS1, completeness_doc: CdsAiProductionCompleteness
    ) -> Union[CdsAiProductionCompleteness, None]:
        """Consolidate AI Product to compute AI completeness

        Args:
            product (CdsProductS1): AISAUX or AI_RAW product
            document (CdsAiProductionCompleteness): consolidated data

        Returns:
            CdsAiProductionCompleteness: Consolided completeness
        """

        if product_doc.product_type == "AISAUX":
            self._common_consolidation(product_doc, completeness_doc)

            if completeness_doc.file_name != product_doc.name:
                self.logger.warning(
                    "[%s] - Completeness document already own by an other document here %s - %s",
                    completeness_doc.meta.id,
                    completeness_doc.input_name,
                    product_doc.name,
                )

            completeness_doc.file_name = product_doc.name

            completeness_doc.completeness = 1

        elif product_doc.product_type == "AI_RAW__0_":
            self._common_consolidation(product_doc, completeness_doc)

            if completeness_doc.input_name != product_doc.name:
                self.logger.warning(
                    "[%s] - Completeness document already own by an other document here %s - %s",
                    completeness_doc.meta.id,
                    completeness_doc.input_name,
                    product_doc.name,
                )

            completeness_doc.input_name = product_doc.name
            completeness_doc.datatake_id = product_doc.datatake_id
            completeness_doc.timeliness = product_doc.timeliness

            if completeness_doc.completeness is None:
                completeness_doc.completeness = 0

        else:
            self.logger.warning(
                "Unexpected product type here %s - %s",
                product_doc.product_type,
                product_doc.meta.id,
            )
            return None

        return completeness_doc
