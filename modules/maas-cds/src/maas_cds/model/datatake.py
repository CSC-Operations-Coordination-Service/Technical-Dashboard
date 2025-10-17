"""Custom CDS model definition"""

from datetime import datetime
import logging
from typing import List

from maas_cds.lib.config import get_good_threshold_config_from_value
from maas_cds.lib.partitionning import get_partionning
from maas_model.date_utils import datetime_to_zulu
from opensearchpy import Keyword, Q
from maas_cds.lib import tolerance
from maas_cds.lib.dateutils import get_microseconds_delta
from maas_cds.lib.periodutils import (
    Period,
    compute_duplicated_indicator,
    compute_missing_sensing_periods,
)
from maas_cds.model import generated
from maas_cds.model.anomaly_mixin import AnomalyMixin
from maas_cds.model.enumeration import CompletenessScope, CompletenessStatus
from maas_cds.model.product import CdsProduct

__all__ = ["CdsDatatake"]


LOGGER = logging.getLogger("CdsModelDatatake")


def evaluate_completeness_status(value):
    """Compute completeness status"""
    value_completeness_status = None
    if value == 0:
        value_completeness_status = CompletenessStatus.MISSING.value
    elif value >= 100:
        value_completeness_status = CompletenessStatus.COMPLETE.value
    else:
        value_completeness_status = CompletenessStatus.PARTIAL.value
    return value_completeness_status


