"""Custom CDS model definition"""

from maas_cds.model import generated

__all__ = [
    "S3pSession",
    "S3pMetricsThinLayer",
    "S3pMetricsCirculationAgent",
    "S3pMetricsRestCaduPollingAgent",
]


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

            orbit = self.filename.split("_O")[1].split("_")[0]
            # Here find the s3p session using the orbit
            rest_cadu_doc = (
                generated.S3pSession.search()
                .filter("term", downlink_orbit={orbit})
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


class S3pMetricsRestCaduPollingAgent(generated.S3pMetricsRestCaduPollingAgent):
    @property
    def s3p_session_name(self) -> str:
        # Start CASE
        if self.domain == "Data Import" and self.code == "IMP" and self.action == "IN":
            return self.filename

        # Stop Case
        elif self.domain == "Timeliness" and self.code == "TL" and self.action == "REF":
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

    @classmethod
    def from_session_name(cls, session_name: str) -> "S3pSession":
        """Create a new instance from a session name"""

        document = cls()
        document.meta.id = session_name
        document.downlink_session = session_name
        document.satellite_id = session_name[:3]
        document.downlink_orbit = session_name[18:]
