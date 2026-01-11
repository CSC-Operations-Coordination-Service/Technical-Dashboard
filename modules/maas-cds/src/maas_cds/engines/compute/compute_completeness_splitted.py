"""Splitted Completeness calculation"""

from maas_cds.engines.reports.mission_mixin import MissionMixinEngine
from maas_cds.lib.config_manager import MaasConfigManager
from maas_cds.lib.parsing_name.utils import DATATAKE_ID_MISSING_VALUE
from maas_cds.model.cds_completeness.cds_completeness_splitted import (
    CdsCompletenessSplitted,
)
from maas_cds.model.configuration import (
    MaasConfigCompleteness,
    MaasConfigDataflow,
    MaasConfigCompletenessS3,
    MaasConfigCompletenessS5,
)
from maas_engine.engine.rawdata import DataEngine
from maas_cds.engines.reports.anomaly_impact import AnomalyImpactMixinEngine

__all__ = ["ComputeCompletenessSplitted"]


class ComputeCompletenessSplitted(
    MissionMixinEngine, AnomalyImpactMixinEngine, DataEngine
):
    """Consolidate splitted completeness"""

    ENGINE_ID = "COMPUTE_COMPLETENESS_SPLITTED"

    # This is not completelty generic, this allow keep some simple state
    cache_no_completeness_key = {"S3": set(), "S5": set()}
    cache_completeness_key = {"S3": set(), "S5": set()}

    def __init__(
        self,
        args=None,
        send_reports=False,
        target_model=None,
        completeness_tolerance=None,
    ):

        super().__init__(args, send_reports)

        self.config_manager = MaasConfigManager(
            config_model_class=[
                MaasConfigDataflow(),
                MaasConfigCompleteness(),
                MaasConfigCompletenessS3(),
                MaasConfigCompletenessS5(),
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

        self.logger.info("[ITER][Publication] - start")

        # Compute all compute key to then load all needed document
        completeness_keys = []
        for publication_document in self.input_documents:

            if publication_document.datatake_id == DATATAKE_ID_MISSING_VALUE:
                continue

            publication_short_key = (
                publication_document.timeliness + publication_document.product_type
            )

            if (
                publication_short_key
                in self.cache_no_completeness_key[publication_document.mission]
            ):
                continue

            if (
                publication_short_key
                in self.cache_completeness_key[publication_document.mission]
            ):
                pass
            else:
                # Try to find a matching
                config_completeness = MaasConfigManager().get_config(
                    f"MaasConfigCompleteness{publication_document.mission}"
                )[0]

                # Filter config completeness item to find the one that matches product_type and timeliness
                matching_items = [
                    item
                    for item in config_completeness["records"]
                    if item.product_type == publication_document.product_type
                    and item.timeliness == publication_document.timeliness
                ]
                if not matching_items:
                    self.cache_no_completeness_key[publication_document.mission].add(
                        publication_short_key
                    )
                    continue
                else:
                    self.cache_completeness_key[publication_document.mission].add(
                        publication_short_key
                    )

            applicable_configs = [
                config
                for config in self.config_manager.get_config("MaasConfigCompleteness")
                if config.mission == publication_document.mission
                and config.satellite_unit == publication_document.satellite_unit
                and config.activated
                and config.start_date <= publication_document.sensing_start_date
                and config.end_date >= publication_document.sensing_end_date
                and config.service_type == publication_document.service_type
                and config.service_id == publication_document.service_id
            ]

            if len(applicable_configs) == 0:
                self.logger.warning(
                    "[ITER][Publication] - Attempts to compute unexpected completeness <%s>",
                    publication_document.meta.id,
                )
                continue

            completeness_key = publication_document.completeness_splitted_key

            if not completeness_key:
                self.logger.warning(
                    "[ITER][Publication] - (%s) : No compute key",
                    publication_document.name,
                )
            elif completeness_key in completeness_keys:
                self.logger.debug(
                    "[ITER][Publication] - (%s) : Compute key already present",
                    publication_document.name,
                )
            else:
                completeness_keys.append(completeness_key)
                self.logger.info(
                    "[ITER][Publication] - (%s) : Add a new compute key (%s)",
                    publication_document.name,
                    len(completeness_keys),
                )

        self.logger.info("[ITER][Publication] - end")

        # This should be after creating missing orbit
        # load related tickets
        self._populate_ticket_cache(
            list(
                set(
                    completeness_key["datatake_id"]
                    for completeness_key in completeness_keys
                )
            )
        )

        self.logger.info("[ITER][Completeness] - start")
        # ? Check performance maybe group into single query
        for completeness_key in completeness_keys:

            self.logger.info(
                "[ITER][Completeness][%s] - On going to evaluate (%s)",
                completeness_key["key"],
                completeness_key["index"],
            )

            completeness_document = self.get_implied_completeness(completeness_key)

            if completeness_document is None:
                completeness_document = completeness_key[
                    "class"
                ].init_completeness_document_from_compute_key(completeness_key)

                original_local_cache_completeness = {}
            else:
                original_local_cache_completeness = completeness_document.to_dict()

            completeness_document.evaluate_completeness()

            if completeness_document.datatake_id in self._cams_tickets_dict:
                self._apply_anomalies(completeness_document, key="datatake_id")

            new_doc_dict = completeness_document.to_dict()

            # update was made
            if (
                original_local_cache_completeness | new_doc_dict
                != original_local_cache_completeness
            ):

                self.logger.info(
                    "[ITER][Completeness][%s] - Pushing update",
                    completeness_key["key"],
                )

                # go feed parallel_bulk
                # completeness_document
                if completeness_document.is_compute_key_to_check_missing_orbit():
                    self.report(completeness_document)

                yield completeness_document.to_bulk_action()

            else:
                self.logger.debug(
                    "[ITER][Completeness][%s] - Nothing to do",
                    completeness_key["key"],
                )

        self.logger.info("[ITER][Completeness] - end")

    def _populate_ticket_cache(self, datatake_ids):

        self._cams_tickets_dict = {}

        self._populate_by_Datatake(datatake_ids)

    def get_implied_completeness(self, compute_key):

        # ? This can be a dedicated class to simplify the usage and avoid this
        completeness_document = compute_key["class"].get_by_id(
            compute_key["key"],
            [compute_key["index"]],
        )

        return completeness_document

    def shall_report(self, document: CdsCompletenessSplitted) -> bool:
        """override to allow reporting for speciifc product

        Args:
            document (document:model.CdsCompletenessSplitted): new completeness

        Returns:
            bool: True if product match extra compute needing
        """
        return document.is_compute_key_to_check_missing_orbit()
