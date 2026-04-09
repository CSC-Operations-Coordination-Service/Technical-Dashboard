"""S3P Session consolidation"""

from maas_engine.engine import DataEngine


import maas_cds.model as model


class S3pSessionConsolidatorEngine(DataEngine):
    """Consolidate raw metrics to S3pSession"""

    ENGINE_ID = "CONSOLIDATE_S3P_SESSION"

    CONSOLIDATED_MODEL = model.S3pSession

    def __init__(
        self,
        args=None,
        raw_data_type=None,
        chunk_size=None,
        send_reports=True,
    ):
        super().__init__(args, chunk_size=chunk_size, send_reports=send_reports)

        self.raw_data_type = raw_data_type

        self.local_session_cache = {}

    def action_iterator(self):
        """override

        Yields:
            Iterator[typing.Generator]: bulk actions
        """

        for s3p_metrics_doc in self.input_documents:
            session_name = s3p_metrics_doc.s3p_session_name

            if session_name is None:
                self.logger.debug(
                    "Skip the %s, as there is no session we skip the document",
                    s3p_metrics_doc,
                )
                continue

            # Retrieve session_name to store it into cache
            session = self.local_session_cache.get(session_name)
            if session is None:
                session = model.S3pSession.get_by_id(session_name)

                if session is None:
                    session = model.S3pSession.from_session_name(session_name)

                self.local_session_cache[session_name] = session

            if session is None:
                self.logger.warning(
                    "Not able to find the session with %s - %s",
                    session_name,
                    s3p_metrics_doc,
                )
                continue

            # Consolidate from the appropriate way
            if self.raw_data_type == "S3pMetricsCirculationAgent":
                self.consolidate_from_S3pMetricsCirculationAgent(
                    s3p_metrics_doc, session
                )
            elif self.raw_data_type == "S3pMetricsRestCaduPollingAgent":
                self.consolidate_from_S3pMetricsRestCaduPollingAgent(
                    s3p_metrics_doc, session
                )
            elif self.raw_data_type == "S3pMetricsThinLayer":
                self.consolidate_from_S3pMetricsThinLayer(s3p_metrics_doc, session)
            else:
                self.logger.warning(
                    "Not able to consolidate data with raw_data_type: %s",
                    self.raw_data_type,
                )

    # consolidate_from_ModelClass
    # pylint: disable=C0103
    def consolidate_from_S3pMetricsCirculationAgent(
        self, raw_document: model.S3pMetricsCirculationAgent, document: model.S3pSession
    ) -> model.S3pSession:

        # hkraw delivery time  - the logdate When the to_url will match   à It can be fond in the log “M&C|Data Circulation|DC|OUT|”, for the moment this is not linked to a timelinesskey using the TL|OUT message, nevertheless it contains the downlink orbit number in the filename, e.g.  the HKRAW for downlink session SVL__DCS_03_S3A_20260402064724052724_dat is S3A_OPER__HK__RAW___20260402T064733_20260402T065339_O52724_0001.TGZ and its delivery time is in the log “M&C|Data Circulation|DC|OUT|” with tourl containing “eumetsat.int”:
        # Apr  2 06:56:50 s3p-s3a-pf-acq-01 CirculationAgent[808464]: M&C|Data Circulation|DC|OUT|filename="S3A_OPER__HK__RAW___20260402T064733_20260402T065339_O52724_0001.TGZ"|queueid=102978|tourl="sftp://s3cgs@vids.eumetsat.int/out/toEUMFOS/S3A/S3A_OPER__HK__RAW___20260402T064733_20260402T065339_O52724_0001.TGZ"|filesize=3500070|

        if "OPER__HK__RAW" in raw_document.filename:
            if document is not None and document.hkraw_name != raw_document.filename:
                self.logger.warning("We are overriding the exisiting hkraw information")

            document.hkraw_name = raw_document.filename
            document.hkraw_size = raw_document.filesize
            document.hkraw_delivery_time = raw_document.log_date

        elif "_G_" in self.filename:
            for granule in document.l0pp_granules:
                if granule.product_name == raw_document.filename:
                    granule.delivery_date_to_eum = raw_document.log_date
                    break
        else:
            self.logger.warning(
                "Not the place to be, there is a mismatch between session_name matching and this function"
            )
        return document

    # consolidate_from_ModelClass
    # pylint: disable=C0103
    def consolidate_from_S3pMetricsRestCaduPollingAgent(
        self,
        raw_document: model.S3pMetricsRestCaduPollingAgent,
        document: model.S3pSession,
    ) -> model.S3pSession:

        if self.domain == "Data Import":
            document.acquisition_start_time = raw_document.creationtime

        elif self.domain == "Timeliness":
            document.acquisition_stop_time = raw_document.eventtime
            document.timeliness_key = raw_document.timelinessKey
        else:
            self.logger.warning(
                "Not the place to be, there is a mismatch between session_name matching and this function"
            )
        return document

    # consolidate_from_ModelClass
    # pylint: disable=C0103
    def consolidate_from_S3pMetricsThinLayer(
        self, raw_document: model.S3pMetricsThinLayer, document: model.S3pSession
    ) -> model.S3pSession:

        #   It is the time of delivery to EUM of the last L0PP granule of a given downlink session, it can be found in the log “M&C|Data Circulation|DC|OUT|” with totoUrl containing “to_MRN”:
        # Apr  2 06:57:13 s3p-s3a-pf-acq-01 ThinLayer[1044962]: M&C|Timeliness|TL|OUT|eventtime="2026-04-02T06:57:13"|eventname="LOPP"|check="OK"|timelinessKey="SVL__DCS_03_S3A_20260402064724052724_dat"|filename="S3A_TM_0_NAT__G_20260402T050553_20260402T064744_20260402T064923_6111______________SVL_O_NR_OPE.ISIP"|pmode="N"|validitystart="2026-04-02T05:05:53.000000"|validitystop="2026-04-02T06:47:44.000000"|generationtime="2026-04-02T06:47:44.000000"|env="N"|ptype="0"|level="0"|sat="S3A"|message=""|reftime="ground"|

        # check if this GR is already
        if document.l0pp_granules is None:
            document.l0pp_granules = []

        for granule in document.l0pp_granules:

            if granule.product_name == raw_document.filename:
                self.logger.warning("This l0pp_granules is already registred")
                break
        else:
            document.l0pp_granules.append({"product_name": raw_document.filename})

        return document
