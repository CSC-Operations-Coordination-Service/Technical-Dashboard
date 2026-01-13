from unittest.mock import patch
from maas_cds.lib.config_manager import MaasConfigManager
from maas_cds.model.cds_completeness.cds_completeness_splitted_s5 import (
    CdsCompletenessSplittedS5,
)
from maas_cds.model.configuration import MaasConfigCompletenessS5
import pytest
from maas_model.date_utils import datestr_to_utc_datetime


@pytest.fixture
def cds_completeness_splitted_s5_dict():
    """Get a basic cds_s5_completeness_dict
    matching

    Usefull to recreate a CdsCompletenessSplittedS5
    Returns:
        dict: return a dict of a CdsCompletenessSplittedS5
    """
    return {
        "key": "S5P-42634-NRTI-L1B_RA_BD4",
        "mission": "S5",
        "satellite_unit": "S5P",
        "datatake_id": "S5P-42634",
        "product_type": "L1B_RA_BD4",
        "timeliness": "NRTI",
        "service_type": "DD",
        "service_id": "DAS",
        "value": 4030000000,
        "status": "Complete",
        "observation_time_start": datestr_to_utc_datetime("2026-01-04T10:27:08.000Z"),
        "observation_time_stop": datestr_to_utc_datetime("2026-01-04T11:34:18.000Z"),
        "updateTime": datestr_to_utc_datetime("2026-01-12T23:26:29.699Z"),
    }


