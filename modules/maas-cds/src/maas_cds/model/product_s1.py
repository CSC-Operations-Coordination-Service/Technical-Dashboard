"""Custom CDS model definition for s1 product"""

from datetime import timedelta
import logging

from maas_cds.lib.parsing_name import utils
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

                start_date = self.sensing_end_date + timedelta(
                    seconds=CdsDatatakeS1.MATCHING_DELTA_PRODUCTS
                )
                end_date = self.sensing_end_date - timedelta(
                    seconds=CdsDatatakeS1.MATCHING_DELTA_PRODUCTS
                )

                ai_filters = (
                    [
                        Q("term", satellite_unit=self.satellite_unit),
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

                if (
                    self.timeliness is not None
                    and self.timeliness != utils.TIMELINESS_NULL_VALUE
                ):
                    ai_filters.append(
                        Q("term", timeliness=self.timeliness),
                    )

                search = (
                    CdsDatatakeS1.search()
                    .filter(Q("bool", filter=ai_filters))
                    .filter("term", instrument_mode="AIS")
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

                datatake_doc.sort(
                    key=lambda d: (
                        min(self.sensing_end_date, d.observation_time_stop)
                        - max(self.sensing_start_date, d.observation_time_start)
                    ).total_seconds(),
                    reverse=True,
                )

                datatake_doc = datatake_doc[0]

                setattr(self, "datatake_id", datatake_doc.datatake_id)
                setattr(self, "timeliness", datatake_doc.timeliness)

            else:
                LOGGER.warning("No datatake for product %s", self.name)
                return None
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
