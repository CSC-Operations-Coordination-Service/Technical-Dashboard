from unittest.mock import patch

import pytest
import datetime

import maas_cds.model as model

from maas_cds.engines.reports import (
    ProductConsolidatorEngine,
    PublicationConsolidatorEngine,
)


@pytest.fixture
def prip_product_s1_eta():
    data_dict = {
        "reportName": "https://s1a.prip.copernicus.eu",
        "product_id": "0d97b026-119a-48f1-b654-9f932ba9fcf1",
        "product_name": "S1A_IW_ETA__AXDV_20230831T201111_20230831T201141_050124_06083C_81A7.SAFE.zip",
        "content_length": 89365277,
        "publication_date": "2023-09-21T15:16:38.245Z",
        "start_date": "2023-08-31T20:11:11.583Z",
        "end_date": "2023-08-31T20:11:41.495Z",
        "origin_date": "2023-09-01T02:46:13.852Z",
        "eviction_date": "2023-10-05T03:16:37.966Z",
        "interface_name": "PRIP_S1A_Serco",
        "production_service_type": "PRIP",
        "production_service_name": "S1A-Serco",
        "ingestionTime": "2023-09-21T15:39:06.238Z",
    }
    raw_document = model.PripProduct(**data_dict)
    raw_document.meta.id = "aecc9319b103df919c7fe929b6f28910"
    raw_document.full_clean()
    return raw_document


@patch("maas_cds.model.CdsDatatake.mget_by_ids")
def test_prip_publication_consolidation_s1_eta(mock_mget_by_ids, prip_product_s1_eta):
    datatake_doc = model.CdsDatatake()

    datatake_doc.datatake_id = "395324"
    datatake_doc.absolute_orbit = "50124"
    datatake_doc.instrument_mode = "IW"
    datatake_doc.timeliness = "NTC"

    mock_mget_by_ids.return_value = [datatake_doc]

    engine = PublicationConsolidatorEngine()

    publication = engine.consolidate_from_PripProduct(
        prip_product_s1_eta, model.CdsPublication()
    )

    engine.consolidated_documents = [publication]

    engine.on_post_consolidate()

    publication = engine.consolidated_documents[0]

    publication.full_clean()

    assert publication.to_dict() == {
        "absolute_orbit": "50124",
        "content_length": 89365277,
        "datatake_id": "395324",
        "eviction_date": "2023-10-05T03:16:37.966Z",
        "from_sensing_timeliness": 1796696750000.0,
        "instrument_mode": "IW",
        "key": "aecc9319b103df919c7fe929b6f28910",
        "mission": "S1",
        "name": "S1A_IW_ETA__AXDV_20230831T201111_20230831T201141_050124_06083C_81A7.SAFE.zip",
        "origin_date": "2023-09-01T02:46:13.852Z",
        "polarization": "DV",
        "product_level": "A",
        "product_class": "X",
        "product_type": "IW_ETA__AX",
        "product_uuid": "0d97b026-119a-48f1-b654-9f932ba9fcf1",
        "publication_date": "2023-09-21T15:16:38.245Z",
        "satellite_unit": "S1A",
        "sensing_start_date": "2023-08-31T20:11:11.583Z",
        "sensing_end_date": "2023-08-31T20:11:41.495Z",
        "sensing_duration": 29912000,
        "service_id": "S1A-Serco",
        "service_type": "PRIP",
        "transfer_timeliness": 1773024393000,
        "timeliness": "NTC",
    }


@pytest.fixture
def prip_product_s1_sm_footprint_bug():
    data_dict = {
        "reportName": "https://s1a.prip.copernicus.eu",
        "product_id": "2617797b-06c8-416c-84f1-38c78b7103cf",
        "product_name": "S1A_S6_RAW__0SDV_20231004T082929_20231004T083002_050613_0618E5_2CB0.SAFE.zip",
        "content_length": 1497084027,
        "publication_date": "2023-10-04T09:17:26.647Z",
        "start_date": "2023-10-04T08:29:29.717Z",
        "end_date": "2023-10-04T08:30:02.417Z",
        "origin_date": "2023-10-04T08:57:21.450Z",
        "eviction_date": "2023-10-17T21:17:25.819Z",
        "footprint": "geography'SRID=4326;Polygon((145.5501 17.3358,146.2801 17.4215,145.8977 19.3978,145.159 19.3133,145.5501 17.3358))'",
        "interface_name": "PRIP_S1A_Serco",
        "production_service_type": "PRIP",
        "production_service_name": "S1A-Serco",
        "ingestionTime": "2023-10-04T09:41:22.535Z",
    }
    raw_document = model.PripProduct(**data_dict)
    raw_document.meta.id = "b134306f56054f80a1801bc983fbc238"
    raw_document.full_clean()
    return raw_document


