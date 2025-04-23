"""Module to test GeoMaskUtils class"""

from unittest.mock import patch
import unittest
import pytest
from maas_cds import model
from maas_cds.lib.geo_mask_utils import GeoMaskUtils
from opensearchpy.helpers.utils import AttrDict


def test_geo_cache():
    geo_mask_utils = GeoMaskUtils()

    # Purge cache for test purpose
    GeoMaskUtils.CACHED_MASK = {}

    assert len(GeoMaskUtils.CACHED_MASK) == 0

    geo_mask_utils.load_mask("ne_110m_ocean.geojson")

    assert len(GeoMaskUtils.CACHED_MASK) > 0


def test_s1_ew(s1_product_ew):
    geo_mask_utils = GeoMaskUtils()

    result = geo_mask_utils.coverage_over_specific_area_s1(
        s1_product_ew.satellite_unit,
        s1_product_ew.instrument_mode,
        s1_product_ew.footprint,
        s1_product_ew.sensing_start_date,
    )

    result_keys = result.keys()

    assert "SLC_coverage_percentage" in result_keys
    assert "OCN_coverage_percentage" in result_keys
    assert "EU_coverage_percentage" in result_keys


def test_s1_wv(s1_product_wv):
    geo_mask_utils = GeoMaskUtils()

    result = geo_mask_utils.coverage_over_specific_area_s1(
        s1_product_wv.satellite_unit,
        s1_product_wv.instrument_mode,
        s1_product_wv.footprint,
        s1_product_wv.sensing_start_date,
    )

    assert result == {"EU_coverage_percentage": 0.0}


@patch("logging.Logger.error")
def test_load_invalid_mask_name(logger_mock):
    geo_mask_utils = GeoMaskUtils()

    with pytest.raises(FileNotFoundError):
        geo_mask_utils.load_mask("YOLO")

    logger_mock.assert_called_once()

    assert "YOLO" not in GeoMaskUtils.CACHED_MASK


@patch("logging.Logger.warning")
def test_load_all_mask(logger_mock):
    geo_mask_utils = GeoMaskUtils()

    for masks_per_sat in GeoMaskUtils.OVER_SPECIFIC_AREA_GEOJSON.values():
        for instrument_mode in masks_per_sat.values():
            for mask_file in instrument_mode.values():
                geo_mask_utils.load_mask(mask_file)

    assert logger_mock.call_count == 0


class MyTestCase(unittest.TestCase):
    def test_load_invalid_mask_path(self):

        GeoMaskUtils.OVER_SPECIFIC_AREA_GEOJSON["WRONGPATH"] = {
            "0": "resources/masks/YOLO"
        }

        with self.assertRaises(FileNotFoundError):
            GeoMaskUtils().load_mask("WRONGPATH")


@patch("logging.Logger.error")
def test_load_invalid_mask_path(logger_mock):
    MyTestCase().test_load_invalid_mask_path()

    logger_mock.assert_called_once()

    assert "WRONGPATH" not in GeoMaskUtils.CACHED_MASK


@patch("logging.Logger.warning")
def test_mask_not_loaded_coverage(logger_mock, s1_product_wv):
    GeoMaskUtils().area_coverage("S1A", s1_product_wv.footprint, "MASKNOTLOAD")

    assert logger_mock.call_count == 2


@patch("logging.Logger.warning")
def test_invalid_footprint_coverage(logger_mock, s1_product_wv):
    GeoMaskUtils().area_coverage("S1A", s1_product_wv.footprint[0:-5], "SLC")

    logger_mock.assert_called_once()


def test_intersect_svalbard():
    footprint = "Polygon((15 79, 15 80, 16 80, 16 79, 15 79))"

    intersect = GeoMaskUtils().area_coverage(
        "S1A", footprint, "SLC", "2024-04-02T12:12:12.000Z"
    )

    assert intersect == 100


def test_intersect_format_geojson():
    footprint = {
        "type": "Polygon",
        "coordinates": [
            [
                [15, 79],
                [15, 80],
                [16, 80],
                [16, 79],
                [15, 79],
            ]
        ],
    }
    intersect = GeoMaskUtils().area_coverage("S1A", footprint, "SLC")

    assert intersect == 100


def test_intersect_specific_product():
    footprint = "POLYGON((128.563 -8.7541,129.2694 -8.6452,128.854 -6.8028,128.1508 -6.9098,128.563 -8.7541))"
    intersect = GeoMaskUtils().area_coverage("S1A", footprint, "SLC")
    assert intersect == 0
    intersect = GeoMaskUtils().area_coverage("S1A", footprint, "OCN")
    assert intersect == 100


def test_from_raw_product_footprint_geo(s1_raw_geopolygon):
    assert isinstance(s1_raw_geopolygon.footprint, AttrDict)
    intersect = GeoMaskUtils().area_coverage("S1A", s1_raw_geopolygon.footprint, "OCN")
    assert intersect == 100


def test_new_masks():
    footprint = {
        "type": "Polygon",
        "coordinates": [
            [
                [-68, -5.1],
                [-66, -5.1],
                [-66, -4.9],
                [-68, -4.9],
                [-68, -5.1],
            ]
        ],
    }

    intersect = GeoMaskUtils().area_coverage(
        "S1A", footprint, "SLC", "2024-04-02T12:12:12.000Z"
    )

    assert intersect == 100


