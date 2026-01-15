"""Custom CDS model definition for Config"""

import logging
from maas_cds.lib.config_manager import MaasConfigManager
from maas_cds.model import generated


__all__ = [
    "MaasConfig",
    "MaasConfigCompleteness",
    "MaasConfigCompletenessS3",
    "MaasConfigCompletenessS5",
    "MaasConfigService",
    "MaasConfigMission",
    "MaasConfigSatellite",
    "MaasConfigDataflow",
]


class MaasConfigError(Exception):
    """Custom exception for MaasConfig related errors"""

    pass


LOGGER = logging.getLogger("MaasConfig")


class MaasConfig(generated.MaasConfig):
    def load(self):
        document_config = list(
            self.search()
            .params(
                size=1000,
            )
            .execute()
        )

        if not document_config:
            LOGGER.warning("[%s] - No config find", self.__class__.__name__)
        else:
            LOGGER.warning(
                "[%s] - Load %s item(s)", self.__class__.__name__, len(document_config)
            )

        return document_config

    @classmethod
    def me(cls):
        return MaasConfigManager().get_config(cls.__name__)


class MaasConfigCompleteness(generated.MaasConfigCompleteness, MaasConfig):
    pass


class MaasConfigCompletenessS3(generated.MaasConfigCompletenessS3, MaasConfig):
    pass


class MaasConfigCompletenessS5(generated.MaasConfigCompletenessS5, MaasConfig):
    pass


class MaasConfigService(generated.MaasConfigService, MaasConfig):
    pass


class MaasConfigMission(generated.MaasConfigMission, MaasConfig):
    pass


class MaasConfigSatellite(generated.MaasConfigSatellite, MaasConfig):
    pass


class MaasConfigDataflow(generated.MaasConfigDataflow, MaasConfig):

    def load(self):
        # Here i need to handle multiple document and detect splitted
        all_latest_dataflows = self.search().filter("term", latest=True).execute()

        # Currently this is enough then need to detect iconsistency
        # "mission": "S1",
        # "product_type": "S1_RAW__0S",
        # "product_level": "L0_",
        aggregated_dataflow = {"records": []}
        existing_keys = set()
        for dataflow in all_latest_dataflows:
            # Check if this dataflow's records are already present
            for existing_record in dataflow["records"]:
                key = (
                    existing_record.get("product_type"),
                    existing_record.get("mission"),
                    existing_record.get("product_level"),
                )
                if key in existing_keys:
                    raise MaasConfigError(
                        f"Duplicate item {key} in dataflow tag as latest"
                    )

                existing_keys.add(key)

            # Use unique_records instead of dataflow.records
            aggregated_dataflow["records"].extend(dataflow.records)

        return aggregated_dataflow

    def load_level_type_mapping():
        # TODO
        pass
