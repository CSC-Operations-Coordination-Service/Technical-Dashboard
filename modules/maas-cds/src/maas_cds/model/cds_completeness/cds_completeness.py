"""Custom CDS model definition"""

import logging

from maas_cds.lib.config_manager import MaasConfigManager
from maas_cds.model.datatake import CdsDatatake

from maas_cds.model import generated
from maas_cds.model.enumeration import CompletenessScope
from maas_cds.lib.status import evaluate_completeness_status

__all__ = ["CdsCompleteness"]


LOGGER = logging.getLogger("CdsModelCompleteness")


class CdsCompleteness(generated.CdsCompleteness, CdsDatatake):

    def find_brother_products_scan(self, product_type, indices=None):
        """Find products with the same datatake and the same product_type

        Note: Common method to extract publication associated on the same completeness key

        Args:
            product_type (str): product_type searched
            indices (): list of indices generated to find with more precision

        Returns:
            list(CdsPublication): list of products matching datatake_id and product_type
        """

        # TODO MAAS_CDS-1236: make a single query to find all the whole brotherhood
        # with list of datatake / product types later post-processed to be grouped by
        # tuple (datatake_id, product_type) in a dict

        search_request = (
            generated.CdsPublication.search()
            .filter("term", datatake_id=self.datatake_id)
            .filter("term", satellite_unit=self.satellite_unit)
            .filter("term", product_type=product_type)
            .filter("term", service_type=self.service_type)
            .filter("term", service_id=self.service_id)
            .params(ignore=404)
        )

        query_scan = search_request.scan()

        return query_scan

    def retrieve_additional_fields_from_publication(
        self, product: generated.CdsPublication
    ):
        """Abstract function which allow to fill additional
        datatake fields during completeness calculation"""
        pass

    def get_all_product_types(self):
        nominal_expected = super().get_all_product_types()
        applicable_config = self.get_applicable_configuration()
        applicable_product_type = [
            dataflow_item.product_type for dataflow_item in applicable_config
        ]

        return [
            product_type
            for product_type in nominal_expected
            if product_type in applicable_product_type
        ]

    def get_applicable_configuration(self):

        # Filter DATAFLOW_CACHE records to match mission, satellite_unit, and service_type
        filtered_records = [
            record
            for record in MaasConfigManager().get_config("MaasConfigDataflow")[
                "records"
            ]
            if record.mission == self.mission
            and self.satellite_unit in record.satellites
            and self.service_type in record.services_config
            and record.services_config[self.service_type]
            and any(
                item.startswith(("C", "P"))
                for item in record.services_config[self.service_type]
            )
        ]

        return filtered_records

    def compute_all_local_completeness(self):
        """Complete all local completeness for this datatake"""
        all_product_type = self.get_all_product_types()

        for product_type in all_product_type:
            related_products = []
            product_type_value = self.compute_local_value(
                product_type, related_products
            )

            self.set_completeness(
                CompletenessScope.LOCAL,
                product_type,
                product_type_value,
            )

    def get_expected_value(self, scope, key_field):
        """Get expected value for local and global"""

        expected_value = 0

        LOGGER.debug(
            "[%s] - Get expected value : %s - %s",
            self.datatake_id,
            scope,
            key_field,
        )

        if scope == CompletenessScope.LOCAL:
            expected_value = self.evaluate_local_expected(key_field)

        elif scope == CompletenessScope.GLOBAL:
            expected_value = self.evaluate_global_expected(key_field)

        else:
            LOGGER.warning("Scope not handle : %s", scope)

        if not expected_value:
            LOGGER.warning(
                "[%s] - No expected value : %s - %s",
                self.datatake_id,
                scope,
                key_field,
            )

        return expected_value

    def set_completeness(
        self,
        scope: CompletenessScope,
        key_field: str,
        completeness_value: int = 0,
    ):
        """Fill a local completeness"""

        LOGGER.debug(
            "[%s] - set completeness for %s %s",
            self.datatake_id,
            scope.value,
            key_field,
        )

        expected_value = self.get_expected_value(
            scope,
            key_field,
        )

        if not expected_value:
            LOGGER.warning(
                "[%s] - Trying to evaluate completeness but expected_value = 0 | %s %s",
                self.datatake_id,
                scope.value,
                key_field,
            )
            if completeness_value:
                # set value if it his different than 0  to raise conflict if expected is compute in parallel
                attr_name_value = f"{key_field}_{scope.value}_value"
                setattr(self, attr_name_value, completeness_value)
        else:
            # compute other value (avoid value superior to expected )
            adjusted_value = min(completeness_value, expected_value)

            percentage_value = adjusted_value / expected_value * 100

            completeness_status_value = evaluate_completeness_status(percentage_value)

            self.set_completeness_attribut(
                scope,
                key_field,
                completeness_value,
                expected_value,
                adjusted_value,
                percentage_value,
                completeness_status_value,
            )

    def compute_global_completeness(self):
        """Compute global completeness"""

        LOGGER.info(
            "[%s] - Compute global completeness",
            self.datatake_id,
        )

        global_values = {}
        global_duplication_indicator = {"max_duration": 0, "max_percentage": 0.0}

        doc_dict = self.to_dict().items()

        for key, value in doc_dict:
            # maybe we can use a function that returns all product_type
            # In the face of ambiguity refuse the temptation to guess
            if key.endswith("_local_value_adjusted"):
                product_type = key.split("_local_value_adjusted")[0]

                key_field = self.get_global_key_field(product_type)

                if key_field not in global_values:
                    global_values[key_field] = 0

                global_values[key_field] += value

            # Duplicated indicator per product type
            if key.endswith("_duplicated_max_duration"):
                if value > global_duplication_indicator["max_duration"]:
                    global_duplication_indicator["max_duration"] = value

            if key.endswith("_duplicated_max_percentage"):
                if value > global_duplication_indicator["max_percentage"]:
                    global_duplication_indicator["max_percentage"] = value

        # Set
        for key_field, value in global_duplication_indicator.items():
            global_key = f"duplicated_{CompletenessScope.GLOBAL.value}_{key_field}"
            setattr(self, global_key, value)

        # update global completness
        for key_field, value in global_values.items():
            self.set_completeness(CompletenessScope.GLOBAL, key_field, value)
        # compute extra completness
        self.compute_extra_completeness()
