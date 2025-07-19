"""Custom CDS model definition for Config"""

import logging

from maas_cds.model import generated
from maas_cds.model.generated import MaasConfig


__all__ = [
    "MaasConfigCompleteness",
    "MaasConfigService",
    "MaasConfigMission",
    "MaasConfigSatellite",
    "MaasConfigDataflow",
]


LOGGER = logging.getLogger("MaasConfigCompleteness")


class MaasConfigCompleteness(generated.MaasConfigCompleteness, MaasConfig):
    pass


class MaasConfigService(generated.MaasConfigService, MaasConfig):
    pass


class MaasConfigMission(generated.MaasConfigMission, MaasConfig):
    pass


class MaasConfigSatellite(generated.MaasConfigSatellite, MaasConfig):
    pass


class MaasConfigDataflow(generated.MaasConfigDataflow, MaasConfig):
    pass
