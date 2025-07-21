"""Update entities after some datatake creation or update"""

from datetime import UTC, datetime
import maas_model
from maas_engine.engine.base import EngineReport
from maas_engine.engine.rawdata import DataEngine


class ComputeDatatakeRelatedEngine(DataEngine):
    """Update documents related to datatake creation or update"""

    ENGINE_ID = "COMPUTE_DATATAKE_RELATED"

    def __init__(
        self, args=None, target_model: str = None, send_reports=True, chunk_size=0
    ):
        """constructor

        Args:
            args (namespace, optional): cli options. Defaults to None.
            target_model (str, optional): Model class name. Defaults to None.
            send_reports (bool, optional): flag. Defaults to True.
        """

        super().__init__(args, send_reports=send_reports, chunk_size=chunk_size)

        self.target_model = target_model

    def action_iterator(self):
        """override

        Yields:
            Iterator[typing.Generator]: bulk actions
        """

        target_class = self.get_model(self.target_model)

        for datatake in self.input_documents:

            # store identifier of future entities to later filter out messages
            if datatake.observation_time_start > datetime.now(tz=UTC):
                self.logger.debug(
                    "[%s] - Skipped : cause this one are planned in the futur"
                )
                continue

            search_request = (
                target_class.search()
                .query(datatake.get_related_documents_query())
                .params(ignore=404, version=True, seq_no_primary_term=True)
            )

            for document in search_request.scan():
                initial_dict = document.to_dict()

                if datatake.timeliness:
                    document.timeliness = datatake.timeliness

                document.absolute_orbit = datatake.absolute_orbit

                document.instrument_mode = datatake.instrument_mode

                document.datatake_id = datatake.datatake_id
                if document.mission == "S1":
                    document.hex_datatake_id = (
                        hex(int(datatake.datatake_id, 10)).replace("0x", "").upper()
                    )

                if initial_dict | document.to_dict() != initial_dict:
                    yield document.to_bulk_action()
