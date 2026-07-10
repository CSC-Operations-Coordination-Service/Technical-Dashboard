"""Datatake S2 model definition"""

import logging

from collections import Counter
from datetime import timedelta
import typing
from maas_cds.lib.parsing_name import utils
from maas_cds.model.product import CdsProduct
from maas_cds.model import generated

from opensearchpy import Q

from maas_cds.model.datatake import CdsDatatake
from maas_cds.lib.status import evaluate_completeness_status

from maas_cds.lib.periodutils import (
    compute_total_sensing_product,
    compute_overlap_percentage,
    compute_overlap_duration,
    Period,
    DuplicationCandidate,
)


from maas_cds.model.enumeration import CompletenessScope

from maas_cds.lib import tolerance
from maas_cds.model import CdsDownlinkDatatake

__all__ = ["CdsDatatakeS2"]


LOGGER = logging.getLogger("CdsModelDatatakeS2")


class CdsDatatakeS2(CdsDatatake):
    """CdsDatatake custom class for Sentinel 2"""

    RATIO_GRANULE_TILE = 10
    TOLERENCE_SENSING_START_GRANULE = 0.002

    # The L0 datastrip is "the datastrip": two MSI_L0__DS whose sensing overlap
    # beyond the duplicated threshold are a duplicated datastrip pair, see
    # compute_duplicated_datastrips. Its identity is the product name.
    DUPLICATED_DATASTRIP_REFERENCE_TYPE = "MSI_L0__DS"

    # Higher-level datastrip product types. L1x granules / tiles reference their
    # OWN level DS (not the L0 DS), so the DS of these levels whose sensing is
    # included in the L0 DS are resolved to reattach their products to the L0
    # datastrip.
    DUPLICATED_DATASTRIP_LEVEL_TYPES = [
        "MSI_L1A_DS",
        "MSI_L1B_DS",
        "MSI_L1C_DS",
        "MSI_L2A_DS",
    ]

    # GR / TL product types (all levels) attached to a datastrip through their
    # ``datastrip_id`` (which holds a DS product name).
    DUPLICATED_DATASTRIP_PRODUCT_TYPES = [
        "MSI_L0__GR",
        "MSI_L1A_GR",
        "MSI_L1B_GR",
        "MSI_L1C_TL",
        "MSI_L2A_TL",
    ]

    # Tolerance when testing that a higher-level DS sensing is included in the
    # L0 DS sensing.
    DUPLICATED_DATASTRIP_SENSING_TOLERANCE = timedelta(seconds=1)

    # S2 duplication is flagged only when two datastrips overlap by at least
    # DUPLICATED_ITEMS_PERCENTAGE_THRESHOLD percent AND at least 15 seconds.
    DUPLICATED_ITEMS_MINIMAL_DURATION = 15.0

    MATCHING_DELTA_PRODUCTS = 15

    REFERENCE_PRODUCT_TYPE_SENSING = "MSI_L1C_DS"

    S2_EXPECTED_TYPE_FROM_PRODUCT_LEVEL_DICT = {
        "L0_": [
            "DS",
            "GR",
        ],
        "L1A": [
            "DS",
            "GR",
        ],
        "L1B": [
            "DS",
            "GR",
        ],
        "L1C": [
            "DS",
            "TL",
            "TC",
        ],
        "L2A": [
            "DS",
            "TL",
            "TC",
        ],
    }

    S2_NUMBER_OF_GR_PER_SCENE_PER_INSTRUMENT_DICT = {
        "NOBS": 12,
        "VIC": 12,
        "RAW": 4,
        "DASC": 12,
        "ABSR": 12,
        "EOBS": 12,
        "DARK-O": 12,
        "DARK-C": 12,
        "SUN": 12,
        "HKTM": 12,
        "MSMOON": 12,
    }

    S2_PRODUCT_LEVEL_FROM_INSTRUMENT_DICT = {
        "NOBS": ["L0_", "L1B", "L1C", "L2A"],
        "VIC": ["L0_", "L1B", "L1C"],
        "RAW": ["L0_", "L1A", "L1B", "L1C", "L2A"],
        "DASC": ["L0_", "L1A"],
        "ABSR": ["L0_", "L1A"],
        "EOBS": ["L0_", "L1A"],
        "DARK-O": ["L0_", "L1A"],
        "DARK-C": ["L0_", "L1A"],
        "SUN": ["L0_", "L1A"],
        "HKTM": ["L0_"],
        "MSMOON": ["L0_"],
    }

    STATIC_COMPLETENESS_VALUE = {"MSI_L.*_DS": 3608000 + 1000000}

    def __init__(self, meta=None, **kwargs):
        super().__init__(meta, **kwargs)
        self.number_of_expected_tiles = 0

    def get_downlinks(self):
        """Get the count of downlink datatake entries with the same satellite and datatake_id"""
        search_request = (
            CdsDownlinkDatatake.search()
            .filter("term", satellite_unit=self.satellite_unit)
            .filter("term", datatake_id=self.datatake_id)
        )
        return search_request.execute()

    def product_type_with_missing_periods(self, product_type: str) -> bool:
        """Do we want missing periods for this product type ?"""
        return product_type == "MSI_L0__DS"

    def product_type_with_duplicated(self, product_type: str) -> bool:
        """Do we want check duplicated for this product type ?"""
        return product_type.endswith("DS")

    def product_type_with_duplicated_items(self, product_type: str) -> bool:
        """Only L0 DS duplications are listed in ``duplicateds.items``.

        The duplicated indicator is still computed for every DS level (see
        ``product_type_with_duplicated``), but the detailed pairs list is
        restricted to the L0 datastrip.
        """
        return product_type == self.DUPLICATED_DATASTRIP_REFERENCE_TYPE

    def get_expected_from_product_level(self, product_level):
        """Get expected from the product level

        Args:
            product_level (str): product level thaht we want expected

        Returns:
            dict: expect dict for the given product level
        """

        if (
            self.instrument_mode
            not in self.S2_NUMBER_OF_GR_PER_SCENE_PER_INSTRUMENT_DICT
        ):
            LOGGER.critical(
                "Unhandled instrument mode '%s' in %s. Unable to calculate expected products.",
                self.instrument_mode,
                self,
            )
            return {}

        # find a better name and set top level conf

        # - 3608000 -> remove one scene (cause first and last gr are at the half)
        # - 1000000 -> remove one sec (cause millisec are truncate)

        s2_number_of_gr_per_scene = self.S2_NUMBER_OF_GR_PER_SCENE_PER_INSTRUMENT_DICT[
            self.instrument_mode
        ]

        s2_expected_from_product_level_dict = {
            "L0_": {
                "DS": self.observation_duration,
                "GR": self.number_of_scenes * s2_number_of_gr_per_scene,
            },
            "L1A": {
                "DS": self.observation_duration - (2 * 3608000),
                "GR": (self.number_of_scenes - 2) * s2_number_of_gr_per_scene,
            },
            "L1B": {
                "DS": self.observation_duration - (2 * 3608000),
                "GR": (self.number_of_scenes - 2) * s2_number_of_gr_per_scene,
            },
            "L1C": {
                "DS": self.observation_duration - (2 * 3608000),
                "TL": self.number_of_expected_tiles,
                "TC": self.number_of_expected_tiles,
            },
            "L2A": {
                "DS": self.observation_duration - (2 * 3608000),
                "TL": self.number_of_expected_tiles,
                "TC": self.number_of_expected_tiles,
            },
        }

        # apply tolerance for product_level only
        product_level_with_tolerance = s2_expected_from_product_level_dict.get(
            product_level, {}
        )
        for key in product_level_with_tolerance:
            tolerance_value = tolerance.get_completeness_tolerance(
                self.COMPLETENESS_TOLERANCE,
                self.mission,
                CompletenessScope.LOCAL,
                f"MSI_{product_level}_{key}",
            )
            sensing_value_with_tolerance = (
                product_level_with_tolerance[key] + tolerance_value
            )

            # avoid negative sensing
            product_level_with_tolerance[key] = max(0, sensing_value_with_tolerance)

        return product_level_with_tolerance

    @classmethod
    def expected_type_per_level(cls, product_level):
        """Return the expected type for the given product_level

        Args:
            product_level (str): The product level to get expecte type

        Returns:
            list(str): the list of the type of product expected for this level
        """
        return cls.S2_EXPECTED_TYPE_FROM_PRODUCT_LEVEL_DICT.get(product_level, [])

    def get_expected_product_level(self):
        """Get expected product_level for the datatake

        Returns:
            list: a list of the expected product level
        """

        product_level_to_get = self.S2_PRODUCT_LEVEL_FROM_INSTRUMENT_DICT.get(
            self.instrument_mode, ["L0_"]
        )

        # We need to get at least 3 scenes to compute level L1 and L2
        if self.number_of_scenes < 3:
            product_level_to_get = ["L0_"]

        return product_level_to_get

    def impact_other_calculation(self, compute_key):
        """MSI_L1C_DS provide footprint to evaluated expected tiles

        Args:
            compute_key (tuple): the key of the compute that will be execute

        Returns:
            list(tuple): compute keys default: []
        """
        compute_product_type = compute_key[1]

        if self.REFERENCE_PRODUCT_TYPE_SENSING in compute_product_type:
            # build compute key to process

            self.number_of_expected_tiles = len(self.search_expected_tiles())

            product_types_to_compute = [
                product_type
                for product_type in self.get_all_product_types()
                if "TL" in product_type or "TC" in product_type
            ]

            return [
                (compute_key[0], product_type)
                for product_type in product_types_to_compute
            ]
        return []

    def load_data_before_compute(self):
        """Some step need to be done before starting compute all completeness"""

        # Evaluate expected tiles before compute completeness
        self.number_of_expected_tiles = len(self.search_expected_tiles())

        setattr(self, "number_of_expected_ds", len(self.get_downlinks()))

        if not self.product_group_ids:
            return

        for product in (
            self.find_related_document_not_attached()
            .params(version=True, seq_no_primary_term=True)
            .scan()
        ):

            self.retrieve_additional_fields_from_product(product)

            if product.datatake_id != self.datatake_id:

                LOGGER.info(
                    "Load_data_before_compute - CdsProduct with key %s had"
                    " no datatake_id, using product group id it has been rattached"
                    " to datatake_id : %s",
                    product.key,
                    self.datatake_id,
                )

                product.datatake_id = self.datatake_id

                if self.timeliness:
                    product.timeliness = self.timeliness

                product.absolute_orbit = self.absolute_orbit
                product.relative_orbit = self.relative_orbit

                product.instrument_mode = self.instrument_mode

                yield product.to_bulk_action()

    def find_related_document_not_attached(self):
        # Try to rattach products which have no datatake id to this datatake using sensing date
        # Also update the datastrip_ds and product_group_ids list of the datatake

        search_request = (
            CdsProduct.search()
            .filter("term", mission=self.mission)
            .filter("term", satellite_unit=self.satellite_unit)
            .filter("exists", field="prip_id")
            .filter(~Q("term", datatake_id=self.datatake_id))
            .filter("term", product_group_id=self.product_group_ids[0])
            .params(ignore=404)
        )

        return search_request

    def search_expected_tiles(self) -> set[str]:
        """Look for expected tiles for this datatake

        Returns:
            int: the number of expected tiles for the whole datatake
        """
        products_scan = self.find_brother_products_scan(
            self.REFERENCE_PRODUCT_TYPE_SENSING,
        )
        expected_tiles = set()
        for product in products_scan:
            if product.expected_tiles:
                expected_tiles.update(product.expected_tiles)

        LOGGER.info(
            "Getting expected tiles %s",
            sorted(expected_tiles),
        )
        return expected_tiles

    def evaluate_all_global_expected(self):
        """Return global expected

        Returns:
            dict: The global expected of this datatake
        """

        global_expected = {}

        product_level_to_get = self.get_expected_product_level()

        for product_level in product_level_to_get:
            expected_for_product_level = self.get_expected_from_product_level(
                product_level
            )

            for key, value in expected_for_product_level.items():
                if key not in global_expected:
                    global_expected[key] = 0

                global_expected[key] += value

        if not global_expected:
            LOGGER.warning(
                "[%s] - No global expected for : %s",
                self.datatake_id,
                self.instrument_mode,
            )

        return global_expected

    def get_all_product_types(self):
        """Return all product type expected for this datatake

        Returns:
            list: List of all product type expected for this datatake
        """
        product_types = []

        product_level_to_get = self.get_expected_product_level()
        for product_level in product_level_to_get:
            expected_types_for_product_level = self.expected_type_per_level(
                product_level
            )

            for key in expected_types_for_product_level:
                # rebuild the product_type
                product_type = f"MSI_{product_level}_{key}"
                product_types.append(product_type)

        return product_types

    def compute_local_value(self, product_type, related_documents=None):
        """Compute local value for a specific product_type

        Args:
            product_type (str): Product type that we want to compute the value
        """

        LOGGER.debug(
            "[%s] - Compute local value for %s",
            self.datatake_id,
            product_type,
        )

        brother_of_datatake_documents = self.get_product_compute_brother(product_type)

        compute_method = self.get_compute_method(product_type)

        value = compute_method(brother_of_datatake_documents)

        if value > 0:
            value += tolerance.get_tolerance_from_scope(
                self.STATIC_COMPLETENESS_VALUE, product_type
            )

        if related_documents is not None:
            related_documents.extend(brother_of_datatake_documents)

        return value

    def get_compute_method(self, product_type):
        """Return the aggragation method for a product type

        Args:
            product_type (str): the product type where we want the compute method

        Returns:
            callable: the method to compute the completeness value
        """
        key_field = self.get_global_key_field(product_type)

        compute_method = len

        # __ is for container
        if key_field in ["TL", "TC", "GR", "__"]:
            compute_method = len

        elif key_field in ["DS"]:
            compute_method = compute_total_sensing_product

        else:
            LOGGER.warning(
                "[%s] - Unhandle product_type for S2 on get_compute_method : %s",
                self.datatake_id,
                product_type,
            )

        return compute_method

    def get_product_compute_brother(self, key_field):
        """The method who returns all product with the same compute key

        Args:
            key_field (str): the product type who is also a part of a compute key

        Returns:
            iterable: products with the same key_field
        """
        # for s2 key_field is the product_type
        product_type = key_field

        LOGGER.debug(
            "[%s] - get_product_compute_brother for %s",
            self.datatake_id,
            product_type,
        )

        # Fetch all products once (deleted included): the result is cached and
        # shared by both completeness passes. Deleted products are filtered out in
        # memory during the live pass.
        products_scan = self.find_brother_products_scan(
            product_type,
            self.get_product_partitionning(day_precision=1),
            include_deleted=True,
        )
        brother_of_datatake_documents = []

        key_field = self.get_global_key_field(product_type)

        if key_field in ["GR"]:
            brother_of_datatake_documents = set()

            intermediary_buffer = {}

            duplicated_item = 0

            for product in products_scan:
                if product.sensing_start_date and product.detector_id:
                    to_be_deleted, deletion_issue = product.deletion_trace()

                    # Live pass ignores the products already deleted.
                    if to_be_deleted and not self._include_deleted_products:
                        continue

                    key = (product.detector_id, product.datastrip_id)

                    # Group product info per detector id and datastrip_id, keeping
                    # the product identity to be able to report duplicated items.
                    intermediary_buffer.setdefault(key, []).append(
                        self._duplicated_product_info(
                            product, to_be_deleted, deletion_issue
                        )
                    )
                else:
                    LOGGER.warning(
                        "[%s][%s] - Failed to add it in document brothers [ %s, %s, %s]",
                        self.datatake_id,
                        product.key,
                        product.sensing_start_date,
                        product.detector_id,
                        product.datastrip_id,
                    )

            # Group by detector id, datastrip_id and ± tolerance on sensing_start_date
            for (
                detector_id,
                datastrip_id,
            ), product_info_list in intermediary_buffer.items():
                ordered_products = sorted(
                    product_info_list, key=lambda info: info["sensing_start_date"]
                )
                prev = None
                for product_info in ordered_products:
                    if (
                        prev
                        and product_info["sensing_start_date"].timestamp()
                        - prev["sensing_start_date"].timestamp()
                        <= self.TOLERENCE_SENSING_START_GRANULE
                    ):
                        duplicated_item += 1
                        LOGGER.warning(
                            "[%s] - Potential duplicate GR for datatake detector_id %s datastrip_id %s sensing %s",
                            self.datatake_id,
                            detector_id,
                            datastrip_id,
                            product_info["sensing_start_date"],
                        )
                        # Only DS duplications are reported in duplicateds.items;
                        # GR duplicates are only counted (_duplicated_gr).

                    else:
                        prev = product_info
                        brother_of_datatake_documents.add(
                            (
                                product_info["sensing_start_date"],
                                detector_id,
                                datastrip_id,
                            )
                        )
            self.store_completeness_value(
                f"{product_type}_duplicated_gr", duplicated_item
            )

        elif key_field in ["TL", "TC", "__"]:
            # get unique TL/TC number
            brother_of_datatake_documents = set()

            duplicated_item = 0
            for product in products_scan:
                if product.tile_number:
                    to_be_deleted, _ = product.deletion_trace()

                    # Live pass ignores the products already deleted.
                    if to_be_deleted and not self._include_deleted_products:
                        continue

                    if product.tile_number in brother_of_datatake_documents:
                        duplicated_item += 1
                        # Only DS duplications are reported in duplicateds.items;
                        # TL/TC duplicates are only counted (_duplicated_tuile).
                    else:
                        brother_of_datatake_documents.add(product.tile_number)

                else:
                    LOGGER.warning(
                        "[%s][%s] - Failed to add it in document brothers [ %s, %s]",
                        self.datatake_id,
                        product.key,
                        product.sensing_start_date,
                        product.tile_number,
                    )
            self.store_completeness_value(
                f"{product_type}_duplicated_tuile", duplicated_item
            )

        elif key_field in ["DS"]:
            brother_of_datatake_documents = []

            for product in products_scan:
                if (
                    product.sensing_duration
                    and product.sensing_start_date
                    and product.sensing_end_date
                ):
                    to_be_deleted, deletion_issue = product.deletion_trace()

                    # Live pass ignores the products already deleted.
                    if to_be_deleted and not self._include_deleted_products:
                        continue

                    by_interface = product.deletion_trace_by_interface()
                    dd_deleted, dd_issue = by_interface["DD"]
                    lta_deleted, lta_issue = by_interface["LTA"]

                    # DuplicationCandidate is a drop-in replacement for Period (only
                    # start / end are used by the compute) and lets the base class
                    # report duplicated DS items via the time-overlap detection.
                    brother_of_datatake_documents.append(
                        DuplicationCandidate(
                            product.name,
                            product.sensing_start_date,
                            product.sensing_end_date,
                            to_be_deleted,
                            deletion_issue,
                            dd_deleted,
                            dd_issue,
                            lta_deleted,
                            lta_issue,
                        )
                    )

                else:
                    LOGGER.warning(
                        "[%s][%s] - Failed to add it in document brothers [ %s, %s]",
                        self.datatake_id,
                        product.key,
                        product.sensing_start_date,
                        product.sensing_end_date,
                    )

            # Sort document by sensing date
            brother_of_datatake_documents.sort(
                key=lambda product: (product.start, product.end)
            )

        else:
            LOGGER.warning(
                "[%s] - Unhandle product_type for S2 on get_product_compute_brother : %s",
                self.datatake_id,
                product_type,
            )

        return brother_of_datatake_documents

    def evaluate_local_expected(self, product_type):
        """Evaluate expected for a specific product_type

        Args:
            product_type (str): product_type that we want to get the local expected

        Returns:
            int: The local expected value of this datatake and the given product_type
        """
        product_level = product_type[4:7]
        local_expected_product_type = self.get_expected_from_product_level(
            product_level
        )

        key_field_value = self.get_global_key_field(product_type)
        expected_value = local_expected_product_type.get(key_field_value, None)

        return expected_value

    def get_global_key_field(self, product_type):
        """Global key is the aggregation of local value.
        Because we can't mix carrots and potatoes we have this method to extract a aggregation key

        Args:
            product_type (_type_): _description_

        Returns:
            _type_: _description_
        """
        return product_type[-2:]

    def compute_extra_completeness(self):
        """Need to compute product level completeness and final for snetinel 2"""

        LOGGER.info(
            "[%s] - Compute extra completeness",
            self.datatake_id,
        )

        final_expected = final_value = 0
        product_level_to_get = self.get_expected_product_level()

        for product_level in product_level_to_get:
            LOGGER.debug(
                "[%s] - Extra completeness : %s", self.datatake_id, product_level
            )

            product_level_expected = product_level_value = 0

            expected_for_product_level = self.get_expected_from_product_level(
                product_level
            )

            for key in expected_for_product_level:
                # rebuild the product_type
                product_type = f"MSI_{product_level}_{key}"

                attr_product_type_value = f"{product_type}_local_value_adjusted"
                product_type_value = self.read_completeness_value(
                    attr_product_type_value, 0
                )

                attr_expected_ds_value = f"MSI_{product_level}_DS_local_expected"
                expected_ds_value = self.read_completeness_value(
                    attr_expected_ds_value, 0
                )

                attr_product_type_expected = f"{product_type}_local_expected"
                expected_value = self.read_completeness_value(
                    attr_product_type_expected, 0
                )

                if 0 in (expected_ds_value, expected_value):
                    # Sometime geometry arrive later
                    LOGGER.warning(
                        "[%s] - Missing expected : %s -> %s | DS : %s -> %s",
                        self.datatake_id,
                        attr_product_type_expected,
                        expected_value,
                        attr_expected_ds_value,
                        expected_ds_value,
                    )
                    value = 0
                    expected = 0

                else:
                    value = expected_ds_value / expected_value * product_type_value
                    expected = expected_ds_value

                product_level_value += value
                product_level_expected += expected

                final_value += value
                final_expected += expected

            # product level completeness
            if product_level_expected == 0:
                LOGGER.warning(
                    "[%s] - No product level expected for : %s",
                    self.datatake_id,
                    product_level,
                )

                product_level_percentage = 0

            else:
                product_level_percentage = (
                    product_level_value / product_level_expected * 100
                )

            self.store_completeness_value(
                f"{product_level}_local_value", product_level_value
            )
            self.store_completeness_value(
                f"{product_level}_local_expected", product_level_expected
            )
            self.store_completeness_value(
                f"{product_level}_local_percentage", product_level_percentage
            )
            self.store_completeness_value(
                f"{product_level}_local_status",
                evaluate_completeness_status(product_level_percentage),
            )

        # final completeness
        if final_expected == 0:
            LOGGER.warning(
                "[%s] - No final expected",
                self.datatake_id,
            )
            percentage = 0
        else:
            percentage = final_value / final_expected * 100

        self.store_completeness_value("final_completeness_value", final_value)
        self.store_completeness_value("final_completeness_expected", final_expected)
        self.store_completeness_value("final_completeness_percentage", percentage)
        self.store_completeness_value(
            "final_completeness_status", evaluate_completeness_status(percentage)
        )

        # Datastrip-centric duplication: detected on the include-deleted pass so
        # that a datastrip stays reported even after its products are deleted.
        # finalize_duplicateds (called just after this pass) reads the buffer.
        if self._include_deleted_products:
            self.compute_duplicated_datastrips()

    @staticmethod
    def _datastrip_key(name):
        """Return the datastrip identifier held by a product ``datastrip_id``.

        The L0 / L1x DS ``datastrip_id`` field is not populated, but the granules
        and tiles carry the *name* of their level DS (without the archive
        extension) in their ``datastrip_id``. This strips the known archive
        suffixes from a DS product name so it matches those references.
        """
        if not name:
            return name
        for suffix in (".tar", ".SAFE", ".zip", ".SEN3"):
            if name.endswith(suffix):
                return name[: -len(suffix)]
        return name

    def _attached_products_by_datastrip(self):
        """Index GR / TL products by the DS name held in their ``datastrip_id``.

        The GR / TL products (all levels, see
        ``DUPLICATED_DATASTRIP_PRODUCT_TYPES``) are fetched once (deleted included)
        and indexed by ``datastrip_id`` (a DS product name), the only field that
        links them to a specific datastrip.

        Returns:
            dict: ``datastrip_id`` (a DS name) -> list of attached products.
        """
        by_datastrip_id = {}

        for product_type in self.DUPLICATED_DATASTRIP_PRODUCT_TYPES:
            products_scan = self.find_brother_products_scan(
                product_type,
                self.get_product_partitionning(day_precision=1),
                include_deleted=True,
            )
            for product in products_scan:
                if product.datastrip_id:
                    by_datastrip_id.setdefault(product.datastrip_id, []).append(product)

        return by_datastrip_id

    def _level_datastrips(self):
        """Resolve the higher-level DS (L1A/L1B/L1C/L2A) with their sensing period.

        L1x granules / tiles reference their own-level DS, so these DS are needed
        to map, by sensing inclusion, the L0 datastrip to the products of the
        higher levels.

        Returns:
            list(dict): one entry per higher-level DS product, with its
                ``name_key`` (matching the ``datastrip_id`` of its products) and
                its sensing ``start`` / ``end``.
        """
        level_datastrips = []
        for product_type in self.DUPLICATED_DATASTRIP_LEVEL_TYPES:
            products_scan = self.find_brother_products_scan(
                product_type,
                self.get_product_partitionning(day_precision=1),
                include_deleted=True,
            )
            for product in products_scan:
                if product.sensing_start_date and product.sensing_end_date:
                    level_datastrips.append(
                        {
                            "name_key": self._datastrip_key(product.name),
                            "start": product.sensing_start_date,
                            "end": product.sensing_end_date,
                        }
                    )
        return level_datastrips

    def _describe_datastrip(
        self, datastrip, by_datastrip_id, level_datastrips, expected_interfaces
    ):
        """Build the reported entry for one L0 datastrip of a duplicated pair.

        The L0 datastrip name attaches the L0 granules directly. For the higher
        levels, the DS whose sensing is included in the L0 DS sensing are resolved
        and their products attached through ``datastrip_id``. Each attached product
        is listed with its per-interface deletion ticket, and a per-interface
        (DD / LTA) deletion summary gives the count, the number of attached products
        the dataflow expects on that interface, and the share of them deleted.

        Args:
            datastrip (dict): the L0 DS ``name_key`` and sensing ``start`` / ``end``.
            by_datastrip_id (dict): index from ``_attached_products_by_datastrip``.
            level_datastrips (list): higher-level DS from ``_level_datastrips``.
            expected_interfaces (dict): ``product_type -> set(service_type)`` from
                ``_dataflow_expected_interfaces``.

        Returns:
            generated.CdsDatatakeDuplicatedsDatastripPairsDatastrips
        """
        # DS names whose products belong to this datastrip: the L0 DS itself plus
        # every higher-level DS whose sensing is included in the L0 sensing.
        tolerance = self.DUPLICATED_DATASTRIP_SENSING_TOLERANCE
        ds_names = {datastrip["name_key"]}
        for level_datastrip in level_datastrips:
            if (
                level_datastrip["start"] >= datastrip["start"] - tolerance
                and level_datastrip["end"] <= datastrip["end"] + tolerance
            ):
                ds_names.add(level_datastrip["name_key"])

        # Dedupe by product name.
        attached = {}
        for ds_name in ds_names:
            for product in by_datastrip_id.get(ds_name, []):
                attached[product.name] = product

        products = []
        deleted_count = {"DD": 0, "LTA": 0}
        deleted_tickets = {"DD": [], "LTA": []}
        for product in attached.values():
            by_interface = product.deletion_trace_by_interface()
            # One deletion entry per interface the product is actually deleted from.
            product_deletions = []
            for interface in ("DD", "LTA"):
                deleted, issue = by_interface[interface]
                if deleted:
                    deleted_count[interface] += 1
                    if issue:
                        deleted_tickets[interface].append(issue)
                    product_deletions.append(
                        generated.CdsDatatakeDuplicatedsDatastripPairsDatastripsProductsDeletions(
                            service_type=interface,
                            ticket=issue,
                        )
                    )

            products.append(
                generated.CdsDatatakeDuplicatedsDatastripPairsDatastripsProducts(
                    product_name=product.name,
                    product_type=product.product_type,
                    deletions=product_deletions,
                )
            )

        # Stable ordering so the stored document is reproducible.
        products.sort(key=lambda item: item.product_name or "")

        # Deletion-share denominator, per interface: only the attached products the
        # dataflow expects on that interface. Without the dataflow config, fall
        # back to the raw attached count.
        expected_per_interface = {"DD": 0, "LTA": 0}
        if expected_interfaces:
            for product in attached.values():
                for interface in expected_interfaces.get(product.product_type, ()):
                    if interface in expected_per_interface:
                        expected_per_interface[interface] += 1
        else:
            total = len(attached)
            expected_per_interface = {"DD": total, "LTA": total}

        deletions = []
        for interface in ("DD", "LTA"):
            if not deleted_count[interface]:
                continue
            tickets = deleted_tickets[interface]
            ticket = Counter(tickets).most_common(1)[0][0] if tickets else None
            expected = expected_per_interface[interface]
            percentage = (
                round(deleted_count[interface] / expected * 100, 2) if expected else 0.0
            )
            deletions.append(
                generated.CdsDatatakeDuplicatedsDatastripPairsDatastripsDeletions(
                    service_type=interface,
                    ticket=ticket,
                    deleted_products_count=deleted_count[interface],
                    deleted_products_expected=expected,
                    deleted_product_percentage=percentage,
                )
            )

        return generated.CdsDatatakeDuplicatedsDatastripPairsDatastrips(
            datastrip_id=datastrip["name_key"],
            products=products,
            deletions=deletions,
        )

    def compute_duplicated_datastrips(self):
        """Detect duplicated L0 datastrips and buffer them for ``finalize_duplicateds``.

        Two ``MSI_L0__DS`` products whose sensing overlaps by at least
        ``DUPLICATED_ITEMS_PERCENTAGE_THRESHOLD`` percent and at least
        ``DUPLICATED_ITEMS_MINIMAL_DURATION`` seconds are a duplicated datastrip
        pair. Each L0 datastrip is identified by its product name; the attached
        GR / TL products (L0 directly, higher levels through the DS whose sensing
        is included in the L0 DS) are listed and their deletion tickets reported.
        """
        ds_products = self.find_brother_products_scan(
            self.DUPLICATED_DATASTRIP_REFERENCE_TYPE,
            self.get_product_partitionning(day_precision=1),
            include_deleted=True,
        )

        datastrips = []
        for product in ds_products:
            # The L0 DS ``datastrip_id`` field is not populated: the product name
            # is the datastrip identity.
            if product.sensing_start_date and product.sensing_end_date:
                datastrips.append(
                    {
                        "name_key": self._datastrip_key(product.name),
                        "start": product.sensing_start_date,
                        "end": product.sensing_end_date,
                    }
                )
            else:
                LOGGER.warning(
                    "[%s][%s] - L0 DS ignored for datastrip duplication [ %s, %s ]",
                    self.datatake_id,
                    product.key,
                    product.sensing_start_date,
                    product.sensing_end_date,
                )

        if len(datastrips) < 2:
            LOGGER.debug(
                "[%s] - Solo L0 datastrip for this datatake, no duplication",
                self.datatake_id,
            )
            return

        # Same convention as the generic time-overlap detection: sort by sensing
        # period and compare each datastrip with the next one.
        datastrips.sort(key=lambda strip: (strip["start"], strip["end"]))

        overlapping_pairs = []
        for previous, brother in zip(datastrips[:-1], datastrips[1:]):
            previous_period = Period(previous["start"], previous["end"])
            brother_period = Period(brother["start"], brother["end"])
            percentage = compute_overlap_percentage(previous_period, brother_period)
            duration = compute_overlap_duration(previous_period, brother_period)
            if (
                percentage >= self.DUPLICATED_ITEMS_PERCENTAGE_THRESHOLD
                and duration >= self.DUPLICATED_ITEMS_MINIMAL_DURATION
            ):
                overlapping_pairs.append((previous, brother, percentage))

        if not overlapping_pairs:
            LOGGER.debug(
                "[%s] - No overlapping L0 datastrip for this datatake",
                self.datatake_id,
            )
            return

        by_datastrip_id = self._attached_products_by_datastrip()
        level_datastrips = self._level_datastrips()
        expected_interfaces = self._dataflow_expected_interfaces()

        for previous, brother, percentage in overlapping_pairs:
            LOGGER.warning(
                "[%s] - Duplicated L0 datastrips %s / %s (overlap %.2f%%)",
                self.datatake_id,
                previous["name_key"],
                brother["name_key"],
                percentage,
            )
            self._dup_datastrip_pairs.append(
                generated.CdsDatatakeDuplicatedsDatastripPairs(
                    overlap_percentage=round(percentage, 2),
                    datastrips=[
                        self._describe_datastrip(
                            previous, by_datastrip_id, level_datastrips,
                            expected_interfaces,
                        ),
                        self._describe_datastrip(
                            brother, by_datastrip_id, level_datastrips,
                            expected_interfaces,
                        ),
                    ],
                )
            )

    def get_related_documents_query(self) -> Q:
        """override"""

        # We match all product between observation ± delta in seconds

        # start_date = self.observation_time_start - timedelta(
        #     seconds=self.MATCHING_DELTA_PRODUCTS
        # )
        # end_date = self.observation_time_stop + timedelta(
        #     seconds=self.MATCHING_DELTA_PRODUCTS
        # )
        # return Q(
        #     "bool",
        #     filter=[
        #         Q("term", satellite_unit=self.satellite_unit),
        #         Q(
        #             "range",
        #             sensing_start_date={"gte": start_date},
        #         ),
        #         Q(
        #             "range",
        #             sensing_end_date={"lte": end_date},
        #         ),
        #     ],
        # )

        # Default behaviour
        return Q(
            "bool",
            filter=[
                Q("term", satellite_unit=self.satellite_unit),
                Q("term", datatake_id=self.datatake_id),
            ],
        )

    def retrieve_additional_fields_from_product(self, product: CdsProduct):
        """Fill the datastrip_ids and product_group_ids field of the datatake using the value
        from the product
        Args:
            products (CdsProduct): Product which belongs to this datatake
        """

        if (
            "datastrip_id" in product
            and product.datastrip_id
            and product.datastrip_id not in self.datastrip_ids
        ):
            LOGGER.debug(
                "datastrip_id %s has been added to the list of datastrip_id of datatake:%s because of CdsProduct:%s",
                product.datastrip_id,
                self.datatake_id,
                product.key,
            )
            self.datastrip_ids.append(product.datastrip_id)

        if (
            "product_group_id" in product
            and product.product_group_id
            and product.product_group_id not in self.product_group_ids
        ):
            LOGGER.debug(
                "product_group_id %s has been added to the list of product_group_ids of datatake:%s because of CdsProduct:%s",
                product.product_group_id,
                self.datatake_id,
                product.key,
            )

            self.product_group_ids.append(product.product_group_id)

            if len(self.product_group_ids) > 1:
                LOGGER.warning(
                    "[%s] - It's unexpected to have more than 1 products group id",
                    self.datatake_id,
                )
