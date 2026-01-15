"""Custom CDS model definition for cds completeness splitted for S5"""

import logging
import re
import typing


from opensearchpy import Keyword
from maas_cds.model import generated
from maas_cds.model.product_s5 import CdsProductS5


from maas_cds.lib.periodutils import (
    compute_total_sensing_product,
    compute_total_sensing_period,
    Period,
)


from maas_cds.model.cds_completeness.cds_completeness_splitted import (
    CdsCompletenessSplitted,
)

__all__ = ["CdsCompletenessSplittedS5"]

LOGGER = logging.getLogger("CdsCompletenessSplittedS5")


class CdsCompletenessSplittedS5(CdsCompletenessSplitted):
    """Document handling cds S5 completeness"""

    MISSION = "S5"

    DATATAKE_ID_REGEX_FORMAT = r"S5[A-Z]-\d\d\d\d\d"

    def find_brother_products_scan(self):
        """Specific method to query productsfor S5 Completeness

        Returns:
            Generator: Publication of implied product
        """
        search_iter = (
            generated.CdsPublication.search()
            .filter("term", satellite_unit=self.satellite_unit)
            .filter("term", datatake_id=self.datatake_id)
            .filter("term", timeliness=self.timeliness)
            .filter("term", product_type=self.product_type)
            .filter("term", service_type=self.service_type)
            .filter("term", service_id=self.service_id)
            .params(ignore=404)
            .scan()
        )

        return search_iter

    def is_compute_key_to_check_missing_orbit(self):
        """Frame method to specify the check if the product launch a
        missing orbit check/generation

        Returns:
            bool: True if this product enable a check
        """
        if self.product_type == "L1B_RA_BD1" and self.timeliness == "OFFL":
            return True
        return False

    @classmethod
    def generate_datatake_ids_list_between_2_ids(
        cls, datatake_ref_1: str, datatake_ref_2: str
    ) -> typing.List[str]:
        """Function which return a list of all S3 datatakes_id string which are
        between 2 S3 datatake_ids given as arguments

        Args:
            datatake_ref_1 (str): 1st datatake_id reference
            datatake_ref_2 (str): 2nd datatake_id reference

        Raises:
            ValueError: ValueError raised if datatake_ids does not respect the expected format

        Returns:
            typing.List[str]: The list of datatake_ids between the 2 references
        """
        datatake_list = []

        if not re.search(cls.DATATAKE_ID_REGEX_FORMAT, datatake_ref_1) or not re.search(
            cls.DATATAKE_ID_REGEX_FORMAT, datatake_ref_2
        ):
            raise ValueError("Inputs arguments does not respect the expected format")

        if datatake_ref_1 == datatake_ref_2:
            return []
        minref, maxref = cls.sort_datatake_id(datatake_ref_1, datatake_ref_2)

        LOGGER.debug("Generate missing datatake between %s and %s", minref, maxref)

        while True:

            satellite, absolute_orbit = minref.split("-")
            absolute_orbit = int(absolute_orbit)

            absolute_orbit += 1
            minref = f"{satellite}-{absolute_orbit:05}"
            if minref == maxref:
                break

            LOGGER.debug("- Add  missing %s", minref)
            datatake_list.append(minref)
        return datatake_list

    @classmethod
    def sort_datatake_id(
        cls, datatake_id_1: str, datatake_id_2: str
    ) -> typing.Tuple[str, str]:
        """This function sort 2 datatake ids in ascending order

        Args:
            datatake_id_1 (str): datatake_id string nb1
            datatake_id_2 (str): datatake_id string nb2

        Raises:
            ValueError: ValueError raised if datatake_id does not respect the expected format

        Returns:
            Tuple[str, str]: The 2 datatake_ids string sorted in ascending order in a tuple
        """
        if not re.search(cls.DATATAKE_ID_REGEX_FORMAT, datatake_id_1) or not re.search(
            cls.DATATAKE_ID_REGEX_FORMAT, datatake_id_2
        ):
            raise ValueError("Inputs arguments does not respect the expected format")

        # Remove satellite part
        ref_part_1 = datatake_id_1[4:]
        ref_part_2 = datatake_id_2[4:]

        # Cycle number contains 385 cycle so it's fine to mulitple by 1000 to sort them
        val1 = int(ref_part_1)
        val2 = int(ref_part_2)
        return (
            (datatake_id_1, datatake_id_2)
            if val2 >= val1
            else (datatake_id_2, datatake_id_1)
        )
