"""Tests for the duplicated items detection and the original completeness pass"""

import datetime
from datetime import timedelta
from unittest.mock import patch

from maas_cds.model.datatake_s1 import CdsDatatakeS1
from maas_cds.model.product import CdsProduct

BASE = datetime.datetime(2024, 1, 1, tzinfo=datetime.timezone.utc)


def _product(
    name, start_offset, end_offset, deleted=False, interface="DD", issue="GSANOM-1"
):
    start = BASE + timedelta(seconds=start_offset)
    end = BASE + timedelta(seconds=end_offset)
    product = CdsProduct(
        name=name,
        sensing_start_date=start,
        sensing_end_date=end,
    )
    product.sensing_duration = int((end - start).total_seconds() * 1_000_000)
    if deleted:
        if interface == "DD":
            product.nb_dd_deleted = 1
            product.DD_DAS_is_deleted = True
            product.DD_DAS_deletion_issue = issue
        else:
            product.nb_lta_deleted = 1
            product.LTA_Werum_is_deleted = True
            product.LTA_Werum_deletion_issue = issue
    return product


@patch.object(CdsDatatakeS1, "get_expected_value", return_value=200_000_000)
@patch.object(CdsDatatakeS1, "product_type_with_missing_periods", return_value=False)
@patch.object(CdsDatatakeS1, "get_all_product_types", return_value=["IW_RAW__0S"])
@patch.object(CdsDatatakeS1, "get_global_key_field", return_value="sensing")
@patch.object(CdsDatatakeS1, "find_brother_products_scan")
def test_compute_completeness_duplicated_items_and_original(mock_scan, *_mocks):
    """A and B overlap by 50% (B is deleted from DD), C is alone.

    - both A and B end up in ``duplicateds.items``
    - the deleted product of the pair is traced per interface
    - the ``deletion`` aggregate names the ticket and the survivor
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

    # --- duplicated items (one entry per pair) ---
    items = list(datatake.duplicateds.items)
    assert len(items) == 1
    assert datatake.duplicateds.pairs_count == 1
    (item,) = items
    assert {item.name, item.paired_with} == {"A", "B"}
    assert item.duplicated_percentage == 50.0

    # deletion trace: B is the deleted member of the pair, from DD
    assert item.deleted_product["DD"] == "B"
    assert item.deleted_product["LTA"] is None

    # deletion aggregate: one row per service_type
    deletion = {row.service_type: row for row in datatake.duplicateds.deletions}
    assert deletion["DD"].ticket == "GSANOM-1"
    assert deletion["DD"].targeted_products_count == 1
    assert deletion["DD"].deleted_not_duplicated_products == []
    assert deletion["DD"].deleted_not_duplicated_products_count == 0
    # the single pair carries a DD deletion, so no DD pair survives
    assert deletion["DD"].surviving_pairs_count == 0
    assert deletion["DD"].expected_pairs_count == 1
    assert deletion["DD"].deletion_completenness_percentange == 100.0
    # nothing on LTA: the pair has no LTA deletion, so it survives on LTA
    assert deletion["LTA"].ticket is None
    assert deletion["LTA"].targeted_products_count == 0
    assert deletion["LTA"].surviving_pairs_count == 1
    assert deletion["LTA"].expected_pairs_count == 1
    assert deletion["LTA"].deletion_completenness_percentange == 0.0

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

    assert datatake.duplicateds.items == []
    assert datatake.duplicateds.pairs_count == 0
    # no deletion -> original and live match
    assert (
        datatake.original_completeness["IW_RAW__0S_local_value"]
        == datatake.IW_RAW__0S_local_value
    )


@patch.object(CdsDatatakeS1, "get_expected_value", return_value=500_000_000)
@patch.object(CdsDatatakeS1, "product_type_with_missing_periods", return_value=False)
@patch.object(CdsDatatakeS1, "get_all_product_types", return_value=["IW_RAW__0S"])
@patch.object(CdsDatatakeS1, "get_global_key_field", return_value="sensing")
@patch.object(CdsDatatakeS1, "find_brother_products_scan")
def test_compute_completeness_deletion_aggregate_not_duplicated(mock_scan, *_mocks):
    """The deletion aggregate reports products deleted but not duplicated.

    A-B are duplicated and B is deleted (DD, GSANOM-1).
    D is also deleted (DD, GSANOM-1) but is not part of any duplicated pair.
    """

    mock_scan.return_value = [
        _product("A", 0, 100),
        _product("B", 50, 150, deleted=True),
        _product("C", 200, 260),
        _product("D", 300, 360, deleted=True),
    ]

    datatake = CdsDatatakeS1(
        datatake_id="DT",
        satellite_unit="S1A",
        mission="S1",
        observation_time_start=BASE,
        observation_time_stop=BASE + timedelta(seconds=400),
    )

    datatake.compute_completeness()

    # one entry for the single A-B pair
    (item,) = list(datatake.duplicateds.items)
    assert {item.name, item.paired_with} == {"A", "B"}

    deletion = {row.service_type: row for row in datatake.duplicateds.deletions}
    assert deletion["DD"].ticket == "GSANOM-1"
    # B and D are both deleted from DD under the ticket.
    assert deletion["DD"].targeted_products_count == 2
    # only D is deleted without being part of a duplicated pair.
    assert deletion["DD"].deleted_not_duplicated_products == ["D"]
    assert deletion["DD"].deleted_not_duplicated_products_count == 1
    # the single pair carries a DD deletion, so no DD pair survives.
    assert deletion["DD"].surviving_pairs_count == 0
    assert deletion["DD"].expected_pairs_count == 1
    assert deletion["DD"].deletion_completenness_percentange == 100.0


@patch.object(CdsDatatakeS1, "get_expected_value", return_value=500_000_000)
@patch.object(CdsDatatakeS1, "product_type_with_missing_periods", return_value=False)
@patch.object(CdsDatatakeS1, "get_all_product_types", return_value=["IW_RAW__0S"])
@patch.object(CdsDatatakeS1, "get_global_key_field", return_value="sensing")
@patch.object(CdsDatatakeS1, "find_brother_products_scan")
def test_compute_completeness_deletion_aggregate_dd_and_lta(mock_scan, *_mocks):
    """DD and LTA deletions are reported independently.

    A-B duplicated, B deleted from DD (SOA-DD).
    C-D duplicated, D deleted from LTA (SOA-LTA).
    """

    mock_scan.return_value = [
        _product("A", 0, 100),
        _product("B", 50, 150, deleted=True, interface="DD", issue="SOA-DD"),
        _product("C", 200, 300),
        _product("D", 250, 350, deleted=True, interface="LTA", issue="SOA-LTA"),
    ]

    datatake = CdsDatatakeS1(
        datatake_id="DT",
        satellite_unit="S1A",
        mission="S1",
        observation_time_start=BASE,
        observation_time_stop=BASE + timedelta(seconds=400),
    )

    datatake.compute_completeness()

    # one entry per pair, keyed by the pair's first (earlier) product
    items_by_name = {item.name: item for item in datatake.duplicateds.items}
    assert set(items_by_name) == {"A", "C"}
    assert datatake.duplicateds.pairs_count == 2

    # per-item deleted product, per interface
    assert items_by_name["A"].deleted_product == {"DD": "B", "LTA": None}
    assert items_by_name["C"].deleted_product == {"DD": None, "LTA": "D"}

    deletion = {row.service_type: row for row in datatake.duplicateds.deletions}
    # DD: only the A-B pair carries a DD deletion -> 1 of 2 pairs survives on DD
    assert deletion["DD"].ticket == "SOA-DD"
    assert deletion["DD"].targeted_products_count == 1
    assert deletion["DD"].surviving_pairs_count == 1
    assert deletion["DD"].expected_pairs_count == 2
    assert deletion["DD"].deletion_completenness_percentange == 50.0
    # LTA: only the C-D pair carries an LTA deletion -> 1 of 2 pairs survives on LTA
    assert deletion["LTA"].ticket == "SOA-LTA"
    assert deletion["LTA"].targeted_products_count == 1
    assert deletion["LTA"].surviving_pairs_count == 1
    assert deletion["LTA"].expected_pairs_count == 2
    assert deletion["LTA"].deletion_completenness_percentange == 50.0
