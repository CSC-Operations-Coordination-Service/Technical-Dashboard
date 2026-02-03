from opensearchpy import Keyword

from maas_cds.model import generated


class CdsDownlinkDatatake(generated.CdsDownlinkDatatake):

    expected_tiles = Keyword(multi=True)
