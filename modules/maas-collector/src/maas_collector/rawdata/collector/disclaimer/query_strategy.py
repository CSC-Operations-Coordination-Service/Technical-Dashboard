"""Base class for SAR-MPC Quality Disclaimer query implementations"""
import datetime
import typing

from maas_collector.rawdata.collector.http.abstract_query_strategy import (
    AbstractHttpQueryStrategy,
)
from maas_collector.rawdata.collector.httpmixin import HttpMixin
from maas_collector.rawdata.collector.journal import (
    CollectorJournal,
    CollectorReplayJournal,
)


class AbstractDisclaimerQueryStrategy(AbstractHttpQueryStrategy):
    """Base class for Quality Disclaimer query implementation.

    Runs the generic HTTP query initialisation first, then stores the
    disclaimer-specific configuration on the instance for the concrete
    implementation to use.
    """

    FILE_NAME_PATTERN = "Disclaimer_{disclaimer_id}.json"

    def __init__(
        self,
        collector: "DisclaimerCollector",
        config: "DisclaimerCollectorConfiguration",
        http_session: HttpMixin,
        start_date: datetime.datetime,
        end_date_without_offset: datetime.datetime,
        journal: typing.Union[CollectorJournal, CollectorReplayJournal],
    ):
        super().__init__(
            collector,
            config,
            http_session,
            start_date,
            end_date_without_offset,
            journal,
        )

        self.listing_path = config.listing_path
        self.page_limit = config.page_limit
        self.stop_on_seen = config.stop_on_seen
        self.disclaimer_ids = config.disclaimer_ids
        self.keep_pdf = config.keep_pdf

        # id of the disclaimer currently being yielded, used by get_filename
        self._current_id: typing.Optional[int] = None

    def get_filename(self, page: int) -> str:
        """Build the temporary file name for the disclaimer being yielded.

        Args:
            page (int): running index provided by the collector (unused, the
                disclaimer id is a more meaningful name)

        Returns:
            str: generated filename
        """
        return self.FILE_NAME_PATTERN.format(disclaimer_id=self._current_id)

    def __iter__(self):
        raise NotImplementedError()
