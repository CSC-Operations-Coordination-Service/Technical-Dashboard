"""Tests for the duplicated items detection and the original completeness pass"""

import datetime
from collections import Counter
from datetime import timedelta
from types import SimpleNamespace
from unittest.mock import patch

from maas_cds.lib.config_manager import MaasConfigManager
from maas_cds.model.datatake_s1 import CdsDatatakeS1
from maas_cds.model.datatake_s2 import CdsDatatakeS2
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


@patch.object(
    CdsDatatakeS1,
    "_dataflow_expected_interfaces",
    return_value={"IW_RAW__0S": {"DD", "LTA"}, "IW_SLC__1S": {"LTA"}},
)
@patch.object(CdsDatatakeS1, "get_expected_value", return_value=200_000_000)
@patch.object(CdsDatatakeS1, "product_type_with_missing_periods", return_value=False)
@patch.object(
    CdsDatatakeS1,
    "get_all_product_types",
    return_value=["IW_RAW__0S", "IW_SLC__1S"],
)
@patch.object(CdsDatatakeS1, "get_global_key_field", return_value="sensing")
@patch.object(CdsDatatakeS1, "find_brother_products_scan")
def test_compute_completeness_expected_pairs_filtered_by_dataflow(
    mock_scan, *_mocks
):
    """Expected pairs to be removed are filtered per interface using the dataflow.

    Two duplicated pairs of different product types:
    - IW_RAW__0S: A-B overlap, B deleted from DD (RAW is expected on DD + LTA)
    - IW_SLC__1S: E-F overlap, F deleted from LTA (SLC is expected on LTA only)

    On DD only the RAW pair is expected (SLC is LTA-only), so DD expects 1 pair
    (deleted -> 100%). On LTA both pairs are expected, only the SLC one is deleted
    -> 1 of 2 survives (50%).
    """

    products_by_type = {
        "IW_RAW__0S": [
            _product("A", 0, 100),
            _product("B", 50, 150, deleted=True, interface="DD", issue="SOA-DD"),
        ],
        "IW_SLC__1S": [
            _product("E", 0, 100),
            _product("F", 50, 150, deleted=True, interface="LTA", issue="SOA-LTA"),
        ],
    }

    def _scan(product_type, indices=None, include_deleted=False):
        return products_by_type.get(product_type, [])

    mock_scan.side_effect = _scan

    datatake = CdsDatatakeS1(
        datatake_id="DT",
        satellite_unit="S1A",
        mission="S1",
        observation_time_start=BASE,
        observation_time_stop=BASE + timedelta(seconds=300),
    )

    datatake.compute_completeness()

    # both pairs are still detected and listed
    assert datatake.duplicateds.pairs_count == 2

    deletion = {row.service_type: row for row in datatake.duplicateds.deletions}

    # DD: SLC is LTA-only, so only the RAW pair is expected on DD and it is deleted
    assert deletion["DD"].expected_pairs_count == 1
    assert deletion["DD"].surviving_pairs_count == 0
    assert deletion["DD"].deletion_completenness_percentange == 100.0

    # LTA: both pairs expected; only the SLC pair carries an LTA deletion
    assert deletion["LTA"].expected_pairs_count == 2
    assert deletion["LTA"].surviving_pairs_count == 1
    assert deletion["LTA"].deletion_completenness_percentange == 50.0


def _dataflow_record(mission, satellites, product_type, services_config):
    return SimpleNamespace(
        mission=mission,
        satellites=satellites,
        product_type=product_type,
        services_config=services_config,
    )


