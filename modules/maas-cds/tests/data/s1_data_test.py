import pytest
from maas_cds.model import DdProduct, DasProduct, PripProduct

from maas_cds.model.product_s1 import CdsProductS1

__all__ = [
    "s1_product_macp",
    "s1_datatake_iw",
    "s1_datatake_ew",
    "s1_datatake_wv",
    "s1_datatake_sm",
    "s1_datatake_rfc",
    "s1_products_ew_raw__0s_over_specific_area",
    "s1_product_ew",
    "s1_product_wv",
    "s1_product_rfc",
    "s1_dd_product_1",
    "s1_ddas_product_1",
    "s1_product_amalfi",
    "s1_raw_geopolygon",
    "s1_datatake_an",
    "s1_datatake_en",
    "s1_datatake_zs",
]

product_macp_dict = {
    "key": "9b644d15eefa49f35179175f90d2b729",
    "mission": "S1",
    "name": "S1B_OPER_REP__MACP__20160429T072531_20220615T224730_0001.TGZ",
    "product_level": "L__",
    "product_type": "REP__MACP_",
    "satellite_unit": "S1B",
    "sensing_start_date": "2016-04-29T07:25:31.000Z",
    "sensing_end_date": "2022-06-15T22:47:30.000Z",
    "sensing_duration": 193418519000000,
    "timeliness": "_",
    "auxip_id": "5c7b36c8-ec8a-11ec-a1af-fa163e7968e5",
    "auxip_publication_date": "2022-06-15T09:05:54.284Z",
    "updateTime": "2022-06-15T09:21:53.333Z",
}


@pytest.fixture
def s1_product_macp():
    product = CdsProductS1(**product_macp_dict)
    product.full_clean()
    return product


from maas_model import datestr_to_utc_datetime
import pytest

from maas_cds.model.datatake_s1 import CdsDatatakeS1
from maas_cds.model.product_s1 import CdsProductS1

# This one is over specific area
datatake_ew_dict = {
    "key": "S1A-340399",
    "datatake_id": "340399",
    "observation_time_start": "2022-06-03T18:01:48.848Z",
    "instrument_mode": "EW",
    "mission": "S1",
    "updateTime": "2022-06-15T16:59:07.650Z",
    "name": "S1A_MP_ACQ__L0__20220603T160000_20220615T180000.csv",
    "satellite_unit": "S1A",
    "observation_duration": 312953000,
    "observation_time_stop": "2022-06-03T18:07:01.801Z",
    "l0_sensing_duration": 315414000,
    "l0_sensing_time_start": "2022-06-03T18:01:47.547Z",
    "l0_sensing_time_stop": "2022-06-03T18:07:02.961Z",
    "absolute_orbit": "43502",
    "relative_orbit": "30",
    "polarization": "DH",
    "timeliness": "NRT-PT",
    "instrument_swath": "0",
    "application_date": "2022-06-03T16:00:00.000Z",
}


@pytest.fixture
def s1_datatake_ew():
    return CdsDatatakeS1(**datatake_ew_dict)


datatake_rfc_dict = {
    "name": "S1A_MP_ACQ__L0__20220503T160000_20220515T180000.csv",
    "key": "S1A-336924",
    "datatake_id": "336924",
    "satellite_unit": "S1A",
    "mission": "S1",
    "observation_time_start": "2022-05-03T22:44:20.996Z",
    "observation_duration": 20000000,
    "observation_time_stop": "2022-05-03T22:44:40.996Z",
    "l0_sensing_duration": 21595000,
    "l0_sensing_time_start": "2022-05-03T22:44:19.695Z",
    "l0_sensing_time_stop": "2022-05-03T22:44:41.290Z",
    "absolute_orbit": "43052",
    "relative_orbit": "105",
    "polarization": "DH",
    "timeliness": "NTC",
    "instrument_mode": "RFC",
    "instrument_swath": "0",
    "application_date": "2022-05-03T16:00:00.000Z",
    "updateTime": "2022-06-15T14:29:51.550Z",
}


@pytest.fixture
def s1_datatake_rfc():
    return CdsDatatakeS1(**datatake_rfc_dict)