@patch("maas_cds.model.configuration.MaasConfigCompletenessS5.load")
def test_expected_splitted_with_tolerence_splitted(
    mock_maas_config_load, cds_completeness_splitted_s5_dict
):
    """Test completeness and observation period computation"""
    mock_maas_config_load.return_value = [
        MaasConfigCompletenessS5(
            **{
                "latest": True,
                "key": "v1",
                "records": [
                    {
                        "timeliness": "OPER",
                        "sensing_in_minutes": 100,
                        "product_type": "L0__ENG_A_",
                    },
                    {
                        "timeliness": "OPER",
                        "sensing_in_minutes": 100,
                        "product_type": "L0__ODB_1_",
                    },
                    {
                        "timeliness": "OPER",
                        "sensing_in_minutes": 100,
                        "product_type": "L0__ODB_2_",
                    },
                    {
                        "timeliness": "OPER",
                        "sensing_in_minutes": 100,
                        "product_type": "L0__ODB_3_",
                    },
                    {
                        "timeliness": "OPER",
                        "sensing_in_minutes": 100,
                        "product_type": "L0__ODB_4_",
                    },
                    {
                        "timeliness": "OPER",
                        "sensing_in_minutes": 100,
                        "product_type": "L0__ODB_5_",
                    },
                    {
                        "timeliness": "OPER",
                        "sensing_in_minutes": 100,
                        "product_type": "L0__ODB_6_",
                    },
                    {
                        "timeliness": "OPER",
                        "sensing_in_minutes": 100,
                        "product_type": "L0__ODB_7_",
                    },
                    {
                        "timeliness": "OPER",
                        "sensing_in_minutes": 100,
                        "product_type": "L0__ODB_8_",
                    },
                    {
                        "timeliness": "OPER",
                        "sensing_in_minutes": 100,
                        "product_type": "L0__SAT_A_",
                    },
                    {
                        "timeliness": "NRTI",
                        "sensing_in_minutes": 100,
                        "product_type": "L1B_ENG_DB",
                    },
                    {
                        "timeliness": "NRTI",
                        "sensing_in_minutes": 60,
                        "product_type": "L1B_RA_BD1",
                    },
                    {
                        "timeliness": "NRTI",
                        "sensing_in_minutes": 60,
                        "product_type": "L1B_RA_BD2",
                    },
                    {
                        "timeliness": "NRTI",
                        "sensing_in_minutes": 60,
                        "product_type": "L1B_RA_BD3",
                    },
                    {
                        "timeliness": "NRTI",
                        "sensing_in_minutes": 60,
                        "product_type": "L1B_RA_BD4",
                    },
                    {
                        "timeliness": "NRTI",
                        "sensing_in_minutes": 60,
                        "product_type": "L1B_RA_BD5",
                    },
                    {
                        "timeliness": "NRTI",
                        "sensing_in_minutes": 60,
                        "product_type": "L1B_RA_BD6",
                    },
                    {
                        "timeliness": "NRTI",
                        "sensing_in_minutes": 60,
                        "product_type": "L1B_RA_BD7",
                    },
                    {
                        "timeliness": "NRTI",
                        "sensing_in_minutes": 60,
                        "product_type": "L1B_RA_BD8",
                    },
                    {
                        "timeliness": "NRTI",
                        "sensing_in_minutes": 55,
                        "product_type": "L2__AER_AI",
                    },
                    {
                        "timeliness": "NRTI",
                        "sensing_in_minutes": 55,
                        "product_type": "L2__AER_LH",
                    },
                    {
                        "timeliness": "NRTI",
                        "sensing_in_minutes": 55,
                        "product_type": "L2__CLOUD_",
                    },
                    {
                        "timeliness": "NRTI",
                        "sensing_in_minutes": 55,
                        "product_type": "L2__CO____",
                    },
                    {
                        "timeliness": "NRTI",
                        "sensing_in_minutes": 55,
                        "product_type": "L2__FRESCO",
                    },
                    {
                        "timeliness": "NRTI",
                        "sensing_in_minutes": 55,
                        "product_type": "L2__HCHO__",
                    },
                    {
                        "timeliness": "NRTI",
                        "sensing_in_minutes": 55,
                        "product_type": "L2__NO2___",
                    },
                    {
                        "timeliness": "NRTI",
                        "sensing_in_minutes": 55,
                        "product_type": "L2__O3__PR",
                    },
                    {
                        "timeliness": "NRTI",
                        "sensing_in_minutes": 55,
                        "product_type": "L2__O3____",
                    },
                    {
                        "timeliness": "NRTI",
                        "sensing_in_minutes": 55,
                        "product_type": "L2__SO2___",
                    },
                    {
                        "timeliness": "OFFL",
                        "sensing_in_minutes": 100,
                        "product_type": "L1B_ENG_DB",
                    },
                    {
                        "timeliness": "OFFL",
                        "sensing_in_minutes": 100,
                        "product_type": "L1B_RA_BD1",
                    },
                    {
                        "timeliness": "OFFL",
                        "sensing_in_minutes": 100,
                        "product_type": "L1B_RA_BD2",
                    },
                    {
                        "timeliness": "OFFL",
                        "sensing_in_minutes": 100,
                        "product_type": "L1B_RA_BD3",
                    },
                    {
                        "timeliness": "OFFL",
                        "sensing_in_minutes": 100,
                        "product_type": "L1B_RA_BD4",
                    },
                    {
                        "timeliness": "OFFL",
                        "sensing_in_minutes": 100,
                        "product_type": "L1B_RA_BD5",
                    },
                    {
                        "timeliness": "OFFL",
                        "sensing_in_minutes": 100,
                        "product_type": "L1B_RA_BD6",
                    },
                    {
                        "timeliness": "OFFL",
                        "sensing_in_minutes": 100,
                        "product_type": "L1B_RA_BD7",
                    },
                    {
                        "timeliness": "OFFL",
                        "sensing_in_minutes": 100,
                        "product_type": "L1B_RA_BD8",
                    },
                    {
                        "timeliness": "OFFL",
                        "sensing_in_minutes": 55,
                        "product_type": "L2__AER_AI",
                    },
                    {
                        "timeliness": "OFFL",
                        "sensing_in_minutes": 55,
                        "product_type": "L2__AER_LH",
                    },
                    {
                        "timeliness": "OFFL",
                        "sensing_in_minutes": 55,
                        "product_type": "L2__CH4___",
                    },
                    {
                        "timeliness": "OFFL",
                        "sensing_in_minutes": 55,
                        "product_type": "L2__CLOUD_",
                    },
                    {
                        "timeliness": "OFFL",
                        "sensing_in_minutes": 55,
                        "product_type": "L2__CO____",
                    },
                    {
                        "timeliness": "OFFL",
                        "sensing_in_minutes": 55,
                        "product_type": "L2__FRESCO",
                    },
                    {
                        "timeliness": "OFFL",
                        "sensing_in_minutes": 55,
                        "product_type": "L2__HCHO__",
                    },
                    {
                        "timeliness": "OFFL",
                        "sensing_in_minutes": 55,
                        "product_type": "L2__NO2___",
                    },
                    {
                        "timeliness": "OFFL",
                        "sensing_in_minutes": 55,
                        "product_type": "L2__NP_BD3",
                    },
                    {
                        "timeliness": "OFFL",
                        "sensing_in_minutes": 55,
                        "product_type": "L2__NP_BD6",
                    },
                    {
                        "timeliness": "OFFL",
                        "sensing_in_minutes": 55,
                        "product_type": "L2__NP_BD7",
                    },
                    {
                        "timeliness": "OFFL",
                        "sensing_in_minutes": 55,
                        "product_type": "L2__O3__PR",
                    },
                    {
                        "timeliness": "OFFL",
                        "sensing_in_minutes": 55,
                        "product_type": "L2__O3____",
                    },
                    {
                        "timeliness": "OFFL",
                        "sensing_in_minutes": 55,
                        "product_type": "L2__SO2___",
                    },
                ],
            }
        )
    ]

    MaasConfigManager(
        config_model_class=[
            MaasConfigCompletenessS5(),
        ]
    )
    completeness_doc = CdsCompletenessSplittedS5(**cds_completeness_splitted_s5_dict)
    completeness_doc.COMPLETENESS_TOLERANCE = {
        "S5": {
            "local": {
                "L0__(ENG_A_|ODB_[1-8]_|SAT_A)": -180000000,
                "L1B_(ENG_DB|RA_BD[1-8])": -180000000,
                "L2__(AER_AI|AER_LH|CH4___|CLOUD_|CO____|FRESCO|HCHO__|NO2___|NP_BD(3|6|7)|O3__PR|O3____|SO2___)": -180000000,
            }
        }
    }
    assert completeness_doc.get_expected_value() == 3420000000