@patch.object(MaasConfigManager, "get_config")
def test_dataflow_expected_interfaces_maps_product_type_to_interfaces(mock_get_config):
    """The dataflow config is parsed into product_type -> {DD, LTA}.

    - a real service (item starting with C or P) marks the interface as expected
    - records of another mission / satellite are ignored
    - a product type with no real DD/LTA service maps to an empty set (never
      counted as an expected pair on either interface)
    """

    mock_get_config.return_value = {
        "records": [
            # RAW: distributed on both DD and LTA
            _dataflow_record(
                "S1", ["S1A", "S1B"], "IW_RAW__0S",
                {"DD": ["C-PRIP", "P"], "LTA": ["C-PRIP", "P"]},
            ),
            # SLC: LTA only (DD holds no real service)
            _dataflow_record(
                "S1", ["S1A"], "IW_SLC__1S",
                {"DD": ["N"], "LTA": ["C-PRIP", "P"]},
            ),
            # OCN annotation: no real DD/LTA service at all
            _dataflow_record("S1", ["S1A"], "IW_OCN__2A", {"DA": ["P"]}),
            # different satellite -> ignored
            _dataflow_record("S1", ["S1B"], "IW_GRDH_1S", {"LTA": ["P"]}),
            # different mission -> ignored
            _dataflow_record("S2", ["S2A"], "MSI_L0__DS", {"LTA": ["P"]}),
        ]
    }

    datatake = CdsDatatakeS1(
        datatake_id="DT",
        satellite_unit="S1A",
        mission="S1",
    )

    assert datatake._dataflow_expected_interfaces() == {
        "IW_RAW__0S": {"DD", "LTA"},
        "IW_SLC__1S": {"LTA"},
        "IW_OCN__2A": set(),
    }


@patch.object(MaasConfigManager, "get_config", return_value=None)
def test_dataflow_expected_interfaces_empty_when_config_not_loaded(_mock_get_config):
    """When the dataflow config is not loaded the map is empty (raw-count fallback)."""

    datatake = CdsDatatakeS2(
        datatake_id="DT",
        satellite_unit="S2A",
        mission="S2",
    )

    assert datatake._dataflow_expected_interfaces() == {}


def _s2_product(
    name,
    product_type,
    datastrip_id=None,
    product_group_id=None,
    start_offset=0,
    end_offset=0,
    deleted=False,
    interface="DD",
    issue="OMCS-1",
):
    product = CdsProduct(
        name=name,
        product_type=product_type,
        sensing_start_date=BASE + timedelta(seconds=start_offset),
        sensing_end_date=BASE + timedelta(seconds=end_offset),
    )
    product.datastrip_id = datastrip_id
    product.product_group_id = product_group_id
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


@patch.object(CdsDatatakeS2, "get_product_partitionning", return_value=None)
@patch.object(CdsDatatakeS2, "find_brother_products_scan")
def test_compute_duplicated_datastrips(mock_scan, _mock_part):
    """Two overlapping L0 datastrips (reprocessing baselines) are reported.

    Mirrors the real data: the L0 DS have no ``datastrip_id`` (the product name is
    the identity), the granules / tiles reference their OWN-level DS name, and the
    higher-level DS are resolved by sensing inclusion in the L0 DS.

    - L0 DS A(0-100) and B(50-150) overlap by 50% -> one datastrip pair
    - datastrip A: 4 L0 granules (direct) + 6 L1C tiles (via its L1C DS)
    - datastrip B: 2 L0 granules + 4 L1C tiles, its L0 DS deleted from LTA
    """

    ds_products = [
        # L0 DS carry no datastrip_id (as in prod); the .tar name is the identity.
        _s2_product("L0DS_A.tar", "MSI_L0__DS", start_offset=0, end_offset=100),
        _s2_product(
            "L0DS_B.tar", "MSI_L0__DS", start_offset=50, end_offset=150,
            deleted=True, interface="LTA", issue="OMCS-42",
        ),
    ]
    # Higher-level DS, sensing included in their L0 DS.
    level_ds = {
        "MSI_L1C_DS": [
            _s2_product("L1CDS_A.tar", "MSI_L1C_DS", start_offset=5, end_offset=95),
            _s2_product("L1CDS_B.tar", "MSI_L1C_DS", start_offset=55, end_offset=145),
        ],
    }
    # Granules / tiles reference their own-level DS name (without .tar).
    attached = {
        "MSI_L0__GR": (
            [_s2_product(f"A_GR_{i}", "MSI_L0__GR", datastrip_id="L0DS_A") for i in range(4)]
            + [_s2_product(f"B_GR_{i}", "MSI_L0__GR", datastrip_id="L0DS_B") for i in range(2)]
        ),
        "MSI_L1C_TL": (
            [_s2_product(f"A_TL_{i}", "MSI_L1C_TL", datastrip_id="L1CDS_A") for i in range(6)]
            + [_s2_product(f"B_TL_{i}", "MSI_L1C_TL", datastrip_id="L1CDS_B") for i in range(4)]
        ),
    }

    def _scan(product_type, indices=None, include_deleted=False):
        if product_type == CdsDatatakeS2.DUPLICATED_DATASTRIP_REFERENCE_TYPE:
            return ds_products
        if product_type in level_ds:
            return level_ds[product_type]
        return attached.get(product_type, [])

    mock_scan.side_effect = _scan

    datatake = CdsDatatakeS2(
        datatake_id="DT",
        satellite_unit="S2A",
        mission="S2",
        observation_time_start=BASE,
        observation_time_stop=BASE + timedelta(seconds=300),
    )
    datatake._init_duplicateds_buffers()
    datatake._include_deleted_products = True

    datatake.compute_duplicated_datastrips()

    (pair,) = datatake._dup_datastrip_pairs
    assert pair.overlap_percentage == 50.0

    strip_a, strip_b = pair.datastrips

    # identity is the L0 DS name without the archive extension
    assert strip_a.datastrip_id == "L0DS_A"
    # datastrip A: 4 L0 granules (direct) + 6 L1C tiles (via L1C DS sensing match)
    assert Counter(p.product_type for p in strip_a.products) == {
        "MSI_L0__GR": 4,
        "MSI_L1C_TL": 6,
    }
    assert list(strip_a.deletions) == []

    # datastrip B: 2 L0 granules + 4 L1C tiles
    assert strip_b.datastrip_id == "L0DS_B"
    assert Counter(p.product_type for p in strip_b.products) == {
        "MSI_L0__GR": 2,
        "MSI_L1C_TL": 4,
    }


