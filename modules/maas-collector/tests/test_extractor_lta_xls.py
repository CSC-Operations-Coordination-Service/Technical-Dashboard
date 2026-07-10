"""
Test extraction of a legacy binary ``.xls`` LTA deletion list.

These tests exercise the real ``maas-collector-conf-lta-deletion.json``
configuration to check that:

* the ``LTA_Deletion_XLSX`` collector ``file_pattern`` matches ``.xls`` files
  (not only ``.xlsx``),
* its :class:`XLSXExtractor` reads the binary ``.xls`` file correctly.

No database injection is involved: only the configuration-driven extraction
is verified.
"""

import os

from maas_collector.rawdata import configuration
from maas_collector.rawdata.collector.filecollector import FileCollectorConfiguration

CURRENT_DIR = os.path.dirname(__file__)

DATA_DIR = os.path.join(CURRENT_DIR, "data")

# copy of the production LTA deletion configuration
CONFIG_PATH = os.path.join(
    CURRENT_DIR, "conf", "maas-collector-conf-lta-deletion.json"
)

XLS_FILENAME = "LTA_S2B__DelList_20250528_V20250526_20250526.xls"

XLS_PATH = os.path.join(DATA_DIR, XLS_FILENAME)


def _matching_config():
    """load the real config and return the collector matching the .xls file"""
    configs = list(
        configuration.load_json(CONFIG_PATH, FileCollectorConfiguration)
    )
    matches = [config for config in configs if config.filename_match(XLS_FILENAME)]
    return matches


def test_lta_deletion_config_matches_xls():
    """the LTA deletion config shall route a .xls file to the XLSX extractor"""
    matches = _matching_config()

    # a single collector shall accept the .xls file
    assert len(matches) == 1

    config = matches[0]

    assert config.interface_name == "LTA_Deletion_XLSX"
    assert type(config.extractor).__name__ == "XLSXExtractor"


def test_lta_deletion_xls_extraction():
    """the configured XLSX extractor shall read every row of the binary .xls"""
    config = _matching_config()[0]

    extract = list(config.extractor.extract(XLS_PATH))

    # one extracted product per row
    assert len(extract) == 2077

    # every record carries the interface type and the source report name
    for record in extract:
        assert record["interface_type"] == "LTA"
        assert record["reportName"] == XLS_FILENAME

    # first and last product names are read verbatim from the binary file
    assert (
        extract[0]["product_name"]
        == "S2B_OPER_MSI_L0__DS_2BPS_20250526T112813_S20250526T091633_N05.11.tar"
    )
    assert (
        extract[-1]["product_name"]
        == "S2B_OPER_MSI_L0__GR_2BPS_20250526T112813_S20250526T091955_D06_N05.11.tar"
    )