datatake_iw_dict = {
    "name": "S1A_MP_ACQ__L0__20220503T160000_20220515T180000.csv",
    "key": "S1A-336890",
    "datatake_id": "336890",
    "satellite_unit": "S1A",
    "mission": "S1",
    "observation_time_start": "2022-05-03T16:11:00.778Z",
    "observation_duration": 215145000,
    "observation_time_stop": "2022-05-03T16:14:35.923Z",
    "l0_sensing_duration": 217232000,
    "l0_sensing_time_start": "2022-05-03T16:10:59.477Z",
    "l0_sensing_time_stop": "2022-05-03T16:14:36.709Z",
    "absolute_orbit": "43048",
    "relative_orbit": "101",
    "polarization": "DV",
    "timeliness": "NTC",
    "instrument_mode": "IW",
    "instrument_swath": "0",
    "application_date": "2022-05-03T16:00:00.000Z",
    "updateTime": "2022-06-15T14:29:44.019Z",
}


@pytest.fixture
def s1_datatake_iw():
    return CdsDatatakeS1(**datatake_iw_dict)


datatake_wv_dict = {
    "name": "S1A_MP_ACQ__L0__20220503T160000_20220515T180000.csv",
    "key": "S1A-336894",
    "datatake_id": "336894",
    "satellite_unit": "S1A",
    "mission": "S1",
    "observation_time_start": "2022-05-03T16:48:18.879Z",
    "observation_duration": 1083876000,
    "observation_time_stop": "2022-05-03T17:06:22.755Z",
    "l0_sensing_duration": 1085733000,
    "l0_sensing_time_start": "2022-05-03T16:48:17.578Z",
    "l0_sensing_time_stop": "2022-05-03T17:06:23.311Z",
    "absolute_orbit": "43049",
    "relative_orbit": "102",
    "polarization": "SV",
    "timeliness": "NTC",
    "instrument_mode": "WV",
    "instrument_swath": "0",
    "application_date": "2022-05-03T16:00:00.000Z",
    "updateTime": "2022-06-15T14:29:50.845Z",
}


@pytest.fixture
def s1_datatake_wv():
    datatake = CdsDatatakeS1(**datatake_wv_dict)
    datatake.full_clean()
    return datatake


datatake_sm_dict = {
    "name": "S1A_MP_ACQ__L0__20220506T160000_20220518T180000.csv",
    "key": "S1A-337321",
    "datatake_id": "337321",
    "satellite_unit": "S1A",
    "mission": "S1",
    "observation_time_start": "2022-05-07T07:23:47.272Z",
    "observation_duration": 24998000,
    "observation_time_stop": "2022-05-07T07:24:12.270Z",
    "l0_sensing_duration": 26589000,
    "l0_sensing_time_start": "2022-05-07T07:23:45.971Z",
    "l0_sensing_time_stop": "2022-05-07T07:24:12.560Z",
    "absolute_orbit": "43101",
    "relative_orbit": "154",
    "polarization": "DV",
    "timeliness": "NTC",
    "instrument_mode": "SM",
    "instrument_swath": "5",
    "application_date": "2022-05-06T16:00:00.000Z",
    "updateTime": "2022-06-15T14:30:39.262Z",
}


@pytest.fixture
def s1_datatake_sm():
    return CdsDatatakeS1(**datatake_sm_dict)


s1_datatake_an_dict = {
    "absolute_orbit": "1367",
    "application_date": "2025-03-05T17:31:59.000Z",
    "datatake_id": "9973",
    "duplicated_global_max_duration": 0,
    "duplicated_global_max_percentage": 0,
    "hex_datatake_id": "26F5",
    "instrument_mode": "AN",
    "instrument_swath": "2",
    "key": "S1C-9973",
    "l0_sensing_duration": 27514000,
    "l0_sensing_time_start": "2025-03-09T16:58:20.021Z",
    "l0_sensing_time_stop": "2025-03-09T16:58:47.535Z",
    "mission": "S1",
    "name": "S1C_MP_ACQ__L0__20250305T173159_20250313T181805.csv",
    "observation_duration": 27003000,
    "observation_time_start": ["2025-03-09T16:58:20.303Z"],
    "observation_time_stop": "2025-03-09T16:58:47.306Z",
    "polarization": "SV",
    "relative_orbit": "44",
    "satellite_unit": "S1C",
    "timeliness": "NTC",
    "updateTime": "2025-03-11T10:26:07.795Z",
}