@patch.object(
    CdsDatatakeS2,
    "_dataflow_expected_interfaces",
    return_value={"MSI_L0__GR": {"DD", "LTA"}, "MSI_L1B_GR": {"DD"}},
)
@patch.object(CdsDatatakeS2, "get_product_partitionning", return_value=None)
@patch.object(CdsDatatakeS2, "find_brother_products_scan")
def test_compute_duplicated_datastrips_deletion_expected_per_interface(
    mock_scan, _mock_part, _mock_dataflow
):
    """deleted_products_expected is filtered per interface using the dataflow.

    Datastrip B has 2 L0 granules (expected on DD + LTA) and 4 L1B granules
    (expected on DD only); one L0 granule is deleted from LTA. The LTA deletion
    share is therefore 1 / 2 (only L0 granules are LTA-expected), not 1 / 6.
    """

    ds_products = [
        _s2_product("L0DS_A.tar", "MSI_L0__DS", start_offset=0, end_offset=100),
        _s2_product("L0DS_B.tar", "MSI_L0__DS", start_offset=50, end_offset=150),
    ]
    # L1B DS with distinct sensing so each nests in a single L0 DS.
    level_ds = {
        "MSI_L1B_DS": [
            _s2_product("L1BDS_A.tar", "MSI_L1B_DS", start_offset=5, end_offset=95),
            _s2_product("L1BDS_B.tar", "MSI_L1B_DS", start_offset=55, end_offset=145),
        ],
    }
    attached = {
        "MSI_L0__GR": (
            [_s2_product(f"A_L0GR_{i}", "MSI_L0__GR", datastrip_id="L0DS_A") for i in range(2)]
            + [_s2_product("B_L0GR_0", "MSI_L0__GR", datastrip_id="L0DS_B")]
            + [
                _s2_product(
                    "B_L0GR_del", "MSI_L0__GR", datastrip_id="L0DS_B",
                    deleted=True, interface="LTA", issue="OMCS-42",
                )
            ]
        ),
        "MSI_L1B_GR": [
            _s2_product(f"B_L1BGR_{i}", "MSI_L1B_GR", datastrip_id="L1BDS_B")
            for i in range(4)
        ],
    }

    def _scan(product_type, indices=None, include_deleted=False):
        if product_type == CdsDatatakeS2.DUPLICATED_DATASTRIP_REFERENCE_TYPE:
            return ds_products
        if product_type in level_ds:
            return level_ds[product_type]
        return attached.get(product_type, [])

    mock_scan.side_effect = _scan

    datatake = CdsDatatakeS2(
        datatake_id="DT",
        satellite_unit="S2A",
        mission="S2",
        observation_time_start=BASE,
        observation_time_stop=BASE + timedelta(seconds=300),
    )
    datatake._init_duplicateds_buffers()
    datatake._include_deleted_products = True

    datatake.compute_duplicated_datastrips()

    (pair,) = datatake._dup_datastrip_pairs
    strip_b = next(s for s in pair.datastrips if s.datastrip_id == "L0DS_B")

    # 2 L0 granules + 4 L1B granules attached to B
    assert Counter(p.product_type for p in strip_b.products) == {
        "MSI_L0__GR": 2,
        "MSI_L1B_GR": 4,
    }

    # the deleted granule carries a per-product deletions entry; others are empty
    products_b = {p.product_name: p for p in strip_b.products}
    assert [
        (row.service_type, row.ticket) for row in products_b["B_L0GR_del"].deletions
    ] == [("LTA", "OMCS-42")]
    assert list(products_b["B_L0GR_0"].deletions) == []

    deletions_b = {row.service_type: row for row in strip_b.deletions}
    assert set(deletions_b) == {"LTA"}
    # LTA-expected products are only the 2 L0 granules -> share is 1/2, not 1/6
    assert deletions_b["LTA"].deleted_products_count == 1
    assert deletions_b["LTA"].deleted_products_expected == 2
    assert deletions_b["LTA"].deleted_product_percentage == 50.0


