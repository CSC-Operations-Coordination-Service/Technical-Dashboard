"""Completeness S2 model definition"""

import logging

from maas_cds.lib.parsing_name import utils
from maas_cds.model.cds_completeness.cds_completeness import CdsCompleteness
from maas_cds.model.datatake_s2 import CdsDatatakeS2
from maas_cds.model.generated import CdsPublication


__all__ = ["CdsCompletenessS2"]


LOGGER = logging.getLogger("CdsModelCompletenessS2")


class CdsCompletenessS2(CdsCompleteness, CdsDatatakeS2):
    """CdsCompleteness custom class for Sentinel 1"""

    # ? What is that
    REFERENCE_PRODUCT_TIME_FIELD = "publication_date"

    def load_data_before_compute(self):
        """Some step need to be done before starting compute all completeness"""

        # Evaluate expected tiles before compute completeness
        self.number_of_expected_tiles = len(self.search_expected_tiles())

        # Try to rattach products which have no datatake id to this datatake using sensing date
        # Also update the datastrip_ds and product_group_ids list of the datatake

        search_request = (
            CdsPublication.search()
            .filter("term", satellite_unit=self.satellite_unit)
            .filter("term", mission=self.mission)
            .filter("term", service_type=self.service_type)
            .filter("term", service_id=self.service_id)
            .filter("range", sensing_start_date={"gte": self.observation_time_start})
            .filter("range", sensing_end_date={"lte": self.observation_time_stop})
            .filter("terms", product_type=self.get_all_product_types())
            .params(ignore=404)
        )
        res = search_request.execute()
        if res:
            for product in res:
                self.retrieve_additional_fields_from_product(product)

                if product.datatake_id in ("", utils.DATATAKE_ID_MISSING_VALUE):
                    product.datatake_id = self.datatake_id
                    LOGGER.info(
                        "Load_data_before_compute - CdsProduct with key:%s had"
                        " no datake_id, using sensing date it has been rattached"
                        " to datatake_id: %s",
                        product.key,
                        self.datatake_id,
                    )
                    yield product