@pytest.fixture
def s1_datatake_an():
    datatake = CdsDatatakeS1(**s1_datatake_an_dict)
    datatake.full_clean()
    return datatake


s1_datatake_en_dict = {
    "absolute_orbit": "1326",
    "application_date": "2025-03-05T17:31:59.000Z",
    "cams_description": "[S1C] D/O 1327 DT´s not extracted",
    "cams_origin": "Acquisition",
    "cams_tickets": ["GSANOM-17957"],
    "datatake_id": "9494",
    "duplicated_global_max_duration": 0,
    "duplicated_global_max_percentage": 0,
    "hex_datatake_id": "2516",
    "instrument_mode": "EN",
    "instrument_swath": "0",
    "key": "S1C-9494",
    "l0_sensing_duration": 120495000,
    "l0_sensing_time_start": "2025-03-06T22:52:24.842Z",
    "l0_sensing_time_stop": "2025-03-06T22:54:25.337Z",
    "last_attached_ticket": "GSANOM-17957",
    "last_attached_ticket_url": "https://esa-cams.atlassian.net/browse/GSANOM-17957",
    "mission": "S1",
    "name": "S1C_MP_ACQ__L0__20250305T173159_20250313T181805.csv",
    "observation_duration": 120017000,
    "observation_time_start": ["2025-03-06T22:52:25.124Z"],
    "observation_time_stop": "2025-03-06T22:54:25.141Z",
    "polarization": "DH",
    "relative_orbit": "3",
    "satellite_unit": "S1C",
    "timeliness": "NTC",
    "updateTime": "2025-03-10T13:46:24.341Z",
}


@pytest.fixture
def s1_datatake_en():
    datatake = CdsDatatakeS1(**s1_datatake_en_dict)
    datatake.full_clean()
    return datatake


s1_datatake_zs_dict = {
    "absolute_orbit": "1206",
    "application_date": "2025-02-24T17:42:06.000Z",
    "datatake_id": "8050",
    "duplicated_global_max_duration": 0,
    "duplicated_global_max_percentage": 0,
    "hex_datatake_id": "1F72",
    "instrument_mode": "ZS",
    "instrument_swath": "3",
    "key": "S1C-8050",
    "l0_sensing_duration": 793000,
    "l0_sensing_time_start": "2025-02-26T15:57:18.556Z",
    "l0_sensing_time_stop": "2025-02-26T15:57:19.349Z",
    "mission": "S1",
    "name": "S1C_MP_ACQ__L0__20250224T174206_20250227T184051.csv",
    "observation_duration": 274000,
    "observation_time_start": ["2025-02-26T15:57:18.883Z"],
    "observation_time_stop": "2025-02-26T15:57:19.157Z",
    "polarization": "SH",
    "relative_orbit": "58",
    "satellite_unit": "S1C",
    "timeliness": "NTC",
    "updateTime": "2025-02-24T14:57:08.865Z",
}


@pytest.fixture
def s1_datatake_zs():
    datatake = CdsDatatakeS1(**s1_datatake_zs_dict)
    datatake.full_clean()
    return datatake


product_ew_over_specific_area_data_dict_1 = {
    "absolute_orbit": "43502",
    "datatake_id": "340399",
    "key": "4d12fffe62a7bf2aed3cf701e7fa42df",
    "instrument_mode": "EW",
    "mission": "S1",
    "name": "S1A_EW_RAW__0SDH_20220603T180447_20220603T180555_043502_0531AF_8F11.SAFE.zip",
    "polarization": "DH",
    "product_class": "S",
    "product_level": "L0_",
    "product_type": "EW_RAW__0S",
    "satellite_unit": "S1A",
    "sensing_start_date": datestr_to_utc_datetime("2022-06-03T18:04:47.009Z"),
    "sensing_end_date": datestr_to_utc_datetime("2022-06-03T18:05:55.209Z"),
    "sensing_duration": 68200000,
    "timeliness": "NRT-PT",
    "prip_id": "752a1e1f-6247-452e-be49-a075c6735ea1",
    "prip_publication_date": "2022-06-03T18:17:42.957Z",
    "prip_service": "PRIP_S1A_Serco",
    "footprint": {
        "type": "Polygon",
        "coordinates": [
            [
                [-22.5228, 73.832],
                [-9.4386, 74.8951],
                [-13.4814, 78.9157],
                [-30.257, 77.5316],
                [-22.5228, 73.832],
            ]
        ],
    },
    "updateTime": "2022-06-15T16:59:07.532Z",
    "OCN_coverage_percentage": 57.10138667695313,
    "SLC_coverage_percentage": 0,
}