@patch.object(CdsDatatakeS2, "get_product_partitionning", return_value=None)
@patch.object(CdsDatatakeS2, "find_brother_products_scan")
def test_compute_duplicated_datastrips_below_minimal_duration(mock_scan, _mock_part):
    """L0 datastrips overlapping >=30% but <15s are not a datastrip pair.

    A(0-20) and B(10-30) overlap for 10s (50% of A) : above the 30% threshold
    but below the 15s minimal overlap duration, so no pair is reported.
    """

    ds_products = [
        _s2_product("L0DS_A.tar", "MSI_L0__DS", start_offset=0, end_offset=20),
        _s2_product("L0DS_B.tar", "MSI_L0__DS", start_offset=10, end_offset=30),
    ]

    mock_scan.side_effect = lambda product_type, indices=None, include_deleted=False: (
        ds_products
        if product_type == CdsDatatakeS2.DUPLICATED_DATASTRIP_REFERENCE_TYPE
        else []
    )

    datatake = CdsDatatakeS2(
        datatake_id="DT",
        satellite_unit="S2A",
        mission="S2",
        observation_time_start=BASE,
        observation_time_stop=BASE + timedelta(seconds=300),
    )
    datatake._init_duplicateds_buffers()
    datatake._include_deleted_products = True

    datatake.compute_duplicated_datastrips()

    assert datatake._dup_datastrip_pairs == []


@patch.object(CdsDatatakeS2, "get_product_partitionning", return_value=None)
@patch.object(CdsDatatakeS2, "find_brother_products_scan")
def test_compute_duplicated_datastrips_no_overlap(mock_scan, _mock_part):
    """Non-overlapping L0 datastrips produce no datastrip pair."""

    ds_products = [
        _s2_product("L0DS_A.tar", "MSI_L0__DS", start_offset=0, end_offset=100),
        _s2_product("L0DS_C.tar", "MSI_L0__DS", start_offset=200, end_offset=300),
    ]

    mock_scan.side_effect = lambda product_type, indices=None, include_deleted=False: (
        ds_products
        if product_type == CdsDatatakeS2.DUPLICATED_DATASTRIP_REFERENCE_TYPE
        else []
    )

    datatake = CdsDatatakeS2(
        datatake_id="DT",
        satellite_unit="S2A",
        mission="S2",
        observation_time_start=BASE,
        observation_time_stop=BASE + timedelta(seconds=300),
    )
    datatake._init_duplicateds_buffers()
    datatake._include_deleted_products = True

    datatake.compute_duplicated_datastrips()

    assert datatake._dup_datastrip_pairs == []
