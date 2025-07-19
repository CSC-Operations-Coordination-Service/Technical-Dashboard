"""Datatake S1 model definition"""

import copy
import logging

from maas_cds.model.cds_completeness.cds_completeness import CdsCompleteness
from maas_cds.model.datatake_s1 import CdsDatatakeS1
from maas_cds.model.generated import CdsPublication, MaasConfigDataflow
from maas_cds.lib.config_manager import MaasConfigManager


__all__ = ["CdsCompletenessS1"]


LOGGER = logging.getLogger("CdsModelCompletenessS1")


class CdsCompletenessS1(CdsCompleteness, CdsDatatakeS1):
    """CdsCompleteness custom class for Sentinel 1"""

    # ? What is that
    REFERENCE_PRODUCT_TIME_FIELD = "publication_date"

    def get_slc_1s_count(self):
        """Count all SLC__1S products that are linked to the datatake

        Returns:
            int: count of products
        """
        search = (
            CdsPublication.search()
            .filter("term", datatake_id=self.datatake_id)
            .filter("term", satellite_unit=self.satellite_unit)
            .filter("term", product_type=f"{self.instrument_mode}_SLC__1S")
            .filter("term", service_type=self.service_type)
            .filter("term", service_id=self.service_id)
        )

        count = search.count()

        return count

    def impact_other_calculation(self, compute_key):
        """Reference product sensing provide expected for OCN or SLC

        Args:
            compute_key (tuple): the key of the compute that will be execute

        Returns:
            list(tuple): compute keys default: []
        """

        compute_product_type = compute_key["product_type"]

        extra_compute_key = []

        if "SLC" in compute_key["product_type"]:
            new_compute_key = copy.deepcopy(compute_key)
            new_compute_key["product_type"] = (
                f"{compute_key['product_type'][:2]}_ETA__AX"
            )
            return [new_compute_key]

        if self.REFERENCE_PRODUCT_TYPE_SENSING in compute_product_type:
            # build compute key to process
            product_types_to_compute = [
                product_type
                for product_type in self.get_all_product_types()
                if self.product_type_over_specific_area(product_type)
            ]

            extra_compute_key = []
            for product_type in product_types_to_compute:
                new_compute_key = copy.deepcopy(compute_key)
                new_compute_key["product_type"] = product_type
                extra_compute_key.append(new_compute_key)

        return extra_compute_key