product_ew_over_specific_area_data_dict_2 = {
    "absolute_orbit": "43502",
    "datatake_id": "340399",
    "key": "6659ec1663ba2b486e10bcf30278a4c7",
    "instrument_mode": "EW",
    "mission": "S1",
    "name": "S1A_EW_RAW__0SDH_20220603T180147_20220603T180255_043502_0531AF_8377.SAFE.zip",
    "polarization": "DH",
    "product_class": "S",
    "product_level": "L0_",
    "product_type": "EW_RAW__0S",
    "satellite_unit": "S1A",
    "sensing_start_date": datestr_to_utc_datetime("2022-06-03T18:01:47.008Z"),
    "sensing_end_date": datestr_to_utc_datetime("2022-06-03T18:02:55.208Z"),
    "sensing_duration": 68200000,
    "timeliness": "NRT-PT",
    "prip_id": "96722805-3715-4c8b-bec6-d62922b22fd3",
    "prip_publication_date": "2022-06-03T18:17:11.605Z",
    "prip_service": "PRIP_S1A_Serco",
    "footprint": {
        "type": "Polygon",
        "coordinates": [
            [
                [-12.1926, 63.4718],
                [-4.0238, 64.1587],
                [-5.6186, 68.2383],
                [-15.1371, 67.4538],
                [-12.1926, 63.4718],
            ]
        ],
    },
    "updateTime": "2022-06-15T16:59:07.559Z",
    "OCN_coverage_percentage": 100,
    "SLC_coverage_percentage": 0,
}

product_ew_over_specific_area_data_dict_3 = {
    "absolute_orbit": "43502",
    "datatake_id": "340399",
    "key": "a85a0237513dfbac451b1a1510f9c90d",
    "instrument_mode": "EW",
    "mission": "S1",
    "name": "S1A_EW_RAW__0SDH_20220603T180547_20220603T180702_043502_0531AF_6CF5.SAFE.zip",
    "polarization": "DH",
    "product_class": "S",
    "product_level": "L0_",
    "product_type": "EW_RAW__0S",
    "satellite_unit": "S1A",
    "sensing_start_date": datestr_to_utc_datetime("2022-06-03T18:05:47.010Z"),
    "sensing_end_date": datestr_to_utc_datetime("2022-06-03T18:07:02.285Z"),
    "sensing_duration": 75275000,
    "timeliness": "NRT-PT",
    "prip_id": "56391afb-8b55-4d3a-ad66-fff7d90106ad",
    "prip_publication_date": "2022-06-03T18:17:43.110Z",
    "prip_service": "PRIP_S1A_Serco",
    "footprint": {
        "type": "Polygon",
        "coordinates": [
            [
                [-29.11, 77.1],
                [-12.8671, 78.4353],
                [-21.2311, 82.784],
                [-43.3422, 80.8219],
                [-29.11, 77.1],
            ]
        ],
    },
    "updateTime": "2022-06-15T16:59:07.525Z",
    "OCN_coverage_percentage": 15.38405660133326,
    "SLC_coverage_percentage": 0,
}

