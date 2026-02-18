"""Completeness S2 model definition"""

import logging

from maas_cds.lib.parsing_name import utils
from maas_cds.lib.status import evaluate_completeness_status
from maas_cds.model.cds_completeness.cds_completeness import CdsCompleteness
from maas_cds.model.datatake_s2 import CdsDatatakeS2
from maas_cds.model.generated import CdsPublication

from maas_cds.lib import tolerance
from maas_cds.model.enumeration import CompletenessScope
from opensearchpy import Q, Keyword
from datetime import timedelta


__all__ = ["CdsCompletenessS2"]


LOGGER = logging.getLogger("CdsModelCompletenessS2")


class CdsCompletenessS2(CdsCompleteness, CdsDatatakeS2):
    """CdsCompleteness custom class for Sentinel 1"""

    # ? What is that
    REFERENCE_PRODUCT_TIME_FIELD = "publication_date"

    S2_EXPECTED_TYPE_FROM_PRODUCT_LEVEL_DICT = {
        "L1A": [
            "DS",
            "GR",
        ],
        "L1B": [
            "DS",
            "GR",
        ],
        "L1C": [
            "__",
        ],
        "L2A": [
            "__",
        ],
    }

    datastrip_ids = Keyword(multi=True)

    product_group_ids = Keyword(multi=True)

    def search_expected_tiles(self):
        return CdsDatatakeS2.get_by_id(self.meta.id).search_expected_tiles()

    def load_data_before_compute(self):
        """Some step need to be done before starting compute all completeness"""

        # Evaluate expected tiles before compute completeness
        self.number_of_expected_tiles = len(self.search_expected_tiles())

        if not self.product_group_ids:
            self.product_group_ids = CdsDatatakeS2.get_by_id(
                self.meta.id
            ).product_group_ids

        # Try to rattach products which have no datatake id to this datatake using sensing date
        # Also update the datastrip_ds and product_group_ids list of the datatake

        if not self.product_group_ids:
            return

        for product in (
            self.find_related_document_not_attached()
            .params(version=True, seq_no_primary_term=True)
            .scan()
        ):
            self.retrieve_additional_fields_from_product(product)

            if product.datatake_id != self.datatake_id:

                LOGGER.info(
                    "Load_data_before_compute - CdsProduct with key:%s had"
                    " no datake_id, using sensing date it has been rattached"
                    " to datatake_id: %s",
                    product.key,
                    self.datatake_id,
                )

                product.datatake_id = self.datatake_id

                if self.timeliness:
                    product.timeliness = self.timeliness

                product.absolute_orbit = self.absolute_orbit
                product.relative_orbit = self.relative_orbit

                product.instrument_mode = self.instrument_mode

                yield product.to_bulk_action()

    def impact_other_calculation(self, compute_key):
        """MSI_L1C_DS provide footprint to evaluated expected tiles

        Args:
            compute_key (tuple): the key of the compute that will be execute

        Returns:
            list(tuple): compute keys default: []
        """
        compute_product_type = compute_key["product_type"]

        if self.REFERENCE_PRODUCT_TYPE_SENSING in compute_product_type:
            # build compute key to process

            self.number_of_expected_tiles = len(self.search_expected_tiles())

            product_types_to_compute = [
                product_type
                for product_type in self.get_all_product_types()
                if "TL" in product_type or "TC" in product_type
            ]

            return [
                {**compute_key, "product_type": product_type}
                for product_type in product_types_to_compute
            ]
        return []

    def get_expected_from_product_level(self, product_level):
        """Get expected from the product level

        Args:
            product_level (str): product level thaht we want expected

        Returns:
            dict: expect dict for the given product level
        """
        if self.service_type != "DD":
            return super().get_expected_from_product_level(product_level)

        if (
            self.instrument_mode
            not in self.S2_NUMBER_OF_GR_PER_SCENE_PER_INSTRUMENT_DICT
        ):
            LOGGER.critical(
                "Unhandled instrument mode '%s' in %s. Unable to calculate expected products.",
                self.instrument_mode,
                self,
            )
            return {}

        # find a better name and set top level conf

        # - 3608000 -> remove one scene (cause first and last gr are at the half)
        # - 1000000 -> remove one sec (cause millisec are truncate)

        s2_number_of_gr_per_scene = self.S2_NUMBER_OF_GR_PER_SCENE_PER_INSTRUMENT_DICT[
            self.instrument_mode
        ]

        s2_expected_from_product_level_dict = {
            "L1A": {
                "DS": self.observation_duration - (2 * 3608000),
                "GR": (self.number_of_scenes - 2) * s2_number_of_gr_per_scene,
            },
            "L1B": {
                "DS": self.observation_duration - (2 * 3608000),
                "GR": (self.number_of_scenes - 2) * s2_number_of_gr_per_scene,
            },
            "L1C": {
                "__": self.number_of_expected_tiles,
            },
            "L2A": {
                "__": self.number_of_expected_tiles,
            },
        }

        # apply tolerance for product_level only
        product_level_with_tolerance = s2_expected_from_product_level_dict.get(
            product_level, {}
        )
        for key in product_level_with_tolerance:
            tolerance_value = tolerance.get_completeness_tolerance(
                self.COMPLETENESS_TOLERANCE,
                self.mission,
                CompletenessScope.LOCAL,
                f"MSI_{product_level}_{key}",
            )
            sensing_value_with_tolerance = (
                product_level_with_tolerance[key] + tolerance_value
            )

            # avoid negative sensing
            product_level_with_tolerance[key] = max(0, sensing_value_with_tolerance)

        return product_level_with_tolerance

    def get_expected_product_level(self):
        """Get expected product_level for the datatake

        Returns:
            list: a list of the expected product level
        """
        if self.service_type != "DD":
            return super().get_expected_product_level()

        product_level_to_get = self.S2_PRODUCT_LEVEL_FROM_INSTRUMENT_DICT.get(
            self.instrument_mode
        )

        # Remove L0_ product levels if they exist
        if product_level_to_get:
            product_level_to_get = [
                level for level in product_level_to_get if level != "L0_"
            ]

        # We need to get at least 3 scenes to compute level L1 and L2
        if self.number_of_scenes < 3:
            product_level_to_get = []

        return product_level_to_get

    def get_all_product_types(self):
        """Return all product type expected for this datatake

        Returns:
            list: List of all product type expected for this datatake
        """
        product_types = []

        product_level_to_get = self.get_expected_product_level()
        for product_level in product_level_to_get:
            expected_types_for_product_level = self.expected_type_per_level(
                product_level
            )

            for key in expected_types_for_product_level:
                # rebuild the product_type
                product_type = f"MSI_{product_level}_{key}"
                product_types.append(product_type)

        return product_types

    def evaluate_local_expected(self, product_type):
        """Evaluate expected for a specific product_type

        Args:
            product_type (str): product_type that we want to get the local expected

        Returns:
            int: The local expected value of this datatake and the given product_type
        """
        product_level = product_type[4:7]
        local_expected_product_type = self.get_expected_from_product_level(
            product_level
        )

        key_field_value = self.get_global_key_field(product_type)
        expected_value = local_expected_product_type.get(key_field_value, None)

        return expected_value

    def compute_extra_completeness(self):
        """Need to compute product level completeness and final for sentinel 2"""

        LOGGER.info(
            "[%s] - Compute extra completeness",
            self.datatake_id,
        )

        final_expected = final_value = 0
        product_level_to_get = self.get_expected_product_level()

        for product_level in product_level_to_get:
            LOGGER.debug(
                "[%s] - Extra completeness : %s", self.datatake_id, product_level
            )

            product_level_expected = product_level_value = 0

            expected_for_product_level = self.get_expected_from_product_level(
                product_level
            )

            for key in expected_for_product_level:
                # rebuild the product_type
                product_type = f"MSI_{product_level}_{key}"

                attr_product_type_value = f"{product_type}_local_value_adjusted"
                product_type_value = getattr(self, attr_product_type_value, 0)

                attr_product_type_expected = f"{product_type}_local_expected"
                expected_value = getattr(self, attr_product_type_expected, 0)

                if expected_value == 0:
                    # Sometime geometry arrive later
                    LOGGER.warning(
                        "[%s] - Missing expected : %s -> %s ",
                        self.datatake_id,
                        attr_product_type_expected,
                        expected_value,
                    )
                    value = 0
                    expected = 0

                else:
                    value = product_type_value / expected_value * 100
                    expected = 100

                product_level_value += value
                product_level_expected += expected

                final_value += value
                final_expected += expected

            # product level completeness
            if product_level_expected == 0:
                LOGGER.warning(
                    "[%s] - No product level expected for : %s",
                    self.datatake_id,
                    product_level,
                )

                product_level_percentage = 0

            else:
                product_level_percentage = (
                    product_level_value / product_level_expected * 100
                )

            setattr(self, f"{product_level}_local_value", product_level_value)
            setattr(self, f"{product_level}_local_expected", product_level_expected)

            setattr(self, f"{product_level}_local_percentage", product_level_percentage)
            setattr(
                self,
                f"{product_level}_local_status",
                evaluate_completeness_status(product_level_percentage),
            )

        # final completeness
        if final_expected == 0:
            LOGGER.warning(
                "[%s] - No final expected",
                self.datatake_id,
            )
            percentage = 0
        else:
            percentage = final_value / final_expected * 100

        setattr(self, "final_completeness_value", final_value)
        setattr(self, "final_completeness_expected", final_expected)

        setattr(self, "final_completeness_percentage", percentage)
        setattr(
            self, "final_completeness_status", evaluate_completeness_status(percentage)
        )

    def find_related_document_not_attached(self):
        # Try to rattach products which have no datatake id to this datatake using sensing date
        # Also update the datastrip_ds and product_group_ids list of the datatake

        search_request = (
            CdsPublication.search()
            .filter("term", satellite_unit=self.satellite_unit)
            .filter("term", mission=self.mission)
            .filter("term", service_type=self.service_type)
            .filter("term", service_id=self.service_id)
            .filter(~Q("term", datatake_id=self.datatake_id))
            .filter("term", product_group_id=self.product_group_ids[0])
            .filter("terms", product_type=self.get_all_product_types())
            .params(ignore=404)
        )

        return search_request