def test_intersect_format_geojson_eu_mask():

    # 🥐🥖
    footprint = {
        "coordinates": [
            [
                [-2, 49],
                [-2, 44],
                [6, 44],
                [6, 49],
                [-2, 49],
            ]
        ],
        "type": "Polygon",
    }
    intersect = GeoMaskUtils().area_coverage("S1A", footprint, "EU")

    assert intersect == 100


def test_groenland_coverage():

    footprint = "Polygon((-39.9765 80.9498,-17.6093 82.9458,-21.0764 83.8781,-44.8408 81.6605,-39.9765 80.9498))"
    intersect = GeoMaskUtils().area_coverage("S1A", footprint, "OCN")

    assert 19.46 < intersect < 19.47


def test_date_masks_impact_bug():
    raw_data_product_dict = {
        "reportName": "https://s1a.prip.copernicus.eu",
        "product_id": "9e839192-d960-4c1b-97b5-515cb46b95d2",
        "product_name": "S1A_IW_RAW__0SDV_20240705T235557_20240705T235629_054632_06A68B_D824.SAFE.zip",
        "content_length": 1604002216,
        "publication_date": "2024-07-06T00:47:36.686Z",
        "start_date": "2024-07-05T23:55:57.545Z",
        "end_date": "2024-01-05T23:56:29.944Z",  # fake previous date
        "origin_date": "2024-07-06T00:37:12.000Z",
        "eviction_date": "2024-07-19T12:47:36.298Z",
        "footprint": {
            "type": "Polygon",
            "coordinates": [
                [
                    [-71.6787, -53.635],
                    [-68.1222, -52.8622],
                    [-69.3888, -51.0393],
                    [-72.8177, -51.7742],
                    [-71.6787, -53.635],
                ]
            ],
        },
        "interface_name": "PRIP_S1A_Serco",
        "production_service_type": "PRIP",
        "production_service_name": "S1A-Serco",
        "ingestionTime": "2024-07-06T01:10:52.044Z",
    }
    raw_document = model.PripProduct(**raw_data_product_dict)
    raw_document.meta.id = "39f5dc8ab626c24fbd12e138679bf2bf"
    raw_document.full_clean()

    # OLD mask 12.7% NEW mask 20.883%
    geo_mask_utils = GeoMaskUtils()

    # OLD
    result = geo_mask_utils.coverage_over_specific_area_s1(
        "S1A",
        "IW",
        raw_document.footprint,
        raw_document.end_date,  # fake previous date
    )

    assert result == {
        "OCN_coverage_percentage": 12.711695280606387,
        "EU_coverage_percentage": 0.0,
    }

    # NEW
    result = geo_mask_utils.coverage_over_specific_area_s1(
        "S1A",
        "IW",
        raw_data_product_dict.get("footprint"),
        raw_document.start_date,
    )

    assert result == {
        "OCN_coverage_percentage": 20.870232761754124,
        "EU_coverage_percentage": 0.0,
    }

    @pytest.mark.parametrize(
        "footprint",
        [
            {
                "type": "Polygon",
                "coordinates": [
                    [
                        [-69.0779, -3.75],
                        [-70.0068, -7.8509],
                        [-66.3711, -8.4129],
                        [-65.4711, -4.2899],
                        [-69.0779, -3.75],
                    ]
                ],
                "crs": {"type": "name", "properties": {"name": "EPSG:4326"}},
            },
            {
                "type": "Polygon",
                "coordinates": [
                    [
                        [-69.8947, -7.359],
                        [-70.7874, -11.1471],
                        [-67.1143, -11.7292],
                        [-66.2635, -7.9181],
                        [-69.8947, -7.359],
                    ]
                ],
                "crs": {"type": "name", "properties": {"name": "EPSG:4326"}},
            },
            {
                "type": "Polygon",
                "coordinates": [
                    [
                        [-69.0797, -3.7507],
                        [-70.0085, -7.8516],
                        [-66.3729, -8.4136],
                        [-65.4729, -4.2906],
                        [-69.0797, -3.7507],
                    ]
                ],
                "crs": {"type": "name", "properties": {"name": "EPSG:4326"}},
            },
            {
                "type": "Polygon",
                "coordinates": [
                    [
                        [-65.1065, -4.3914],
                        [-66.0417, -8.4912],
                        [-62.3995, -9.057],
                        [-61.4963, -4.9347],
                        [-65.1065, -4.3914],
                    ]
                ],
                "crs": {"type": "name", "properties": {"name": "EPSG:4326"}},
            },
            {
                "type": "Polygon",
                "coordinates": [
                    [
                        [-65.9271, -7.9987],
                        [-66.8266, -11.7855],
                        [-63.1444, -12.3719],
                        [-62.2898, -8.5616],
                        [-65.9271, -7.9987],
                    ]
                ],
                "crs": {"type": "name", "properties": {"name": "EPSG:4326"}},
            },
        ],
    )
    def test_strange_masks_s1(footprint):
        geo_mask_utils = GeoMaskUtils()
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
            "interface_name": "PRIP_S1C_Werum",
            "production_service_type": "PRIP",
            "production_service_name": "S1C-Werum",
            "ingestionTime": "2025-04-14T21:16:07.186Z",
            "footprint": footprint,
        }
        raw_document = model.PripProduct(**data_dict)
        raw_document.meta.id = "b759d82f721504ea0c0db5f7ddd73fe7"
        raw_document.full_clean()

        result_dict = geo_mask_utils.coverage_over_specific_area_s1(
            "S1C",
            "EW",
            raw_document.footprint,
            raw_document.start_date,
        )

        # only want to check runtime
        assert result_dict != {}