product_ew_over_specific_area_data_dict_4 = {
    "absolute_orbit": "43502",
    "datatake_id": "340399",
    "key": "e5e5b7eb61f34fd287338281b055e3f5",
    "instrument_mode": "EW",
    "mission": "S1",
    "name": "S1A_EW_RAW__0SDH_20220603T180247_20220603T180355_043502_0531AF_5125.SAFE.zip",
    "polarization": "DH",
    "product_class": "S",
    "product_level": "L0_",
    "product_type": "EW_RAW__0S",
    "satellite_unit": "S1A",
    "sensing_start_date": datestr_to_utc_datetime("2022-06-03T18:02:47.009Z"),
    "sensing_end_date": datestr_to_utc_datetime("2022-06-03T18:03:55.208Z"),
    "sensing_duration": 68199000,
    "timeliness": "NRT-PT",
    "prip_id": "de5ea742-936c-4777-8f5b-d491fb3ae0a7",
    "prip_publication_date": "2022-06-03T18:17:37.607Z",
    "prip_service": "PRIP_S1A_Serco",
    "footprint": {
        "type": "Polygon",
        "coordinates": [
            [
                [-14.7388, 66.9777],
                [-5.4069, 67.7484],
                [-7.404, 71.8173],
                [-18.5582, 70.9084],
                [-14.7388, 66.9777],
            ]
        ],
    },
    "updateTime": "2022-06-15T16:59:07.549Z",
    "OCN_coverage_percentage": 100,
    "SLC_coverage_percentage": 0,
}
product_ew_over_specific_area_data_dict_5 = {
    "absolute_orbit": "43502",
    "datatake_id": "340399",
    "key": "e8b0f28c1813c38dbaf0d69d015ea536",
    "instrument_mode": "EW",
    "mission": "S1",
    "name": "S1A_EW_RAW__0SDH_20220603T180347_20220603T180455_043502_0531AF_0EEB.SAFE.zip",
    "polarization": "DH",
    "product_class": "S",
    "product_level": "L0_",
    "product_type": "EW_RAW__0S",
    "satellite_unit": "S1A",
    "sensing_start_date": datestr_to_utc_datetime("2022-06-03T18:03:47.009Z"),
    "sensing_end_date": datestr_to_utc_datetime("2022-06-03T18:04:55.209Z"),
    "sensing_duration": 68200000,
    "timeliness": "NRT-PT",
    "prip_id": "3236677b-fb17-40f5-a387-f4d19bc7d31a",
    "prip_publication_date": "2022-06-03T18:17:41.937Z",
    "prip_service": "PRIP_S1A_Serco",
    "footprint": {
        "type": "Polygon",
        "coordinates": [
            [
                [-18.0291, 70.4399],
                [-7.1308, 71.329],
                [-9.8229, 75.3808],
                [-23.2716, 74.2877],
                [-18.0291, 70.4399],
            ]
        ],
    },
    "updateTime": "2022-06-15T16:59:07.538Z",
    "OCN_coverage_percentage": 95.74322120516635,
    "SLC_coverage_percentage": 0,
}


@pytest.fixture
def s1_products_ew_raw__0s_over_specific_area():
    return [
        CdsProductS1(**product_ew_over_specific_area_data_dict_1),
        CdsProductS1(**product_ew_over_specific_area_data_dict_2),
        CdsProductS1(**product_ew_over_specific_area_data_dict_3),
        CdsProductS1(**product_ew_over_specific_area_data_dict_4),
        CdsProductS1(**product_ew_over_specific_area_data_dict_5),
    ]


@pytest.fixture
def s1_product_ew():
    data_dict = {
        "absolute_orbit": "42587",
        "datatake_id": "332942",
        "footprint": {
            "type": "Polygon",
            "coordinates": [
                [
                    [95.597549, 15.290585],
                    [95.986031, 17.170599],
                    [93.623131, 17.606874],
                    [93.258141, 15.731363],
                    [95.597549, 15.290585],
                ]
            ],
        },
        "key": "5a068da5b0ed1cf471a8a61b0cfffd3d",
        "instrument_mode": "EW",
        "mission": "S1",
        "name": "S1A_EW_RAW__0SSH_20220402T010915_20220402T011024_042587_05148E_44D6.SAFE.zip",
        "polarization": "SH",
        "product_class": "S",
        "product_level": "L0_",
        "product_type": "EW_RAW__0S",
        "satellite_unit": "S1A",
        "sensing_start_date": "2022-04-02T01:09:15.874Z",
        "sensing_end_date": "2022-04-02T01:10:24.073Z",
        "sensing_duration": 68199000,
        "timeliness": "NTC",
        "prip_id": "d6d6ead9-8db3-47ca-b226-7187636c81ec",
        "prip_publication_date": "2022-04-02T02:16:28.532Z",
        "prip_service": "PRIP_S1A_Serco",
        "updateTime": "2022-06-15T08:21:44.952Z",
    }
    product_doc = CdsProductS1(**data_dict)
    product_doc.meta.id = "5a068da5b0ed1cf471a8a61b0cfffd3d"
    product_doc.full_clean()
    return product_doc