class CdsDatatake(AnomalyMixin, generated.CdsDatatake):
    """CdsDatatake custom"""

    COVERING_AREA_FIELD = "_coverage_percentage"

    COMPLETENESS_TOLERANCE = {}

    STATIC_COMPLETENESS_VALUE = {}

    MISSING_PERIODS_MAXIMAL_OFFSET = None

    cams_tickets = Keyword(multi=True)

    datastrip_ids = Keyword(multi=True)

    product_group_ids = Keyword(multi=True)

    def get_product_partitionning(self, day_precision=10) -> List[str]:
        """Utils function to get the partitionning of the product
        This function is used to get the partitionning of the product

        Args:
            day_precision (int, optional): Add some tolerance for the location. Defaults to 10.

        Returns:
            List[str]: Return the list of the indices where product are located
        """

        if not self.observation_time_start or not self.observation_time_stop:
            LOGGER.warning("Observation time start or stop is not set.")
            return []

        date_set = get_partionning(
            self.observation_time_start, self.observation_time_stop, day_precision
        )

        return [
            f"{CdsProduct.Index.name}-{date_part}" for date_part in sorted(date_set)
        ]

    def get_service_for_completeness(self):

        # TODO Move this to a more global configuration and in a external stuff (ie db)
        # Before 2022-04 the service id wasn't set maybe update all data with SX-legacy ?
        completeness_service_dict = {
            "S1A": {
                "0": ["S1-legacy"],
                "2022-04-06T00:00:00.000Z": ["PRIP_S1A_Serco"],
            },
            "S1B": {
                "0": ["S1-legacy"],
                "2022-04-01T00:00:00.000Z": ["PRIP_S1B_DLR"],
            },
            "S1C": {
                "0": ["PRIP_S1C_Serco", "PRIP_S1C_Werum"],
                "2025-02-17T11:00:00.000Z": ["PRIP_S1C_Werum"],
            },
            "S1D": {
                "0": ["PRIP_S1C_Serco"],
            },
            "S2A": {
                "0": ["S2-legacy"],
                "2022-04-01T00:00:00.000Z": ["PRIP_S2A_ATOS"],
                "2025-01-28T00:00:00.000Z": ["PRIP_S2C_ATOS_datatest"],
            },
            "S2B": {
                "0": ["S2-legacy"],
                "2022-04-01T00:00:00.000Z": ["PRIP_S2B_CAPGEMINI"],
            },
            "S2C": {
                "0": ["PRIP_S2C_ATOS_datatest"],
            },
            # "S3A": {
            #     "0": ["PRIP_S3_Legacy"],
            #     "2022-04-01T00:00:00.000Z": ["PRIP_S3A_ACRI"],  # Approx
            # },
            # "S3B": {
            #     "0": ["PRIP_S3_Legacy"],
            #     "2022-04-01T00:00:00.000Z": ["PRIP_S3B_SERCO"],  # Approx
            #     "2025-02-01T00:00:00.000Z": ["PRIP_S3B_TPZ"],
            # },
            # "S5P": {"0": ["PRIP_SSP_DLR"]},
        }

        config_completeness = completeness_service_dict.get(self.satellite_unit, None)

        if config_completeness is None:
            LOGGER.warning(
                "[CompletenessConfig] - Unknow satellite : %s", self.satellite_unit
            )
            return None

        # Maybe use
        (nearest_time_indicator, allowed_prip_name) = (
            get_good_threshold_config_from_value(
                config_completeness, datetime_to_zulu(self.observation_time_start)
            )
        )

        return allowed_prip_name

    def compute_local_value(self, product_type, related_documents=None):
        """Compute value for a specific product_type"""

        # TODO this can be refacto here
        # flow are the same :  get brother, use a compute method and add value in the doc

        raise NotImplementedError(
            f"Must be implement in subclasses in CdsDatatake{self.mission}"
        )

    def evaluate_local_expected(self, key_field):
        """Evaluate local expected for a product_type"""

        raise NotImplementedError(
            f"Must be implement in subclasses in CdsDatatake{self.mission}",
        )

    def evaluate_all_global_expected(
        self,
    ):
        """Evaluate all global expected"""

        raise NotImplementedError(
            f"Must be implement in subclasses in CdsDatatake{self.mission}"
        )

    def get_all_product_types(self):
        """Return the list of all product_type that need to be compute for this mission

        Raises:
            NotImplementedError: This method is mission's speficic
        """
        raise NotImplementedError(
            f"Must be implement in subclasses in CdsDatatake{self.mission}"
        )

    def product_type_with_missing_periods(self, product_type: str) -> bool:
        """Do we want missing periods for this product type ?"""
        raise NotImplementedError(
            f"Must be implement in subclasses in CdsDatatake{self.mission}"
        )

    def product_type_with_duplicated(self, product_type: str) -> bool:
        """Do we want check duplicated for this product type ?"""
        raise NotImplementedError(
            f"Must be implement in subclasses in CdsDatatake{self.mission}"
        )

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

            self.compute_missing_production(product_type, related_products)
            self.compute_duplicated(product_type, related_products)

    def compute_missing_production(
        self, product_type: str, related_products: List[Period]
    ):
        """Find and store missing sensing periods on this datatake

        Args:
            product_type (str): The current product type
            related_products (List[Period]): The list of products for
                this datatake/product-type
        """

        if (
            self.product_type_with_missing_periods(product_type)
            and self.MISSING_PERIODS_MAXIMAL_OFFSET is not None
        ):
            tolerance_value = tolerance.get_completeness_tolerance(
                self.COMPLETENESS_TOLERANCE,
                self.mission,
                CompletenessScope.LOCAL,
                product_type,
            )

            # product_type have some value added to have a better coherence we substract it
            tolerance_value -= tolerance.get_tolerance_from_scope(
                self.STATIC_COMPLETENESS_VALUE, product_type
            )

            missing_periods_maximal_offset = tolerance.get_completeness_tolerance(
                self.MISSING_PERIODS_MAXIMAL_OFFSET,
                self.mission,
                CompletenessScope.LOCAL,
                product_type,
            )

            missing_periods = compute_missing_sensing_periods(
                Period(
                    self.observation_time_start,
                    self.observation_time_stop,
                ),
                related_products,
                missing_periods_maximal_offset,
                tolerance_value,
            )

            LOGGER.debug(
                "[%s] - Missing periods : %r", self.datatake_id, missing_periods
            )

            self.missing_periods = [
                generated.CdsDatatakeMissingPeriods(
                    name="Missing Product",
                    product_type=product_type,
                    sensing_start_date=missing_period.start,
                    sensing_end_date=missing_period.end,
                    duration=int(
                        get_microseconds_delta(missing_period.start, missing_period.end)
                    ),
                )
                for missing_period in missing_periods
            ]

    def compute_duplicated(self, product_type: str, related_products: List[Period]):
        """Find and store duplicated indicator on this datatake

        Args:
            product_type (str): The current product type
            related_products (List[Period]): The list of products for
                this datatake/product-type
        """

        if self.product_type_with_duplicated(product_type):
            indicator = compute_duplicated_indicator(related_products)
            for key_indicator, value in indicator.items():
                setattr(self, f"{product_type}_duplicated_{key_indicator}", value)

    def load_data_before_compute(self):
        """Some step need to be done before starting compute all completeness"""

    def impact_other_calculation(self, compute_key):
        """Some compute provide more information and make possible other compute

        Args:
            compute_key (tuple): the key of the compute that will be execute

        Returns:
            list(tuple): compute keys default: []
        """

        return []

    def evaluate_global_expected(self, key_field) -> int:
        """Evaluate global expected

        Args:
            key_field (str): the global key field we want the value

        Returns:
            int: the value associate to the global expext field given in parameters
        """

        global_expected = self.evaluate_all_global_expected()

        global_value = global_expected.get(key_field, 0)

        if not global_value:
            LOGGER.warning(
                "[%s] - Unhandle key : %s",
                self.datatake_id,
                key_field,
            )

        return global_value

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

    def get_global_key_field(self, product_type):
        """Get the key to group local value in a top level value

        Set a static string to get a unique global value

        """

        raise NotImplementedError(
            f"Must be implement in subclasses in CdsDatatake{self.mission} : {product_type}"
        )

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

    # pylint: disable=R0913
    # Parameters must be mandatory
    def set_completeness_attribut(
        self,
        scope: CompletenessScope,
        key_field: str,
        completeness_value: int,
        expected_value: int,
        adjusted_value: int,
        percentage_value: float,
        completeness_status_value: CompletenessStatus,
    ):
        """_summary_

        Args:
            scope (CompletenessScope): scope value (local, global, final)
            key_field (str): key field value
            completeness_value (int): completeness value
            expected_value (int): expected value
            adjusted_value (int): adjusyed value
            percentage_value (float): percentage value
            completeness_status_value (CompletenessStatus): completeness value
        """

        # value
        attr_name_value = f"{key_field}_{scope.value}_value"
        setattr(self, attr_name_value, completeness_value)

        # expected
        attr_name_expected_value = f"{key_field}_{scope.value}_expected"
        setattr(self, attr_name_expected_value, expected_value)

        # adjusted
        attr_name_value_adjusted = f"{key_field}_{scope.value}_value_adjusted"
        setattr(self, attr_name_value_adjusted, adjusted_value)

        # percentage
        if completeness_status_value != CompletenessStatus.UNKNOWN.value:
            attr_name_value_percentage = f"{key_field}_{scope.value}_percentage"
            setattr(self, attr_name_value_percentage, percentage_value)

        # status
        attr_name_completeness_status = f"{key_field}_{scope.value}_status"
        setattr(
            self,
            attr_name_completeness_status,
            completeness_status_value,
        )

    # pylint: enable

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

    def compute_extra_completeness(self):
        """Method to add specific completeness compute"""

    def get_related_documents_query(self) -> Q:
        """
        Builds a query for documents related to this datatake. Typically product
        or publication.

        Returns:
            Q: ES query
        """

    def find_brother_products_scan(self, product_type, indices=None):
        """Find products with the same datatake and the same product_type

        Note: Seek only product with a prip_id

        Args:
            product_type (str): product_type searched

        Returns:
            list(CdsProduct): list of products matching datatake_id and product_type
        """
        # TODO MAAS_CDS-1236: make a single query to find all the whole brotherhood
        # with list of datatake / product types later post-processed to be grouped by
        # tuple (datatake_id, product_type) in a dict

        completeness_service = self.get_service_for_completeness()

        if not completeness_service:
            LOGGER.warning(
                "Try to compute completess but no service identified : %s %s %s",
                self.satellite_unit,
                self.datatake_id,
                product_type,
            )
            completeness_service = ["NO_SERVICE_FOR_THIS"]

        base_search = CdsProduct.search()
        if indices:
            base_search = CdsProduct.search(index=indices)

        # Ignore if index are missing -
        # This can be dangerous to not raise an error on missing index this can hide an database issue

        search_request = (
            base_search.filter("term", datatake_id=self.datatake_id)
            .filter("term", satellite_unit=self.satellite_unit)
            .filter("term", product_type=product_type)
            .filter("terms", prip_service=completeness_service)
            .filter("exists", field="prip_id")
            .filter(
                "bool",
                should=[
                    {"bool": {"must_not": {"exists": {"field": "nb_dd_deleted"}}}},
                    {"term": {"nb_dd_deleted": 0}},
                ],
            )
            .filter(
                "bool",
                should=[
                    {"bool": {"must_not": {"exists": {"field": "nb_lta_deleted"}}}},
                    {"term": {"nb_lta_deleted": 0}},
                ],
            )
            .params(ignore=404, ignore_unavailable=True)
        )

        query_scan = search_request.scan()

        return query_scan

    def retrieve_additional_fields_from_product(self, product: CdsProduct):
        """Abstract function which allow to fill additional
        datatake fields during completeness calculation"""