@patch("maas_cds.model.CdsDatatake.mget_by_ids")
def test_prip_publication_consolidation_s1_sm_footprint_bug(
    mock_mget_by_ids, prip_product_s1_sm_footprint_bug
):
    datatake_doc = model.CdsDatatake()

    datatake_doc.datatake_id = "399589"
    datatake_doc.absolute_orbit = "50613"
    datatake_doc.instrument_mode = "SM"
    datatake_doc.timeliness = "NTC"

    mock_mget_by_ids.return_value = [datatake_doc]

    engine = ProductConsolidatorEngine()

    product = engine.consolidate_from_PripProduct(
        prip_product_s1_sm_footprint_bug, model.CdsProduct()
    )

    engine.consolidated_documents = [product]

    engine.on_post_consolidate()

    product = engine.consolidated_documents[0]

    product.full_clean()

    assert product.to_dict() == {
        "absolute_orbit": "50613",
        "datatake_id": "399589",
        "PRIP_S1A_Serco_id": "2617797b-06c8-416c-84f1-38c78b7103cf",
        "PRIP_S1A_Serco_is_published": True,
        "PRIP_S1A_Serco_publication_date": datetime.datetime(
            2023, 10, 4, 9, 17, 26, 647000, tzinfo=datetime.timezone.utc
        ),
        "nb_prip_served": 1,
        "key": "4a19a9cc4b96420de2c15df1d90704a2",
        "instrument_mode": "SM",
        "mission": "S1",
        "name": "S1A_S6_RAW__0SDV_20231004T082929_20231004T083002_050613_0618E5_2CB0.SAFE.zip",
        "polarization": "DV",
        "product_class": "S",
        "product_type": "S6_RAW__0S",
        "product_level": "L0_",
        "satellite_unit": "S1A",
        "sensing_start_date": "2023-10-04T08:29:29.717Z",
        "sensing_end_date": "2023-10-04T08:30:02.417Z",
        "sensing_duration": 32700000,
        "timeliness": "NTC",
        "content_length": 1497084027,
        "prip_id": "2617797b-06c8-416c-84f1-38c78b7103cf",
        "prip_publication_date": "2023-10-04T09:17:26.647Z",
        "prip_service": "PRIP_S1A_Serco",
        "OCN_coverage_percentage": 100.0,
        "EU_coverage_percentage": 0.0,
    }


@pytest.fixture
def prip_product_s1c_ew_footprint_bug_antimeridian():
    data_dict = {
        "reportName": "https://prip.s1c.werum.copernicus.eu",
        "product_id": "9484cbcc-c1d0-48d8-0de6-010756521dd2",
        "product_name": "S1C_EW_RAW__0SDH_20250414T184546_20250414T184636_001893_003A5F_9B06.SAFE.zip",
        "content_length": 743895196,
        "publication_date": "2025-04-14T21:00:00.586Z",
        "start_date": "2025-04-14T18:45:46.712Z",
        "end_date": "2025-04-14T18:46:36.182Z",
        "origin_date": "2025-04-14T20:07:28.053Z",
        "eviction_date": "2025-05-14T21:00:00.586Z",
        "footprint": {
            "type": "Polygon",
            "coordinates": [
                [
                    [174.9862, 71.1153],
                    [173.5574, 68.1633],
                    [-176.9544, 67.381],
                    [-174.2251, 70.2348],
                    [174.9862, 71.1153],
                ]
            ],
            "crs": {"type": "name", "properties": {"name": "EPSG:4326"}},
        },
        "interface_name": "PRIP_S1C_Werum",
        "production_service_type": "PRIP",
        "production_service_name": "S1C-Werum",
        "ingestionTime": "2025-04-14T21:16:07.186Z",
    }
    raw_document = model.PripProduct(**data_dict)
    raw_document.meta.id = "b759d82f721504ea0c0db5f7ddd73fe7"
    raw_document.full_clean()
    return raw_document


