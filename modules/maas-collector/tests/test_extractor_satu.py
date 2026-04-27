"""SatUnavailabilityExtractor tests"""

import os

from maas_collector.rawdata.extractor.xml import XMLExtractor
from opensearchpy import (
    Text,
    Integer,
    Keyword,
)

from maas_model import MAASRawDocument
from maas_collector.rawdata.extractor import SatUnavailabilityExtractor


DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


class SatUnavailabilityProduct(MAASRawDocument):
    class Index:
        name = "raw-data-sat-unavailability-product"

    _PARTITION_FIELD = "ingestionTime"
    _PARTITION_FIELD_FORMAT = "static"

    comment = Text()

    end_anx_offset = Integer()

    end_orbit = Keyword()

    end_time = Text()

    file_name = Text()

    interface_name = Keyword()

    mission = Keyword()

    production_service_name = Keyword()

    production_service_type = Keyword()

    start_anx_offset = Integer()

    start_orbit = Keyword()

    start_time = Text()

    subsystem = Keyword()

    type = Keyword()

    unavailability_reference = Keyword()

    unavailability_type = Keyword()


def test_satu_extractor():
    jext = SatUnavailabilityExtractor()

    extract = list(
        jext.extract(
            os.path.join(
                DATA_DIR,
                "S5P_OPER_REP__SUP___20221007T012935_20221007T035455_0001.EOF.xml",
            )
        )
    )[0]

    assert extract["start_orbit"] == "25817"
    assert extract["end_orbit"] == "25818"

    satu_product = SatUnavailabilityProduct(**extract)

    satu_product.full_clean()

    assert satu_product.to_dict() == {
        "comment": "Due to a collision risk identified for Sentinel-5P on 07/10/2022 "
        "a Collision Avoidance Manoeuvre (CAM) has been scheduled. Refer "
        "to event #27468 in SCARF for further details.",
        "end_orbit": "25818",
        "end_time": "UTC=2022-10-07T03:54:55",
        "file_name": "S5P_OPER_REP__SUP___20221007T012935_20221007T035455_0001",
        "interface_name": "Satellite-Unavailability",
        "mission": "Sentinel-5P",
        "production_service_name": "Exprivia",
        "production_service_type": "AUXIP",
        "reportName": "S5P_OPER_REP__SUP___20221007T012935_20221007T035455_0001.EOF.xml",
        "start_orbit": "25817",
        "start_time": "UTC=2022-10-07T01:29:35",
        "subsystem": "S/C Manoeuvre",
        "type": "Planned",
        "unavailability_reference": "S5P-UNA-2022/0009",
        "unavailability_type": "Return to Operations",
    }


def test_satu_extractor_format_v1():
    satu_ext = SatUnavailabilityExtractor()

    old_extract = list(
        satu_ext.extract(
            os.path.join(
                DATA_DIR,
                "Satu/S1A_OPER_REP__SUP___20251202T152325_20251202T171537_0001-OLD.EOF.xml",
            )
        )
    )[0]

    assert old_extract["start_orbit"] == "62138"
    assert old_extract["end_orbit"] == "62139"

    satu_product = SatUnavailabilityProduct(**old_extract)

    satu_product.full_clean()

    assert satu_product.to_dict() == {
        "file_name": "S1A_OPER_REP__SUP___20251202T152325_20251202T171537_0001",
        "mission": "Sentinel-1A",
        "unavailability_reference": "S1A-UNA-2025/0039",
        "unavailability_type": "Return to Operations",
        "subsystem": "OCP",
        "start_time": "UTC=2025-12-02T15:23:25",
        "start_orbit": "62138",
        "start_anx_offset": 3489,
        "end_time": "UTC=2025-12-02T17:15:37",
        "end_orbit": "62139",
        "end_anx_offset": 4297,
        "type": "UNPLANNED",
        "comment": "The PDHT was unavailable due to a Passthrough Blockage anomaly re-occurrence (GS1_SC-283) on 02/12/2025 at 15:23:25 UTC. The OCP link with T0 = 16:43:58 UTC was lost.",
        "interface_name": "Satellite-Unavailability",
        "production_service_type": "AUXIP",
        "production_service_name": "Exprivia",
        "reportName": "S1A_OPER_REP__SUP___20251202T152325_20251202T171537_0001-OLD.EOF.xml",
    }

    # Then start with the XMLExtractor


