"""Custom CDS model definition for s1 product"""

from datetime import timedelta
import logging

from maas_cds.model.product import CdsProduct, DynamicPartitionMixin
from maas_cds.model.datatake_s1 import CdsDatatakeS1
from opensearchpy import Q

__all__ = ["CdsProductS1"]


LOGGER = logging.getLogger("CdsModelProductS1")


class CdsProductS1(CdsProduct):
    """CdsProduct specific for sentinel 1"""

    def get_compute_key(self):
        """override specific method for sentinel 1

        Returns:
            tuple: a tuple as key allowing us to group product computation
        """

        # We match all product between observation ± delta in seconds

        # Corner case
        if CdsDatatakeS1.is_product_type_without_datatake_id(self.product_type):
            if self.product_type == "AI_RAW__0_":
                search = (
                    CdsDatatakeS1.search()
                    .filter(
                        Q(
                            "bool",
                            filter=[
                                Q("term", satellite_unit=self.satellite_unit),
                                Q(
                                    "range",
                                    observation_time_start={
                                        "lte": self.sensing_start_date
                                    },
                                ),
                                Q(
                                    "range",
                                    observation_time_stop={
                                        "gte": self.sensing_end_date
                                    },
                                ),
                            ],
                        )
                    )
                    .filter("term", instrument_mode="AIS")
                    .filter("term", absolute_orbit=self.absolute_orbit)
                )
            if "ERRMAT" in self.product_type:
                start_date = self.sensing_end_date + timedelta(
                    seconds=CdsDatatakeS1.MATCHING_DELTA_PRODUCTS
                )
                end_date = self.sensing_end_date - timedelta(
                    seconds=CdsDatatakeS1.MATCHING_DELTA_PRODUCTS
                )
                search = (
                    CdsDatatakeS1.search()
                    .filter(
                        Q(
                            "bool",
                            filter=[
                                Q(
                                    "range",
                                    observation_time_start={"lte": start_date},
                                ),
                                Q(
                                    "range",
                                    observation_time_stop={"gte": end_date},
                                ),
                            ],
                        )
                    )
                    .filter("term", satellite_unit=self.satellite_unit)
                    .filter("term", instrument_mode="RFC")
                    .filter("term", polarization=f"D{self.product_type[2]}")
                )

            datatake_doc = list(search.execute())
            if datatake_doc:
                if len(datatake_doc) > 1:
                    LOGGER.warning("Too much datatake for product %s", self.name)
                datatake_doc = datatake_doc[0]
            else:
                LOGGER.warning("No datatake for product %s", self.name)

            return (datatake_doc.meta.id, self.product_type)

        # Protective behaviour
        # This is based on dataflow
        if (
            not self.get_datatake_id()
            and self.product_level
            not in DynamicPartitionMixin.PRODUCT_LEVEL_THAT_MAKE_SENSE
            or self.instrument_mode
            not in (
                "SM",
                "IW",
                "EW",
                "WV",
                "RFC",
                "ZI",
                "ZE",
                "ZW",
                "AN",
                "ZS",
                "AI",
            )
            or self.product_type in CdsDatatakeS1.EXCLUDES_PRODUCTED_TYPES
        ):
            return None

        return (self.get_datatake_id(), self.product_type)
