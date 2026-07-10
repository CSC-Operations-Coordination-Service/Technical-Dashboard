"""Custom CDS model definition"""

from collections import Counter
from datetime import datetime
import logging
from typing import List

from maas_cds.lib.config import get_good_threshold_config_from_value
from maas_cds.lib.config_manager import MaasConfigManager
from maas_cds.lib.partitionning import get_partionning
from maas_model.date_utils import datetime_to_zulu
from opensearchpy import Keyword, Q
from maas_cds.lib import tolerance
from maas_cds.lib.dateutils import get_microseconds_delta
from maas_cds.lib.status import evaluate_completeness_status
from maas_cds.lib.periodutils import (
    Period,
    DuplicationCandidate,
    compute_duplicated_indicator,
    compute_duplicated_items,
    compute_missing_sensing_periods,
)
from maas_cds.model import generated
from maas_cds.model.anomaly_mixin import AnomalyMixin
from maas_cds.model.enumeration import CompletenessScope, CompletenessStatus
from maas_cds.model.product import CdsProduct
from datetime import timedelta

__all__ = ["CdsDatatake"]


LOGGER = logging.getLogger("CdsModelDatatake")


class CdsDatatake(AnomalyMixin, generated.CdsDatatake):
    """CdsDatatake custom"""

    COVERING_AREA_FIELD = "_coverage_percentage"

    COMPLETENESS_TOLERANCE = {}

    STATIC_COMPLETENESS_VALUE = {}

    MISSING_PERIODS_MAXIMAL_OFFSET = None

    # Duplication detection: minimal overlap percentage between two consecutive
    # products to consider them as duplicated of each other.
    DUPLICATED_ITEMS_PERCENTAGE_THRESHOLD = 30.0

    # Duplication detection: minimal overlap duration (in seconds) between two
    # consecutive products to consider them as duplicated. 0 disables the
    # constraint (only the percentage threshold applies); subclasses can raise it
    # (e.g. S2 also requires at least 15s of overlap).
    DUPLICATED_ITEMS_MINIMAL_DURATION = 0.0

    # Transient compute flags (never persisted on the document).

    # When True, the current completeness pass keeps the products already flagged
    # as deleted (the "original" / with-all-products pass). When False (the live
    # pass) the deleted products are filtered out in memory.
    _include_deleted_products = False

    # When set to a dict, the completeness setters write into it instead of on the
    # document attributes (used to capture the "original completeness" without
    # clobbering the live values). When None, setters write on the document.
    _completeness_sink = None

    # Per-datatake cache of the brother products materialized once per
    # (product_type, indices, include_deleted) so the two completeness passes
    # share a single query instead of hitting the database twice.
    _brother_products_cache = None

    # Buffers feeding ``finalize_duplicateds`` (declared as class attributes so the
    # DSL keeps them as plain Python objects instead of wrapping them in AttrDict).
    _dup_items = None
    _dup_pair_count = 0
    _dup_paired_names = None
    _dup_deleted = None
    _dup_pairs = None
    _dup_datastrip_pairs = None

    cams_tickets = Keyword(multi=True)

    datastrip_ids = Keyword(multi=True)

    product_group_ids = Keyword(multi=True)

    def get_product_partitionning(self, day_precision=10) -> List[str]:
        """Utils function to get the partitionning of the product
        This function is used to get the partitionning of the product

        Args:
            day_precision (int, optional): Add some tolerance for the location. Defaults to 10.

        Returns:
            List[str]: Return the list of the indices where product are located
        """

        if not self.observation_time_start or not self.observation_time_stop:
            LOGGER.warning("Observation time start or stop is not set.")
            return []

        date_set = get_partionning(
            self.observation_time_start, self.observation_time_stop, day_precision
        )

        return [
            f"{CdsProduct.Index.name}-{date_part}" for date_part in sorted(date_set)
        ]

    def get_service_for_completeness(self):

        # TODO Move this to a more global configuration and in a external stuff (ie db)
        # Before 2022-04 the service id wasn't set maybe update all data with SX-legacy ?
        completeness_service_dict = {
            "S1A": {
                "0": ["S1-legacy"],
                "2022-04-06T00:00:00.000Z": ["PRIP_S1A_Serco"],
            },
            "S1B": {
                "0": ["S1-legacy"],
                "2022-04-01T00:00:00.000Z": ["PRIP_S1B_DLR"],
            },
            "S1C": {
                "0": ["PRIP_S1C_Serco", "PRIP_S1C_Werum"],
                "2025-02-17T11:00:00.000Z": ["PRIP_S1C_Werum"],
            },
            "S1D": {
                "0": ["PRIP_S1D_Serco"],
            },
            "S2A": {
                "0": ["S2-legacy"],
                "2022-04-01T00:00:00.000Z": ["PRIP_S2A_ATOS"],
                "2025-01-28T00:00:00.000Z": ["PRIP_S2C_ATOS_datatest"],
            },
            "S2B": {
                "0": ["S2-legacy"],
                "2022-04-01T00:00:00.000Z": ["PRIP_S2B_CAPGEMINI"],
            },
            "S2C": {
                "0": ["PRIP_S2C_ATOS_datatest"],
            },
            # "S3A": {
            #     "0": ["PRIP_S3_Legacy"],
            #     "2022-04-01T00:00:00.000Z": ["PRIP_S3A_ACRI"],  # Approx
            # },
            # "S3B": {
            #     "0": ["PRIP_S3_Legacy"],
            #     "2022-04-01T00:00:00.000Z": ["PRIP_S3B_SERCO"],  # Approx
            #     "2025-02-01T00:00:00.000Z": ["PRIP_S3B_TPZ"],
            # },
            # "S5P": {"0": ["PRIP_SSP_DLR"]},
        }

        config_completeness = completeness_service_dict.get(self.satellite_unit, None)

        if config_completeness is None:
            LOGGER.warning(
                "[CompletenessConfig] - Unknow satellite : %s", self.satellite_unit
            )
            return None

        # Maybe use
        nearest_time_indicator, allowed_prip_name = (
            get_good_threshold_config_from_value(
                config_completeness, datetime_to_zulu(self.observation_time_start)
            )
        )

        return allowed_prip_name

    def compute_local_value(self, product_type, related_documents=None):
        """Compute value for a specific product_type"""

        # TODO this can be refacto here
        # flow are the same :  get brother, use a compute method and add value in the doc

        raise NotImplementedError(
            f"Must be implement in subclasses in CdsDatatake{self.mission}"
        )

    def evaluate_local_expected(self, key_field):
        """Evaluate local expected for a product_type"""

        raise NotImplementedError(
            f"Must be implement in subclasses in CdsDatatake{self.mission}",
        )

    def evaluate_all_global_expected(
        self,
    ):
        """Evaluate all global expected"""

        raise NotImplementedError(
            f"Must be implement in subclasses in CdsDatatake{self.mission}"
        )

    def get_all_product_types(self):
        """Return the list of all product_type that need to be compute for this mission

        Raises:
            NotImplementedError: This method is mission's speficic
        """
        raise NotImplementedError(
            f"Must be implement in subclasses in CdsDatatake{self.mission}"
        )

    def product_type_with_missing_periods(self, product_type: str) -> bool:
        """Do we want missing periods for this product type ?"""
        raise NotImplementedError(
            f"Must be implement in subclasses in CdsDatatake{self.mission}"
        )

    def product_type_with_duplicated(self, product_type: str) -> bool:
        """Do we want check duplicated for this product type ?"""
        raise NotImplementedError(
            f"Must be implement in subclasses in CdsDatatake{self.mission}"
        )

    def compute_all_local_completeness(self):
        """Complete all local completeness for this datatake"""
        all_product_type = self.get_all_product_types()

        for product_type in all_product_type:
            related_products = []
            product_type_value = self.compute_local_value(
                product_type, related_products
            )

            self.set_completeness(
                CompletenessScope.LOCAL,
                product_type,
                product_type_value,
            )

            self.compute_missing_production(product_type, related_products)
            self.compute_duplicated(product_type, related_products)

    def compute_missing_production(
        self, product_type: str, related_products: List[Period]
    ):
        """Find and store missing sensing periods on this datatake

        Args:
            product_type (str): The current product type
            related_products (List[Period]): The list of products for
                this datatake/product-type
        """

        # ``missing_periods`` is a mapped field reflecting the live products: only
        # compute it during the live pass, not during the "original" (with all
        # products) pass which only captures completeness values.
        if self._completeness_sink is not None:
            return

        if (
            self.product_type_with_missing_periods(product_type)
            and self.MISSING_PERIODS_MAXIMAL_OFFSET is not None
        ):
            tolerance_value = tolerance.get_completeness_tolerance(
                self.COMPLETENESS_TOLERANCE,
                self.mission,
                CompletenessScope.LOCAL,
                product_type,
            )

            # product_type have some value added to have a better coherence we substract it
            tolerance_value -= tolerance.get_tolerance_from_scope(
                self.STATIC_COMPLETENESS_VALUE, product_type
            )

            missing_periods_maximal_offset = tolerance.get_completeness_tolerance(
                self.MISSING_PERIODS_MAXIMAL_OFFSET,
                self.mission,
                CompletenessScope.LOCAL,
                product_type,
            )

            missing_periods = compute_missing_sensing_periods(
                Period(
                    self.observation_time_start,
                    self.observation_time_stop,
                ),
                related_products,
                missing_periods_maximal_offset,
                tolerance_value,
            )

            LOGGER.debug(
                "[%s] - Missing periods : %r", self.datatake_id, missing_periods
            )

            self.missing_periods = [
                generated.CdsDatatakeMissingPeriods(
                    name="Missing Product",
                    product_type=product_type,
                    sensing_start_date=missing_period.start,
                    sensing_end_date=missing_period.end,
                    duration=int(
                        get_microseconds_delta(missing_period.start, missing_period.end)
                    ),
                )
                for missing_period in missing_periods
            ]

    def compute_duplicated(self, product_type: str, related_products: List[Period]):
        """Find and store duplicated indicator on this datatake

        Args:
            product_type (str): The current product type
            related_products (List[Period]): The list of products for
                this datatake/product-type
        """

        if self.product_type_with_duplicated(product_type):

            # Here depend of the product type adjust the method
            indicator = compute_duplicated_indicator(related_products)
            for key_indicator, value in indicator.items():
                self.store_completeness_value(
                    f"{product_type}_duplicated_{key_indicator}", value
                )

            # Detailed duplicated items (both members of each duplicated pair) are
            # only collected during the include-deleted pass so that a pair stays
            # visible even after one of its products has been deleted.
            if (
                self._include_deleted_products
                and self.product_type_with_duplicated_items(product_type)
            ):
                candidates = [
                    product
                    for product in related_products
                    if isinstance(product, DuplicationCandidate)
                ]
                self.add_duplicated_items(product_type, candidates)

    def product_type_with_duplicated_items(self, product_type: str) -> bool:
        """Whether this product type contributes detailed pairs to ``duplicateds.items``.

        Defaults to the same rule as the duplicated indicator; subclasses can
        narrow it (e.g. S2 lists only L0 DS in ``items``).
        """
        return self.product_type_with_duplicated(product_type)

    @staticmethod
    def _duplicated_product_info(product, to_be_deleted, deletion_issue):
        """Build the per-product dict consumed by ``append_duplicated_pair``.

        Carries the product identity, sensing period and both the global and the
        per-interface (DD / LTA) deletion trace.
        """
        by_interface = product.deletion_trace_by_interface()
        dd_deleted, dd_issue = by_interface["DD"]
        lta_deleted, lta_issue = by_interface["LTA"]
        return {
            "name": product.name,
            "sensing_start_date": product.sensing_start_date,
            "sensing_end_date": product.sensing_end_date,
            "to_be_deleted": to_be_deleted,
            "deletion_issue": deletion_issue,
            "dd_deleted": dd_deleted,
            "dd_issue": dd_issue,
            "lta_deleted": lta_deleted,
            "lta_issue": lta_issue,
        }

    def _init_duplicateds_buffers(self):
        """(Re)set the datatake-level buffers feeding ``finalize_duplicateds``."""
        self._dup_items = []
        self._dup_pair_count = 0
        self._dup_paired_names = set()
        # name -> deletion issue, per interface, for every deleted product seen
        self._dup_deleted = {"DD": {}, "LTA": {}}
        # one record per duplicated pair: its product type and, per interface,
        # whether the pair carries a product deleted from it. Feeds the
        # per-interface expected / surviving pair counts in finalize_duplicateds.
        self._dup_pairs = []
        # datastrip-centric duplicated pairs (S2 only, see
        # CdsDatatakeS2.compute_duplicated_datastrips)
        self._dup_datastrip_pairs = []

    def _record_deleted_product(
        self, name, dd_deleted, dd_issue, lta_deleted, lta_issue
    ):
        """Remember a deleted product and its ticket, per interface."""
        if dd_deleted:
            self._dup_deleted["DD"][name] = dd_issue
        if lta_deleted:
            self._dup_deleted["LTA"][name] = lta_issue

    def _register_pair_item(self, item):
        """Buffer a single duplicated pair (one entry per pair).

        ``item`` is a dict with keys ``product_type``, ``name``, ``paired_with``,
        ``deleted_product`` and the sensing period. Both members are recorded as
        paired, and the pair is buffered with its product type and per-interface
        deletion flags (consumed by ``finalize_duplicateds``).
        """
        self._dup_paired_names.add(item["name"])
        self._dup_paired_names.add(item["paired_with"])

        deleted_product = item["deleted_product"]
        self._dup_pairs.append(
            {
                "product_type": item["product_type"],
                "deleted": {
                    interface: bool(deleted_product.get(interface))
                    for interface in ("DD", "LTA")
                },
            }
        )

        self._dup_items.append(generated.CdsDatatakeDuplicatedsItems(**item))
        self._dup_pair_count += 1

    def append_duplicated_pair(self, product_type, first, second, percentage=100.0):
        """Register a duplicated pair as a single item.

        Used by detections that do not rely on the time-overlap percentage (e.g. S2
        granules or tiles), where two products are considered full duplicates.

        Args:
            product_type (str): the current product type
            first (dict): first product, keys ``name``, ``sensing_start_date``,
                ``sensing_end_date`` and the per-interface deletion trace
                (``dd_deleted`` / ``dd_issue`` / ``lta_deleted`` / ``lta_issue``)
            second (dict): the other product of the pair (same keys)
            percentage (float): duplicated percentage to store on the item
        """
        deleted_product = {"DD": None, "LTA": None}
        for info in (first, second):
            if info.get("dd_deleted"):
                deleted_product["DD"] = info["name"]
            if info.get("lta_deleted"):
                deleted_product["LTA"] = info["name"]
            self._record_deleted_product(
                info["name"],
                info.get("dd_deleted"),
                info.get("dd_issue"),
                info.get("lta_deleted"),
                info.get("lta_issue"),
            )

        self._register_pair_item(
            {
                "product_type": product_type,
                "name": first["name"],
                "sensing_start_date": first.get("sensing_start_date"),
                "sensing_end_date": first.get("sensing_end_date"),
                "duplicated_percentage": float(percentage),
                "paired_with": second["name"],
                "deleted_product": deleted_product,
            }
        )

    def add_duplicated_items(
        self, product_type: str, candidates: List[DuplicationCandidate]
    ):
        """Register duplicated products of a product type.

        Two consecutive products overlapping by at least
        ``DUPLICATED_ITEMS_PERCENTAGE_THRESHOLD`` percent and at least
        ``DUPLICATED_ITEMS_MINIMAL_DURATION`` seconds are considered as
        duplicated of each other; the pair is added once to the buffer.

        Args:
            product_type (str): the current product type
            candidates (List[DuplicationCandidate]): products carrying their
                identity and deletion trace, sorted by sensing start date
        """

        items = compute_duplicated_items(
            candidates,
            self.DUPLICATED_ITEMS_PERCENTAGE_THRESHOLD,
            self.DUPLICATED_ITEMS_MINIMAL_DURATION,
        )

        # ``compute_duplicated_items`` returns one entry per detected pair.
        for item in items:
            self._register_pair_item({"product_type": product_type, **item})

        # Record every deleted product of the type (including those not part of a
        # pair) so ``finalize_duplicateds`` can report deleted-not-duplicated.
        for candidate in candidates:
            self._record_deleted_product(
                candidate.name,
                candidate.dd_deleted,
                candidate.dd_issue,
                candidate.lta_deleted,
                candidate.lta_issue,
            )

    def _dataflow_expected_interfaces(self):
        """Map each product type to the interfaces (DD / LTA) the dataflow expects.

        Reads the ``MaasConfigDataflow`` records for this mission / satellite: a
        product type is expected on an interface when its ``services_config`` for
        that interface holds a real service (an item starting with ``C`` or ``P``),
        the same rule used by the splitted completeness.

        Returns:
            dict: ``product_type -> set(service_type)``; empty when the dataflow
                config is not loaded (callers then fall back to the raw count).
        """
        expected = {}
        config = MaasConfigManager().get_config("MaasConfigDataflow")
        if not config:
            return expected

        for record in config["records"]:
            if record.mission != self.mission:
                continue
            if self.satellite_unit not in getattr(record, "satellites", []):
                continue
            services_config = getattr(record, "services_config", None)
            if not services_config:
                continue
            interfaces = set()
            for service_type in ("DD", "LTA"):
                if service_type in services_config and any(
                    item.startswith(("C", "P"))
                    for item in services_config[service_type]
                ):
                    interfaces.add(service_type)
            expected[record.product_type] = interfaces

        return expected

    def finalize_duplicateds(self):
        """Assemble the nested ``duplicateds`` object from the buffers.

        Called once at the end of the include-deleted completeness pass, when both
        members of every duplicated pair and all deleted products are known.
        """
        # Each product type is distributed only on the interfaces the dataflow
        # declares for it. A duplicated pair is "expected to be removed" from an
        # interface only when that interface actually distributes its product type
        # (e.g. an S1 SLC pair is never expected to be deleted from DD since SLC is
        # LTA-only). When the dataflow config is not loaded the map is empty and
        # every pair is counted, preserving the previous behaviour.
        expected_interfaces = self._dataflow_expected_interfaces()

        def pair_expected_on(pair, interface):
            if not expected_interfaces:
                return True
            return interface in expected_interfaces.get(pair["product_type"], ())

        # One row per service_type (DD / LTA): a flat, Grafana-friendly shape.
        deletions = []
        for interface in ("DD", "LTA"):
            deleted = self._dup_deleted[interface]  # name -> issue

            issues = [issue for issue in deleted.values() if issue]
            distinct_issues = set(issues)
            if len(distinct_issues) > 1:
                LOGGER.warning(
                    "[%s] Several %s deletion tickets on duplicated products: %s",
                    self.datatake_id,
                    interface,
                    distinct_issues,
                )
            ticket = Counter(issues).most_common(1)[0][0] if issues else None

            # Products deleted from this interface in this datatake.
            targeted = sorted(deleted)
            # Deleted here but not part of any duplicated pair.
            not_duplicated = sorted(
                name for name in targeted if name not in self._dup_paired_names
            )

            # Only pairs whose product type the dataflow distributes on this
            # interface are expected to have their duplicate removed from it.
            expected_pairs = sum(
                1 for pair in self._dup_pairs if pair_expected_on(pair, interface)
            )
            pairs_with_deletion = sum(
                1
                for pair in self._dup_pairs
                if pair_expected_on(pair, interface) and pair["deleted"][interface]
            )
            # Duplicated pairs that survived: expected on this interface but without
            # a product deleted from it (we cannot tell which single product
            # "should" survive, so this is counted at the pair level).
            surviving_pairs = expected_pairs - pairs_with_deletion

            # Share of expected duplicated pairs whose duplicate was actually
            # deleted from this interface. 100% when there is no pair to delete.
            if expected_pairs:
                completeness = round(
                    (expected_pairs - surviving_pairs) / expected_pairs * 100, 2
                )
            else:
                completeness = 100.0

            deletions.append(
                generated.CdsDatatakeDuplicatedsDeletions(
                    service_type=interface,
                    ticket=ticket,
                    targeted_products_count=len(targeted),
                    surviving_pairs_count=surviving_pairs,
                    deleted_not_duplicated_products=not_duplicated,
                    deleted_not_duplicated_products_count=len(not_duplicated),
                    expected_pairs_count=expected_pairs,
                    deletion_completenness_percentange=completeness,
                )
            )

        self.duplicateds = generated.CdsDatatakeDuplicateds(
            items=self._dup_items,
            pairs_count=self._dup_pair_count,
            deletions=deletions,
            datastrip_pairs=self._dup_datastrip_pairs,
        )

    def load_data_before_compute(self):
        """Some step need to be done before starting compute all completeness"""

        if False:
            yield

    def impact_other_calculation(self, compute_key):
        """Some compute provide more information and make possible other compute

        Args:
            compute_key (tuple): the key of the compute that will be execute

        Returns:
            list(tuple): compute keys default: []
        """

        return []

    def evaluate_global_expected(self, key_field) -> int:
        """Evaluate global expected

        Args:
            key_field (str): the global key field we want the value

        Returns:
            int: the value associate to the global expext field given in parameters
        """

        global_expected = self.evaluate_all_global_expected()

        global_value = global_expected.get(key_field, 0)

        if not global_value:
            LOGGER.warning(
                "[%s] - Unhandle key : %s",
                self.datatake_id,
                key_field,
            )

        return global_value

    def get_expected_value(self, scope, key_field):
        """Get expected value for local and global"""

        expected_value = 0

        LOGGER.debug(
            "[%s] - Get expected value : %s - %s",
            self.datatake_id,
            scope,
            key_field,
        )

        if scope == CompletenessScope.LOCAL:
            expected_value = self.evaluate_local_expected(key_field)

        elif scope == CompletenessScope.GLOBAL:
            expected_value = self.evaluate_global_expected(key_field)

        else:
            LOGGER.warning("Scope not handle : %s", scope)

        if not expected_value:
            LOGGER.warning(
                "[%s] - No expected value : %s - %s",
                self.datatake_id,
                scope,
                key_field,
            )

        return expected_value

    def get_global_key_field(self, product_type):
        """Get the key to group local value in a top level value

        Set a static string to get a unique global value

        """

        raise NotImplementedError(
            f"Must be implement in subclasses in CdsDatatake{self.mission} : {product_type}"
        )

    def store_completeness_value(self, attr_name, value):
        """Store a computed completeness value.

        Writes either on the document (live pass) or into the
        ``_completeness_sink`` dict (the "original completeness" pass), so the live
        values are not clobbered while computing the completeness with all products.
        """
        if self._completeness_sink is None:
            setattr(self, attr_name, value)
        else:
            self._completeness_sink[attr_name] = value

    def read_completeness_value(self, attr_name, default=0):
        """Read a completeness value from the current completeness target.

        Mirror of :meth:`store_completeness_value`: reads from the
        ``_completeness_sink`` dict during the original pass, from the document
        otherwise.
        """
        if self._completeness_sink is None:
            return getattr(self, attr_name, default)
        return self._completeness_sink.get(attr_name, default)

    def completeness_items(self):
        """Items of the current completeness target (sink dict or document)."""
        if self._completeness_sink is None:
            return self.to_dict().items()
        return self._completeness_sink.items()

    def set_completeness(
        self,
        scope: CompletenessScope,
        key_field: str,
        completeness_value: int = 0,
    ):
        """Fill a local completeness"""

        LOGGER.debug(
            "[%s] - set completeness for %s %s",
            self.datatake_id,
            scope.value,
            key_field,
        )

        expected_value = self.get_expected_value(
            scope,
            key_field,
        )

        if not expected_value:
            LOGGER.warning(
                "[%s] - Trying to evaluate completeness but expected_value = 0 | %s %s",
                self.datatake_id,
                scope.value,
                key_field,
            )
            if completeness_value:
                # set value if it his different than 0  to raise conflict if expected is compute in parallel
                attr_name_value = f"{key_field}_{scope.value}_value"
                self.store_completeness_value(attr_name_value, completeness_value)
        else:
            # compute other value (avoid value superior to expected )
            adjusted_value = min(completeness_value, expected_value)

            percentage_value = adjusted_value / expected_value * 100

            completeness_status_value = evaluate_completeness_status(percentage_value)

            self.set_completeness_attribut(
                scope,
                key_field,
                completeness_value,
                expected_value,
                adjusted_value,
                percentage_value,
                completeness_status_value,
            )

    # pylint: disable=R0913
    # Parameters must be mandatory
    def set_completeness_attribut(
        self,
        scope: CompletenessScope,
        key_field: str,
        completeness_value: int,
        expected_value: int,
        adjusted_value: int,
        percentage_value: float,
        completeness_status_value: CompletenessStatus,
    ):
        """_summary_

        Args:
            scope (CompletenessScope): scope value (local, global, final)
            key_field (str): key field value
            completeness_value (int): completeness value
            expected_value (int): expected value
            adjusted_value (int): adjusyed value
            percentage_value (float): percentage value
            completeness_status_value (CompletenessStatus): completeness value
        """

        # value
        attr_name_value = f"{key_field}_{scope.value}_value"
        self.store_completeness_value(attr_name_value, completeness_value)

        # expected
        attr_name_expected_value = f"{key_field}_{scope.value}_expected"
        self.store_completeness_value(attr_name_expected_value, expected_value)

        # adjusted
        attr_name_value_adjusted = f"{key_field}_{scope.value}_value_adjusted"
        self.store_completeness_value(attr_name_value_adjusted, adjusted_value)

        # percentage
        if completeness_status_value != CompletenessStatus.UNKNOWN.value:
            attr_name_value_percentage = f"{key_field}_{scope.value}_percentage"
            self.store_completeness_value(attr_name_value_percentage, percentage_value)

        # status
        attr_name_completeness_status = f"{key_field}_{scope.value}_status"
        self.store_completeness_value(
            attr_name_completeness_status,
            completeness_status_value,
        )

    # pylint: enable

    def compute_global_completeness(self):
        """Compute global completeness"""

        LOGGER.info(
            "[%s] - Compute global completeness",
            self.datatake_id,
        )

        global_values = {}
        global_duplication_indicator = {"max_duration": 0, "max_percentage": 0.0}

        doc_dict = self.completeness_items()

        for key, value in doc_dict:
            # maybe we can use a function that returns all product_type
            # In the face of ambiguity refuse the temptation to guess
            if key.endswith("_local_value_adjusted"):
                product_type = key.split("_local_value_adjusted")[0]

                key_field = self.get_global_key_field(product_type)

                if key_field not in global_values:
                    global_values[key_field] = 0

                global_values[key_field] += value

            # Duplicated indicator per product type
            if key.endswith("_duplicated_max_duration"):
                if value > global_duplication_indicator["max_duration"]:
                    global_duplication_indicator["max_duration"] = value

            if key.endswith("_duplicated_max_percentage"):
                if value > global_duplication_indicator["max_percentage"]:
                    global_duplication_indicator["max_percentage"] = value

        # Set
        for key_field, value in global_duplication_indicator.items():
            global_key = f"duplicated_{CompletenessScope.GLOBAL.value}_{key_field}"
            self.store_completeness_value(global_key, value)

        # update global completness
        for key_field, value in global_values.items():
            self.set_completeness(CompletenessScope.GLOBAL, key_field, value)
        # compute extra completness

    def compute_extra_completeness(self):
        """Method to add specific completeness compute"""

    def compute_completeness(self):
        """Compute the local and global completeness of this datatake.

        Products are fetched once (including the ones flagged as deleted) and the
        completeness is computed twice:

        - an "original" pass over all the products, captured into the
          ``original_completeness`` dict and used to also assemble the nested
          ``duplicateds`` object;
        - the regular live pass which ignores the deleted products and writes the
          completeness values on the document.

        Comparing ``original_completeness`` with the live values tells whether a
        product deletion impacts the completeness.
        """

        # Enable the single-query cache shared by both passes.
        self._brother_products_cache = {}

        try:
            # --- Original pass: all products, results captured in a dict ---
            self._init_duplicateds_buffers()
            original_completeness = {}
            self._completeness_sink = original_completeness
            self._include_deleted_products = True
            try:
                self.compute_all_local_completeness()
                self.compute_global_completeness()
                self.compute_extra_completeness()
                # Both members of every duplicated pair and all deleted products
                # are now known: assemble the nested ``duplicateds`` object.

                self.finalize_duplicateds()
            finally:
                self._completeness_sink = None
                self._include_deleted_products = False

            self.original_completeness = original_completeness

            # --- Live pass: deleted products ignored, results on the document ---
            self.compute_all_local_completeness()
            self.compute_global_completeness()
            self.compute_extra_completeness()

        finally:
            self._brother_products_cache = None

    def get_related_documents_query(self) -> Q:
        """
        Builds a query for documents related to this datatake. Typically product
        or publication.

        Returns:
            Q: ES query
        """

    def find_brother_products_scan(
        self, product_type, indices=None, include_deleted=False
    ):
        """Find products with the same datatake and the same product_type

        Note: Seek only product with a prip_id

        Args:
            product_type (str): product_type searched
            indices: optional indices to restrict the search to
            include_deleted (bool): when True, products already flagged as deleted
                (``nb_dd_deleted`` / ``nb_lta_deleted``) are kept in the result.

        Returns:
            list(CdsProduct): list of products matching datatake_id and product_type
        """
        # TODO MAAS_CDS-1236: make a single query to find all the whole brotherhood
        # with list of datatake / product types later post-processed to be grouped by
        # tuple (datatake_id, product_type) in a dict

        # Reuse a previously fetched result during the two completeness passes so a
        # single query is issued for both the "with all products" and the live pass.
        cache_key = (product_type, tuple(indices) if indices else None, include_deleted)
        if (
            self._brother_products_cache is not None
            and cache_key in self._brother_products_cache
        ):
            return self._brother_products_cache[cache_key]

        completeness_service = self.get_service_for_completeness()

        if not completeness_service:
            LOGGER.warning(
                "Try to compute completess but no service identified : %s %s %s",
                self.satellite_unit,
                self.datatake_id,
                product_type,
            )
            completeness_service = ["NO_SERVICE_FOR_THIS"]

        base_search = CdsProduct.search()
        if indices:
            base_search = CdsProduct.search(index=indices)

        # Ignore if index are missing -
        # This can be dangerous to not raise an error on missing index this can hide an database issue

        # Add 1 hour tolerance to the time range
        time_start_with_tolerance = self.observation_time_start - timedelta(hours=1)
        time_stop_with_tolerance = self.observation_time_stop + timedelta(hours=1)

        search_request = (
            base_search.filter("term", datatake_id=self.datatake_id)
            .filter("term", satellite_unit=self.satellite_unit)
            .filter("term", product_type=product_type)
            .filter("terms", prip_service=completeness_service)
            .filter("range", sensing_start_date={"lte": time_stop_with_tolerance})
            .filter("range", sensing_end_date={"gte": time_start_with_tolerance})
            .filter("exists", field="prip_id")
        )

        # Unless explicitly asked to include them, exclude products already flagged
        # as deleted so the live completeness is not impacted by deletions.
        if not include_deleted:
            search_request = search_request.filter(
                "bool",
                should=[
                    {"bool": {"must_not": {"exists": {"field": "nb_dd_deleted"}}}},
                    {"term": {"nb_dd_deleted": 0}},
                ],
            ).filter(
                "bool",
                should=[
                    {"bool": {"must_not": {"exists": {"field": "nb_lta_deleted"}}}},
                    {"term": {"nb_lta_deleted": 0}},
                ],
            )

        search_request = search_request.params(ignore=404, ignore_unavailable=True)

        # When caching is active (completeness two-pass) the result must be
        # materialized so it can be iterated twice.
        if self._brother_products_cache is not None:
            result = list(search_request.scan())
            self._brother_products_cache[cache_key] = result
            return result

        return search_request.scan()

    def retrieve_additional_fields_from_product(self, product: CdsProduct):
        """Abstract function which allow to fill additional
        datatake fields during completeness calculation"""