@patch("maas_cds.model.CdsDatatake.mget_by_ids")
def test_prip_publication_consolidation_s1c_ew_footprint_bug_antimeridian(
    mock_mget_by_ids, prip_product_s1c_ew_footprint_bug_antimeridian
):
    datatake_doc = model.CdsDatatake()

    datatake_doc.datatake_id = "399589"
    datatake_doc.absolute_orbit = "50613"
    datatake_doc.instrument_mode = "SM"
    datatake_doc.timeliness = "NTC"

    mock_mget_by_ids.return_value = [datatake_doc]

    engine = ProductConsolidatorEngine()

    product = engine.consolidate_from_PripProduct(
        prip_product_s1c_ew_footprint_bug_antimeridian, model.CdsProduct()
    )

    engine.consolidated_documents = [product]

    engine.on_post_consolidate()

    product = engine.consolidated_documents[0]

    product.full_clean()

    print(product.to_dict())

    assert product.to_dict() == {
        "absolute_orbit": "50613",
        "datatake_id": "399589",
        "key": "7bd04c364f658646b5644cd4b36ab29e",
        "instrument_mode": "SM",
        "mission": "S1",
        "name": "S1C_EW_RAW__0SDH_20250414T184546_20250414T184636_001893_003A5F_9B06.SAFE.zip",
        "polarization": "DH",
        "product_class": "S",
        "product_type": "EW_RAW__0S",
        "product_level": "L0_",
        "satellite_unit": "S1C",
        "sensing_start_date": "2025-04-14T18:45:46.712Z",
        "sensing_end_date": "2025-04-14T18:46:36.182Z",
        "sensing_duration": 49470000,
        "timeliness": "NTC",
        "content_length": 743895196,
        "PRIP_S1C_Werum_is_published": True,
        "PRIP_S1C_Werum_publication_date": datetime.datetime(
            2025, 4, 14, 21, 0, 0, 586000, tzinfo=datetime.timezone.utc
        ),
        "PRIP_S1C_Werum_id": "9484cbcc-c1d0-48d8-0de6-010756521dd2",
        "nb_prip_served": 1,
        "prip_id": "9484cbcc-c1d0-48d8-0de6-010756521dd2",
        "prip_publication_date": "2025-04-14T21:00:00.586Z",
        "prip_service": "PRIP_S1C_Werum",
        "OCN_coverage_percentage": 100,
        "SLC_coverage_percentage": 100,
        "EU_coverage_percentage": 51.216492373449185,
    }


@pytest.fixture
def prip_product_s1_aisaux():
    data_dict = {
        "reportName": "https://s1c.prip.onda-dias.com",
        "product_id": "d3cacb4d-391c-4f5e-8cc9-e1401faa2a22",
        "product_name": "S1C_AISAUX_20241208T055101_20241208T055110_260C.SAFE.zip",
        "content_length": 11310,
        "publication_date": "2024-12-08T15:32:40.774Z",
        "start_date": "2024-12-08T05:51:01.487Z",
        "end_date": "2024-12-08T05:51:10.996Z",
        "origin_date": "2024-12-08T15:25:08.000Z",
        "eviction_date": "5721-02-10T15:32:40.768Z",
        "interface_name": "PRIP_S1C_Serco",
        "production_service_type": "PRIP",
        "production_service_name": "S1C-Serco",
        "ingestionTime": "2024-12-08T15:54:34.977Z",
    }
    raw_document = model.PripProduct(**data_dict)
    raw_document.meta.id = "196a723136985ffe5642ce4e38be93e0"
    raw_document.full_clean()
    return raw_document


