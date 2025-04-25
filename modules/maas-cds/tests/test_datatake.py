import pytest
from maas_cds.model import CdsDatatake


@pytest.mark.parametrize(
    "observation_time_start, observation_time_stop, day_proximity, expected",
    [
        (
            "2023-01-01T00:00:00.000Z",
            "2023-01-15T00:00:00.000Z",
            15,
            ["cds-product-2022-12", "cds-product-2023-01"],
        ),
        (
            "2023-01-01T00:00:00.000Z",
            "2023-01-15T00:00:00.000Z",
            0,
            ["cds-product-2023-01"],
        ),
        (
            "2023-01-15T00:00:00.000Z",
            "2023-02-15T00:00:00.000Z",
            10,
            ["cds-product-2023-01", "cds-product-2023-02"],
        ),
        (
            "2023-01-01T00:00:00.000Z",
            "2023-03-02T00:00:00.000Z",
            30,
            [
                "cds-product-2022-12",
                "cds-product-2023-01",
                "cds-product-2023-02",
                "cds-product-2023-03",
                "cds-product-2023-04",
            ],
        ),
        (
            None,
            "2023-03-01T00:00:00.000Z",
            15,
            [],
        ),
        (
            "2023-01-01T00:00:00.000Z",
            None,
            15,
            [],
        ),
    ],
)
def test_get_product_partitionning(
    observation_time_start, observation_time_stop, day_proximity, expected
):
    datatake = CdsDatatake()
    datatake.observation_time_start = observation_time_start
    datatake.observation_time_stop = observation_time_stop
    datatake.full_clean()

    result = datatake.get_product_partitionning(day_proximity)

    assert result == expected
