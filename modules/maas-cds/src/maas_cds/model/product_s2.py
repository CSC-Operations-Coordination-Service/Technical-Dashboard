"""Custom CDS model definition for s2 product"""

import logging

from maas_cds.lib.queryutils.find_datatake_from_sensing import (
    find_datatake_from_sensing,
)
from maas_cds.lib.queryutils.find_datatake_from_product_group_id import (
    find_datatake_from_product_group_id,
)
from maas_cds.model.product import CdsProduct
import maas_cds.lib.parsing_name.utils as utils

__all__ = ["CdsProductS2"]


LOGGER = logging.getLogger("CdsModelProductS2")


class CdsProductS2(CdsProduct):
    """CdsProduct specific for sentinel 2"""

    NO_DATATAKE_PRODUCT_TYPES = ("AUX_SADATA", "OLQC_REPORT", "PRD_HKTM__")

    PRODUCT_TYPES_WITH_TILES = ("MSI_L1C_DS", "MSI_L2A_DS")

    def get_datatake_id(self):
        """Return the associate datatake id of the product

        Returns:
            str: associate datatake id
        """

        if not self.datatake_id or self.datatake_id == utils.DATATAKE_ID_MISSING_VALUE:
            self.find_datatake_id()

        return (
            f"{self.satellite_unit}-{self.datatake_id}"
            if not self.datatake_id_is_missing()
            else None
        )

    def find_datatake_id(self):
        """Find datatake id associate to the product

        For sentinel 2 we need to look in datatake if a mission planning cover the product range
        This method allow product to search in datatake
        and retrieve all matching datatake who cover the product

        """
        # prevent search for products that are not attached to any datastrip
        if self.product_type in CdsProductS2.NO_DATATAKE_PRODUCT_TYPES:
            return

        datatake_document_that_match = []

        if self.product_type[-2:] != "DS":
            datatake_document_that_match = find_datatake_from_product_group_id(
                mission=self.mission,
                satellite=self.satellite_unit,
                product_group_id=self.product_group_id,
            )

        #! For GR and TL/TC we need to be careful of MP shift and only trust product_group_id
        if len(datatake_document_that_match) == 0 and self.product_type[-2:] == "DS":

            datatake_document_that_match = find_datatake_from_sensing(
                start_date=self.sensing_start_date,
                end_date=self.sensing_end_date,
                mission=self.mission,
                satellite=self.satellite_unit,
            )

            # `find_datatake_from_sensing` already ranks the candidates by the
            # distance of the product middle to the datatake window (0 when the
            # middle falls inside the window) and applies the S2C +30s shift
            # consistently. We must NOT re-sort here with a divergent heuristic /
            # shift, otherwise a product whose middle sits inside a long datatake
            # gets stolen by an adjacent datatake whose edge happens to be closer.
            # We only keep the duration guard, which preserves the incoming order.
            product_duration = (
                self.sensing_end_date - self.sensing_start_date
            ).total_seconds()

            # Filter out datatakes with duration lower than product duration (tolerance of 6 sec)
            datatake_document_that_match = [
                dt
                for dt in datatake_document_that_match
                if (
                    dt.observation_time_stop - dt.observation_time_start
                ).total_seconds()
                >= (product_duration - 6)
            ]

        nb_datatake_document_that_match = len(datatake_document_that_match)

        # Already hard to know if the algo match the right one
        if nb_datatake_document_that_match > 1:
            LOGGER.warning(
                "[%s] - Product match with %s datatake document",
                self.key,
                nb_datatake_document_that_match,
            )

        if nb_datatake_document_that_match == 0:
            LOGGER.warning(
                "[%s] - Product can't match with datatake document", self.key
            )
            product_datatake_id = utils.DATATAKE_ID_MISSING_VALUE
        else:
            product_datatake_id = datatake_document_that_match[0].datatake_id

        setattr(
            self, "nb_datatake_document_that_match", nb_datatake_document_that_match
        )
        setattr(self, "datatake_id", product_datatake_id)

        return product_datatake_id

    def get_compute_key(self):
        if self.product_type[-2:] not in ["GR", "TL", "TC", "DS"]:
            LOGGER.debug("Compute Key -> wrong product_type : %s", self.product_type)
            return None

        if self.get_datatake_id() is None:
            LOGGER.debug("Compute Key -> no datatake_id : %s", self.datatake_id)
            return None

        return (self.get_datatake_id(), self.product_type)

    def search_expected_tiles(self):
        results = (
            CdsProductS2.search()
            .filter("term", mission=self.mission)
            .filter("term", satellite_unit=self.satellite_unit)
            .filter("range", sensing_start_date={"gte": self.sensing_start_date})
            .filter("range", sensing_end_date={"lte": self.sensing_end_date})
            .filter("exists", field="expected_tiles")
            .execute()
        )

        if len(results) == 0:
            LOGGER.warning(
                "[%s] - No DS Found products with expected_tiles, expected at lease one",
                self.key,
            )

            return []
        elif len(results) > 1:
            LOGGER.warning(
                "[%s] - Found %s products with expected_tiles, expected only one",
                self.key,
                len(results),
            )

        return results[0].expected_tiles