@patch("maas_cds.model.CdsDatatake.mget_by_ids")
def test_prip_publication_consolidation_s1_eta(
    mock_mget_by_ids, prip_product_s1_aisaux
):
    datatake_doc = model.CdsDatatake()

    datatake_doc.datatake_id = "123456"
    datatake_doc.absolute_orbit = "123456"
    datatake_doc.instrument_mode = "AIS"
    datatake_doc.timeliness = "___"

    mock_mget_by_ids.return_value = [datatake_doc]

    engine = PublicationConsolidatorEngine()

    publication = engine.consolidate_from_PripProduct(
        prip_product_s1_aisaux, model.CdsPublication()
    )

    engine.consolidated_documents = [publication]

    engine.on_post_consolidate()

    publication = engine.consolidated_documents[0]

    publication.full_clean()

    assert publication.to_dict() == {
        "content_length": 11310,
        "sensing_duration": 9509000,
        "from_sensing_timeliness": 34889778000,
        "key": "196a723136985ffe5642ce4e38be93e0",
        "origin_date": "2024-12-08T15:25:08.000Z",
        "product_level": "AUX",
        "sensing_end_date": "2024-12-08T05:51:10.996Z",
        "datatake_id": "______",
        "eviction_date": "5721-02-10T15:32:40.768Z",
        "transfer_timeliness": 452774000,
        "service_id": "S1C-Serco",
        "service_type": "PRIP",
        "timeliness": "_",
        "mission": "S1",
        "product_type": "AISAUX",
        "satellite_unit": "S1C",
        "name": "S1C_AISAUX_20241208T055101_20241208T055110_260C.SAFE.zip",
        "publication_date": "2024-12-08T15:32:40.774Z",
        "sensing_start_date": "2024-12-08T05:51:01.487Z",
        "product_uuid": "d3cacb4d-391c-4f5e-8cc9-e1401faa2a22",
    }


@pytest.fixture
def prip_product_s1_ai_l0():
    data_dict = {
        "reportName": "https://s1c.prip.onda-dias.com",
        "product_id": "a662ebc0-779d-4a7b-bcf1-4169ee18ad15",
        "product_name": "S1C_AI_RAW__0____20200901T050304_20200901T064451_000017________44E0.SAFE.zip",
        "content_length": 94067550,
        "publication_date": "2024-10-16T09:20:31.289Z",
        "start_date": "2020-09-01T05:03:04.502Z",
        "end_date": "2020-09-01T06:44:51.249Z",
        "origin_date": "2024-09-13T02:40:00.000Z",
        "eviction_date": "5720-12-19T09:20:31.138Z",
        "interface_name": "PRIP_S1C_Serco",
        "production_service_type": "PRIP",
        "production_service_name": "S1C-Serco",
        "ingestionTime": "2024-10-20T20:46:29.503Z",
    }
    raw_document = model.PripProduct(**data_dict)
    raw_document.meta.id = "c5f5823312fe65ffa7291a6846e2993b"
    raw_document.full_clean()
    return raw_document


@patch("maas_cds.model.CdsDatatake.mget_by_ids")
def test_prip_publication_consolidation_s1_eta(mock_mget_by_ids, prip_product_s1_ai_l0):
    datatake_doc = model.CdsDatatake()

    datatake_doc.datatake_id = "123456"
    datatake_doc.absolute_orbit = "123456"
    datatake_doc.instrument_mode = "AIS"
    datatake_doc.timeliness = "___"

    mock_mget_by_ids.return_value = [datatake_doc]

    engine = PublicationConsolidatorEngine()

    publication = engine.consolidate_from_PripProduct(
        prip_product_s1_ai_l0, model.CdsPublication()
    )

    engine.consolidated_documents = [publication]

    engine.on_post_consolidate()

    publication = engine.consolidated_documents[0]

    publication.full_clean()

    assert publication.to_dict() == {
        "absolute_orbit": "17",
        "content_length": 94067550,
        "datatake_id": "______",
        "eviction_date": "5720-12-19T09:20:31.138Z",
        "from_sensing_timeliness": 130127740040000,
        "instrument_mode": "AI",
        "key": "c5f5823312fe65ffa7291a6846e2993b",
        "mission": "S1",
        "name": "S1C_AI_RAW__0____20200901T050304_20200901T064451_000017________44E0.SAFE.zip",
        "origin_date": "2024-09-13T02:40:00.000Z",
        "polarization": "__",
        "product_class": "_",
        "product_level": "L0_",
        "product_type": "AI_RAW__0_",
        "product_uuid": "a662ebc0-779d-4a7b-bcf1-4169ee18ad15",
        "publication_date": "2024-10-16T09:20:31.289Z",
        "satellite_unit": "S1C",
        "sensing_duration": 6106747000,
        "sensing_end_date": "2020-09-01T06:44:51.249Z",
        "sensing_start_date": "2020-09-01T05:03:04.502Z",
        "service_id": "S1C-Serco",
        "service_type": "PRIP",
        "timeliness": "_",
        "transfer_timeliness": 2875231289000,
    }