@pytest.fixture
def s1_product_wv():
    data_dict = {
        "absolute_orbit": "42575",
        "datatake_id": "332825",
        "footprint": "Polygon((95.597549 15.290585,95.986031 17.170599,93.623131 17.606874,93.258141 15.731363,95.597549 15.290585))'",
        "key": "b6d7e85303df7fd89179968ce86922f6",
        "instrument_mode": "WV",
        "mission": "S1",
        "name": "S1A_WV_RAW__0SSV_20220401T050401_20220401T051841_042575_051419_D03D.SAFE.zip",
        "polarization": "SV",
        "product_class": "S",
        "product_level": "L0_",
        "product_type": "WV_RAW__0S",
        "satellite_unit": "S1A",
        "sensing_start_date": "2022-04-01T05:04:01.414Z",
        "sensing_end_date": "2022-04-01T05:18:41.331Z",
        "sensing_duration": 879917000,
        "timeliness": "NTC",
        "prip_id": "bd878ac7-ae36-433c-983a-322e95286cbe",
        "prip_publication_date": "2022-04-02T09:59:03.390Z",
        "prip_service": "PRIP_S1A_Serco",
        "updateTime": "2022-06-15T08:23:02.559Z",
    }
    product_doc = CdsProductS1(**data_dict)
    product_doc.meta.id = "b6d7e85303df7fd89179968ce86922f6"
    product_doc.full_clean()
    return product_doc


@pytest.fixture
def s1_product_rfc():
    data_dict = {
        "absolute_orbit": "45775",
        "datatake_id": "358847",
        "key": "534a4191023c27c0b2931a84ad3fe1d5",
        "instrument_mode": "RFC",
        "mission": "S1",
        "name": "S1A_RF_RAW__0SDV_20221106T154325_20221106T154327_045775_0579BF_DFFA.SAFE.zip",
        "polarization": "DV",
        "product_class": "S",
        "product_type": "RF_RAW__0S",
        "product_level": "L0_",
        "satellite_unit": "S1A",
        "sensing_start_date": "2022-11-06T15:43:25.800Z",
        "sensing_end_date": "2022-11-06T15:43:27.208Z",
        "sensing_duration": 1408000,
        "timeliness": "NTC",
        "prip_id": "46fa6366-e604-4935-927f-f9ebf4454124",
        "prip_publication_date": "2022-11-06T16:31:26.298Z",
        "prip_service": "PRIP_S1A_Serco",
        "updateTime": "2022-11-06T17:22:13.317Z",
        "expected_lta_number": 4,
        "LTA_CloudFerro_is_published": True,
        "LTA_CloudFerro_publication_date": "2022-11-06T16:38:26.240000+00:00",
        "nb_lta_served": 4,
        "LTA_Werum_is_published": True,
        "LTA_Werum_publication_date": "2022-11-06T16:37:39.705000+00:00",
        "LTA_Acri_is_published": True,
        "LTA_Acri_publication_date": "2022-11-06T16:38:57.071000+00:00",
        "LTA_Exprivia_S1_is_published": True,
        "LTA_Exprivia_S1_publication_date": "2022-11-06T16:56:54.624000+00:00",
    }
    product_doc = CdsProductS1(**data_dict)
    product_doc.meta.id = "534a4191023c27c0b2931a84ad3fe1d5"
    product_doc.full_clean()
    return product_doc


