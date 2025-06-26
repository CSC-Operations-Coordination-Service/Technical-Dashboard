"""Custom CDS model definition for s1 product"""

import logging

from maas_cds.model import generated
from maas_cds.model.generated import MaasConfig


__all__ = ["MaasConfigCompleteness"]


LOGGER = logging.getLogger("MaasConfigCompleteness")


class MaasConfigCompleteness(generated.MaasConfigCompleteness, MaasConfig):
    pass
