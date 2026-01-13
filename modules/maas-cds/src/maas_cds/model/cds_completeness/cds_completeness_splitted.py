"""Custom CDS model definition for Cds Completeness is a splitted method"""

import logging

from maas_cds.lib.config_manager import MaasConfigManager
from maas_cds.lib.status import evaluate_completeness_status
from maas_cds.model import generated
from maas_cds.model.enumeration import CompletenessScope


from maas_cds.lib.periodutils import (
    compute_total_sensing_product,
    compute_total_sensing_period,
    Period,
)
from maas_cds.lib import tolerance

from maas_cds.model.anomaly_mixin import AnomalyMixin
from opensearchpy import Q, Keyword

__all__ = ["CdsCompletenessSplitted"]


LOGGER = logging.getLogger("CdsCompletenessSplitted")


class CdsCompletenessSplitted(AnomalyMixin, generated.CdsCompletenessSplitted):
    """Document handeling completeness splitted"""

    cams_tickets = Keyword(multi=True)
    cams_origin = Keyword(multi=True)
    cams_descriptions = Keyword(multi=True)

    DATAFLOW_CACHE = None

    COMPLETENESS_TOLERANCE = {}

    @property
    def completeness_key(self):
        return {
            "index": self.meta.index,
            "class": self.__class__,
            "key": self.key,
            "mission": self.mission,
            "satellite_unit": self.satellite_unit,
            "datatake_id": self.datatake_id,
            "product_type": self.product_type,
            "product_level": self.product_level,
            "timeliness": self.timeliness,
            "service_type": self.service_type,
            "service_id": self.service_id,
        }

    def set_completeness(
        self,
        sensing_value,
        observation_period,
    ):
        """Applies the field for display purpose

        Args:
            sensing_value (int): Value of the completeness (most of the time the sensing_duration)
            observation_period (Period): The start and end of the production
        """

        LOGGER.debug(
            "[%s] - set completeness for %s %s",
            self.datatake_id,
            self.product_type,
            self.timeliness,
        )

        # get expected for current completeness document
        expected_value = self.get_expected_value()

        if not expected_value:
            LOGGER.warning(
                "[%s] - Trying to evaluate completeness but expected_value = 0 | %s %s",
                self.datatake_id,
                self.product_type,
                self.timeliness,
            )
            return

        # value
        self.value = sensing_value
        self.expected = expected_value
        self.value_adjusted = min(sensing_value, expected_value)
        self.percentage = self.value_adjusted / expected_value * 100

        self.status = evaluate_completeness_status(self.percentage)

        if observation_period is None:
            LOGGER.warning("[%s] - Unable to retrieve a period", self.meta.id)
        else:
            self.observation_time_start = observation_period.start
            self.observation_time_stop = observation_period.end

    def get_expected_value(self):
        config_completeness = MaasConfigManager().get_config(
            f"MaasConfigCompleteness{self.MISSION}"
        )[0]

        # Filter config completeness item to find the one that matches product_type and timeliness
        matching_items = [
            item
            for item in config_completeness.records
            if item.product_type == self.product_type
            and item.timeliness == self.timeliness
        ]

        if not matching_items:
            LOGGER.warning(
                "[%s] - No matching config item found for product_type=%s, timeliness=%s",
                self.datatake_id,
                self.product_type,
                self.timeliness,
            )
            return 0

        if len(matching_items) > 1:
            LOGGER.warning(
                "[%s] - Matching two many config item found for product_type=%s, timeliness=%s",
                self.datatake_id,
                self.product_type,
                self.timeliness,
            )

        expected_value = matching_items[0].sensing_in_minutes * 60 * 1000000

        LOGGER.debug(
            "Expected value from config for %s are %s",
            self.product_type,
            expected_value,
        )

        tolerance_value = tolerance.get_completeness_tolerance(
            self.COMPLETENESS_TOLERANCE,
            self.mission,
            CompletenessScope.LOCAL,
            self.product_type,
        )

        expected_value += tolerance_value

        return expected_value

    def get_applicable_configuration(self):

        dataflow_product_types = []

        for config in MaasConfigManager().get_config("MaasConfigDataflow")["records"]:
            if (
                config.mission == self.MISSION
                and self.satellite_unit in config.satellites
                and self.service_type in config.services_config
                and any(
                    item.startswith(("C", "P"))
                    for item in config.services_config[self.service_type]
                )
            ):
                LOGGER.debug(
                    "Adding product_type %s for mission %s, satellite_unit %s, service_type %s",
                    config.product_type,
                    self.MISSION,
                    self.satellite_unit,
                    self.service_type,
                )
                dataflow_product_types.append(config)
            else:
                LOGGER.debug(
                    "Skipping product_type %s for mission %s, satellite_unit %s, service_type %s - conditions not met",
                    config.product_type,
                    self.MISSION,
                    self.satellite_unit,
                    self.service_type,
                )

        return dataflow_product_types

    def generate_brother_completeness_key(self, exclude_me=False):
        """From a compute_key generate also expected completeness key
        base on configuration
        """

        expected_items = self.get_applicable_configuration()

        LOGGER.info("Load %s item from config dataflow", len(expected_items))

        # Get all timeliness expected for each product_type
        configs_completeness = (
            MaasConfigManager()
            .get_config(f"MaasConfigCompleteness{self.MISSION}")[0]
            .records
        )

        LOGGER.debug(
            "Load %s item from config completeness %s",
            len(configs_completeness),
            self.MISSION,
        )

        # Filter product_type and remove the current one

        product_type_from_dataflow = [item.product_type for item in expected_items]
        product_level_from_product_type = {
            item.product_type: item.product_level for item in expected_items
        }

        matching_items = [
            item
            for item in configs_completeness
            if item.product_type in product_type_from_dataflow
            and (
                not exclude_me
                or not (
                    item.product_type == self.product_type
                    and item.timeliness == self.timeliness
                )
            )
        ]

        LOGGER.debug("Load %s item after filter config", len(matching_items))

        completeness_key_brother = []
        for matching_item in matching_items:
            completeness_key = self.completeness_key.copy()

            completeness_key["timeliness"] = matching_item.timeliness
            completeness_key["product_type"] = matching_item.product_type
            completeness_key["product_level"] = product_level_from_product_type[
                matching_item.product_type
            ]

            completeness_key["key"] = "-".join(
                [
                    completeness_key["datatake_id"],  # Already prefixed by satellite
                    matching_item.timeliness,
                    matching_item.product_type,
                ]
            )
            # This can be used as fallback date to indexi n the time this datatake
            completeness_key["observation_time_start"] = self.observation_time_start
            completeness_key["observation_time_stop"] = self.observation_time_stop

            completeness_key_brother.append(completeness_key)

        return completeness_key_brother

    def evaluate_completeness(self):
        """Evaluate completeness with the element provide"""

        implied_documents = self.find_brother_products_scan()

        product_periods = [
            Period(product.sensing_start_date, product.sensing_end_date)
            for product in implied_documents
        ]

        product_periods.sort(key=lambda product: product.start)

        completeness_value = compute_total_sensing_product(product_periods)

        observation_period = compute_total_sensing_period(product_periods)

        LOGGER.debug(
            "[%s] - Computed value : %s for period : %s",
            self.meta.id,
            completeness_value,
            observation_period,
        )

        self.set_completeness(completeness_value, observation_period)

    def find_brother_products_scan(self):
        """Common way to search product

        Returns:
            Generator: Publication of implied product
        """
        search_iter = (
            generated.CdsPublication.search()
            .filter("term", satellite_unit=self.satellite_unit)
            .filter("term", datatake_id=self.datatake_id)
            .filter("term", product_type=self.product_type)
            .filter("term", service_type=self.service_type)
            .filter("term", service_id=self.service_id)
            .params(ignore=404)
            .scan()
        )

        return search_iter

    @staticmethod
    def init_completeness_document_from_compute_key(compute_key):
        """The goal of this method it's to generated the initial
        Completeness splitted document from a compute key

        Note:
            The observation time start/stop is not include in the compute key

        Args:
            compute_key (dict): compute_key to base the completeness document

        Returns:
            CdsSplittedDocument: The document that will match the compute_key
        """

        # A bit force, but idea is here
        completeness_document = compute_key["class"](**compute_key)
        completeness_document.purge_dynamic_fields()
        completeness_document.meta.id = compute_key["key"]
        completeness_document.meta.index = compute_key["index"]

        return completeness_document

    def is_compute_key_to_check_missing_orbit(self):
        """Frame method to specify the check if the product launch a
        missing orbit check/generation

        Returns:
            bool: True if this product enable a check
        """
        return False

    def get_previous_orbit_document(self):
        """Find the document with the same criteria, just a different datatake_id and also a lower sensing_start_date"""

        query = (
            self.search()
            .filter("term", satellite_unit=self.satellite_unit)
            .filter("bool", must_not=Q("term", datatake_id=self.datatake_id))
            .filter("term", timeliness=self.timeliness)
            .filter("term", product_type=self.product_type)
            .filter("term", service_type=self.service_type)
            .filter("term", service_id=self.service_id)
            .filter(
                "range",
                observation_time_start={"lt": self.observation_time_start},
            )
            .sort({"observation_time_start": {"order": "desc"}})
            .params(size=1)
        )
        try:
            previous_orbit_document = list(query.params(ignore=404).execute())[0]
        except IndexError as error:
            LOGGER.warning("[%s] - No previous orbit for this document", self.key)
            return None

        return previous_orbit_document