@pytest.fixture
def s1_dd_product_1():
    data_dict = {
        "product_id": "7fe19497-072c-4ff0-87a3-903ec8b87903",
        "product_name": "S1A_IW_OCN__2SDH_20220207T093448_20220207T093513_041805_04F9D1_820F",
        "content_length": 6808830,
        "ingestion_date": "2022-02-07T12:30:05.341Z",
        "modification_date": "2022-02-07T12:33:02.606Z",
        "creation_date": "2022-02-07T12:33:02.606Z",
        "start_date": "2022-02-07T08:34:48.170Z",
        "end_date": "2022-02-07T08:35:13.169Z",
        "interface_name": "DD_DHUS",
        "production_service_type": "DD",
        "production_service_name": "DHUS",
    }
    raw_document = DdProduct(**data_dict)
    raw_document.meta.id = "c43d34bf843b455cdb83505fb49714f3"
    raw_document.full_clean()
    return raw_document


@pytest.fixture
def s1_ddas_product_1():
    data_dict = {
        "product_id": "7fe19497-072c-4ff0-87a3-903ec8b87903",
        "product_name": "S1A_IW_OCN__2SDH_20220207T093448_20220207T093513_041805_04F9D1_820F",
        "content_length": 6808830,
        "publication_date": "2022-02-07T12:33:02.606Z",
        "origin_date": "2022-02-07T12:33:02.606Z",
        "eviction_date": "2022-02-07T12:30:05.341Z",
        "start_date": "2022-02-07T08:34:48.170Z",
        "end_date": "2022-02-07T08:35:13.169Z",
        "interface_name": "DD_DAS",
        "production_service_type": "DD",
        "production_service_name": "DAS",
    }
    raw_document = DasProduct(**data_dict)
    raw_document.meta.id = "c43d34bf843b455cdb83505fb49714f2"
    raw_document.full_clean()
    return raw_document


@pytest.fixture
def s1_product_amalfi():
    data_dict = {
        "absolute_orbit": "45906",
        "datatake_id": "359972",
        "key": "110c602e23e60ef3e39016e437c354fd",
        "instrument_mode": "IW",
        "mission": "S1",
        "name": "S1A_IW_SLC__1SDV_20221115T153910_20221115T153940_045906_057E24_619B.SAFE-report-20221115T181601.xml",
        "polarization": "DV",
        "product_class": "S",
        "product_type": "AMALFI_REPORT",
        "product_level": "Quality",
        "satellite_unit": "S1A",
        "sensing_start_date": "2022-11-15T15:39:10.000Z",
        "sensing_end_date": "2022-11-15T15:39:40.000Z",
        "sensing_duration": 30000000,
        "timeliness": "_",
        "prip_id": "d74f4707-b183-469e-ac2a-edca87ec0b26",
        "prip_publication_date": "2022-11-15T18:20:29.357Z",
        "prip_service": "PRIP_S1A_Serco",
        "updateTime": "2022-11-15T18:38:24.948Z",
    }
    raw_document = CdsProductS1(**data_dict)
    raw_document.meta.id = "110c602e23e60ef3e39016e437c354fd"
    raw_document.full_clean()
    return raw_document


@pytest.fixture
def s1_raw_geopolygon():
    data_dict = {
        "reportName": "https://s1a.prip.copernicus.eu",
        "product_id": "0b79ce4d-e0e2-471f-815c-ec7d0eb34c97",
        "product_name": "S1A_IW_RAW__0SDV_20240105T130451_20240105T130524_051972_0647B4_AA35.SAFE.zip",
        "content_length": 1595655028,
        "publication_date": "2024-01-05T13:40:13.090Z",
        "start_date": "2024-01-05T13:04:51.829Z",
        "end_date": "2024-01-05T13:05:24.229Z",
        "origin_date": "2024-01-05T13:24:04.000Z",
        "eviction_date": "2024-01-19T01:40:12.369Z",
        "footprint": {
            "type": "Polygon",
            "coordinates": [[[60, 11], [65, 11], [65, 13], [60, 13], [60, 11]]],
        },
        "interface_name": "PRIP_S1A_Serco",
        "production_service_type": "PRIP",
        "production_service_name": "S1A-Serco",
        "ingestionTime": "2024-01-05T13:56:17.904Z",
    }
    raw_document = PripProduct(**data_dict)
    raw_document.meta.id = "863af8d6bb48b4c251a8b7883f2d9d53"
    raw_document.meta.index = "raw-data-prip-product-2024-01"
    raw_document.full_clean()

    return raw_document
