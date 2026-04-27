"""Custom CDS model definition"""

import logging

from maas_cds.model import generated
from maas_model.date_utils import (
    datestr_to_utc_datetime,
)
from opensearchpy import Keyword

__all__ = [
    "S3pSession",
    "S3pMetricsThinLayer",
    "S3pMetricsCirculationAgent",
    "S3pMetricsRestCaduPollingAgent",
]


LOGGER = logging.getLogger("S3pSession")


class S3pMetricsCirculationAgent(generated.S3pMetricsCirculationAgent):
    @property
    def s3p_session_name(self) -> str:
        # HK CASE
        if (
            self.code == "DC"
            and self.action == "OUT"
            and "OPER__HK__RAW" in self.filename
            and "eumetsat.int" in self.tourl
        ):
            # S3A_OPER__HK__RAW___20260316T105033_20260316T105636_O52484_0001.TGZ
            orbit = self.filename.split("_O")[2].split("_")[0]

            # Here find the s3p session using the orbit
            rest_cadu_doc = (
                generated.S3pSession.search()
                .filter("term", downlink_orbit=orbit.zfill(6))
                .execute()
            )

            if len(rest_cadu_doc) == 0:
                return None

            return rest_cadu_doc[0].downlink_session

        # GR Case
        if (
            self.code == "DC"
            and self.action == "OUT"
            and "_G_" in self.filename
            and "to_MRN" in self.tourl
        ):
            # Here find the s3p session using the filename with the thinlayer
            thinlayer_doc = (
                S3pMetricsThinLayer.search()
                .filter("term", filename=self.filename)
                .execute()
            )
            if len(thinlayer_doc) == 0:
                return None

            return thinlayer_doc[0].timelinessKey[12:-4]

        if (
            self.domain == "Data Circulation"
            and self.code == "DC"
            and self.action in ("OUT", "IN")
            and "DSIB.xml" in self.filename
        ):
            return self.filename[7:31]


class S3pMetricsRestCaduPollingAgent(generated.S3pMetricsRestCaduPollingAgent):
    @property
    def s3p_session_name(self) -> str:
        # Start CASE
        if (
            self.domain == "Data Import"
            and self.code == "IMP"
            and self.action == "IN"
            and self.filename
        ):
            return self.filename

        # Stop Case
        elif (
            self.domain == "Timeliness"
            and self.code == "TL"
            and self.action == "REF"
            and self.timelinessKey
            and self.eventtime
        ):
            return self.timelinessKey[12:-4]

        else:
            # Match nothing
            return None


class S3pMetricsThinLayer(generated.S3pMetricsThinLayer):
    @property
    def s3p_session_name(self) -> str:
        #  It is the time of delivery to EUM of the last L0PP granule of a given downlink session, it can be found in the log “M&C|Data Circulation|DC|OUT|” with totoUrl containing “to_MRN”:
        # Currently the filter is made at the collect level

        # Here find the s3p session using the timelinessKey
        return self.timelinessKey[12:-4]


class S3pSession(generated.S3pSession):
    """

    Override to store business logic
    """

    l0pp_granules = Keyword(multi=True)

    cadu_files = Keyword(multi=True)

    @classmethod
    def from_session_name(cls, session_name: str) -> "S3pSession":
        """Create a new instance from a session name"""

        document = cls()
        document.meta.id = session_name
        document.downlink_session = session_name
        document.satellite_id = session_name[:3]
        document.downlink_orbit = session_name[18:]
        return document

    def compute_kpi(self):

        # self.last_cadu_chunk_delivery = max(
        #     (f.cadu_delivery_out for f in self.cadu_files), default=None
        # )

        if isinstance(self.acquisition_stop_time, str):
            self.acquisition_stop_time = datestr_to_utc_datetime(
                self.acquisition_stop_time
            )

        latest_gr_published_to_eum = max(
            (
                f.delivery_date_to_eum
                for f in self.l0pp_granules
                if hasattr(f, "delivery_date_to_eum") and f.delivery_date_to_eum
            ),
            default=None,
        )
        if latest_gr_published_to_eum and isinstance(latest_gr_published_to_eum, str):

            latest_gr_published_to_eum = datestr_to_utc_datetime(
                latest_gr_published_to_eum
            )

        if self.l0pp_granules:

            # GR Completeness
            gr_delivered = [
                f.delivery_date_to_eum
                for f in self.l0pp_granules
                if hasattr(f, "delivery_date_to_eum") and f.delivery_date_to_eum
            ]
            self.delivery_to_eum_completeness = len(gr_delivered) / len(
                self.l0pp_granules
            )
        else:
            LOGGER.debug("No gr set the completeness to 0")
            self.delivery_to_eum_completeness = 0

        if latest_gr_published_to_eum and self.acquisition_stop_time:
            self.delivery_to_eum_timeliness = (
                latest_gr_published_to_eum - self.acquisition_stop_time
            ).total_seconds()
        else:

            LOGGER.debug(
                "Missing information can't set timeliness: stop  %s  latest %s",
                self.acquisition_stop_time,
                latest_gr_published_to_eum,
            )