def test_satu_extractor_format_v2():

    xext = XMLExtractor(
        iterate_nodes="Data_Block/List_Of_Subsystem_Unavailabilities/",
        allow_partial=False,
        attr_map={
            "file_name": {"root_path": "Earth_Explorer_Header/Fixed_Header/File_Name"},
            "description": {
                "root_path": "Earth_Explorer_Header/Fixed_Header/File_Description"
            },
            "notes": {"root_path": "Earth_Explorer_Header/Fixed_Header/Notes"},
            "mission": {"root_path": "Earth_Explorer_Header/Fixed_Header/Mission"},
            "file_class": {
                "root_path": "Earth_Explorer_Header/Fixed_Header/File_Class"
            },
            "file_type": {"root_path": "Earth_Explorer_Header/Fixed_Header/File_Type"},
            "validity_start": {
                "root_path": "Earth_Explorer_Header/Fixed_Header/Validity_Period/Validity_Start"
            },
            "validity_stop": {
                "root_path": "Earth_Explorer_Header/Fixed_Header/Validity_Period/Validity_Stop"
            },
            "file_version": {
                "root_path": "Earth_Explorer_Header/Fixed_Header/File_Version"
            },
            "source_system": {
                "root_path": "Earth_Explorer_Header/Fixed_Header/Source/System"
            },
            "source_creator": {
                "root_path": "Earth_Explorer_Header/Fixed_Header/Source/Creator"
            },
            "source_creation_date": {
                "root_path": "Earth_Explorer_Header/Fixed_Header/Source/Creation_Date"
            },
            "unique_identifier": {"root_path": "Data_Block/Unique_Identifier"},
            "unavailability_reference": {
                "root_path": "Data_Block/Unavailability_Reference"
            },
            "unavailability_type": {"root_path": "Data_Block/Unavailability_Type"},
            "unavailability_status": {"root_path": "Data_Block/Unavailability_Status"},
            "comment": {"root_path": "Data_Block/Comment"},
            # Specific iteration
            "subsystem": "Subsystem",
            "start_time": "StartTime",
            "start_doy": "StartDOY",
            "start_orbit": "StartOrbit",
            "start_anx_offset": "StartAnxOffset",
            "end_time": "EndTime",
            "end_doy": "EndDOY",
            "end_orbit": "EndOrbit",
            "end_anx_offset": "EndAnxOffset",
            "type": "Type",
            "category": "Category",
            "comment": "Description",
            # Generic stuff
            "interface_name": {"python": "lambda c: 'Satellite-Unavailability'"},
            "production_service_type": {"python": "lambda c: 'AUXIP'"},
            "production_service_name": {"python": "lambda c: 'Exprivia'"},
        },
        converter_map={
            "creation_date": {
                "type": "python",
                "python": "lambda creation_date: creation_date[4:]",
            },
            "source_creation_date": {
                "type": "python",
                "python": "lambda source_creation_date: source_creation_date[4:]",
            },
            "validity_start": {
                "type": "python",
                "python": "lambda validity_start: validity_start[4:]",
            },
            "validity_stop": {
                "type": "python",
                "python": "lambda validity_stop: validity_stop[4:]",
            },
            "start_time": {
                "type": "python",
                "python": "lambda start_time: start_time[4:]",
            },
            "end_time": {
                "type": "python",
                "python": "lambda end_time: end_time[4:]",
            },
        },
    )
    new_extract = list(
        xext.extract(
            os.path.join(
                DATA_DIR,
                "Satu/S1A_OPER_REP__SUP___20251202T152325_20251202T171537_0001-NEW.EOF.xml",
            )
        )
    )[0]

    new_satu_product = SatUnavailabilityProduct(**new_extract)

    new_satu_product.full_clean()

    assert new_satu_product.to_dict() == {
        "description": "FOS and Spacecraft Unavailability Report",
        "file_version": "0001",
        "file_class": "OPER",
        "file_type": "REP__SUP__",
        "notes": "",
        "source_creation_date": "2025-12-02T00:00:00",
        "source_creator": "Unavailability Tool",
        "source_system": "FOS",
        "validity_start": "2025-12-02T15:23:25",
        "validity_stop": "2025-12-02T17:15:37",
        "category": "Secondary",
        "end_doy": "336",
        "start_doy": "336",
        "unavailability_status": "Closed",
        "unique_identifier": "3e3370bb-e9c6-40b1-b582-3d2f2d1c6584",
        # ---
        "file_name": "S1A_OPER_REP__SUP___20251202T152325_20251202T171537_0001",
        "mission": "Sentinel-1A",
        "unavailability_reference": "S1A-UNA-2025/0039",
        "unavailability_type": "Unplanned",
        "subsystem": "OCP",
        "start_time": "2025-12-02T15:23:25",
        "start_orbit": "62138",
        "start_anx_offset": 3489,
        "end_time": "2025-12-02T17:15:37",
        "end_orbit": "62139",
        "end_anx_offset": 4297,
        "type": "Unplanned",
        "comment": "The PDHT was unavailable due to a Passthrough Blockage anomaly re-occurrence (GS1_SC-283) on 02/12/2025 at 15:23:25 UTC. The OCP link with T0 = 16:43:58 UTC was lost.",
        "interface_name": "Satellite-Unavailability",
        "production_service_type": "AUXIP",
        "production_service_name": "Exprivia",
        "reportName": "S1A_OPER_REP__SUP___20251202T152325_20251202T171537_0001-NEW.EOF.xml",
    }
