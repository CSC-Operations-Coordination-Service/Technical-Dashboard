"""Custom CDS model definition for s2 product"""

import logging

from maas_cds.lib.queryutils.find_datatake_from_sensing import (
    find_datatake_from_sensing,
)
from maas_cds.lib.queryutils.find_datatake_from_product_group_id import (
    find_datatake_from_product_group_id,
)
from maas_cds.model.product import CdsProduct
from datetime import timedelta
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

            # Filter out datatakes that already have a product_group_id and
            # order by nearest sensing duration, filtering out those with duration lower than product
            filtered_datatakes = []
            product_duration = (
                self.sensing_end_date - self.sensing_start_date
            ).total_seconds()

            for dt in datatake_document_that_match:
                # Skip datatakes that already have product_group_ids
                if (
                    hasattr(dt, "product_group_ids")
                    and dt.product_group_ids is not None
                ):
                    continue

                # Calculate datatake duration
                datatake_duration = (
                    dt.observation_time_stop - dt.observation_time_start
                ).total_seconds()

                # Filter out datatakes with duration lower than product duration (tolerance of 11 sec)
                if datatake_duration >= (product_duration - 6):
                    filtered_datatakes.append(dt)
            # Sort by nearest datatake (by middle point distance to product middle)
            product_middle = (
                self.sensing_start_date
                + (self.sensing_end_date - self.sensing_start_date) / 2
            )

            # For S2C, adjust product middle by 10 seconds to handle timing differences
            if self.satellite_unit == "S2C":
                product_middle = product_middle + timedelta(seconds=20)

            # This can be improve using nb ds expected and also the datastrips_groups
            datatake_document_that_match = sorted(
                filtered_datatakes,
                key=lambda dt: min(
                    abs((dt.observation_time_start - product_middle).total_seconds()),
                    abs((dt.observation_time_stop - product_middle).total_seconds()),
                ),
            )

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
