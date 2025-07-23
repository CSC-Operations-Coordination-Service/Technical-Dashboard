"""Custom consolidated acquisition pass status"""

from datetime import timedelta, datetime
from opensearchpy import Q, Keyword

from maas_cds.model import generated
from maas_cds.model.anomaly_mixin import AnomalyMixin
from maas_cds.model.timeliness_mixin import TimelinessCalculationMixin
from maas_cds.model.bitrate_mixin import BitrateCalculationMixin

__all__ = [
    "CdsAcquisitionPassStatus",
    "CdsCadipAcquisitionPassStatus",
    "CdsEdrsAcquisitionPassStatus",
]


class CdsAcquisitionPassStatus(
    generated.CdsAcquisitionPassStatus,
    AnomalyMixin,
    TimelinessCalculationMixin,
    BitrateCalculationMixin,
):
    """overide to add cams_tickets as a multi keyword"""

    cams_tickets = Keyword(multi=True)

    _TIMELINESS_START_FIELD = "first_frame_start"
    _TIMELINESS_END_FIELD = "stop_delivery"

    _BITRATE_VOLUME = "overall_data_volume"
    _BITRATE_DURATION = "from_acq_delivery_timeliness"


class CdsCadipAcquisitionPassStatus(
    generated.CdsCadipAcquisitionPassStatus,
    AnomalyMixin,
    TimelinessCalculationMixin,
    BitrateCalculationMixin,
):
    """overide to add cams_tickets as a multi keyword"""

    cams_tickets = Keyword(multi=True)

    _TIMELINESS_START_FIELD = "downlink_start"
    _TIMELINESS_END_FIELD = "delivery_stop"

    _BITRATE_VOLUME = "TotalVolume"
    _BITRATE_DURATION = "from_acq_delivery_timeliness"

    def get_status(self):
        return self.global_status

    def search_acquistion_completeness_document(self):
        """Return the search method to find the associated completeness document for CADIP

        Returns:
            Search: The search query
        """
        session_id = self.session_id

        # The session_id coming from the CADIP is sliglthy different than the one in the MP
        # session_id ie S1A_20250529221710059415
        datetime_str = session_id[4:18]  # e.g., '20250529221710'
        datetime_format = "%Y%m%d%H%M%S"
        session_datetime = datetime.strptime(datetime_str, datetime_format)

        # TODO add this magic number in configuration
        lower_bound_datetime = session_datetime - timedelta(seconds=5)
        upper_bound_datetime = session_datetime + timedelta(seconds=5)

        # Create a range query
        lower_bound_str = lower_bound_datetime.strftime(datetime_format)
        upper_bound_str = upper_bound_datetime.strftime(datetime_format)

        # Construct the new session_id bounds
        lower_bound = f"{session_id[:4]}{lower_bound_str}{session_id[18:]}"
        upper_bound = f"{session_id[:4]}{upper_bound_str}{session_id[18:]}"

        range_query = Q("range", session_id={"gte": lower_bound, "lte": upper_bound})

        search = (
            generated.CdsHktmAcquisitionCompleteness.search()
            .filter("term", downlink_orbit=session_id[18:])
            .query(range_query)
        )

        return search


class CdsEdrsAcquisitionPassStatus(
    generated.CdsEdrsAcquisitionPassStatus, AnomalyMixin
):
    """overide to add cams_tickets as a multi keyword"""

    cams_tickets = Keyword(multi=True)

    def get_status(self):
        return self.status

    def search_acquistion_completeness_document(self):
        """Return the search method to find the associated completeness document for EDRS

        Returns:
            Search: The search query
        """

        search = generated.CdsHktmAcquisitionCompleteness.search().filter(
            "term", session_id=self.link_session_id
        )

        return search
