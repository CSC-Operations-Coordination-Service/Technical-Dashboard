"""Tests for the duplicated items detection and the original completeness pass"""

import datetime
from datetime import timedelta
from unittest.mock import patch

from maas_cds.model.datatake_s1 import CdsDatatakeS1
from maas_cds.model.product import CdsProduct


BASE = datetime.datetime(2024, 1, 1, tzinfo=datetime.timezone.utc)


def _product(name, start_offset, end_offset, deleted=False):
    start = BASE + timedelta(seconds=start_offset)
    end = BASE + timedelta(seconds=end_offset)
    product = CdsProduct(
        name=name,
        sensing_start_date=start,
        sensing_end_date=end,
    )
    product.sensing_duration = int((end - start).total_seconds() * 1_000_000)
    if deleted:
        product.nb_dd_deleted = 1
        product.DD_CDSE_is_deleted = True
        product.DD_CDSE_deletion_issue = "GSANOM-1"
    return product


@patch.object(CdsDatatakeS1, "get_expected_value", return_value=200_000_000)
@patch.object(CdsDatatakeS1, "product_type_with_missing_periods", return_value=False)
@patch.object(CdsDatatakeS1, "get_all_product_types", return_value=["IW_RAW__0S"])
@patch.object(CdsDatatakeS1, "get_global_key_field", return_value="sensing")
@patch.object(CdsDatatakeS1, "find_brother_products_scan")
def test_compute_completeness_duplicated_items_and_original(
    mock_scan, *_mocks
):
    """A and B overlap by 50% (B is deleted), C is alone.

    - both A and B end up in ``duplicateds_items``
    - the deletion trace is carried on item B
    - ``original_completeness`` (all products) is bigger than the live value
      (which ignores the deleted product B)
    """

    products = [
        _product("A", 0, 100),
        _product("B", 50, 150, deleted=True),
        _product("C", 200, 300),
    ]
    mock_scan.return_value = products

    datatake = CdsDatatakeS1(
        datatake_id="DT",
        satellite_unit="S1A",
        mission="S1",
        observation_time_start=BASE,
        observation_time_stop=BASE + timedelta(seconds=300),
    )

    datatake.compute_completeness()

    # --- duplicated items ---
    items_by_name = {item.name: item for item in datatake.duplicateds_items}
    assert set(items_by_name) == {"A", "B"}
    assert items_by_name["A"].paired_with == "B"
    assert items_by_name["B"].paired_with == "A"
    assert items_by_name["A"].duplicated_percentage == 50.0

    # deletion trace
    assert items_by_name["A"].to_be_deleted is False
    assert items_by_name["B"].to_be_deleted is True
    assert items_by_name["B"].deletion_issue == "GSANOM-1"

    # --- original vs live completeness ---
    # live ignores deleted B : A(0-100) + C(200-300) = 200s
    assert datatake.IW_RAW__0S_local_value == 200_000_000
    # original keeps B : A(0-100) + B(extends to 150) + C(200-300) = 250s
    assert datatake.original_completeness["IW_RAW__0S_local_value"] == 250_000_000
    assert (
        datatake.original_completeness["IW_RAW__0S_local_value"]
        > datatake.IW_RAW__0S_local_value
    )


@patch.object(CdsDatatakeS1, "get_expected_value", return_value=200_000_000)
@patch.object(CdsDatatakeS1, "product_type_with_missing_periods", return_value=False)
@patch.object(CdsDatatakeS1, "get_all_product_types", return_value=["IW_RAW__0S"])
@patch.object(CdsDatatakeS1, "get_global_key_field", return_value="sensing")
@patch.object(CdsDatatakeS1, "find_brother_products_scan")
def test_compute_completeness_no_duplicate(mock_scan, *_mocks):
    """Two non-overlapping products produce no duplicated items."""

    mock_scan.return_value = [
        _product("A", 0, 100),
        _product("C", 200, 300),
    ]

    datatake = CdsDatatakeS1(
        datatake_id="DT",
        satellite_unit="S1A",
        mission="S1",
        observation_time_start=BASE,
        observation_time_stop=BASE + timedelta(seconds=300),
    )

    datatake.compute_completeness()

    assert datatake.duplicateds_items == []
    # no deletion -> original and live match
    assert (
        datatake.original_completeness["IW_RAW__0S_local_value"]
        == datatake.IW_RAW__0S_local_value
    )
