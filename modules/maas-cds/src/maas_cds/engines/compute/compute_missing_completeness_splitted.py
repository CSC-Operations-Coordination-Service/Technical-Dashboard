"""Splitted Completeness calculation"""

import re
import typing
from maas_cds.lib.config_manager import MaasConfigManager
from maas_cds.model.configuration import MaasConfigCompleteness, MaasConfigDataflow
from maas_cds.model.configuration.maas_config import (
    MaasConfigCompletenessS5,
    MaasConfigCompletenessS3,
)
from maas_engine.engine.rawdata import DataEngine
from maas_cds.engines.reports.anomaly_impact import AnomalyImpactMixinEngine

__all__ = ["ComputeMissingCompletenessSplitted"]


class ComputeMissingCompletenessSplitted(AnomalyImpactMixinEngine, DataEngine):
    """Consolidate splitted completeness"""

    ENGINE_ID = "COMPUTE_MISSING_COMPLETENESS_SPLITTED"

    # * This is why current subclass are needed

    def __init__(self, args=None, target_model=None, completeness_tolerance=None):

        super().__init__(args)

        self.config_manager = MaasConfigManager(
            config_model_class=[
                MaasConfigDataflow(),
                MaasConfigCompleteness(),
                MaasConfigCompletenessS5(),
                MaasConfigCompletenessS3(),
            ]
        )

        self.target_model = self.get_model(target_model)
        self.target_model.COMPLETENESS_TOLERANCE = completeness_tolerance

        if self.target_model is None:
            raise KeyError(f"The target model doesn't exist: {self.target_model }")

    def action_iterator(self):
        """Compute completeness from CdsProduct

        Yields:
            dict: bulk action
        """

        self.logger.info("[ITER][%s] - start", self.target_model.__name__)

        # Get all compute key to then check all missing document

        for completeness_document in self.input_documents:

            if completeness_document.is_compute_key_to_check_missing_orbit():

                # To keep a ref on class/index
                self.logger.info(
                    "[ITER][Local Missing][%s] - start",
                    completeness_document.datatake_id,
                )

                current_brothers = (
                    completeness_document.generate_brother_completeness_key(
                        exclude_me=True
                    )
                )

                yield from self.try_get_and_create_it_if_missing(current_brothers)

                self.logger.info(
                    "[ITER][Local Missing][%s] - end", completeness_document.datatake_id
                )

                self.logger.info(
                    "[ITER][Orbit Missing][%s] - start",
                    completeness_document.datatake_id,
                )

                # Here completeness_document.get_previous_orbit_document()
                previous_orbit_document = (
                    completeness_document.get_previous_orbit_document()
                )

                if previous_orbit_document is None:
                    self.logger.info(
                        "[ITER][Orbit Missing][%s] - No previous",
                        completeness_document.datatake_id,
                    )
                    continue

                self.logger.info(
                    "[ITER][Orbit Missing][%s] - Previous was %s",
                    completeness_document.datatake_id,
                    previous_orbit_document.datatake_id,
                )

                missing_datatake_id = (
                    self.target_model.generate_datatake_ids_list_between_2_ids(
                        previous_orbit_document.datatake_id,
                        completeness_document.datatake_id,
                    )
                )

                previous_observation_time_start = (
                    completeness_document.observation_time_start
                )
                previous_observation_time_stop = (
                    completeness_document.observation_time_stop
                )
                duration = (
                    previous_observation_time_stop - previous_observation_time_start
                )

                self._populate_ticket_cache(missing_datatake_id)

                for datatake_id_to_create in missing_datatake_id:
                    self.logger.info(
                        "[ITER][Orbit Missing][%s] - In process of generation",
                        datatake_id_to_create,
                    )
                    current_brothers = (
                        completeness_document.generate_brother_completeness_key(
                            exclude_me=False
                        )
                    )

                    # Calculate new observation times
                    previous_observation_time_start -= duration
                    previous_observation_time_stop -= duration

                    # Update datatake_id in current_brothers for the missing datatake
                    for brother in current_brothers:
                        brother["datatake_id"] = datatake_id_to_create
                        brother["key"] = brother["key"].replace(
                            completeness_document.datatake_id, datatake_id_to_create
                        )

                        # Patch expected date
                        brother["observation_time_start"] = (
                            previous_observation_time_start
                        )
                        brother["observation_time_stop"] = (
                            previous_observation_time_stop
                        )

                    yield from self.try_get_and_create_it_if_missing(current_brothers)

                self.logger.info(
                    "[ITER][Orbit Missing][%s] - end", completeness_document.datatake_id
                )

            else:
                self.logger.debug(
                    "[ITER][%s] - Skipping compute key - %s",
                    self.target_model.__name__,
                    completeness_document.datatake_id,
                )

        self.logger.info("[ITER][%s] - end", self.target_model.__name__)

    def _populate_ticket_cache(self, datatake_ids):

        self._cams_tickets_dict = {}

        self._populate_by_Datatake(datatake_ids)

    def try_get_and_create_it_if_missing(self, current_brothers):

        current_brothers_keys = [bro["key"] for bro in current_brothers]

        if len(current_brothers) == 0:
            self.logger.debug(
                "[ITER][%s] - No brother provide",
            )
            return

        indices = [current_brothers[0]["index"]]

        # Here perform mget on current_brothers
        for (
            brother_key,
            brother_completeness_key,
            brother_completeness_document,
        ) in zip(
            current_brothers_keys,
            current_brothers,
            self.target_model.mget_by_ids(current_brothers_keys, indices),
        ):
            self.logger.debug(
                "[ITER][%s] - Checking existance of - %s",
                brother_key,
                brother_completeness_key["key"],
            )
            if brother_completeness_document is None:

                new_completeness_document = (
                    self.target_model.init_completeness_document_from_compute_key(
                        brother_completeness_key
                    )
                )

                new_completeness_document.evaluate_completeness()
                # Here this will be create to relocated the obervation time base also on the expected

                if new_completeness_document.observation_time_start is None:

                    self.logger.info(
                        "[Creating missing][%s] - Inflating Observation date for this missing product",
                        new_completeness_document.key,
                    )

                    new_completeness_document.observation_time_start = (
                        brother_completeness_key["observation_time_start"]
                    )
                    new_completeness_document.observation_time_stop = (
                        brother_completeness_key["observation_time_stop"]
                    )

                    # Recenter observation date if expected duration differs from actual
                    current_duration = (
                        new_completeness_document.observation_time_stop
                        - new_completeness_document.observation_time_start
                    )
                    expected_duration = new_completeness_document.expected

                    if expected_duration < current_duration:
                        center_time = (
                            new_completeness_document.observation_time_start
                            + expected_duration / 2
                        )
                        new_completeness_document.observation_time_start = (
                            center_time - expected_duration / 2
                        )
                        new_completeness_document.observation_time_stop = (
                            center_time + expected_duration / 2
                        )

                # Check anom
                if new_completeness_document.datatake_id in self._cams_tickets_dict:
                    self._apply_anomalies(new_completeness_document, key="datatake_id")

                # ? Add document to cache to flush all at the end
                yield new_completeness_document.to_bulk_action()

            else:
                self.logger.debug(
                    "[ITER][%s] - Document already exist key - %s",
                    self.target_model.__name__,
                    brother_key,
                )
