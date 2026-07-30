# pylint: skip-file
"""
DA0 classes generated from index templates.

**DO NOT EDIT, ONLY INHERIT !**

Generated date: 2026-07-30T14:33:50.420499+00:00

Generated from:
    - resources/templates/cds-acquisition-pass-status_template.json
    - resources/templates/cds-ai-production-completeness_template.json
    - resources/templates/cds-anomaly-correlation_template.json
    - resources/templates/cds-cadip-acquisition-pass-status_template.json
    - resources/templates/cds-cams-tickets_template.json
    - resources/templates/cds-completeness-splitted_template.json
    - resources/templates/cds-completeness_template.json
    - resources/templates/cds-databudget_template.json
    - resources/templates/cds-dataflow_template.json
    - resources/templates/cds-datatake_template.json
    - resources/templates/cds-ddp-data-available_template.json
    - resources/templates/cds-deletion-issue_template.json
    - resources/templates/cds-downlink-datatake_template.json
    - resources/templates/cds-edrs-acquisition-pass-status_template.json
    - resources/templates/cds-expected_template.json
    - resources/templates/cds-grafana-usage_template.json
    - resources/templates/cds-hktm-acquisition-completeness_template.json
    - resources/templates/cds-hktm-production-completeness_template.json
    - resources/templates/cds-interface-product-deletion_template.json
    - resources/templates/cds-interface-status_template.json
    - resources/templates/cds-lta-download-quota_template.json
    - resources/templates/cds-metrics-product_template.json
    - resources/templates/cds-product_template.json
    - resources/templates/cds-publication_template.json
    - resources/templates/cds-s2-tilpar_template.json
    - resources/templates/cds-s3-completeness_template.json
    - resources/templates/cds-s5-completeness_template.json
    - resources/templates/cds-sat-unavailability_template.json
    - resources/templates/maas-config-collector_template.json
    - resources/templates/maas-config-completeness-s3_template.json
    - resources/templates/maas-config-completeness-s5_template.json
    - resources/templates/maas-config-completeness_template.json
    - resources/templates/maas-config-dataflow_template.json
    - resources/templates/maas-config-mission_template.json
    - resources/templates/maas-config-satellite_template.json
    - resources/templates/maas-config-service_template.json
    - resources/templates/maas-config_template.json
    - resources/templates/raw-data-acq-passes-status-edrs_template.json
    - resources/templates/raw-data-app-product_template.json
    - resources/templates/raw-data-aps-edrs_template.json
    - resources/templates/raw-data-aps-file_template.json
    - resources/templates/raw-data-aps-per-pass_template.json
    - resources/templates/raw-data-aps-product_template.json
    - resources/templates/raw-data-aps-quality-info_template.json
    - resources/templates/raw-data-aps-session_template.json
    - resources/templates/raw-data-auxip-product_template.json
    - resources/templates/raw-data-cams-anomaly-correlation_template.json
    - resources/templates/raw-data-cams-cloud-anomaly-correlation_template.json
    - resources/templates/raw-data-cams-cloud-tickets_template.json
    - resources/templates/raw-data-cams-tickets_template.json
    - resources/templates/raw-data-creodias-product_template.json
    - resources/templates/raw-data-das-product_template.json
    - resources/templates/raw-data-databudget_template.json
    - resources/templates/raw-data-dd-archive_template.json
    - resources/templates/raw-data-dd-product_template.json
    - resources/templates/raw-data-ddp-data-available_template.json
    - resources/templates/raw-data-deletion-issue_template.json
    - resources/templates/raw-data-download-volume-count_template.json
    - resources/templates/raw-data-grafana-usage_template.json
    - resources/templates/raw-data-interface-probe_template.json
    - resources/templates/raw-data-lta-product_template.json
    - resources/templates/raw-data-metrics-product_template.json
    - resources/templates/raw-data-mp-all-product_template.json
    - resources/templates/raw-data-mp-hktm-acquisition-product_template.json
    - resources/templates/raw-data-mp-hktm-downlink_template.json
    - resources/templates/raw-data-mp-product_template.json
    - resources/templates/raw-data-mpcip-product_template.json
    - resources/templates/raw-data-mpip-product_template.json
    - resources/templates/raw-data-prip-product_template.json
    - resources/templates/raw-data-product-deletion_template.json
    - resources/templates/raw-data-s3p-metrics-circulation-agent_template.json
    - resources/templates/raw-data-s3p-metrics-rest-cadu-polling-agent_template.json
    - resources/templates/raw-data-s3p-metrics-thin-layer_template.json
    - resources/templates/raw-data-sat-unavailability-product_template.json
    - resources/templates/s3p-session_template.json
"""

from opensearchpy import (
    Boolean,
    Float,
    GeoShape,
    Integer,
    Keyword,
    Long,
    Object,
    Text,
    InnerDoc,
)

from maas_model import MAASDocument, MAASRawDocument, ZuluDate

__all__ = [
    "AcqPassesStatusEdrs",
    "AppProduct",
    "ApsEdrs",
    "ApsFile",
    "ApsPerPass",
    "ApsProduct",
    "ApsQualityInfo",
    "ApsSession",
    "ApsSessionQualityInfos",
    "AuxipProduct",
    "CamsAnomalyCorrelation",
    "CamsCloudAnomalyCorrelation",
    "CamsCloudTickets",
    "CamsTickets",
    "CdsAcquisitionPassStatus",
    "CdsAiProductionCompleteness",
    "CdsAnomalyCorrelation",
    "CdsCadipAcquisitionPassStatus",
    "CdsCadipAcquisitionPassStatusQualityInfos",
    "CdsCamsTickets",
    "CdsCompleteness",
    "CdsCompletenessMissingPeriods",
    "CdsCompletenessSplitted",
    "CdsDatabudget",
    "CdsDataflow",
    "CdsDatatake",
    "CdsDatatakeDuplicateds",
    "CdsDatatakeDuplicatedsDatastripPairs",
    "CdsDatatakeDuplicatedsDatastripPairsDatastrips",
    "CdsDatatakeDuplicatedsDatastripPairsDatastripsDeletions",
    "CdsDatatakeDuplicatedsDatastripPairsDatastripsProducts",
    "CdsDatatakeDuplicatedsDatastripPairsDatastripsProductsDeletions",
    "CdsDatatakeDuplicatedsDeletions",
    "CdsDatatakeDuplicatedsItems",
    "CdsDatatakeDuplicatedsItemsDeletedProduct",
    "CdsDatatakeMissingPeriods",
    "CdsDdpDataAvailable",
    "CdsDeletionIssue",
    "CdsDownlinkDatatake",
    "CdsEdrsAcquisitionPassStatus",
    "CdsExpected",
    "CdsGrafanaUsage",
    "CdsHktmAcquisitionCompleteness",
    "CdsHktmProductionCompleteness",
    "CdsInterfaceProductDeletion",
    "CdsInterfaceStatus",
    "CdsLtaDownloadQuota",
    "CdsMetricsProduct",
    "CdsProduct",
    "CdsPublication",
    "CdsS2Tilpar",
    "CdsS3Completeness",
    "CdsS5Completeness",
    "CdsSatUnavailability",
    "CreodiasProduct",
    "DasProduct",
    "Databudget",
    "DdArchive",
    "DdProduct",
    "DdpDataAvailable",
    "DeletionIssue",
    "DownloadVolumeCount",
    "GrafanaUsage",
    "InterfaceProbe",
    "LtaProduct",
    "MaasConfig",
    "MaasConfigCollector",
    "MaasConfigCompleteness",
    "MaasConfigCompletenessS3",
    "MaasConfigCompletenessS3Records",
    "MaasConfigCompletenessS5",
    "MaasConfigCompletenessS5Records",
    "MaasConfigDataflow",
    "MaasConfigDataflowMetadata",
    "MaasConfigDataflowRecords",
    "MaasConfigDataflowRecordsAuxip",
    "MaasConfigDataflowRecordsServicesConfig",
    "MaasConfigDataflowRecordsStb",
    "MaasConfigMission",
    "MaasConfigSatellite",
    "MaasConfigService",
    "MetricsProduct",
    "MpAllProduct",
    "MpHktmAcquisitionProduct",
    "MpHktmDownlink",
    "MpProduct",
    "MpcipProduct",
    "MpipProduct",
    "PripProduct",
    "ProductDeletion",
    "S3pMetricsCirculationAgent",
    "S3pMetricsRestCaduPollingAgent",
    "S3pMetricsThinLayer",
    "S3pSession",
    "S3pSessionCaduFiles",
    "S3pSessionL0PpGranules",
    "SatUnavailabilityProduct",
]


class AcqPassesStatusEdrs(MAASRawDocument):
    """
    Mapping class for index: raw-data-acq-passes-status-edrs

    Generated from: resources/templates/raw-data-acq-passes-status-edrs_template.json
    """

    class Index:
        "inner class for DSL"

        name = "raw-data-acq-passes-status-edrs"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("raw-data-acq-passes-status-edrs")

    creation_date = ZuluDate()

    """Creation date of the report"""

    dcsu_id = Keyword()

    """Identifier of the DCSU (data collection/storage unit) involved in the session"""

    description = Text()

    """Free-text description of the report"""

    direction = Keyword()

    """Direction of the acquisition pass"""

    duration = Keyword()

    """Duration of the acquisition session"""

    emergency_flag = Keyword()

    """Flag indicating whether the session was handled as an emergency"""

    execution_status = Keyword()

    """Execution status of the acquisition session"""

    file_class = Keyword()

    """File class of the source report"""

    file_name = Keyword()

    """File name of the source report"""

    file_type = Keyword()

    """File type of the source report"""

    geo_satellite_id = Keyword()

    """Identifier of the GEO (geostationary EDRS relay) satellite"""

    leo_satellite_id = Keyword()

    """Identifier of the LEO (low Earth orbit) satellite whose data is relayed"""

    link_session_completion_time = ZuluDate()

    """Completion time of the link session"""

    link_session_fer = Float()

    """Frame Error Rate of the link session"""

    notes = Text()

    """Additional free-text notes attached to the report"""

    number_of_delivered_cadu = Long()

    """Number of CADUs (Channel Access Data Units) delivered during the session"""

    number_of_missing_cadu = Long()

    """Number of CADUs (Channel Access Data Units) missing during the session"""

    priority = Keyword()

    """Priority assigned to the acquisition session"""

    production_service_name = Keyword()

    """Production service name providing the report"""

    production_service_type = Keyword()

    """Production service type providing the report"""

    reception_profile_id = Keyword()

    """Identifier of the reception profile used for the session"""

    reportFolder = Keyword()

    """Source folder or path where the report file was collected"""

    session_id_data = Keyword()

    """Identifier of the EDRS acquisition/data session"""

    source_creation_date = ZuluDate()

    """Creation date of the source report as declared by the producer"""

    source_creator = Keyword()

    """Identifier of the entity that created the source report"""

    source_creator_version = Keyword()

    """Version of the entity that created the source report"""

    source_system = Keyword()

    """System that produced the source report"""

    start_time = ZuluDate()

    """Start time of the acquisition session"""

    stop_time = ZuluDate()

    """Stop time of the acquisition session"""

    trans_mode = Keyword()

    """Transmission mode used for the session"""

    user_id = Keyword()

    """Identifier of the user associated with the acquisition session"""


class AppProduct(MAASRawDocument):
    """
    Mapping class for index: raw-data-app-product

    Generated from: resources/templates/raw-data-app-product_template.json
    """

    class Index:
        "inner class for DSL"

        name = "raw-data-app-product"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("raw-data-app-product")

    _PARTITION_FIELD = "ingestionTime"

    _PARTITION_FIELD_FORMAT = "static"

    acquisition_id = Keyword()

    """Identifier of the acquisition"""

    downlink_duration = Long()

    """Duration of the downlink"""

    downlink_orbit = Keyword()

    """Orbit number of the X-Band downlink"""

    downlink_start_date = ZuluDate()

    """Start date and time of the downlink"""

    downlink_stop_date = ZuluDate()

    """Stop date and time of the downlink"""

    interface_name = Keyword()

    """Name of the source interface providing the acquisition data"""

    production_service_name = Keyword()

    """Name of the production service that provided the record"""

    production_service_type = Keyword()

    """Type of the production service that provided the record"""

    reportFolder = Keyword()

    """Folder path of the source report file"""

    satellite_id = Keyword()

    """Identifier of the satellite for the acquisition pass"""

    station_id = Keyword()

    """Identifier of the ground/acquisition station"""


class ApsEdrs(MAASRawDocument):
    """
    Mapping class for index: raw-data-aps-edrs

    Generated from: resources/templates/raw-data-aps-edrs_template.json
    """

    class Index:
        "inner class for DSL"

        name = "raw-data-aps-edrs"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("raw-data-aps-edrs")

    _PARTITION_FIELD = "ingestionTime"

    _PARTITION_FIELD_FORMAT = "product"

    archived_data_size = Float()

    """Size of the archived data for the link session"""

    cadus = Long()

    """Number of CADUs disseminated for the link session"""

    dcsu_archive_status = Keyword()

    """DCSU archive status of the link session"""

    disseminated_data = Float()

    """Volume of data disseminated for the link session"""

    dissemination_start = ZuluDate()

    """Start time of data dissemination from the ground station"""

    dissemination_stop = ZuluDate()

    """Stop time of data dissemination from the ground station"""

    doy = Integer()

    """Day of year of the link session as reported in the EDRS report"""

    edte_acquisition_status = Keyword()

    """EDTE acquisition status of the link session"""

    fer = Float()

    """Frame Error Rate reported for the link session"""

    geo_satellite_id = Keyword()

    """Identifier of the geostationary EDRS relay satellite used for the link"""

    ground_station = Keyword()

    """Ground station that disseminated the acquired data"""

    interface_name = Keyword()

    """Name of the collector interface that produced this record, set to Jira_EDRS"""

    link_session_id = Keyword()

    """EDRS link session identifier from the LINK SESSIONS DETAILS column"""

    mission = Keyword()

    """Mission code derived from the first two characters of the satellite identifier"""

    moc_accept_status = Keyword()

    """MOC acceptance status of the link session"""

    notes = Keyword()

    """Free-text notes from the EDRS report"""

    planned_link_session_start = ZuluDate()

    """Planned start time of the EDRS link session, computed from the report base date and day of year"""

    planned_link_session_stop = ZuluDate()

    """Planned stop time of the EDRS link session, computed from the report base date and day of year"""

    production_service_name = Keyword()

    """Name of the production service that provided the report, set to EDRS-Operations"""

    production_service_type = Keyword()

    """Type of the production service that provided the report, set to EDRS"""

    reportFolder = Keyword()

    """Source folder or path where the report file was collected"""

    report_type = Keyword()

    """Reporting period derived from the report file name (daily for DOR, weekly for WOR, monthly for MOR)"""

    satellite_id = Keyword()

    """Identifier of the LEO satellite that performed the acquisition"""

    sfdap_dissem_status = Keyword()

    """SFDAP dissemination status of the link session"""

    spacecraft_execution = Keyword()

    """Spacecraft execution status of the link session"""

    total_status = Keyword()

    """Overall status of the link session"""

    uplink_status = Keyword()

    """Uplink status of the link session"""


class ApsFile(MAASRawDocument):
    """
    Mapping class for index: raw-data-aps-file

    Generated from: resources/templates/raw-data-aps-file_template.json
    """

    class Index:
        "inner class for DSL"

        name = "raw-data-aps-file"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("raw-data-aps-file")

    _PARTITION_FIELD = "ingestionTime"

    _PARTITION_FIELD_FORMAT = "static"

    block_number = Long()

    """Sequence block number of the file within the session (from BlockNumber)"""

    channel = Long()

    """Channel number the file was acquired on (from Channel)"""

    eviction_date = ZuluDate()

    """Date the file is scheduled to be evicted from the CADIP store (from EvictionDate)"""

    final_block = Boolean()

    """Whether this file is the final block of the transfer (from FinalBlock)"""

    interface_name = Keyword()

    """Name of the collector interface that produced this record (e.g. CADIP_<station>_Files)"""

    name = Keyword()

    """File name as published by the CADIP service (from Name)"""

    production_service_name = Keyword()

    """Name of the CADIP ground station service that provided the file"""

    production_service_type = Keyword()

    """Type of the production service that provided the file, set to CADIP"""

    publication_date = ZuluDate()

    """Date the file was published by the CADIP service (from PublicationDate)"""

    reportFolder = Keyword()

    """Source folder or path where the report file was collected"""

    retransfer = Boolean()

    """Whether the file was delivered as a retransfer (from Retransfer)"""

    session_id = Keyword()

    """CADIP acquisition session identifier the file belongs to (from SessionId)"""

    size = Long()

    """Size of the file in bytes (from Size)"""


class ApsPerPass(MAASRawDocument):
    """
    Mapping class for index: raw-data-aps-per-pass

    Generated from: resources/templates/raw-data-aps-per-pass_template.json
    """

    class Index:
        "inner class for DSL"

        name = "raw-data-aps-per-pass"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("raw-data-aps-per-pass")

    _PARTITION_FIELD = "ingestionTime"

    _PARTITION_FIELD_FORMAT = "static"

    acquisition_id = Keyword()

    """Acquisition identifier of the pass (StationDownlinkDetails/Acq_Id)"""

    antenna_id = Keyword()

    """Identifier of the antenna used for the downlink (StationDownlinkDetails/AntennaId)"""

    comments = Keyword()

    """Free-text comments from the station acquisition report (StationDownlinkDetails/Comments)"""

    downlink_end_time = ZuluDate()

    """End time of the downlink pass (StationDownlinkDetails/DownlinkEndTime)"""

    downlink_orbit = Keyword()

    """Orbit number during which the downlink occurred (Variable_Header/Downlink_Orbit)"""

    downlink_start_time = ZuluDate()

    """Start time of the downlink pass (StationDownlinkDetails/DownlinkStartTime)"""

    downlink_status = Keyword()

    """Status of the downlink pass (StationDownlinkDetails/DownlinkStatus)"""

    fer_data = Float()

    """Frame Error Rate reported for the data (FEP_Information/FER_Data)"""

    fer_downlink = Float()

    """Frame Error Rate reported for the downlink (FEP_Information/FER_Downlink)"""

    interface_name = Keyword()

    """Name of the collector interface that produced this record, set to AcqPassesStatusEDS"""

    mission = Keyword()

    """Mission code derived from the report Mission header (Earth_Explorer_Header/Fixed_Header/Mission)"""

    production_service_name = Keyword()

    """Name of the production service that provided the report, set to CGS"""

    production_service_type = Keyword()

    """Type of the production service that provided the report, set to EDS"""

    reportFolder = Keyword()

    """Source folder or path where the report file was collected"""

    satellite_id = Keyword()

    """Satellite identifier derived from the report Mission header (Earth_Explorer_Header/Fixed_Header/Mission)"""

    station_id = Keyword()

    """Ground station identifier of the acquisition (StationAcquisitionReport/StationId)"""


class ApsProduct(MAASRawDocument):
    """
    Mapping class for index: raw-data-aps-product

    Generated from: resources/templates/raw-data-aps-product_template.json
    """

    class Index:
        "inner class for DSL"

        name = "raw-data-aps-product"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("raw-data-aps-product")

    _PARTITION_FIELD = "ingestionTime"

    _PARTITION_FIELD_FORMAT = "static"

    antenna_id = Keyword()

    """Identifier of the antenna used for the pass (from the Antenna ID column)"""

    antenna_status = Keyword()

    """Operational status of the antenna for the pass (from the Antenna status column)"""

    delivery_push_status = Keyword()

    """Status of the delivery push for the pass (from the Delivery Push status column)"""

    downlink_orbit = Keyword()

    """Downlink orbit number of the pass (from the Downlink Orbit column)"""

    doy = Integer()

    """Day of year of the acquisition pass (from the DOY column)"""

    fer_data = Float()

    """Frame Error Rate for the acquired data (from the FER_Data column)"""

    fer_downlink = Float()

    """Frame Error Rate for the downlink (from the FER_Downlink column)"""

    first_frame_start = ZuluDate()

    """Time of the first acquired frame (from the First Frame start column)"""

    front_end_id = Keyword()

    """Identifier of the front-end equipment used for the pass (from the Front End ID column)"""

    front_end_status = Keyword()

    """Operational status of the front-end equipment (from the Front End status column)"""

    ground_station = Keyword()

    """Ground station identifier, set to a per-station constant (e.g. DLR, INS)"""

    interface_name = Keyword()

    """Interface that provided the product, set to a per-station constant (e.g. DDP_S5P-DLR_DAILY, DDP_INS-Inuvik)"""

    last_frame_stop = ZuluDate()

    """Time of the last acquired frame (from the Last Frame stop column)"""

    mission = Keyword()

    """Mission identifier, derived from the Satellite column and normalized to an S-prefixed mission code"""

    notes = Keyword()

    """Free-text notes about the pass (from the Notes column)"""

    number_of_chunks = Integer()

    """Number of chunks delivered for the pass (from the Number of chunks column)"""

    overall_data_volume = Long()

    """Overall data volume of the pass (from the Overall Data Volume column)"""

    overall_number_of_bad_data_acquired_frames = Long()

    """Total number of bad data-acquired frames (from the Overall Number of bad data acquired frames column)"""

    overall_number_of_bad_downlinked_frames = Long()

    """Total number of bad downlinked frames (from the Overall Number of bad downlinked frames column)"""

    overall_number_of_data_acquired_frames = Long()

    """Total number of data-acquired frames (from the Overall Number of data acquired frames column)"""

    overall_number_of_downlinked_frames = Long()

    """Total number of downlinked frames (from the Overall Number of downlinked frames column)"""

    planned_data_start = ZuluDate()

    """Planned start time of the data acquisition (from the Planned Data start column)"""

    planned_data_stop = ZuluDate()

    """Planned stop time of the data acquisition (from the Planned Data stop column)"""

    production_service_name = Keyword()

    """Production service name, set to a per-station constant (e.g. S5P-DLR, INS-Inuvik)"""

    production_service_type = Keyword()

    """Production service type, set to the constant DDP"""

    reportFolder = Keyword()

    """Source folder or path where the report file was collected"""

    report_type = Keyword()

    """Type of the report, set to the constant daily"""

    satellite_id = Keyword()

    """Satellite unit identifier, derived from the Satellite column and normalized to an S-prefixed unit code"""

    start_delivery = ZuluDate()

    """Start time of the delivery (from the Start Delivery column)"""

    stop_delivery = ZuluDate()

    """Stop time of the delivery (from the Stop Delivery column)"""


class ApsQualityInfo(MAASRawDocument):
    """
    Mapping class for index: raw-data-aps-quality-info

    Generated from: resources/templates/raw-data-aps-quality-info_template.json
    """

    class Index:
        "inner class for DSL"

        name = "raw-data-aps-quality-info"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("raw-data-aps-quality-info")

    _PARTITION_FIELD = "ingestionTime"

    _PARTITION_FIELD_FORMAT = "static"

    acquired_tfs = Long()

    """Total number of transfer frames acquired on the channel (from AcquiredTFs)"""

    channel = Long()

    """Channel number the quality metrics apply to (from Channel)"""

    corrected_data_tfs = Long()

    """Number of data transfer frames corrected by error correction (from CorrectedDataTFs)"""

    corrected_tfs = Long()

    """Number of transfer frames corrected by error correction (from CorrectedTFs)"""

    data_tfs = Long()

    """Number of data transfer frames acquired on the channel (from DataTFs)"""

    delivery_start = ZuluDate()

    """Start time of the delivery of the channel data (from DeliveryStart)"""

    delivery_stop = ZuluDate()

    """Stop time of the delivery of the channel data (from DeliveryStop)"""

    error_data_tfs = Long()

    """Number of data transfer frames received with errors (from ErrorDataTFs)"""

    error_tfs = Long()

    """Number of transfer frames received with errors (from ErrorTFs)"""

    interface_name = Keyword()

    """Name of the collector interface that produced this record"""

    production_service_name = Keyword()

    """Name of the CADIP ground station service that provided the quality info"""

    production_service_type = Keyword()

    """Type of the production service that provided the quality info, set to CADIP"""

    reportFolder = Keyword()

    """Source folder or path where the report file was collected"""

    session_id = Keyword()

    """CADIP acquisition session identifier the quality info belongs to (from SessionId)"""

    total_chunks = Long()

    """Total number of data chunks delivered for the channel (from TotalChunks)"""

    total_volume = Long()

    """Total data volume delivered for the channel in bytes (from TotalVolume)"""

    uncorrectable_data_tfs = Long()

    """Number of data transfer frames that could not be corrected (from UncorrectableDataTFs)"""

    uncorrectable_tfs = Long()

    """Number of transfer frames that could not be corrected (from UncorrectableTFs)"""


class ApsSessionQualityInfos(InnerDoc):
    """
    Inner document class for parent class: ApsSession

    Generated from property: quality_infos
    """

    Channel = Long()

    """Channel number the quality metrics apply to"""

    AcquiredTFs = Long()

    """Total number of transfer frames acquired on the channel"""

    SessionId = Keyword()

    """Acquisition session identifier the quality info belongs to"""

    ErrorTFs = Long()

    """Number of transfer frames received with errors"""

    CorrectedTFs = Long()

    """Number of transfer frames corrected by error correction"""

    UncorrectableTFs = Long()

    """Number of transfer frames that could not be corrected"""

    DataTFs = Long()

    """Number of data transfer frames acquired on the channel"""

    ErrorDataTFs = Long()

    """Number of data transfer frames received with errors"""

    CorrectedDataTFs = Long()

    """Number of data transfer frames corrected by error correction"""

    UncorrectableDataTFs = Long()

    """Number of data transfer frames that could not be corrected"""

    DeliveryStart = ZuluDate()

    """Start time of the delivery of the channel data"""

    DeliveryStop = ZuluDate()

    """Stop time of the delivery of the channel data"""

    TotalChunks = Long()

    """Total number of data chunks delivered for the channel"""

    TotalVolume = Long()

    """Total data volume delivered for the channel in bytes"""


class ApsSession(MAASRawDocument):
    """
    Mapping class for index: raw-data-aps-session

    Generated from: resources/templates/raw-data-aps-session_template.json
    """

    class Index:
        "inner class for DSL"

        name = "raw-data-aps-session"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("raw-data-aps-session")

    _PARTITION_FIELD = "ingestionTime"

    _PARTITION_FIELD_FORMAT = "static"

    acquisition_id = Keyword()

    """Acquisition identifier of the downlink session (from AcquisitionId)"""

    antenna_id = Keyword()

    """Identifier of the antenna used for the downlink (from AntennaId)"""

    antenna_status = Boolean()

    """Whether the antenna operated nominally during the session (from AntennaStatusOK)"""

    delivery_push_status = Boolean()

    """Whether the delivery push of the session completed successfully (from DeliveryPushOK)"""

    downlink_orbit = Keyword()

    """Orbit number during which the downlink occurred (from DownlinkOrbit)"""

    downlink_start = ZuluDate()

    """Actual start time of the data downlink (from DownlinkStart)"""

    downlink_status = Boolean()

    """Whether the downlink completed successfully (from DownlinkStatusOK)"""

    downlink_stop = ZuluDate()

    """Actual stop time of the data downlink (from DownlinkStop)"""

    front_end_id = Keyword()

    """Identifier of the front-end processor used for the session (from FrontEndId)"""

    front_end_status = Boolean()

    """Whether the front-end processor operated nominally (from FrontEndStatusOK)"""

    ground_station = Keyword()

    """Ground station code where the session was acquired"""

    interface_name = Keyword()

    """Name of the collector interface that produced this record (e.g. CADIP_<station>_Sessions)"""

    num_channels = Long()

    """Number of channels used for the downlink session (from NumChannels)"""

    planned_data_start = ZuluDate()

    """Planned start time of the data downlink (from PlannedDataStart)"""

    planned_data_stop = ZuluDate()

    """Planned stop time of the data downlink (from PlannedDataStop)"""

    production_service_name = Keyword()

    """Name of the CADIP ground station service that provided the session"""

    production_service_type = Keyword()

    """Type of the production service that provided the session, set to CADIP"""

    publication_date = ZuluDate()

    """Date the session was published by the CADIP service (from PublicationDate)"""

    quality_infos = Object(ApsSessionQualityInfos)

    """Per-channel transfer-frame quality metrics for the session (from the QualityInfo expansion)"""

    reportFolder = Keyword()

    """Source folder or path where the report file was collected"""

    retransfer = Boolean()

    """Whether the session data was delivered as a retransfer (from Retransfer)"""

    satellite_id = Keyword()

    """Identifier of the satellite that performed the downlink (from Satellite)"""

    session_id = Keyword()

    """CADIP acquisition session identifier (from SessionId)"""

    station_id = Keyword()

    """CADIP station identifier (from StationId, defaulted per station when absent)"""

    station_unit_id = Keyword()

    """Identifier of the station unit that acquired the session (from StationUnitId)"""


class AuxipProduct(MAASRawDocument):
    """
    Mapping class for index: raw-data-auxip-product

    Generated from: resources/templates/raw-data-auxip-product_template.json
    """

    class Index:
        "inner class for DSL"

        name = "raw-data-auxip-product"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("raw-data-auxip-product")

    _PARTITION_FIELD = "ingestionTime"

    _PARTITION_FIELD_FORMAT = "static"

    content_length = Long()

    """Product file size in bytes (OData ContentLength)"""

    end_date = ZuluDate()

    """Product sensing end date (OData ContentDate.End)"""

    eviction_date = ZuluDate()

    """Date the product is scheduled to be evicted from the AUXIP interface (OData EvictionDate)"""

    interface_name = Keyword()

    """Name of the AUXIP interface instance the product was collected from"""

    origin_date = ZuluDate()

    """Product origin date at the source (OData OriginDate)"""

    product_id = Keyword()

    """Product identifier from the AUXIP interface (OData Id)"""

    product_name = Keyword()

    """Product file name from the AUXIP interface (OData Name)"""

    production_service_name = Keyword()

    """Name of the AUXIP production service instance providing the product"""

    production_service_type = Keyword()

    """Type of the production service providing the product (AUXIP)"""

    publication_date = ZuluDate()

    """Date the product was published on the AUXIP interface (OData PublicationDate)"""

    reportFolder = Keyword()

    """Folder or path of the source report file from which this record was extracted"""

    start_date = ZuluDate()

    """Product sensing start date (OData ContentDate.Start)"""


class CamsAnomalyCorrelation(MAASRawDocument):
    """
    Mapping class for index: raw-data-cams-anomaly-correlation

    Generated from: resources/templates/raw-data-cams-anomaly-correlation_template.json
    """

    class Index:
        "inner class for DSL"

        name = "raw-data-cams-anomaly-correlation"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("raw-data-cams-anomaly-correlation")

    _PARTITION_FIELD = "ingestionTime"

    _PARTITION_FIELD_FORMAT = "static"

    acquisition_pass = Keyword()

    """Acquisition pass keys impacted by the anomaly (satellite, station type, identifier and ground station)"""

    cams_issue = Keyword()

    """Key of the CAMS ticket this anomaly correlation is linked to"""

    datatake_ids = Keyword()

    """Identifiers of the datatakes impacted by the anomaly"""

    description = Keyword()

    """Free-text description of the anomaly, propagated to the linked CAMS ticket"""

    interface_name = Keyword()

    """Name of the collector interface that produced the record"""

    key = Keyword()

    """Unique key identifying the anomaly correlation record"""

    origin = Keyword()

    """Origin of the anomaly, propagated to the linked CAMS ticket"""

    products = Keyword()

    """Names of the products impacted by the anomaly"""

    reportFolder = Keyword()

    """Source folder of the ingested report"""


class CamsCloudAnomalyCorrelation(MAASRawDocument):
    """
    Mapping class for index: raw-data-cams-cloud-anomaly-correlation

    Generated from: resources/templates/raw-data-cams-cloud-anomaly-correlation_template.json
    """

    class Index:
        "inner class for DSL"

        name = "raw-data-cams-cloud-anomaly-correlation"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("raw-data-cams-cloud-anomaly-correlation")

    _PARTITION_FIELD = "ingestionTime"

    _PARTITION_FIELD_FORMAT = "static"

    created = ZuluDate()

    """Date the anomaly correlation issue was created in Jira"""

    description = Keyword()

    """Free-text description of the anomaly (Jira description field)"""

    impacted_observations = Keyword()

    """Observations impacted by the anomaly (Jira impacted-observations custom field)"""

    impacted_passes = Keyword()

    """Acquisition passes impacted by the anomaly (Jira impacted-passes custom field)"""

    interface_name = Keyword()

    """Name of the collector interface that produced the record (Jira_CAMS_Cloud_Anomaly_Correlation)"""

    issue = Keyword()

    """Key of the CAMS anomaly issue this correlation is linked to (derived from Jira issue links)"""

    key = Keyword()

    """Jira issue key uniquely identifying the anomaly correlation record"""

    origin = Keyword()

    """Origin of the anomaly (Jira origin custom field)"""

    products = Keyword()

    """Names of the products impacted by the anomaly (Jira products custom field)"""

    reportFolder = Keyword()

    """Source folder of the ingested report"""

    satellite_unit = Keyword()

    """Satellite unit(s) impacted by the anomaly (Jira satellite-unit custom field)"""

    station = Keyword()

    """Ground station involved (Jira station custom field, child value)"""

    station_type = Keyword()

    """Type of ground station involved (Jira station custom field, parent value)"""

    status = Keyword()

    """Current workflow status of the Jira issue"""

    summary = Keyword()

    """Summary text of the Jira anomaly correlation issue"""

    title = Keyword()

    """Title taken from the Jira issue summary"""

    updated = ZuluDate()

    """Date the anomaly correlation issue was last updated in Jira"""


class CamsCloudTickets(MAASRawDocument):
    """
    Mapping class for index: raw-data-cams-cloud-tickets

    Generated from: resources/templates/raw-data-cams-cloud-tickets_template.json
    """

    class Index:
        "inner class for DSL"

        name = "raw-data-cams-cloud-tickets"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("raw-data-cams-cloud-tickets")

    _PARTITION_FIELD = "created"

    _PARTITION_FIELD_FORMAT = "static"

    addressed_entities = Keyword()

    """Entities addressed by the ticket (Jira addressed-entities custom field)"""

    affected_systems = Keyword()

    """Ground segment systems affected by the anomaly (Jira affected-systems custom field)"""

    assigned_element = Keyword()

    """Element(s) the ticket is assigned to (Jira assigned-element custom field)"""

    created = ZuluDate()

    """Date the CAMS ticket was created in Jira"""

    criticality = Keyword()

    """Criticality level of the anomaly (Jira criticality custom field)"""

    entity = Keyword()

    """Primary entity responsible for the ticket (Jira entity custom field)"""

    environment = Keyword()

    """Environment description of the ticket (Jira environment field)"""

    esa_group = Keyword()

    """ESA group associated with the ticket (Jira ESA-group custom field)"""

    interface_name = Keyword()

    """Name of the collector interface that produced the record (Jira_CAMS_Cloud_Tickets)"""

    involved_entities = Keyword()

    """Entities involved in the ticket (Jira involved-entities custom field)"""

    key = Keyword()

    """Jira issue key uniquely identifying the CAMS ticket"""

    linked_issues = Keyword()

    """Keys of Jira issues linked to this ticket (inward issue links)"""

    occurence_date = ZuluDate()

    """Date the anomaly occurred (Jira occurrence-date custom field)"""

    originating_entity = Keyword()

    """Entity that originated the ticket (Jira originating-entity custom field)"""

    reportFolder = Keyword()

    """Source folder of the ingested report"""

    reporter = Keyword()

    """Display name of the Jira user who reported the ticket"""

    review_board_dispositions = Keyword()

    """Review board dispositions recorded on the ticket (Jira custom field)"""

    status = Keyword()

    """Current workflow status of the Jira ticket"""

    title = Keyword()

    """Ticket title taken from the Jira issue summary"""

    updated = ZuluDate()

    """Date the CAMS ticket was last updated in Jira"""

    urgency = Keyword()

    """Urgency level of the anomaly (Jira urgency custom field)"""


class CamsTickets(MAASRawDocument):
    """
    Mapping class for index: raw-data-cams-tickets

    Generated from: resources/templates/raw-data-cams-tickets_template.json
    """

    class Index:
        "inner class for DSL"

        name = "raw-data-cams-tickets"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("raw-data-cams-tickets")

    _PARTITION_FIELD = "created"

    _PARTITION_FIELD_FORMAT = "static"

    affected_systems = Keyword()

    """Ground segment systems affected by the anomaly (Jira affected-systems field)"""

    assigned_element = Keyword()

    """Element(s) the ticket is assigned to (Jira assigned-element field)"""

    created = ZuluDate()

    """Date the CAMS ticket was created in Jira"""

    criticality = Keyword()

    """Criticality level of the anomaly (Jira criticality field)"""

    entity = Keyword()

    """Primary entity responsible for the ticket (Jira entity field)"""

    environment = Keyword()

    """Environment description of the ticket (Jira environment field)"""

    interface_name = Keyword()

    """Name of the collector interface that produced the record"""

    involved_entities = Keyword()

    """Entities involved in the ticket (Jira involved-entities field)"""

    key = Keyword()

    """Jira issue key uniquely identifying the CAMS ticket"""

    linked_issues = Keyword()

    """Keys of Jira issues linked to this ticket"""

    occurence_date = ZuluDate()

    """Date the anomaly occurred (Jira occurrence-date field)"""

    originating_entity = Keyword()

    """Entity that originated the ticket (Jira originating-entity field)"""

    reportFolder = Keyword()

    """Source folder of the ingested report"""

    reporter = Keyword()

    """Display name of the Jira user who reported the ticket"""

    review_board_dispositions = Keyword()

    """Review board dispositions recorded on the ticket (Jira field)"""

    status = Keyword()

    """Current workflow status of the Jira ticket"""

    title = Keyword()

    """Ticket title taken from the Jira issue summary"""

    updated = ZuluDate()

    """Date the CAMS ticket was last updated in Jira"""

    urgency = Keyword()

    """Urgency level of the anomaly (Jira urgency field)"""


class CdsAcquisitionPassStatus(MAASDocument):
    """
    Mapping class for index: cds-acquisition-pass-status

    Generated from: resources/templates/cds-acquisition-pass-status_template.json
    """

    class Index:
        "inner class for DSL"

        name = "cds-acquisition-pass-status"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("cds-acquisition-pass-status")

    _PARTITION_FIELD = "planned_data_start"

    _PARTITION_FIELD_FORMAT = "static"

    antenna_id = Keyword()

    """Identifier of the antenna used for the acquisition"""

    antenna_status = Keyword()

    """Status of the antenna during the acquisition pass"""

    cams_description = Keyword()

    """Description of the linked CAMS ticket(s)"""

    cams_origin = Keyword()

    """Origin of the linked CAMS ticket(s)"""

    cams_tickets = Keyword()

    """Identifiers of the CAMS tickets linked to this acquisition pass"""

    delivery_bitrate = Float()

    """Computed delivery bitrate of the acquisition pass"""

    delivery_push_status = Keyword()

    """Status of the delivery push step of the acquisition pass"""

    downlink_orbit = Keyword()

    """Downlink orbit number of the acquisition pass"""

    doy = Integer()

    """Day of year of the acquisition pass"""

    fer_data = Float()

    """Frame error rate of the data"""

    fer_downlink = Float()

    """Frame error rate of the downlink"""

    first_frame_start = ZuluDate()

    """Start time of the first acquired frame"""

    from_acq_delivery_timeliness = Long()

    """Timeliness between acquisition and delivery, computed from first_frame_start to stop_delivery"""

    front_end_id = Keyword()

    """Identifier of the front-end used for the acquisition"""

    front_end_status = Keyword()

    """Status of the front-end during the acquisition pass"""

    ground_station = Keyword()

    """Ground station where the acquisition pass was performed"""

    last_attached_ticket = Keyword()

    """Identifier of the last CAMS ticket attached to this acquisition pass"""

    last_attached_ticket_url = Keyword()

    """URL of the last CAMS ticket attached to this acquisition pass"""

    last_frame_stop = ZuluDate()

    """Stop time of the last acquired frame"""

    mission = Keyword()

    """Mission the satellite belongs to (e.g. S1, S2, S3, S5)"""

    notes = Text()

    """Free-text notes about the acquisition pass"""

    number_of_chunks = Integer()

    """Number of chunks in the acquisition pass"""

    overall_data_volume = Long()

    """Overall acquired data volume of the acquisition pass"""

    overall_number_of_bad_data_acquired_frames = Long()

    """Overall number of bad acquired data frames"""

    overall_number_of_bad_downlinked_frames = Long()

    """Overall number of bad downlinked frames"""

    overall_number_of_data_acquired_frames = Long()

    """Overall number of acquired data frames"""

    overall_number_of_downlinked_frames = Long()

    """Overall number of downlinked frames"""

    planned_data_start = ZuluDate()

    """Planned start time of the data acquisition"""

    planned_data_stop = ZuluDate()

    """Planned stop time of the data acquisition"""

    report_name_daily = Keyword()

    """Name of the daily source report the document was ingested from"""

    report_name_monthly = Keyword()

    """Name of the monthly source report the document was ingested from"""

    report_name_weekly = Keyword()

    """Name of the weekly source report the document was ingested from"""

    report_type = Keyword()

    """Type of the source report (daily, weekly or monthly)"""

    satellite_id = Keyword()

    """Identifier of the acquiring satellite"""

    start_delivery = ZuluDate()

    """Start time of the data delivery"""

    stop_delivery = ZuluDate()

    """Stop time of the data delivery"""

    updateTime = ZuluDate()

    """Timestamp of the last update of this document"""


class CdsAiProductionCompleteness(MAASDocument):
    """
    Mapping class for index: cds-ai-production-completeness

    Generated from: resources/templates/cds-ai-production-completeness_template.json
    """

    class Index:
        "inner class for DSL"

        name = "cds-ai-production-completeness"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("cds-ai-production-completeness")

    completeness = Long()

    """AI production completeness indicator: 1 when the AISAUX product is produced, 0 otherwise"""

    datatake_id = Keyword()

    """Datatake identifier taken from the input AI_RAW__0_ product"""

    file_name = Keyword()

    """Name of the produced AISAUX product"""

    input_name = Keyword()

    """Name of the input AI_RAW__0_ product"""

    mission = Keyword()

    """Mission of the AI product (Sentinel-1)"""

    satellite_unit = Keyword()

    """Satellite unit of the AI product (e.g. S1A, S1B)"""

    sensing_end_date = ZuluDate()

    """End of the sensing window of the AI product, part of the completeness identity (UTC)"""

    sensing_start_date = ZuluDate()

    """Start of the sensing window of the AI product, part of the completeness identity (UTC)"""

    timeliness = Keyword()

    """Timeliness of the input AI_RAW__0_ product"""

    updateTime = ZuluDate()

    """Timestamp of the last consolidation update of this AI production completeness document (UTC)"""


class CdsAnomalyCorrelation(MAASDocument):
    """
    Mapping class for index: cds-anomaly-correlation

    Generated from: resources/templates/cds-anomaly-correlation_template.json
    """

    class Index:
        "inner class for DSL"

        name = "cds-anomaly-correlation"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("cds-anomaly-correlation")

    created = ZuluDate()

    """Creation date of the anomaly correlation file"""

    description = Keyword()

    """Description of the anomaly"""

    impacted_observations = Keyword()

    """Impacted observations declared in the anomaly, used to derive corrected datatake identifiers"""

    impacted_passes = Keyword()

    """Impacted acquisition passes declared in the anomaly, used to derive acquisition pass keys"""

    issue = Keyword()

    """Linked issue identifiers associated with the anomaly, searched for the related GSANOM issue"""

    key = Keyword()

    """Key uniquely identifying the anomaly correlation file"""

    origin = Keyword()

    """Origin of the anomaly"""

    products = Keyword()

    """Normalized names of products impacted by the anomaly"""

    satellite_unit = Keyword()

    """Satellite unit(s) impacted by the anomaly"""

    station = Keyword()

    """Ground station(s) impacted by the anomaly, used to build acquisition pass keys"""

    station_type = Keyword()

    """Type of the ground station impacted by the anomaly, used to build acquisition pass keys"""

    status = Keyword()

    """Current status of the anomaly correlation file"""

    summary = Keyword()

    """Summary of the anomaly"""

    ticket_id = Keyword()

    """Identifier of the associated GSANOM issue extracted from the title or the linked issues"""

    title = Keyword()

    """Title of the anomaly correlation file, parsed to extract the associated GSANOM issue"""

    updateTime = ZuluDate()

    """Date and time when this consolidated anomaly correlation document was last updated by the consolidation engine"""

    updated = ZuluDate()

    """Last update date of the anomaly correlation file"""


class CdsCadipAcquisitionPassStatusQualityInfos(InnerDoc):
    """
    Inner document class for parent class: CdsCadipAcquisitionPassStatus

    Generated from property: quality_infos
    """

    Channel = Long()

    """Channel number"""

    AcquiredTFs = Long()

    """Number of acquired transfer frames on this channel"""

    SessionId = Keyword()

    """Identifier of the acquisition session for this channel"""

    ErrorTFs = Long()

    """Number of transfer frames in error on this channel"""

    CorrectedTFs = Long()

    """Number of corrected transfer frames on this channel"""

    UncorrectableTFs = Long()

    """Number of uncorrectable transfer frames on this channel"""

    DataTFs = Long()

    """Number of data transfer frames on this channel"""

    ErrorDataTFs = Long()

    """Number of data transfer frames in error on this channel"""

    CorrectedDataTFs = Long()

    """Number of corrected data transfer frames on this channel"""

    UncorrectableDataTFs = Long()

    """Number of uncorrectable data transfer frames on this channel"""

    DeliveryStart = ZuluDate()

    """Delivery start time on this channel"""

    DeliveryStop = ZuluDate()

    """Delivery stop time on this channel"""

    TotalChunks = Long()

    """Total number of chunks on this channel"""

    TotalVolume = Long()

    """Acquired data volume on this channel"""


class CdsCadipAcquisitionPassStatus(MAASDocument):
    """
    Mapping class for index: cds-cadip-acquisition-pass-status

    Generated from: resources/templates/cds-cadip-acquisition-pass-status_template.json
    """

    class Index:
        "inner class for DSL"

        name = "cds-cadip-acquisition-pass-status"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("cds-cadip-acquisition-pass-status")

    _PARTITION_FIELD = "publication_date"

    _PARTITION_FIELD_FORMAT = "static"

    AcquiredTFs = Long()

    """Number of acquired transfer frames, aggregated across all channels"""

    CorrectedDataTFs = Long()

    """Number of corrected data transfer frames, aggregated across all channels"""

    CorrectedTFs = Long()

    """Number of corrected transfer frames, aggregated across all channels"""

    DataTFs = Long()

    """Number of data transfer frames, aggregated across all channels"""

    ErrorDataTFs = Long()

    """Number of data transfer frames in error, aggregated across all channels"""

    ErrorTFs = Long()

    """Number of transfer frames in error, aggregated across all channels"""

    TotalChunks = Long()

    """Total number of chunks, aggregated across all channels"""

    TotalVolume = Long()

    """Total acquired data volume, aggregated across all channels"""

    UncorrectableDataTFs = Long()

    """Number of uncorrectable data transfer frames, aggregated across all channels"""

    UncorrectableTFs = Long()

    """Number of uncorrectable transfer frames, aggregated across all channels"""

    acquisition_id = Keyword()

    """Identifier of the acquisition"""

    antenna_id = Keyword()

    """Identifier of the antenna used for the acquisition"""

    antenna_status = Boolean()

    """Status of the antenna during the acquisition pass"""

    cams_description = Keyword()

    """Description of the linked CAMS ticket(s)"""

    cams_origin = Keyword()

    """Origin of the linked CAMS ticket(s)"""

    cams_tickets = Keyword()

    """Identifiers of the CAMS tickets linked to this acquisition pass"""

    delivery_bitrate = Float()

    """Computed delivery bitrate of the acquisition pass"""

    delivery_push_status = Boolean()

    """Status of the delivery push step of the acquisition pass"""

    delivery_start = ZuluDate()

    """Earliest delivery start time across all channels"""

    delivery_stop = ZuluDate()

    """Latest delivery stop time across all channels"""

    downlink_orbit = Keyword()

    """Downlink orbit number of the acquisition pass"""

    downlink_start = ZuluDate()

    """Start time of the downlink"""

    downlink_status = Boolean()

    """Status of the downlink step of the acquisition pass"""

    downlink_stop = ZuluDate()

    """Stop time of the downlink"""

    fer_data = Float()

    """Frame error rate of the data, computed as UncorrectableTFs divided by AcquiredTFs"""

    from_acq_delivery_timeliness = Long()

    """Timeliness between acquisition and delivery, computed from downlink_start to delivery_stop"""

    front_end_id = Keyword()

    """Identifier of the front-end used for the acquisition"""

    front_end_status = Boolean()

    """Status of the front-end during the acquisition pass"""

    global_status = Keyword()

    """Overall status of the acquisition pass (OK, NOK or INCOMPLETE) derived from the antenna, front-end and delivery push statuses"""

    ground_station = Keyword()

    """Ground station where the acquisition pass was performed"""

    interface_name = Keyword()

    """Name of the interface the data was collected from"""

    last_attached_ticket = Keyword()

    """Identifier of the last CAMS ticket attached to this acquisition pass"""

    last_attached_ticket_url = Keyword()

    """URL of the last CAMS ticket attached to this acquisition pass"""

    mission = Keyword()

    """Mission the satellite belongs to (e.g. S1, S2), derived from the satellite identifier"""

    num_channels = Long()

    """Number of channels used during the acquisition session"""

    planned_data_start = ZuluDate()

    """Planned start time of the data acquisition"""

    planned_data_stop = ZuluDate()

    """Planned stop time of the data acquisition"""

    production_service_name = Keyword()

    """Name of the production service that provided the data"""

    production_service_type = Keyword()

    """Type of the production service that provided the data"""

    publication_date = ZuluDate()

    """Publication date of the session on the CADIP interface"""

    quality_infos = Object(CdsCadipAcquisitionPassStatusQualityInfos)

    """Per-channel quality information of the acquisition session"""

    reportFolder = Keyword()

    """Folder of the source report the document was ingested from"""

    retransfer = Boolean()

    """Flag indicating whether the session is a retransfer"""

    satellite_id = Keyword()

    """Identifier of the acquiring satellite"""

    session_id = Keyword()

    """Identifier of the CADIP acquisition session, used as the consolidated document identifier"""

    station_id = Keyword()

    """Identifier of the ground station"""

    station_unit_id = Keyword()

    """Identifier of the ground station unit"""

    updateTime = ZuluDate()

    """Timestamp of the last update of this document"""


class CdsCamsTickets(MAASDocument):
    """
    Mapping class for index: cds-cams-tickets

    Generated from: resources/templates/cds-cams-tickets_template.json
    """

    class Index:
        "inner class for DSL"

        name = "cds-cams-tickets"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("cds-cams-tickets")

    _PARTITION_FIELD = "created"

    _PARTITION_FIELD_FORMAT = "static"

    acquisition_pass = Keyword()

    """Acquisition pass keys impacted by the ticket, aggregated from linked anomaly correlation files"""

    addressed_entities = Keyword()

    """Entities addressed by the ticket"""

    affected_systems = Keyword()

    """Systems affected by the anomaly reported in the ticket"""

    assigned_element = Keyword()

    """Ground segment element(s) or station(s) the ticket is assigned to"""

    correlation_file_id = Keyword()

    """Identifiers of the linked anomaly correlation (AN) files associated with this ticket"""

    created = ZuluDate()

    """Creation date of the ticket"""

    criticality = Keyword()

    """Criticality level of the anomaly ticket"""

    datatake_ids = Keyword()

    """Datatake identifiers impacted by the ticket, aggregated from linked anomaly correlation files"""

    description = Keyword()

    """Description of the anomaly taken from the latest linked anomaly correlation file"""

    entity = Keyword()

    """Entity responsible for or associated with the ticket"""

    environment = Keyword()

    """Impacted environment(s) referenced by the ticket, used to link impacted entities"""

    esa_group = Keyword()

    """ESA group associated with the ticket"""

    involved_entities = Keyword()

    """Entities involved in the ticket"""

    key = Keyword()

    """CAMS ticket key uniquely identifying the ticket"""

    linked_issues = Keyword()

    """Keys of issues linked to this ticket"""

    occurence_date = ZuluDate()

    """Date when the reported anomaly occurred"""

    origin = Keyword()

    """Origin of the anomaly taken from the latest linked anomaly correlation file"""

    originating_entity = Keyword()

    """Entity that originated the ticket"""

    products = Keyword()

    """Product names impacted by the ticket, aggregated from linked anomaly correlation files"""

    publications = Keyword()

    """Publication names impacted by the ticket, aggregated from linked anomaly correlation files"""

    reporter = Keyword()

    """Author who reported the ticket"""

    review_board_dispositions = Keyword()

    """Review board dispositions recorded for the ticket"""

    status = Keyword()

    """Current status of the ticket"""

    title = Keyword()

    """Title of the CAMS anomaly ticket"""

    updateTime = ZuluDate()

    """Date and time when this consolidated CAMS ticket document was last updated by the consolidation engine"""

    updated = ZuluDate()

    """Last update date of the ticket"""

    urgency = Keyword()

    """Urgency level of the anomaly ticket"""

    url = Keyword()

    """URL to the ticket in the CAMS browse interface"""


class CdsCompletenessMissingPeriods(InnerDoc):
    """
    Inner document class for parent class: CdsCompleteness

    Generated from property: missing_periods
    """

    name = Keyword()

    """Name of the missing period entry"""

    product_type = Keyword()

    """Product type for which the sensing period is missing"""

    sensing_start_date = ZuluDate()

    """Start of the missing sensing period (UTC)"""

    sensing_end_date = ZuluDate()

    """End of the missing sensing period (UTC)"""

    duration = Long()

    """Duration of the missing sensing period in microseconds"""


class CdsCompleteness(MAASDocument):
    """
    Mapping class for index: cds-completeness

    Generated from: resources/templates/cds-completeness_template.json
    """

    class Index:
        "inner class for DSL"

        name = "cds-completeness"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("cds-completeness")

    _PARTITION_FIELD = ["mission", "satellite_unit", "service_type", "service_id"]

    _PARTITION_FIELD_FORMAT = "{mission}-{satellite_unit}-{service_type}-{service_id}"

    absolute_orbit = Keyword()

    """Absolute orbit number of the datatake"""

    application_date = ZuluDate()

    """Application date of the mission plan file that declared this datatake (UTC)"""

    cams_description = Keyword()

    """Description reported by the attached CAMS anomaly ticket(s)"""

    cams_origin = Keyword()

    """Origin reported by the attached CAMS anomaly ticket(s)"""

    cams_tickets = Keyword()

    """CAMS anomaly ticket identifiers attached to this datatake completeness"""

    datastrip_ids = Keyword()

    """Identifiers of the datastrips associated with this datatake"""

    datatake_id = Keyword()

    """Identifier of the datatake whose production completeness is measured"""

    hex_datatake_id = Keyword()

    """Hexadecimal representation of the datatake identifier"""

    instrument_mode = Keyword()

    """Instrument acquisition mode of the datatake"""

    instrument_swath = Keyword()

    """Instrument swath of the datatake"""

    key = Keyword()

    """Unique identifier of the completeness document, derived from the datatake"""

    l0_sensing_duration = Long()

    """Duration of the level-0 sensing window in microseconds"""

    l0_sensing_time_start = ZuluDate()

    """Start of the level-0 sensing window for this datatake (UTC)"""

    l0_sensing_time_stop = ZuluDate()

    """End of the level-0 sensing window for this datatake (UTC)"""

    last_attached_ticket = Keyword()

    """Identifier of the most recently attached CAMS anomaly ticket"""

    last_attached_ticket_url = Keyword()

    """URL of the most recently attached CAMS anomaly ticket"""

    missing_periods = Object(CdsCompletenessMissingPeriods)

    """Sensing periods for which expected products are missing in the production"""

    mission = Keyword()

    """Mission the datatake belongs to (e.g. S1, S2)"""

    name = Keyword()

    """Name of the datatake this completeness relates to"""

    number_of_expected_tiles = Integer()

    """Number of tiles expected to be produced for the datatake"""

    number_of_scenes = Integer()

    """Number of scenes planned for the datatake (Sentinel-2)"""

    observation_duration = Long()

    """Duration of the datatake observation window in microseconds"""

    observation_time_start = ZuluDate()

    """Start of the datatake observation/sensing window (UTC)"""

    observation_time_stop = ZuluDate()

    """End of the datatake observation/sensing window (UTC)"""

    polarization = Keyword()

    """Polarisation configuration of the datatake (Sentinel-1)"""

    product_group_ids = Keyword()

    """Identifiers of the product groups associated with this datatake"""

    relative_orbit = Keyword()

    """Relative orbit number of the datatake"""

    satellite_unit = Keyword()

    """Satellite unit of the datatake (e.g. S1A, S2B)"""

    service_id = Keyword()

    """Identifier of the production service instance providing the products (partition field)"""

    service_type = Keyword()

    """Type of the production service providing the products (partition field)"""

    timeliness = Keyword()

    """Timeliness category of the expected products (e.g. NRT, NTC)"""

    updateTime = ZuluDate()

    """Timestamp of the last consolidation update of this datatake completeness document (UTC)"""


class CdsCompletenessSplitted(MAASDocument):
    """
    Mapping class for index: cds-completeness-splitted

    Generated from: resources/templates/cds-completeness-splitted_template.json
    """

    class Index:
        "inner class for DSL"

        name = "cds-completeness-splitted"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("cds-completeness-splitted")

    _PARTITION_FIELD = ["mission", "satellite_unit", "service_type", "service_id"]

    _PARTITION_FIELD_FORMAT = "{mission}-{satellite_unit}-{service_type}-{service_id}"

    absolute_orbit = Keyword()

    """Absolute orbit number of the datatake"""

    cams_description = Keyword()

    """Description reported by the attached CAMS anomaly ticket(s)"""

    cams_origin = Keyword()

    """Origin reported by the attached CAMS anomaly ticket(s)"""

    cams_tickets = Keyword()

    """CAMS anomaly ticket identifiers attached to this completeness entry"""

    datatake_id = Keyword()

    """Identifier of the datatake whose production completeness is measured"""

    expected = Long()

    """Expected sensing value for this product type and timeliness, in microseconds, derived from the completeness configuration"""

    key = Keyword()

    """Unique identifier of the splitted completeness entry, built from datatake_id, timeliness and product_type"""

    last_attached_ticket = Keyword()

    """Identifier of the most recently attached CAMS anomaly ticket"""

    last_attached_ticket_url = Keyword()

    """URL of the most recently attached CAMS anomaly ticket"""

    mission = Keyword()

    """Mission the datatake belongs to (e.g. S1, S3, S5)"""

    observation_duration = Long()

    """Duration of the observation period in microseconds"""

    observation_time_start = ZuluDate()

    """Start of the observation period covered by the produced products (UTC)"""

    observation_time_stop = ZuluDate()

    """End of the observation period covered by the produced products (UTC)"""

    percentage = Long()

    """Completeness percentage, computed as the adjusted value divided by the expected value"""

    product_level = Keyword()

    """Product level tracked by this completeness entry"""

    product_type = Keyword()

    """Product type tracked by this completeness entry"""

    relative_orbit = Keyword()

    """Relative orbit number of the datatake"""

    satellite_unit = Keyword()

    """Satellite unit of the datatake (e.g. S1A, S3B)"""

    service_id = Keyword()

    """Identifier of the production service instance providing the products (partition field)"""

    service_type = Keyword()

    """Type of the production service providing the products (partition field)"""

    status = Keyword()

    """Completeness status evaluated from the percentage"""

    timeliness = Keyword()

    """Timeliness of the products tracked by this completeness entry"""

    updateTime = ZuluDate()

    """Timestamp of the last consolidation update of this splitted completeness document (UTC)"""

    value = Long()

    """Measured produced sensing value for this product type and timeliness, in microseconds"""

    value_adjusted = Long()

    """Produced value capped at the expected value, in microseconds"""


class CdsDatabudget(MAASDocument):
    """
    Mapping class for index: cds-databudget

    Generated from: resources/templates/cds-databudget_template.json
    """

    class Index:
        "inner class for DSL"

        name = "cds-databudget"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("cds-databudget")

    _PARTITION_FIELD = "ingestionTime"

    _PARTITION_FIELD_FORMAT = "conf"

    archived = Keyword()

    """Archiving service value for the product type as declared in the databudget"""

    data_category = Keyword()

    """Category of the record: RAW, GLOBAL_THRESHOLD, SPECIFIC_THRESHOLD or TIMELINESS_LUT"""

    database_timeliness = Keyword()

    """Timeliness label as used in the database, mapped from the databudget timeliness through the lookup table"""

    database_type = Keyword()

    """Product type as used in the database, expanded from the compacted databudget type notation"""

    databudget_type = Keyword()

    """Original product type as declared in the databudget report"""

    disseminated = Keyword()

    """Dissemination service value for the product type as declared in the databudget"""

    level = Keyword()

    """Product processing level (e.g. L0, L1, L2)"""

    mission = Keyword()

    """Mission the databudget entry applies to (e.g. S1, S2)"""

    num_day = Keyword()

    """Expected number of products per day declared in the databudget"""

    produced = Keyword()

    """Production service value for the product type as declared in the databudget"""

    threshold_count = Float()

    """Expected daily product count threshold, summed from the databudget count per day"""

    threshold_subtype = Keyword()

    """Service type (e.g. PRIP, LTA, DA) the threshold applies to"""

    threshold_volume = Float()

    """Expected daily data volume threshold, summed from the databudget volume per day"""

    timeliness = Keyword()

    """Timeliness of the product as declared in the databudget"""

    version = Keyword()

    """Version of the databudget the record was generated from"""

    volume_day = Float()

    """Expected data volume produced per day for the product type"""


class CdsDataflow(MAASDocument):
    """
    Mapping class for index: cds-dataflow

    Generated from: resources/templates/cds-dataflow_template.json
    """

    class Index:
        "inner class for DSL"

        name = "cds-dataflow"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("cds-dataflow")

    _PARTITION_FIELD = "ingestionTime"

    _PARTITION_FIELD_FORMAT = "conf"

    consumed_by = Keyword()

    """Interfaces or services that consume the product type"""

    groups = Keyword()

    """Groups the product type belongs to"""

    instrument = Keyword()

    """Instrument that produces the product type"""

    level = Keyword()

    """Processing level of the product type"""

    mission = Keyword()

    """Mission the product type belongs to (e.g. S1, S2, S3)"""

    mode = Keyword()

    """Acquisition mode of the product type"""

    origin_level = Keyword()

    """Origin processing level from which the product is derived"""

    product_type = Keyword()

    """Product type described by this dataflow entry"""

    published_by = Keyword()

    """Interfaces or services that publish the product type"""

    type = Keyword()

    """Type category of the dataflow entry"""


class CdsDatatakeDuplicatedsItemsDeletedProduct(InnerDoc):
    """
    Inner document class for parent class: CdsDatatakeDuplicatedsItems

    Generated from property: deleted_product
    """

    DD = Keyword()

    """Name of the pair product deleted from the DD interface"""

    LTA = Keyword()

    """Name of the pair product deleted from the LTA interface"""


class CdsDatatakeDuplicatedsItems(InnerDoc):
    """
    Inner document class for parent class: CdsDatatakeDuplicateds

    Generated from property: items
    """

    name = Keyword()

    """Name of the first product of the duplicated pair"""

    product_type = Keyword()

    """Product type of the duplicated pair"""

    sensing_start_date = ZuluDate()

    """Sensing start date of the product"""

    sensing_end_date = ZuluDate()

    """Sensing end date of the product"""

    duplicated_percentage = Float()

    """Overlap percentage between the two products of the pair"""

    paired_with = Keyword()

    """Name of the other product forming the duplicated pair"""

    deleted_product = Object(CdsDatatakeDuplicatedsItemsDeletedProduct)

    """Name of the pair product deleted from each interface"""


class CdsDatatakeDuplicatedsDeletions(InnerDoc):
    """
    Inner document class for parent class: CdsDatatakeDuplicateds

    Generated from property: deletions
    """

    service_type = Keyword()

    """Interface the deletion figures apply to (DD or LTA)"""

    ticket = Keyword()

    """Most frequent deletion ticket for this interface"""

    targeted_products_count = Integer()

    """Number of products deleted from this interface"""

    surviving_pairs_count = Integer()

    """Number of duplicated pairs still present on this interface"""

    deleted_not_duplicated_products = Keyword()

    """Products deleted from this interface that are not part of any duplicated pair"""

    deleted_not_duplicated_products_count = Integer()

    """Count of deleted products not part of any duplicated pair"""

    expected_pairs_count = Integer()

    """Number of duplicated pairs expected to be removed from this interface"""

    deletion_completenness_percentange = Float()

    """Percentage of expected duplicated pairs actually removed from this interface"""


class CdsDatatakeDuplicatedsDatastripPairsDatastripsProductsDeletions(InnerDoc):
    """
    Inner document class for parent class: CdsDatatakeDuplicatedsDatastripPairsDatastripsProducts

    Generated from property: deletions
    """

    service_type = Keyword()

    """Interface the product was deleted from (DD or LTA)"""

    ticket = Keyword()

    """Deletion ticket associated with this product"""


class CdsDatatakeDuplicatedsDatastripPairsDatastripsProducts(InnerDoc):
    """
    Inner document class for parent class: CdsDatatakeDuplicatedsDatastripPairsDatastrips

    Generated from property: products
    """

    product_name = Keyword()

    """Name of the product"""

    product_type = Keyword()

    """Type of the product"""

    deletions = Object(CdsDatatakeDuplicatedsDatastripPairsDatastripsProductsDeletions)

    """Deletion trace for this product"""


class CdsDatatakeDuplicatedsDatastripPairsDatastripsDeletions(InnerDoc):
    """
    Inner document class for parent class: CdsDatatakeDuplicatedsDatastripPairsDatastrips

    Generated from property: deletions
    """

    service_type = Keyword()

    """Interface the deletion figures apply to (DD or LTA)"""

    ticket = Keyword()

    """Deletion ticket associated with the datastrip"""

    deleted_products_count = Integer()

    """Number of datastrip products deleted from this interface"""

    deleted_products_expected = Integer()

    """Number of datastrip products expected to be deleted from this interface"""

    deleted_product_percentage = Float()

    """Percentage of expected datastrip products actually deleted from this interface"""


class CdsDatatakeDuplicatedsDatastripPairsDatastrips(InnerDoc):
    """
    Inner document class for parent class: CdsDatatakeDuplicatedsDatastripPairs

    Generated from property: datastrips
    """

    datastrip_id = Keyword()

    """Identifier of the datastrip"""

    products = Object(CdsDatatakeDuplicatedsDatastripPairsDatastripsProducts)

    """Products belonging to the datastrip"""

    deletions = Object(CdsDatatakeDuplicatedsDatastripPairsDatastripsDeletions)

    """Per-interface deletion summary for the datastrip"""


class CdsDatatakeDuplicatedsDatastripPairs(InnerDoc):
    """
    Inner document class for parent class: CdsDatatakeDuplicateds

    Generated from property: datastrip_pairs
    """

    overlap_percentage = Float()

    """Overlap percentage between the paired datastrips"""

    datastrips = Object(CdsDatatakeDuplicatedsDatastripPairsDatastrips)

    """Datastrips composing the duplicated pair"""


class CdsDatatakeDuplicateds(InnerDoc):
    """
    Inner document class for parent class: CdsDatatake

    Generated from property: duplicateds
    """

    items = Object(CdsDatatakeDuplicatedsItems)

    """Individual duplicated product pairs detected on this datatake"""

    pairs_count = Integer()

    """Total number of duplicated pairs detected on this datatake"""

    deletions = Object(CdsDatatakeDuplicatedsDeletions)

    """Per-interface summary of duplicated product deletions"""

    datastrip_pairs = Object(CdsDatatakeDuplicatedsDatastripPairs)

    """Datastrip-centric duplicated pairs (Sentinel-2)"""


class CdsDatatakeMissingPeriods(InnerDoc):
    """
    Inner document class for parent class: CdsDatatake

    Generated from property: missing_periods
    """

    name = Keyword()

    """Label of the missing period (e.g. Missing Product)"""

    product_type = Keyword()

    """Product type for which the sensing period is missing"""

    sensing_start_date = ZuluDate()

    """Start of the missing sensing period"""

    sensing_end_date = ZuluDate()

    """End of the missing sensing period"""

    duration = Long()

    """Duration of the missing sensing period in microseconds"""


class CdsDatatake(MAASDocument):
    """
    Mapping class for index: cds-datatake

    Generated from: resources/templates/cds-datatake_template.json
    """

    class Index:
        "inner class for DSL"

        name = "cds-datatake"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("cds-datatake")

    _PARTITION_FIELD = "observation_time_start"

    _PARTITION_FIELD_FORMAT = "s1-s2"

    absolute_orbit = Keyword()

    """Absolute orbit number of the datatake"""

    application_date = ZuluDate()

    """Application date extracted from the source mission planning report name"""

    cams_description = Keyword()

    """Description of the last attached CAMS ticket"""

    cams_origin = Keyword()

    """Origin of the last attached CAMS ticket"""

    cams_tickets = Keyword()

    """List of CAMS ticket identifiers linked to this datatake"""

    datastrip_ids = Keyword()

    """List of datastrip identifiers associated with this datatake"""

    datatake_id = Keyword()

    """Identifier of the datatake, the scheduled acquisition segment"""

    duplicateds = Object(CdsDatatakeDuplicateds)

    """Detected duplicated products and their deletion status for this datatake"""

    hex_datatake_id = Keyword()

    """Hexadecimal representation of the datatake identifier, set for Sentinel-1"""

    instrument_mode = Keyword()

    """Instrument mode of the acquisition"""

    instrument_swath = Keyword()

    """Instrument swath of the acquisition"""

    key = Keyword()

    """Unique document key built from the satellite unit and the datatake identifier"""

    l0_sensing_duration = Long()

    """Duration of the L0 sensing window in microseconds"""

    l0_sensing_time_start = ZuluDate()

    """Start time of the L0 sensing window"""

    l0_sensing_time_stop = ZuluDate()

    """Stop time of the L0 sensing window"""

    last_attached_ticket = Keyword()

    """Identifier of the most recently attached CAMS ticket"""

    last_attached_ticket_url = Keyword()

    """URL of the most recently attached CAMS ticket"""

    missing_periods = Object(CdsDatatakeMissingPeriods)

    """Sensing periods missing from the expected datatake coverage"""

    mission = Keyword()

    """Mission identifier derived from the satellite unit (e.g. S1, S2)"""

    name = Keyword()

    """Name of the source mission planning report this datatake was consolidated from"""

    number_of_expected_tiles = Integer()

    """Number of tiles expected for this datatake (Sentinel-2)"""

    number_of_scenes = Integer()

    """Number of scenes in the datatake, used to derive Sentinel-2 expected completeness"""

    observation_duration = Long()

    """Duration of the datatake observation in microseconds"""

    observation_time_start = ZuluDate()

    """Start time of the datatake observation"""

    observation_time_stop = ZuluDate()

    """Stop time of the datatake observation"""

    polarization = Keyword()

    """Polarization of the acquisition"""

    product_group_ids = Keyword()

    """List of product group identifiers associated with this datatake"""

    relative_orbit = Keyword()

    """Relative orbit number of the datatake"""

    satellite_unit = Keyword()

    """Satellite unit that acquired this datatake (e.g. S1A, S2B)"""

    timeliness = Keyword()

    """Timeliness category of the datatake"""

    updateTime = ZuluDate()

    """Date and time when this datatake document was last updated"""


class CdsDdpDataAvailable(MAASDocument):
    """
    Mapping class for index: cds-ddp-data-available

    Generated from: resources/templates/cds-ddp-data-available_template.json
    """

    class Index:
        "inner class for DSL"

        name = "cds-ddp-data-available"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("cds-ddp-data-available")

    _PARTITION_FIELD = "time_created"

    _PARTITION_FIELD_FORMAT = "static"

    data_size = Long()

    """Size of the available data in bytes"""

    interface_name = Keyword()

    """Name of the interface that provided the data"""

    mission = Keyword()

    """Mission the data belongs to (e.g. S1, S2, S3)"""

    production_service_name = Keyword()

    """Name of the production service that provided the data"""

    production_service_type = Keyword()

    """Type of the production service that provided the data"""

    satellite_unit = Keyword()

    """Satellite unit the data belongs to (e.g. S1A, S2B)"""

    session_id = Keyword()

    """Identifier of the DDP data-available session"""

    time_created = ZuluDate()

    """Time the data was created on the interface"""

    time_finished = ZuluDate()

    """Time the data transfer finished"""

    time_start = ZuluDate()

    """Start time of the data availability period"""

    time_stop = ZuluDate()

    """Stop time of the data availability period"""

    transfer_time = Long()

    """Duration of the data transfer"""

    updateTime = ZuluDate()

    """Timestamp of the last update of this consolidated document"""


class CdsDeletionIssue(MAASDocument):
    """
    Mapping class for index: cds-deletion-issue

    Generated from: resources/templates/cds-deletion-issue_template.json
    """

    class Index:
        "inner class for DSL"

        name = "cds-deletion-issue"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("cds-deletion-issue")

    created = ZuluDate()

    """Creation date of the deletion issue"""

    deletion_cause = Keyword()

    """Cause of the product deletion"""

    deletion_date = ZuluDate()

    """Date at which the product deletion is performed"""

    deletion_interfaces = Keyword()

    """List of interfaces on which the product must be deleted"""

    interface_name = Keyword()

    """Name of the interface concerned by the deletion issue"""

    interface_type = Keyword()

    """Type of interface concerned by the deletion issue"""

    key = Keyword()

    """Jira issue key of the deletion issue"""

    reportFolder = Keyword()

    """Folder of the source report this deletion issue was consolidated from"""

    satellite = Keyword()

    """Satellite unit concerned by the deletion issue"""

    status = Keyword()

    """Current status of the deletion issue"""

    updateTime = ZuluDate()

    """Timestamp of the last update of this consolidated document"""


class CdsDownlinkDatatake(MAASDocument):
    """
    Mapping class for index: cds-downlink-datatake

    Generated from: resources/templates/cds-downlink-datatake_template.json
    """

    class Index:
        "inner class for DSL"

        name = "cds-downlink-datatake"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("cds-downlink-datatake")

    _PARTITION_FIELD = "effective_downlink_start"

    _PARTITION_FIELD_FORMAT = "static"

    acquisition_absolute_orbit = Keyword()

    """Absolute orbit number of the acquisition"""

    acquisition_relative_orbit = Keyword()

    """Relative orbit number of the acquisition"""

    acquisition_start = ZuluDate()

    """Start time of the acquisition being downlinked"""

    acquisition_stop = ZuluDate()

    """Stop time of the acquisition being downlinked"""

    channel = Keyword()

    """Downlink channel"""

    datatake_id = Keyword()

    """Identifier of the datatake being downlinked"""

    delivery_stop = ZuluDate()

    """Time at which delivery of the downlinked data completed, derived from correlated acquisitions"""

    downlink_absolute_orbit = Keyword()

    """Absolute orbit number during the downlink"""

    downlink_duration = Long()

    """Duration of the downlink"""

    downlink_polarization = Keyword()

    """Polarization used for the downlink"""

    ds_product_name = Keyword()

    """Name of the datastrip product associated with the downlink"""

    ds_sensing_start_date = ZuluDate()

    """Sensing start date of the datastrip associated with the downlink"""

    effective_downlink_start = ZuluDate()

    """Effective start time of the downlink"""

    effective_downlink_stop = ZuluDate()

    """Effective stop time of the downlink"""

    expected_tiles = Keyword()

    """List of tiles expected from the datatake downlink (Sentinel-2)"""

    from_ds_sensing_to_downlink_stop_timeliness = Long()

    """Elapsed time from datastrip sensing to downlink delivery stop in microseconds"""

    from_sensing_to_delivery_stop_timeliness = Long()

    """Elapsed time from sensing to delivery stop in microseconds"""

    latency = Long()

    """Latency of the downlink"""

    mission = Keyword()

    """Mission identifier derived from the satellite unit (e.g. S1, S2)"""

    observation_time_start = ZuluDate()

    """Observation start time of the associated datatake"""

    partial = Keyword()

    """Flag indicating whether the downlink is partial"""

    satellite_unit = Keyword()

    """Satellite unit that performed the downlink (e.g. S1A, S2B)"""

    session_id = Keyword()

    """Downlink session identifier"""

    station = Keyword()

    """Ground or geostationary station that received the downlink"""

    updateTime = ZuluDate()

    """Date and time when this downlink datatake document was last updated"""


class CdsEdrsAcquisitionPassStatus(MAASDocument):
    """
    Mapping class for index: cds-edrs-acquisition-pass-status

    Generated from: resources/templates/cds-edrs-acquisition-pass-status_template.json
    """

    class Index:
        "inner class for DSL"

        name = "cds-edrs-acquisition-pass-status"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("cds-edrs-acquisition-pass-status")

    _PARTITION_FIELD = "planned_link_session_start"

    _PARTITION_FIELD_FORMAT = "product"

    archived_data_size = Float()

    """Size of the archived data for the link session"""

    cadus = Long()

    """Number of CADUs (Channel Access Data Units) processed during the link session"""

    cams_description = Keyword()

    """Description of the linked CAMS ticket(s)"""

    cams_origin = Keyword()

    """Origin of the linked CAMS ticket(s)"""

    cams_tickets = Keyword()

    """Identifiers of the CAMS tickets linked to this link session"""

    dcsu_archive_status = Keyword()

    """Status of the DCSU archiving step of the link session"""

    disseminated_data = Float()

    """Volume of disseminated data for the link session"""

    dissemination_start = ZuluDate()

    """Start time of the data dissemination"""

    dissemination_stop = ZuluDate()

    """Stop time of the data dissemination"""

    doy = Integer()

    """Day of year of the link session"""

    edte_acquisition_status = Keyword()

    """Status of the EDTE acquisition step of the link session"""

    fer = Float()

    """Frame error rate of the link session"""

    geo_satellite_id = Keyword()

    """Identifier of the geostationary relay satellite (EDRS node)"""

    ground_station = Keyword()

    """Ground station where the link session data was disseminated"""

    last_attached_ticket = Keyword()

    """Identifier of the last CAMS ticket attached to this link session"""

    last_attached_ticket_url = Keyword()

    """URL of the last CAMS ticket attached to this link session"""

    link_session_id = Keyword()

    """Identifier of the EDRS link session"""

    mission = Keyword()

    """Mission the satellite belongs to (e.g. S1, S2)"""

    moc_accept_status = Keyword()

    """Status of the MOC acceptance step of the link session"""

    notes = Keyword()

    """Free-text notes about the link session"""

    planned_link_session_start = ZuluDate()

    """Planned start time of the EDRS link session"""

    planned_link_session_stop = ZuluDate()

    """Planned stop time of the EDRS link session"""

    report_name_daily = Keyword()

    """Name of the daily source report the document was ingested from"""

    report_name_monthly = Keyword()

    """Name of the monthly source report the document was ingested from"""

    report_name_weekly = Keyword()

    """Name of the weekly source report the document was ingested from"""

    report_type = Keyword()

    """Type of the source report (daily, weekly or monthly)"""

    satellite_id = Keyword()

    """Identifier of the acquiring satellite"""

    sfdap_dissem_status = Keyword()

    """Status of the SFDAP dissemination step of the link session"""

    spacecraft_execution = Keyword()

    """Status of the spacecraft execution step of the link session"""

    total_status = Keyword()

    """Overall status of the link session, aggregating the individual processing step statuses"""

    updateTime = ZuluDate()

    """Timestamp of the last update of this document"""

    uplink_status = Keyword()

    """Status of the uplink step of the link session"""


class CdsExpected(MAASDocument):
    """
    Mapping class for index: cds-expected

    Generated from: resources/templates/cds-expected_template.json
    """

    class Index:
        "inner class for DSL"

        name = "cds-expected"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("cds-expected")

    daily_expected = Float()

    """Expected number of products for the given day"""

    date = ZuluDate()

    """Date the daily expected value applies to"""

    mission = Keyword()

    """Mission identifier the expected value applies to (e.g. S1, S2)"""

    product_type = Keyword()

    """Product type the expected value applies to"""

    provider = Keyword()

    """Provider or production service the expected value applies to"""

    satellite = Keyword()

    """Satellite the expected value applies to"""

    service_type = Keyword()

    """Service or interface type the expected value applies to"""


class CdsGrafanaUsage(MAASDocument):
    """
    Mapping class for index: cds-grafana-usage

    Generated from: resources/templates/cds-grafana-usage_template.json
    """

    class Index:
        "inner class for DSL"

        name = "cds-grafana-usage"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("cds-grafana-usage")

    _PARTITION_FIELD = "access_date"

    _PARTITION_FIELD_FORMAT = "%Y-%m"

    access_date = ZuluDate()

    """Date and time the Grafana dashboard was accessed"""

    dashboard_title = Keyword()

    """Title of the accessed Grafana dashboard"""

    dashboard_uid = Keyword()

    """Unique identifier of the accessed Grafana dashboard"""

    interface_name = Keyword()

    """Name of the interface associated with the access"""

    user = Keyword()

    """User who accessed the Grafana dashboard"""


class CdsHktmAcquisitionCompleteness(MAASDocument):
    """
    Mapping class for index: cds-hktm-acquisition-completeness

    Generated from: resources/templates/cds-hktm-acquisition-completeness_template.json
    """

    class Index:
        "inner class for DSL"

        name = "cds-hktm-acquisition-completeness"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("cds-hktm-acquisition-completeness")

    _PARTITION_FIELD = "ingestionTime"

    _PARTITION_FIELD_FORMAT = "static"

    absolute_orbit = Keyword()

    """Absolute orbit number of the HKTM acquisition"""

    cadip_completeness = Long()

    """CADIP acquisition completeness indicator: 1 if a matching OK CADIP pass status is found, 0 otherwise"""

    cams_description = Keyword()

    """Description reported by the attached CAMS anomaly ticket(s)"""

    cams_origin = Keyword()

    """Origin reported by the attached CAMS anomaly ticket(s)"""

    cams_tickets = Keyword()

    """CAMS anomaly ticket identifiers attached to this acquisition completeness"""

    channel = Long()

    """Acquisition channel number"""

    edrs_completeness = Long()

    """EDRS acquisition completeness indicator: 1 if a matching non-NOK EDRS pass status is found, 0 otherwise"""

    execution_time = ZuluDate()

    """Execution time of the acquisition, used to discard outdated raw documents (UTC)"""

    ground_station = Keyword()

    """Ground station that performed the HKTM acquisition"""

    interface_name = Keyword()

    """Name of the interface that provided the source report"""

    last_attached_ticket = Keyword()

    """Identifier of the most recently attached CAMS anomaly ticket"""

    last_attached_ticket_url = Keyword()

    """URL of the most recently attached CAMS anomaly ticket"""

    mission = Keyword()

    """Mission the HKTM acquisition belongs to (e.g. S1, S2)"""

    production_service_name = Keyword()

    """Name of the production service that generated the source report"""

    production_service_type = Keyword()

    """Type of the production service that generated the source report"""

    related_document_id = Keyword()

    """Identifier of the document correlated to this HKTM acquisition"""

    related_document_name = Keyword()

    """Name of the document correlated to this HKTM acquisition"""

    reportFolder = Keyword()

    """Folder of the source report"""

    satellite_unit = Keyword()

    """Satellite unit of the HKTM acquisition (e.g. S1A, S2B)"""

    session_id = Keyword()

    """Identifier of the acquisition session (CADIP or EDRS)"""

    session_id_full = Keyword()

    """Full acquisition session identifier"""


class CdsHktmProductionCompleteness(MAASDocument):
    """
    Mapping class for index: cds-hktm-production-completeness

    Generated from: resources/templates/cds-hktm-production-completeness_template.json
    """

    class Index:
        "inner class for DSL"

        name = "cds-hktm-production-completeness"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("cds-hktm-production-completeness")

    _PARTITION_FIELD = "ingestionTime"

    _PARTITION_FIELD_FORMAT = "static"

    absolute_orbit = Keyword()

    """Absolute orbit number associated with the HKTM sensing"""

    acquisition_duration = Long()

    """Duration of the HKTM acquisition in microseconds"""

    acquisition_start = ZuluDate()

    """Start of the HKTM acquisition window (UTC)"""

    acquisition_stop = ZuluDate()

    """End of the HKTM acquisition window (UTC)"""

    completeness = Long()

    """HKTM production completeness indicator: 1 if the expected HKTM product was produced, 0 otherwise"""

    datatake_id = Keyword()

    """Identifier of the datatake associated with the HKTM downlink"""

    downlink_absolute_orbit = Keyword()

    """Absolute orbit number during which the HKTM downlink occurred"""

    downlink_duration = Long()

    """Duration of the HKTM downlink in microseconds"""

    downlink_execution_time = ZuluDate()

    """Execution time of the HKTM downlink (UTC)"""

    downlink_start = ZuluDate()

    """Planned start of the HKTM downlink (UTC)"""

    downlink_stop = ZuluDate()

    """Planned end of the HKTM downlink (UTC)"""

    effective_downlink_start = ZuluDate()

    """Effective start of the HKTM downlink, used as reference time to correlate produced HKTM products (UTC)"""

    effective_downlink_stop = ZuluDate()

    """Effective end of the HKTM downlink (UTC)"""

    fos_pushing_date_backup = ZuluDate()

    """FOS backup pushing date of the related HKTM product (UTC)"""

    fos_pushing_date_nominal = ZuluDate()

    """FOS nominal pushing date of the related HKTM product (UTC)"""

    interface_name = Keyword()

    """Name of the interface that provided the source report"""

    latency = Long()

    """Latency of the HKTM downlink"""

    mission = Keyword()

    """Mission the HKTM downlink belongs to (e.g. S1, S2)"""

    number_of_scenes = Long()

    """Number of scenes associated with the HKTM downlink"""

    partial = Keyword()

    """Flag indicating whether the HKTM downlink is partial"""

    related_document_id = Keyword()

    """Identifier of the produced HKTM product proving completeness"""

    related_document_name = Keyword()

    """Name of the produced HKTM product proving completeness"""

    reportFolder = Keyword()

    """Folder of the source mission plan report"""

    satellite_unit = Keyword()

    """Satellite unit performing the HKTM downlink (e.g. S1A, S2B)"""

    station = Keyword()

    """Ground station performing the HKTM downlink"""

    x_off = ZuluDate()

    """X-Band downlink switch-off time (UTC)"""

    x_on = ZuluDate()

    """X-Band downlink switch-on time (UTC)"""


class CdsInterfaceProductDeletion(MAASDocument):
    """
    Mapping class for index: cds-interface-product-deletion

    Generated from: resources/templates/cds-interface-product-deletion_template.json
    """

    class Index:
        "inner class for DSL"

        name = "cds-interface-product-deletion"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("cds-interface-product-deletion")

    DD_DAS_status = Keyword()

    """Deletion status of the product on the DD/DAS interface"""

    LTA_Acri_status = Keyword()

    """Deletion status of the product on the LTA Acri interface"""

    LTA_CloudFerro_status = Keyword()

    """Deletion status of the product on the LTA CloudFerro interface"""

    LTA_Exprivia_status = Keyword()

    """Deletion status of the product on the LTA Exprivia interface"""

    LTA_S5P_DLR_status = Keyword()

    """Deletion status of the product on the LTA S5P DLR interface"""

    LTA_Werum_status = Keyword()

    """Deletion status of the product on the LTA Werum interface"""

    effective_product_name = Keyword()

    """Effective product name used to match the product across interfaces"""

    interface_type = Keyword()

    """Type of interface on which the deletion is tracked"""

    jira_issue = Keyword()

    """Jira issue key associated with the deletion request"""

    product_name = Keyword()

    """Name of the product to be deleted"""

    updateTime = ZuluDate()

    """Timestamp of the last update of this consolidated document"""


class CdsInterfaceStatus(MAASDocument):
    """
    Mapping class for index: cds-interface-status

    Generated from: resources/templates/cds-interface-status_template.json
    """

    class Index:
        "inner class for DSL"

        name = "cds-interface-status"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("cds-interface-status")

    _PARTITION_FIELD = "status_time_start"

    _PARTITION_FIELD_FORMAT = "monitoring"

    interface_name = Keyword()

    """Name of the monitored interface"""

    status = Keyword()

    """Availability status of the interface"""

    status_duration = Long()

    """Duration of the status period in seconds"""

    status_time_start = ZuluDate()

    """Start time of the interface status period"""

    status_time_stop = ZuluDate()

    """Stop time of the interface status period"""

    updateTime = ZuluDate()

    """Timestamp of the last update of this consolidated document"""


class CdsLtaDownloadQuota(MAASDocument):
    """
    Mapping class for index: cds-lta-download-quota

    Generated from: resources/templates/cds-lta-download-quota_template.json
    """

    class Index:
        "inner class for DSL"

        name = "cds-lta-download-quota"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("cds-lta-download-quota")

    _PARTITION_FIELD = "timestamp"

    _PARTITION_FIELD_FORMAT = "conf"

    daily_download_quota = Long()

    """Daily download quota for the service"""

    service_name = Keyword()

    """Name of the LTA service the quota applies to"""

    timestamp = ZuluDate()

    """Timestamp of the download quota record"""


class CdsMetricsProduct(MAASDocument):
    """
    Mapping class for index: cds-metrics-product

    Generated from: resources/templates/cds-metrics-product_template.json
    """

    class Index:
        "inner class for DSL"

        name = "cds-metrics-product"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("cds-metrics-product")

    _PARTITION_FIELD = "timestamp"

    _PARTITION_FIELD_FORMAT = "%Y"

    counter = Long()

    """Value of the metric counter"""

    interface_name = Keyword()

    """Name of the interface the metric originates from"""

    metric_name = Keyword()

    """Metric action derived from the raw name, such as archived or download"""

    metric_type = Keyword()

    """Type of the metric as provided by the source"""

    mission = Keyword()

    """Short mission name derived from the metric name (e.g. S1, S2)"""

    name = Keyword()

    """Raw metric name from the source, parsed to derive the metric, product type, mission and satellite unit (e.g. Archived.<productType>.<mission>.<unit>.<metricType>)"""

    product_type = Keyword()

    """Product type derived from the metric name"""

    production_service_name = Keyword()

    """Name of the production service associated with the metric"""

    production_service_type = Keyword()

    """Type of the production service associated with the metric"""

    satellite_unit = Keyword()

    """Satellite unit derived from the metric name (e.g. S1A)"""

    timestamp = ZuluDate()

    """Timestamp of the metric measurement"""

    updateTime = ZuluDate()

    """Date and time when this consolidated metric document was last updated by the consolidation engine"""


class CdsProduct(MAASDocument):
    """
    Mapping class for index: cds-product

    Generated from: resources/templates/cds-product_template.json
    """

    class Index:
        "inner class for DSL"

        name = "cds-product"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("cds-product")

    _PARTITION_FIELD = "sensing_start_date"

    _PARTITION_FIELD_FORMAT = "%Y-%m"

    EU_coverage_percentage = Float()

    """Percentage of the product footprint intersecting the European coverage mask (S1)"""

    absolute_orbit = Keyword()

    """Absolute orbit number during which the product was acquired"""

    auxip_id = Keyword()

    """Product identifier on the AUXIP (auxiliary data) interface"""

    auxip_publication_date = ZuluDate()

    """Date the product was published on the AUXIP (auxiliary data) interface"""

    cams_description = Keyword()

    """Description of the attached CAMS anomaly ticket"""

    cams_origin = Keyword()

    """Origin (root cause category) reported by the attached CAMS anomaly ticket"""

    cams_tickets = Keyword()

    """Identifiers of the CAMS anomaly tickets correlated to this product"""

    centre = Keyword()

    """Processing centre parsed from the product name (S3-specific)"""

    cloud_cover = Float()

    """Cloud cover percentage of the product"""

    collection_number = Keyword()

    """Collection number of the product"""

    content_length = Long()

    """Size of the product content, in bytes"""

    dataflow_status = Keyword()

    """Dataflow processing status of the product"""

    datastrip_id = Keyword()

    """Identifier of the datastrip the product is associated with"""

    datatake_cams_ticket = Keyword()

    """CAMS anomaly ticket propagated from the product's datatake"""

    datatake_id = Keyword()

    """Identifier of the datatake (acquisition segment) the product belongs to"""

    ddcreodias_id = Keyword()

    """Product identifier on the CreoDIAS dissemination interface"""

    ddcreodias_name = Keyword()

    """Product name on the CreoDIAS dissemination interface"""

    ddcreodias_publication_date = ZuluDate()

    """Date the product was published on the CreoDIAS dissemination interface"""

    dddas_id = Keyword()

    """Product identifier on the DAS (Data Access Service) dissemination interface"""

    dddas_name = Keyword()

    """Product name on the DAS (Data Access Service) dissemination interface"""

    dddas_publication_date = ZuluDate()

    """Date the product was published on the DAS dissemination interface"""

    ddip_id = Keyword()

    """Product identifier on the DD DHUS (data dissemination) interface"""

    ddip_name = Keyword()

    """Product name on the DD DHUS (data dissemination) interface"""

    ddip_publication_date = ZuluDate()

    """Date the product was published on the DD DHUS interface"""

    detector_id = Keyword()

    """Detector identifier parsed from the product name (S2-specific)"""

    expected_lta_number = Integer()

    """Number of LTA (Long Term Archive) services expected to serve this product"""

    expected_tiles = Keyword()

    """List of S2 grid tiles the product footprint is expected to cover"""

    fos_pushing_date_backup = ZuluDate()

    """Date the product was pushed by the FOS through the backup channel"""

    fos_pushing_date_nominal = ZuluDate()

    """Date the product was pushed by the FOS through the nominal channel"""

    from_prip_ddcreodias_timeliness = Long()

    """Time elapsed between PRIP publication and CreoDIAS publication, in microseconds"""

    from_prip_dddas_timeliness = Long()

    """Time elapsed between PRIP publication and DAS publication, in microseconds"""

    from_prip_ddip_timeliness = Long()

    """Time elapsed between PRIP publication and DD DHUS publication, in microseconds"""

    hex_datatake_id = Keyword()

    """Datatake identifier in hexadecimal form"""

    instrument_mode = Keyword()

    """Instrument acquisition mode of the product"""

    instrument_swath = Keyword()

    """Instrument swath of the product (S1-specific)"""

    key = Keyword()

    """Unique consolidated product identifier (MD5 hash of the product name without extension)"""

    last_attached_ticket = Keyword()

    """Identifier of the most recently attached CAMS anomaly ticket"""

    last_attached_ticket_url = Keyword()

    """URL of the most recently attached CAMS anomaly ticket"""

    mission = Keyword()

    """Mission identifier the product belongs to (e.g. S1, S2, S3, S5)"""

    name = Keyword()

    """Product name as delivered by the source interface"""

    nb_lta_served = Integer()

    """Number of LTA (Long Term Archive) services that have served this product"""

    platform = Keyword()

    """Platform identifier parsed from the product name (S3-specific)"""

    polarization = Keyword()

    """Radar polarization of the product (S1-specific)"""

    prip_id = Keyword()

    """Product identifier on the PRIP (Production Interface Delivery Point)"""

    prip_publication_date = ZuluDate()

    """Date the product was published on the PRIP interface"""

    prip_service = Keyword()

    """Name of the PRIP interface that published the product"""

    processor_version = Keyword()

    """Version of the processor that generated the product"""

    product_class = Keyword()

    """Product class parsed from the product name (S1-specific)"""

    product_discriminator_date = ZuluDate()

    """Product discriminator (creation) date used to distinguish reprocessed products"""

    product_granularity = Keyword()

    """Product granularity parsed from the product name (S2-specific)"""

    product_group_id = Keyword()

    """Product group identifier used to link related products (e.g. S2 datastrip/granule grouping)"""

    product_level = Keyword()

    """Processing level of the product, resolved from the dataflow configuration"""

    product_type = Keyword()

    """Product type as parsed from the product name"""

    quality_control = Keyword()

    """Quality control status of the product"""

    quality_status = Keyword()

    """Quality status of the product as reported by the source interface"""

    relative_orbit = Keyword()

    """Relative orbit number during which the product was acquired"""

    satellite_unit = Keyword()

    """Satellite unit that produced the product (e.g. S1A, S2B)"""

    sensing_duration = Long()

    """Length of the sensing window, in microseconds (sensing_end_date minus sensing_start_date)"""

    sensing_end_date = ZuluDate()

    """Sensing end date of the product observation window"""

    sensing_start_date = ZuluDate()

    """Sensing start date of the product observation window"""

    site_center = Keyword()

    """Processing/production centre that generated the product"""

    tile_number = Keyword()

    """S2 tile (granule) number parsed from the product name (S2-specific)"""

    timeliness = Keyword()

    """Timeliness category of the product (e.g. NRT, NTC), inherited from its datatake for S1/S2"""

    updateTime = ZuluDate()

    """Timestamp of the last update of this consolidated document"""


class CdsPublication(MAASDocument):
    """
    Mapping class for index: cds-publication

    Generated from: resources/templates/cds-publication_template.json
    """

    class Index:
        "inner class for DSL"

        name = "cds-publication"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("cds-publication")

    _PARTITION_FIELD = "sensing_start_date"

    _PARTITION_FIELD_FORMAT = "%Y-%m"

    absolute_orbit = Keyword()

    """Absolute orbit number during which the product was acquired"""

    cams_description = Keyword()

    """Description of the attached CAMS anomaly ticket"""

    cams_origin = Keyword()

    """Origin (root cause category) reported by the attached CAMS anomaly ticket"""

    cams_tickets = Keyword()

    """Identifiers of the CAMS anomaly tickets correlated to this publication"""

    centre = Keyword()

    """Processing centre parsed from the product name (S3-specific)"""

    cloud_cover = Float()

    """Cloud cover percentage of the product"""

    collection_number = Keyword()

    """Collection number of the product"""

    content_length = Long()

    """Size of the published product content, in bytes"""

    datastrip_id = Keyword()

    """Identifier of the datastrip the product is associated with"""

    datatake_cams_ticket = Keyword()

    """CAMS anomaly ticket propagated from the publication's datatake"""

    datatake_id = Keyword()

    """Identifier of the datatake (acquisition segment) the product belongs to"""

    deletion_cause = Keyword()

    """Cause of the publication deletion, as reported by the deletion issue"""

    deletion_date = ZuluDate()

    """Date the publication was deleted from the service"""

    deletion_issue = Keyword()

    """Jira/CAMS issue key that triggered the deletion of this publication"""

    eviction_date = ZuluDate()

    """Date the product is scheduled to be evicted from the publishing service"""

    expected = Boolean()

    """Whether this publication was expected"""

    fos_pushing_date_backup = ZuluDate()

    """Date the product was pushed by the FOS through the backup channel"""

    fos_pushing_date_nominal = ZuluDate()

    """Date the product was pushed by the FOS through the nominal channel"""

    from_sensing_time = Long()

    """Time between sensing end and publication, in seconds"""

    from_sensing_timeliness = Long()

    """Time elapsed between sensing end date and publication date, in microseconds"""

    hex_datatake_id = Keyword()

    """Datatake identifier in hexadecimal form"""

    instrument_mode = Keyword()

    """Instrument acquisition mode of the product"""

    instrument_swath = Keyword()

    """Instrument swath of the product (S1-specific)"""

    key = Keyword()

    """Unique consolidated publication identifier (MD5 hash of the source interface name and product name)"""

    last_attached_ticket = Keyword()

    """Identifier of the most recently attached CAMS anomaly ticket"""

    last_attached_ticket_url = Keyword()

    """URL of the most recently attached CAMS anomaly ticket"""

    mission = Keyword()

    """Mission identifier the product belongs to (e.g. S1, S2, S3, S5)"""

    modification_date = ZuluDate()

    """Date the product was last modified on the publishing service"""

    name = Keyword()

    """Product name as delivered by the publishing interface"""

    origin_date = ZuluDate()

    """Date the product became available at the producer (origin) before publication"""

    platform = Keyword()

    """Platform identifier parsed from the product name (S3-specific)"""

    polarization = Keyword()

    """Radar polarization of the product (S1-specific)"""

    processor_version = Keyword()

    """Version of the processor that generated the product"""

    product_class = Keyword()

    """Product class parsed from the product name (S1-specific)"""

    product_discriminator_date = ZuluDate()

    """Product discriminator (creation) date used to distinguish reprocessed products"""

    product_granularity = Keyword()

    """Product granularity parsed from the product name (S2-specific)"""

    product_group_id = Keyword()

    """Product group identifier used to link related products (e.g. S2 datastrip/granule grouping)"""

    product_level = Keyword()

    """Processing level of the product, resolved from the dataflow configuration"""

    product_type = Keyword()

    """Product type as parsed from the product name"""

    product_uuid = Keyword()

    """UUID of the product on the publishing service"""

    publication_count = Long()

    """Number of publications recorded for the product"""

    publication_date = ZuluDate()

    """Date the product was published on the service"""

    quality_control = Keyword()

    """Quality control status of the product"""

    quality_status = Keyword()

    """Quality status of the product as reported by the source interface"""

    relative_orbit = Keyword()

    """Relative orbit number during which the product was acquired"""

    satellite_unit = Keyword()

    """Satellite unit that produced the product (e.g. S1A, S2B)"""

    sensing_duration = Long()

    """Length of the sensing window, in microseconds (sensing_end_date minus sensing_start_date)"""

    sensing_end_date = ZuluDate()

    """Sensing end date of the product observation window"""

    sensing_start_date = ZuluDate()

    """Sensing start date of the product observation window"""

    service_id = Keyword()

    """Identifier/name of the production/dissemination service that published the product"""

    service_type = Keyword()

    """Type of the production/dissemination service that published the product"""

    site_center = Keyword()

    """Processing/production centre that generated the product"""

    tile_number = Keyword()

    """S2 tile (granule) number parsed from the product name (S2-specific)"""

    timeliness = Keyword()

    """Timeliness category of the product (e.g. NRT, NTC), inherited from its datatake for S1/S2"""

    transfer_time = Long()

    """Transfer time of the product, in seconds"""

    transfer_timeliness = Long()

    """Time elapsed between origin date and publication date, in microseconds"""

    updateTime = ZuluDate()

    """Timestamp of the last update of this consolidated document"""

    within_from_sensing_timeliness = Long()

    """Whether the publication met the from-sensing timeliness target, as a percentage"""

    within_transfer_timeliness = Long()

    """Whether the publication met the transfer timeliness target, as a percentage"""


class CdsS2Tilpar(MAASDocument):
    """
    Mapping class for index: cds-s2-tilpar

    Generated from: resources/templates/cds-s2-tilpar_template.json
    """

    class Index:
        "inner class for DSL"

        name = "cds-s2-tilpar"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("cds-s2-tilpar")

    _PARTITION_FIELD = "timestamp"

    _PARTITION_FIELD_FORMAT = "tiles"

    geometry = GeoShape()

    """Geographic shape (footprint) of the Sentinel-2 tile"""

    name = Keyword()

    """Name of the Sentinel-2 tile"""

    timestamp = ZuluDate()

    """Timestamp of the tile document"""


class CdsS3Completeness(MAASDocument):
    """
    Mapping class for index: cds-s3-completeness

    Generated from: resources/templates/cds-s3-completeness_template.json
    """

    class Index:
        "inner class for DSL"

        name = "cds-s3-completeness"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("cds-s3-completeness")

    _PARTITION_FIELD = "observation_time_start"

    _PARTITION_FIELD_FORMAT = "static"

    cams_description = Keyword()

    """Description of the last attached CAMS ticket"""

    cams_origin = Keyword()

    """Origin of the last attached CAMS ticket"""

    cams_tickets = Keyword()

    """List of CAMS ticket identifiers linked to this completeness"""

    datatake_id = Keyword()

    """Identifier of the datatake this completeness is computed for"""

    expected = Long()

    """Expected sensing value for the product type, in microseconds, including tolerance"""

    key = Keyword()

    """Unique document key built from the datatake identifier, product type and timeliness"""

    last_attached_ticket = Keyword()

    """Identifier of the most recently attached CAMS ticket"""

    last_attached_ticket_url = Keyword()

    """URL of the most recently attached CAMS ticket"""

    mission = Keyword()

    """Mission identifier derived from the satellite unit (S3)"""

    observation_duration = Long()

    """Duration of the observation period in microseconds"""

    observation_time_start = ZuluDate()

    """Start of the observation period covered by this completeness"""

    observation_time_stop = ZuluDate()

    """Stop of the observation period covered by this completeness"""

    percentage = Long()

    """Completeness percentage of adjusted value over expected value"""

    product_level = Keyword()

    """Product level of the product type (e.g. L0_, L1, L2)"""

    product_type = Keyword()

    """Product type this completeness applies to"""

    satellite_unit = Keyword()

    """Satellite unit this completeness applies to (e.g. S3A, S3B)"""

    status = Keyword()

    """Completeness status label derived from the percentage"""

    timeliness = Keyword()

    """Timeliness of the products this completeness applies to"""

    updateTime = ZuluDate()

    """Date and time when this Sentinel-3 completeness document was last updated"""

    value = Long()

    """Measured completeness value, total sensing of the produced products in microseconds"""

    value_adjusted = Long()

    """Completeness value capped at the expected value to avoid percentages above 100%"""


class CdsS5Completeness(MAASDocument):
    """
    Mapping class for index: cds-s5-completeness

    Generated from: resources/templates/cds-s5-completeness_template.json
    """

    class Index:
        "inner class for DSL"

        name = "cds-s5-completeness"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("cds-s5-completeness")

    _PARTITION_FIELD = "observation_time_start"

    _PARTITION_FIELD_FORMAT = "static"

    absolute_orbit = Keyword()

    """Absolute orbit number this completeness applies to"""

    cams_description = Keyword()

    """Description of the last attached CAMS ticket"""

    cams_origin = Keyword()

    """Origin of the last attached CAMS ticket"""

    cams_tickets = Keyword()

    """List of CAMS ticket identifiers linked to this completeness"""

    datatake_id = Keyword()

    """Identifier of the datatake this completeness is computed for"""

    expected = Long()

    """Expected sensing value for the product type, in microseconds, including tolerance"""

    key = Keyword()

    """Unique document key built from the datatake identifier and product type"""

    last_attached_ticket = Keyword()

    """Identifier of the most recently attached CAMS ticket"""

    last_attached_ticket_url = Keyword()

    """URL of the most recently attached CAMS ticket"""

    mission = Keyword()

    """Mission identifier derived from the satellite unit (S5)"""

    observation_duration = Long()

    """Duration of the observation period in microseconds"""

    observation_time_start = ZuluDate()

    """Start of the observation period covered by this completeness"""

    observation_time_stop = ZuluDate()

    """Stop of the observation period covered by this completeness"""

    percentage = Long()

    """Completeness percentage of adjusted sensing value over expected value"""

    product_level = Keyword()

    """Product level of the product type (e.g. L0_, L1B, L2_)"""

    product_type = Keyword()

    """Product type this completeness applies to"""

    satellite_unit = Keyword()

    """Satellite unit this completeness applies to (e.g. S5P)"""

    slice_expected = Long()

    """Expected number of product slices for this product type"""

    slice_value = Long()

    """Number of product slices produced for this completeness"""

    status = Keyword()

    """Completeness status label derived from the percentage"""

    timeliness = Keyword()

    """Timeliness of the products this completeness applies to (e.g. NRTI, OFFL, OPER)"""

    updateTime = ZuluDate()

    """Date and time when this Sentinel-5P completeness document was last updated"""

    value = Long()

    """Measured sensing completeness value, total sensing of the produced products in microseconds"""

    value_adjusted = Long()

    """Sensing completeness value capped at the expected value to avoid percentages above 100%"""


class CdsSatUnavailability(MAASDocument):
    """
    Mapping class for index: cds-sat-unavailability

    Generated from: resources/templates/cds-sat-unavailability_template.json
    """

    class Index:
        "inner class for DSL"

        name = "cds-sat-unavailability"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("cds-sat-unavailability")

    _PARTITION_FIELD = "start_time"

    _PARTITION_FIELD_FORMAT = "static"

    comment = Keyword()

    """Free-text comment associated with the unavailability"""

    end_anx_offset = Integer()

    """Offset from the ascending node crossing at the end of the unavailability"""

    end_orbit = Keyword()

    """Orbit number at the end of the unavailability, with leading zeros stripped"""

    end_time = ZuluDate()

    """End date and time of the unavailability period, empty while the unavailability is still ongoing"""

    file_name = Keyword()

    """Name of the source unavailability file the record was ingested from"""

    key = Keyword()

    """Document identifier computed as an MD5 hash of mission, subsystem and start_time"""

    mission = Keyword()

    """Mission identifier derived from the satellite unit (e.g. S1, S2)"""

    raw_data_ingestion_time = ZuluDate()

    """Ingestion time of the source raw unavailability data, used to arbitrate between concurrent updates"""

    real_causal_anomaly = Keyword()

    """Set to PDHT when an S1 OCP or SAR unavailability shares its file with a PDHT subsystem entry, indicating the real causal anomaly"""

    satellite_unit = Keyword()

    """Satellite unit affected by the unavailability (e.g. S1A)"""

    start_anx_offset = Integer()

    """Offset from the ascending node crossing at the start of the unavailability"""

    start_orbit = Keyword()

    """Orbit number at the start of the unavailability, with leading zeros stripped"""

    start_time = ZuluDate()

    """Start date and time of the unavailability period"""

    subsystem = Keyword()

    """Satellite subsystem concerned by the unavailability"""

    type = Keyword()

    """Category of the unavailability record as declared in the source file"""

    unavailability_duration = Long()

    """Duration of the unavailability period in microseconds, computed from start_time and end_time"""

    unavailability_reference = Keyword()

    """Reference identifier of the unavailability declaration"""

    unavailability_type = Keyword()

    """Type of unavailability as declared in the source file"""

    updateTime = ZuluDate()

    """Date and time when this consolidated unavailability document was last updated by the consolidation engine"""


class CreodiasProduct(MAASRawDocument):
    """
    Mapping class for index: raw-data-creodias-product

    Generated from: resources/templates/raw-data-creodias-product_template.json
    """

    class Index:
        "inner class for DSL"

        name = "raw-data-creodias-product"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("raw-data-creodias-product")

    _PARTITION_FIELD = "ingestionTime"

    _PARTITION_FIELD_FORMAT = "%Y"

    content_length = Long()

    """Product file size in bytes (OData ContentLength)"""

    end_date = ZuluDate()

    """Product sensing end date (ContentDate End)"""

    footprint = Keyword()

    """Geographic footprint of the product as reported by the CreoDIAS interface"""

    ingestion_date = ZuluDate()

    """Date the product was ingested into the CreoDIAS interface (IngestionDate)"""

    interface_name = Keyword()

    """Name of the CreoDIAS interface instance the product was collected from"""

    modification_date = ZuluDate()

    """Last modification date of the product on the CreoDIAS interface (ModificationDate)"""

    online = Boolean()

    """Whether the product is currently online and available for download on the CreoDIAS interface"""

    origin_date = ZuluDate()

    """Product origin date at the source (OriginDate)"""

    product_id = Keyword()

    """Product identifier from the CreoDIAS interface (OData Id)"""

    product_name = Keyword()

    """Product file name from the CreoDIAS interface (OData Name)"""

    production_service_name = Keyword()

    """Name of the CreoDIAS production service instance providing the product"""

    production_service_type = Keyword()

    """Type of the production service providing the product (DD)"""

    publication_date = ZuluDate()

    """Date the product was published on the CreoDIAS interface (PublicationDate)"""

    reportFolder = Keyword()

    """Folder or path of the source report file from which this record was extracted"""

    s3_path = Keyword()

    """Path of the product in the CreoDIAS S3 object storage"""

    start_date = ZuluDate()

    """Product sensing start date (ContentDate Start)"""


class DasProduct(MAASRawDocument):
    """
    Mapping class for index: raw-data-das-product

    Generated from: resources/templates/raw-data-das-product_template.json
    """

    class Index:
        "inner class for DSL"

        name = "raw-data-das-product"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("raw-data-das-product")

    _PARTITION_FIELD = "ingestionTime"

    _PARTITION_FIELD_FORMAT = "%Y"

    content_length = Long()

    """Product file size in bytes (OData ContentLength)"""

    end_date = ZuluDate()

    """Product sensing end date (OData ContentDate.End)"""

    eviction_date = ZuluDate()

    """Date the product is scheduled to be evicted from the DD/DAS interface (OData EvictionDate)"""

    interface_name = Keyword()

    """Name of the DD/DAS interface instance the product was collected from (DD_DAS)"""

    modification_date = ZuluDate()

    """Last modification date of the product on the DD/DAS interface (OData ModificationDate)"""

    origin_date = ZuluDate()

    """Product origin date at the source (OData OriginDate)"""

    product_id = Keyword()

    """Product identifier from the DD/DAS interface (OData Id)"""

    product_name = Keyword()

    """Product file name from the DD/DAS interface (OData Name)"""

    production_service_name = Keyword()

    """Name of the production service instance providing the product (DAS)"""

    production_service_type = Keyword()

    """Type of the production service providing the product (DD)"""

    publication_date = ZuluDate()

    """Date the product was published on the DD/DAS interface (OData PublicationDate)"""

    start_date = ZuluDate()

    """Product sensing start date (OData ContentDate.Start)"""


class Databudget(MAASRawDocument):
    """
    Mapping class for index: raw-data-databudget

    Generated from: resources/templates/raw-data-databudget_template.json
    """

    class Index:
        "inner class for DSL"

        name = "raw-data-databudget"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("raw-data-databudget")

    _PARTITION_FIELD = "ingestionTime"

    _PARTITION_FIELD_FORMAT = "conf"

    archived = Keyword()

    """Expected archived volume/count from the 'A' column"""

    disseminated = Keyword()

    """Expected disseminated volume/count from the 'D' column"""

    level = Keyword()

    """Processing level from the 'Level' column ('AUX' for the auxiliary databudget)"""

    mission = Keyword()

    """Mission from the 'Mission' column of the Databudget CSV"""

    num_day = Keyword()

    """Expected number of products per day from the '#Num/day' column"""

    produced = Keyword()

    """Expected produced volume/count from the 'P' column"""

    reportFolder = Keyword()

    """Folder path of the source Databudget report file"""

    timeliness = Keyword()

    """Timeliness from the 'Timeliness' column ('AUX' for the auxiliary databudget)"""

    type = Keyword()

    """Product type from the 'TYPE' column of the Databudget CSV"""

    version = Keyword()

    """Databudget version from the 'Version' column"""

    volume_day = Keyword()

    """Expected volume per day in GB from the 'Volume per day [GB]' column"""


class DdArchive(MAASRawDocument):
    """
    Mapping class for index: raw-data-dd-archive

    Generated from: resources/templates/raw-data-dd-archive_template.json
    """

    class Index:
        "inner class for DSL"

        name = "raw-data-dd-archive"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("raw-data-dd-archive")

    _PARTITION_FIELD = "ingestion_date"

    _PARTITION_FIELD_FORMAT = "%Y"

    content_length = Long()

    """Product file size in bytes (CSV ContentLength)"""

    end_date = ZuluDate()

    """Product sensing end date (CSV ContentDate:End)"""

    ingestion_date = ZuluDate()

    """Date the product was ingested into the DHUS archive (CSV IngestionDate)"""

    product_id = Keyword()

    """Product identifier from the DHUS archive catalogue (CSV Id)"""

    product_name = Keyword()

    """Product file name from the DHUS archive catalogue (CSV Name)"""

    reportFolder = Keyword()

    """Folder or path of the source catalogue CSV file from which this record was extracted"""

    start_date = ZuluDate()

    """Product sensing start date (CSV ContentDate:Start)"""


class DdProduct(MAASRawDocument):
    """
    Mapping class for index: raw-data-dd-product

    Generated from: resources/templates/raw-data-dd-product_template.json
    """

    class Index:
        "inner class for DSL"

        name = "raw-data-dd-product"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("raw-data-dd-product")

    _PARTITION_FIELD = "ingestionTime"

    _PARTITION_FIELD_FORMAT = "%Y"

    content_length = Long()

    """Product file size in bytes (OData ContentLength)"""

    creation_date = ZuluDate()

    """Date the product was created on the DD (DHUS) interface, used as the publication date"""

    end_date = ZuluDate()

    """Product sensing end date (ContentDate End)"""

    ingestion_date = ZuluDate()

    """Date the product was ingested into the DD (DHUS) interface (IngestionDate)"""

    interface_name = Keyword()

    """Name of the DD (DHUS) interface instance the product was collected from"""

    modification_date = ZuluDate()

    """Last modification date of the product on the DD (DHUS) interface (ModificationDate)"""

    product_id = Keyword()

    """Product identifier from the DD (DHUS) interface (OData Id)"""

    product_name = Keyword()

    """Product file name from the DD (DHUS) interface (OData Name)"""

    production_service_name = Keyword()

    """Name of the DD production service instance providing the product"""

    production_service_type = Keyword()

    """Type of the production service providing the product (DD)"""

    reportFolder = Keyword()

    """Folder or path of the source report file from which this record was extracted"""

    start_date = ZuluDate()

    """Product sensing start date (ContentDate Start)"""


class DdpDataAvailable(MAASRawDocument):
    """
    Mapping class for index: raw-data-ddp-data-available

    Generated from: resources/templates/raw-data-ddp-data-available_template.json
    """

    class Index:
        "inner class for DSL"

        name = "raw-data-ddp-data-available"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("raw-data-ddp-data-available")

    _PARTITION_FIELD = "ingestionTime"

    _PARTITION_FIELD_FORMAT = "static"

    data_size = Long()

    """Data size of the session extracted from the DSIB file"""

    interface_name = Keyword()

    """Name of the source DDP interface (DDP_EDRS_EDIP)"""

    production_service_name = Keyword()

    """Name of the production service (EDRS_EDIP)"""

    production_service_type = Keyword()

    """Type of the production service (DDP)"""

    reportFolder = Keyword()

    """Folder path of the source DSIB report file"""

    session_id = Keyword()

    """DDP session identifier extracted from the DSIB file"""

    time_created = ZuluDate()

    """DSIB creation time extracted from the DSIB file"""

    time_finished = ZuluDate()

    """Session finished time extracted from the DSIB file"""

    time_start = ZuluDate()

    """Session start time extracted from the DSIB file"""

    time_stop = ZuluDate()

    """Session stop time extracted from the DSIB file"""


class DeletionIssue(MAASRawDocument):
    """
    Mapping class for index: raw-data-deletion-issue

    Generated from: resources/templates/raw-data-deletion-issue_template.json
    """

    class Index:
        "inner class for DSL"

        name = "raw-data-deletion-issue"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("raw-data-deletion-issue")

    _PARTITION_FIELD = "ingestionTime"

    _PARTITION_FIELD_FORMAT = "static"

    created = ZuluDate()

    """Creation date of the Jira deletion issue"""

    deletion_cause = Keyword()

    """Cause of the deletion (from the Jira deletion-cause custom field)"""

    deletion_date = ZuluDate()

    """Requested deletion date (from the Jira deletion-date custom field)"""

    deletion_interfaces = Keyword()

    """Interfaces from which the product must be deleted (from the Jira deletion-interfaces custom field)"""

    interface_name = Keyword()

    """Name of the source Jira deletion interface (e.g. Jira_OMCS_Deletion_CDSE, Jira_OMCS_Deletion_LTA)"""

    interface_type = Keyword()

    """Type of interface targeted by the deletion ('DD' for datahub, 'LTA' for long term archive)"""

    key = Keyword()

    """Jira issue key of the deletion issue (from the issue 'key' field)"""

    reportFolder = Keyword()

    """Folder path of the source report file"""

    satellite = Keyword()

    """Satellite concerned by the deletion issue"""

    status = Keyword()

    """Status of the Jira deletion issue"""


class DownloadVolumeCount(MAASRawDocument):
    """
    Mapping class for index: raw-data-download-volume-count

    Generated from: resources/templates/raw-data-download-volume-count_template.json
    """

    class Index:
        "inner class for DSL"

        name = "raw-data-download-volume-count"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("raw-data-download-volume-count")

    _PARTITION_FIELD = "ingestionTime"

    _PARTITION_FIELD_FORMAT = "statistics"

    instrument = Keyword()

    """Instrument the download volume statistics relate to"""

    interface_name = Keyword()

    """Name of the interface the download volume statistics relate to"""

    mission = Keyword()

    """Mission the download volume statistics relate to"""

    number = Long()

    """Total number of downloaded products"""

    number_increase = Long()

    """Increase in the number of downloaded products compared to the previous count"""

    reportFolder = Keyword()

    """Folder path of the source report file"""

    type = Keyword()

    """Product type the download volume statistics relate to"""

    volume = Long()

    """Total downloaded volume"""

    volume_increase = Long()

    """Increase in downloaded volume compared to the previous count"""


class GrafanaUsage(MAASRawDocument):
    """
    Mapping class for index: raw-data-grafana-usage

    Generated from: resources/templates/raw-data-grafana-usage_template.json
    """

    class Index:
        "inner class for DSL"

        name = "raw-data-grafana-usage"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("raw-data-grafana-usage")

    _PARTITION_FIELD = "ingestionTime"

    _PARTITION_FIELD_FORMAT = "%Y-%m"

    access_date = ZuluDate()

    """Grafana access timestamp from the Loki log stream 't' field"""

    dashboard = Keyword()

    """Accessed dashboard path from the Loki log stream 'path' field"""

    interface_name = Keyword()

    """Name of the source Grafana usage interface (e.g. Grafana_Usage_Prod)"""

    user = Keyword()

    """User name that accessed Grafana from the Loki log stream 'uname' field"""


class InterfaceProbe(MAASRawDocument):
    """
    Mapping class for index: raw-data-interface-probe

    Generated from: resources/templates/raw-data-interface-probe_template.json
    """

    class Index:
        "inner class for DSL"

        name = "raw-data-interface-probe"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("raw-data-interface-probe")

    _PARTITION_FIELD = "ingestionTime"

    _PARTITION_FIELD_FORMAT = "monitoring"

    details = Keyword()

    """Probe details from the monitoring 'details' field"""

    interface_name = Keyword()

    """Name of the probed interface from the monitoring 'interface_name' field"""

    most_recent_modification_date = ZuluDate()

    """Most recent modification date from the monitoring 'most_recent_modification_date' field"""

    probe_duration = Float()

    """Probe duration from the monitoring 'probe_duration' field"""

    probe_time_start = ZuluDate()

    """Probe start time from the monitoring 'probe_time_start' field"""

    probe_time_stop = ZuluDate()

    """Probe stop time from the monitoring 'probe_time_end' field"""

    reportFolder = Keyword()

    """Folder path of the source monitoring report file"""

    status = Keyword()

    """Probe result status from the monitoring 'status' field"""

    status_code = Integer()

    """Probe HTTP/response status code from the monitoring 'status_code' field"""


class LtaProduct(MAASRawDocument):
    """
    Mapping class for index: raw-data-lta-product

    Generated from: resources/templates/raw-data-lta-product_template.json
    """

    class Index:
        "inner class for DSL"

        name = "raw-data-lta-product"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("raw-data-lta-product")

    _PARTITION_FIELD = "ingestionTime"

    _PARTITION_FIELD_FORMAT = "%Y-%m"

    content_length = Long()

    """Product file size in bytes (OData ContentLength)"""

    end_date = ZuluDate()

    """Product sensing end date (OData ContentDate.End)"""

    eviction_date = ZuluDate()

    """Date the product is scheduled to be evicted from the LTA interface (OData EvictionDate)"""

    interface_name = Keyword()

    """Name of the LTA interface instance the product was collected from"""

    modification_date = ZuluDate()

    """Last modification date of the product on the LTA interface (OData ModificationDate)"""

    origin_date = ZuluDate()

    """Product origin date at the source (OData OriginDate)"""

    product_id = Keyword()

    """Product identifier from the LTA interface (OData Id)"""

    product_name = Keyword()

    """Product file name from the LTA interface (OData Name)"""

    production_service_name = Keyword()

    """Name of the LTA production service instance providing the product"""

    production_service_type = Keyword()

    """Type of the production service providing the product (LTA)"""

    publication_date = ZuluDate()

    """Date the product was published on the LTA interface (OData PublicationDate)"""

    reportFolder = Keyword()

    """Folder or path of the source report file from which this record was extracted"""

    start_date = ZuluDate()

    """Product sensing start date (OData ContentDate.Start)"""


class MaasConfig(MAASDocument):
    """
    Mapping class for index: maas-config

    Generated from: resources/templates/maas-config_template.json
    """

    class Index:
        "inner class for DSL"

        name = "maas-config"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("maas-config")


class MaasConfigCollector(MAASDocument):
    """
    Mapping class for index: maas-config-collector

    Generated from: resources/templates/maas-config-collector_template.json
    """

    class Index:
        "inner class for DSL"

        name = "maas-config-collector"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("maas-config-collector")


class MaasConfigCompleteness(MAASDocument):
    """
    Mapping class for index: maas-config-completeness

    Generated from: resources/templates/maas-config-completeness_template.json
    """

    class Index:
        "inner class for DSL"

        name = "maas-config-completeness"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("maas-config-completeness")

    activated = Boolean()

    """Whether this completeness configuration entry is activated"""

    end_date = ZuluDate()

    """End date of validity for this completeness configuration"""

    key = Keyword()

    """Unique key of the completeness configuration entry"""

    mission = Keyword()

    """Mission the completeness configuration applies to (e.g. S1, S2, S3)"""

    satellite_unit = Keyword()

    """Satellite unit the completeness configuration applies to"""

    service_id = Keyword()

    """Identifier of the service the completeness configuration applies to"""

    service_type = Keyword()

    """Service type the completeness configuration applies to (e.g. DD, LTA)"""

    start_date = ZuluDate()

    """Start date of validity for this completeness configuration"""


class MaasConfigCompletenessS3Records(InnerDoc):
    """
    Inner document class for parent class: MaasConfigCompletenessS3

    Generated from property: records
    """

    product_type = Keyword()

    """Product type described by this completeness record"""

    sensing_in_minutes = Long()

    """Expected sensing duration of the product type in minutes"""

    timeliness = Keyword()

    """Timeliness category of the product type"""


class MaasConfigCompletenessS3(MAASDocument):
    """
    Mapping class for index: maas-config-completeness-s3

    Generated from: resources/templates/maas-config-completeness-s3_template.json
    """

    class Index:
        "inner class for DSL"

        name = "maas-config-completeness-s3"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("maas-config-completeness-s3")

    key = Keyword()

    """Unique key of the Sentinel-3 completeness configuration entry"""

    latest = Boolean()

    """Whether this is the latest version of the completeness configuration"""

    records = Object(MaasConfigCompletenessS3Records)

    """Completeness configuration records, one per product type"""


class MaasConfigCompletenessS5Records(InnerDoc):
    """
    Inner document class for parent class: MaasConfigCompletenessS5

    Generated from property: records
    """

    product_type = Keyword()

    """Product type described by this completeness record"""

    sensing_in_minutes = Long()

    """Expected sensing duration of the product type in minutes"""

    timeliness = Keyword()

    """Timeliness category of the product type"""


class MaasConfigCompletenessS5(MAASDocument):
    """
    Mapping class for index: maas-config-completeness-s5

    Generated from: resources/templates/maas-config-completeness-s5_template.json
    """

    class Index:
        "inner class for DSL"

        name = "maas-config-completeness-s5"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("maas-config-completeness-s5")

    key = Keyword()

    """Unique key of the Sentinel-5P completeness configuration entry"""

    latest = Boolean()

    """Whether this is the latest version of the completeness configuration"""

    records = Object(MaasConfigCompletenessS5Records)

    """Completeness configuration records, one per product type"""


class MaasConfigDataflowMetadata(InnerDoc):
    """
    Inner document class for parent class: MaasConfigDataflow

    Generated from property: metadata
    """

    createAt = ZuluDate()

    """Creation timestamp of the dataflow configuration"""

    updateAt = ZuluDate()

    """Last update timestamp of the dataflow configuration"""


class MaasConfigDataflowRecordsServicesConfig(InnerDoc):
    """
    Inner document class for parent class: MaasConfigDataflowRecords

    Generated from property: services_config
    """


class MaasConfigDataflowRecordsStb(InnerDoc):
    """
    Inner document class for parent class: MaasConfigDataflowRecords

    Generated from property: STB
    """

    stb_timeliness = Keyword()

    """Standard timeliness budget target for the product type"""

    real_timeliness = Keyword()

    """Real observed timeliness for the product type"""

    num_products_per_day = Float()

    """Expected number of products per day"""

    volume_per_day = Float()

    """Expected data volume per day"""


class MaasConfigDataflowRecordsAuxip(InnerDoc):
    """
    Inner document class for parent class: MaasConfigDataflowRecords

    Generated from property: AUXIP
    """

    frequency = Long()

    """Expected production frequency on the AUXIP interface"""

    provider = Keyword()

    """Provider of the product on the AUXIP interface"""

    timeliness = Long()

    """Expected timeliness on the AUXIP interface"""


class MaasConfigDataflowRecords(InnerDoc):
    """
    Inner document class for parent class: MaasConfigDataflow

    Generated from property: records
    """

    product_type = Keyword()

    """Product type described by this dataflow record"""

    product_level = Keyword()

    """Processing level of the product type"""

    description = Text()

    """Human-readable description of the product type"""

    note = Text()

    """Free-text note about the dataflow record"""

    payload = Keyword()

    """Payload associated with the product type"""

    mode = Keyword()

    """Acquisition mode of the product type"""

    services_config = Object(MaasConfigDataflowRecordsServicesConfig)

    """Per-service configuration mapping each service type to the services expected to publish the product type"""

    STB = Object(MaasConfigDataflowRecordsStb)

    """Standard timeliness budget (STB) configuration for the product type"""

    AUXIP = Object(MaasConfigDataflowRecordsAuxip)

    """AUXIP interface configuration for the product type"""


class MaasConfigDataflow(MAASDocument):
    """
    Mapping class for index: maas-config-dataflow

    Generated from: resources/templates/maas-config-dataflow_template.json
    """

    class Index:
        "inner class for DSL"

        name = "maas-config-dataflow"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("maas-config-dataflow")

    key = Keyword()

    """Unique key of the dataflow configuration entry"""

    latest = Boolean()

    """Whether this is the latest version of the dataflow configuration"""

    metadata = Object(MaasConfigDataflowMetadata)

    """Metadata of the dataflow configuration"""

    name = Keyword()

    """Name of the dataflow configuration"""

    records = Object(MaasConfigDataflowRecords)

    """Dataflow configuration records, one per product type"""

    version = Keyword()

    """Version of the dataflow configuration"""


class MaasConfigMission(MAASDocument):
    """
    Mapping class for index: maas-config-mission

    Generated from: resources/templates/maas-config-mission_template.json
    """

    class Index:
        "inner class for DSL"

        name = "maas-config-mission"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("maas-config-mission")

    display_name = Keyword()

    """Human-readable display name of the mission"""

    key = Keyword()

    """Unique key of the mission configuration entry"""

    short_name = Keyword()

    """Short name of the mission"""


class MaasConfigSatellite(MAASDocument):
    """
    Mapping class for index: maas-config-satellite

    Generated from: resources/templates/maas-config-satellite_template.json
    """

    class Index:
        "inner class for DSL"

        name = "maas-config-satellite"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("maas-config-satellite")

    display_name = Keyword()

    """Human-readable display name of the satellite"""

    key = Keyword()

    """Unique key of the satellite configuration entry"""

    mission = Keyword()

    """Mission the satellite belongs to (e.g. S1, S2, S3)"""

    short_name = Keyword()

    """Short name of the satellite"""


class MaasConfigService(MAASDocument):
    """
    Mapping class for index: maas-config-service

    Generated from: resources/templates/maas-config-service_template.json
    """

    class Index:
        "inner class for DSL"

        name = "maas-config-service"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("maas-config-service")

    display_name = Keyword()

    """Human-readable display name of the service"""

    key = Keyword()

    """Unique key of the service configuration entry"""

    short_name = Keyword()

    """Short name of the service"""


class MetricsProduct(MAASRawDocument):
    """
    Mapping class for index: raw-data-metrics-product

    Generated from: resources/templates/raw-data-metrics-product_template.json
    """

    class Index:
        "inner class for DSL"

        name = "raw-data-metrics-product"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("raw-data-metrics-product")

    _PARTITION_FIELD = "ingestionTime"

    _PARTITION_FIELD_FORMAT = "%Y"

    counter = Long()

    """Metric counter value from the OData 'Counter' property"""

    interface_name = Keyword()

    """Name of the source LTA metrics interface (e.g. metrics_LTA_Werum)"""

    metric_type = Keyword()

    """Metric type from the OData 'MetricType' property"""

    modification_date = ZuluDate()

    """Date the metric record was last modified"""

    name = Keyword()

    """Metric name from the OData 'Name' property"""

    production_service_name = Keyword()

    """Name of the production service providing the metrics (e.g. Werum)"""

    production_service_type = Keyword()

    """Type of the production service (LTA)"""

    reportFolder = Keyword()

    """Folder path of the source metrics report file"""

    timestamp = ZuluDate()

    """Metric timestamp from the OData 'Timestamp' property"""


class MpAllProduct(MAASRawDocument):
    """
    Mapping class for index: raw-data-mp-all-product

    Generated from: resources/templates/raw-data-mp-all-product_template.json
    """

    class Index:
        "inner class for DSL"

        name = "raw-data-mp-all-product"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("raw-data-mp-all-product")

    _PARTITION_FIELD = "ingestionTime"

    _PARTITION_FIELD_FORMAT = "static"

    absolute_orbit = Keyword()

    """Absolute orbit number from the AbsoluteOrbit column"""

    acquisition_duration = Long()

    """Acquisition duration in milliseconds from the SensingDuration [msec] (S1) or AcquisitionDuration [msec] (S2) column"""

    acquisition_start = ZuluDate()

    """Acquisition start time from the SensingTimeStart (S1) or AcquisitionStart (S2) column"""

    acquisition_stop = ZuluDate()

    """Acquisition stop time from the AcquisitionStop column"""

    channel = Keyword()

    """Downlink channel from the Channel column"""

    datatake_id = Keyword()

    """Datatake identifier from DatatakeId(dec) (S1) or ID/AcquisitionID (S2)"""

    downlink_absolute_orbit = Keyword()

    """Absolute orbit of the downlink from the DownlinkAbsoluteOrbit (S1) or DownlinkOrbit (S2) column"""

    downlink_duration = Long()

    """Downlink duration in milliseconds from the DownlinkDuration [msec] column"""

    downlink_execution_time = ZuluDate()

    """Downlink execution time from the DownlinkExecutionTime column"""

    downlink_polarization = Keyword()

    """Downlink polarization from the DownlinkPolarization column"""

    effective_downlink_start = ZuluDate()

    """Effective downlink start time from the EffectiveDownlinkStart column"""

    effective_downlink_stop = ZuluDate()

    """Effective downlink stop time from the EffectiveDownlinkStop column"""

    instrument_mode = Keyword()

    """Instrument acquisition mode from the InstrumentMode column"""

    interface_name = Keyword()

    """Collector interface name set to S1MissionPlanningALL or S2MissionPlanningALL"""

    latency = Long()

    """Latency in minutes from the Latency [min] column"""

    mission = Keyword()

    """Mission identifier set by the collector (S1 or S2 depending on the source report)"""

    number_of_scenes = Integer()

    """Number of scenes from the Scenes column"""

    partial = Keyword()

    """Partial acquisition indicator from the Partial column"""

    polarization = Keyword()

    """Acquisition polarization from the Polarization column"""

    relative_orbit = Keyword()

    """Relative orbit number from the RelativeOrbit column"""

    reportFolder = Keyword()

    """Folder or interface path from which the source report was collected"""

    satellite_id = Keyword()

    """Satellite identifier extracted from the SatelliteID column"""

    session_id = Keyword()

    """Downlink session identifier from the DLSession column, split on hyphen or whitespace"""

    station = Keyword()

    """Ground station acquiring the downlink, from the CGS (S1) or Station (S2) column"""

    status = Keyword()

    """Acquisition or downlink status from the Status column"""

    timeliness = Keyword()

    """Timeliness category from the Timeliness column"""


class MpHktmAcquisitionProduct(MAASRawDocument):
    """
    Mapping class for index: raw-data-mp-hktm-acquisition-product

    Generated from: resources/templates/raw-data-mp-hktm-acquisition-product_template.json
    """

    class Index:
        "inner class for DSL"

        name = "raw-data-mp-hktm-acquisition-product"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("raw-data-mp-hktm-acquisition-product")

    _PARTITION_FIELD = "ingestionTime"

    _PARTITION_FIELD_FORMAT = "static"

    absolute_orbit = Keyword()

    """Absolute orbit number from the AbsoluteOrbit column"""

    channel = Long()

    """Acquisition channel from the channel column"""

    execution_time = ZuluDate()

    """Acquisition execution time from the ExecutionTime column"""

    ground_station = Keyword()

    """Ground station performing the acquisition from the CGS column"""

    interface_name = Keyword()

    """Collector interface name set to S1MissionPlanning"""

    production_service_name = Keyword()

    """Production service name set by the collector to CGS"""

    production_service_type = Keyword()

    """Production service type set by the collector to AUXIP"""

    reportFolder = Keyword()

    """Folder or interface path from which the source report was collected"""

    satellite_id = Keyword()

    """Satellite identifier from the SatelliteID column"""

    session_id = Keyword()

    """HKTM acquisition session identifier from the SessionID column"""


class MpHktmDownlink(MAASRawDocument):
    """
    Mapping class for index: raw-data-mp-hktm-downlink

    Generated from: resources/templates/raw-data-mp-hktm-downlink_template.json
    """

    class Index:
        "inner class for DSL"

        name = "raw-data-mp-hktm-downlink"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("raw-data-mp-hktm-downlink")

    _PARTITION_FIELD = "ingestionTime"

    _PARTITION_FIELD_FORMAT = "static"

    absolute_orbit = Keyword()

    """Absolute orbit number from the AbsoluteOrbit column"""

    acquisition_duration = Long()

    """Acquisition duration in milliseconds from the AcquisitionDuration [msec] column"""

    acquisition_start = ZuluDate()

    """Acquisition start time from the AcquisitionStart column"""

    acquisition_stop = ZuluDate()

    """Acquisition stop time from the AcquisitionStop column"""

    datatake_id = Keyword()

    """Datatake identifier from the AcquisitionID column"""

    downlink_absolute_orbit = Keyword()

    """Absolute orbit of the downlink pass (not populated by this collector)"""

    downlink_duration = Long()

    """Downlink duration in milliseconds from the DownlinkDuration [msec] column"""

    downlink_execution_time = ZuluDate()

    """Downlink execution time (not populated by this collector)"""

    downlink_mode = Keyword()

    """Downlink mode from the DwlMode column"""

    downlink_start = ZuluDate()

    """Downlink start time from the DownlinkStart column"""

    downlink_stop = ZuluDate()

    """Downlink stop time from the DownlinkStop column"""

    effective_downlink_start = ZuluDate()

    """Effective downlink start time from the EffectiveDownlinkStart column"""

    effective_downlink_stop = ZuluDate()

    """Effective downlink stop time from the EffectiveDownlinkStop column"""

    interface_name = Keyword()

    """Collector interface name set to S2MissionPlanning"""

    latency = Long()

    """Latency in minutes from the Latency [min] column"""

    mission = Keyword()

    """Mission identifier set by the collector to S2"""

    number_of_scenes = Long()

    """Number of scenes from the Scenes column"""

    partial = Keyword()

    """Partial acquisition indicator from the Partial column"""

    relative_orbit = Keyword()

    """Relative orbit number (not populated by this collector)"""

    reportFolder = Keyword()

    """Folder or interface path from which the source report was collected"""

    satellite_id = Keyword()

    """Satellite identifier from the Satellite ID column"""

    station = Keyword()

    """Ground station acquiring the downlink from the Station column"""

    x_off = ZuluDate()

    """X-band transmitter switch-off time for the HKTM downlink"""

    x_on = ZuluDate()

    """X-band transmitter switch-on time for the HKTM downlink"""


class MpProduct(MAASRawDocument):
    """
    Mapping class for index: raw-data-mp-product

    Generated from: resources/templates/raw-data-mp-product_template.json
    """

    class Index:
        "inner class for DSL"

        name = "raw-data-mp-product"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("raw-data-mp-product")

    _PARTITION_FIELD = "ingestionTime"

    _PARTITION_FIELD_FORMAT = "static"

    absolute_orbit = Keyword()

    """Absolute orbit number from the AbsoluteOrbit column"""

    datatake_id = Keyword()

    """Datatake identifier from DatatakeId (S1) or ID/AcquisitionID (S2)"""

    instrument_mode = Keyword()

    """Instrument acquisition mode from the InstrumentMode column"""

    instrument_swath = Keyword()

    """Instrument swath from the InstrumentSwath column (S1)"""

    interface_name = Keyword()

    """Collector interface name set to S1MissionPlanning or S2MissionPlanning"""

    l0_sensing_duration = Long()

    """Level-0 sensing duration in milliseconds from the L0SensingDuration [msec] column (S1)"""

    l0_sensing_time_start = ZuluDate()

    """Level-0 sensing start time from the L0SensingTimeStart column (S1)"""

    number_of_scenes = Integer()

    """Number of scenes from the NumberOfScenes column (S2)"""

    observation_duration = Long()

    """Observation duration in milliseconds from the ObservationDuration [msec] column"""

    observation_time_start = ZuluDate()

    """Observation start time from the ObservationTimeStart column"""

    observation_time_stop = ZuluDate()

    """Observation stop time from the ObservationTimeStop column (S2)"""

    polarization = Keyword()

    """Acquisition polarization from the Polarization column (S1)"""

    production_service_name = Keyword()

    """Production service name set by the collector to CGS"""

    production_service_type = Keyword()

    """Production service type set by the collector to AUXIP"""

    relative_orbit = Keyword()

    """Relative orbit number from the RelativeOrbit column"""

    reportFolder = Keyword()

    """Folder or interface path from which the source report was collected"""

    satellite_id = Keyword()

    """Satellite identifier from the SatelliteID column"""

    timeliness = Keyword()

    """Timeliness category from the Timeliness column"""


class MpcipProduct(MAASRawDocument):
    """
    Mapping class for index: raw-data-mpcip-product

    Generated from: resources/templates/raw-data-mpcip-product_template.json
    """

    class Index:
        "inner class for DSL"

        name = "raw-data-mpcip-product"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("raw-data-mpcip-product")

    _PARTITION_FIELD = "ingestionTime"

    _PARTITION_FIELD_FORMAT = "%Y-%m"

    content_length = Long()

    """Product content size in bytes from the ContentLength field of the source OData node"""

    end_date = ZuluDate()

    """Product content end date from the ContentDate.End field of the source OData node"""

    eviction_date = ZuluDate()

    """Product eviction date from the EvictionDate field of the source OData node"""

    footprint = Keyword()

    """Geographic footprint of the product as a WKT/GeoJSON geometry string"""

    interface_name = Keyword()

    """Collector interface name set to MPCIP_Acri"""

    origin_date = ZuluDate()

    """Product origin date from the OriginDate field of the source OData node"""

    product_id = Keyword()

    """Product identifier from the Id field of the source OData node"""

    product_name = Keyword()

    """Product name from the Name field of the source OData node"""

    production_service_name = Keyword()

    """Production service name set by the collector to Acri"""

    production_service_type = Keyword()

    """Production service type set by the collector to MPCIP"""

    publication_date = ZuluDate()

    """Product publication date from the PublicationDate field of the source OData node"""

    reportFolder = Keyword()

    """Folder or interface path from which the source report was collected"""

    start_date = ZuluDate()

    """Product content start date from the ContentDate.Start field of the source OData node"""


class MpipProduct(MAASRawDocument):
    """
    Mapping class for index: raw-data-mpip-product

    Generated from: resources/templates/raw-data-mpip-product_template.json
    """

    class Index:
        "inner class for DSL"

        name = "raw-data-mpip-product"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("raw-data-mpip-product")

    _PARTITION_FIELD = "ingestionTime"

    _PARTITION_FIELD_FORMAT = "static"

    ingestion_date = ZuluDate()

    """Product ingestion date from the ingestionDate field of the source JSON node"""

    interface_name = Keyword()

    """Collector interface name set to MPIP_GMV"""

    product_name = Keyword()

    """Product file name from the filename field of the source JSON node"""

    production_service_name = Keyword()

    """Production service name set by the collector to GMV"""

    production_service_type = Keyword()

    """Production service type set by the collector to MPIP"""

    reportFolder = Keyword()

    """Folder or interface path from which the source report was collected"""

    validity_start_time = ZuluDate()

    """Product validity start time from the validityStartTime field of the source JSON node"""

    validity_stop_time = ZuluDate()

    """Product validity stop time from the validityStopTime field of the source JSON node"""


class PripProduct(MAASRawDocument):
    """
    Mapping class for index: raw-data-prip-product

    Generated from: resources/templates/raw-data-prip-product_template.json
    """

    class Index:
        "inner class for DSL"

        name = "raw-data-prip-product"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("raw-data-prip-product")

    _PARTITION_FIELD = "ingestionTime"

    _PARTITION_FIELD_FORMAT = "%Y-%m"

    cloud_cover = Float()

    """Cloud cover percentage of the product (OData Attribute cloudCover)"""

    content_length = Long()

    """Product file size in bytes (OData ContentLength)"""

    datastrip_id = Keyword()

    """Datastrip identifier of the product for S2 (OData Attribute datastripId)"""

    end_date = ZuluDate()

    """Product sensing end date (OData ContentDate.End)"""

    eviction_date = ZuluDate()

    """Date the product is scheduled to be evicted from the PRIP interface (OData EvictionDate)"""

    footprint = GeoShape()

    """Geographic footprint of the product (OData GeoFootprint), populated for selected product types"""

    fos_pushing_date_backup = ZuluDate()

    """Date the product was pushed by the FOS backup chain, used for HKTM completeness"""

    fos_pushing_date_nominal = ZuluDate()

    """Date the product was pushed by the FOS nominal chain, used for HKTM completeness"""

    interface_name = Keyword()

    """Name of the PRIP interface instance the product was collected from"""

    origin_date = ZuluDate()

    """Product origin date at the source (OData OriginDate)"""

    packet_store_id = Keyword()

    """Packet store identifier used to derive S1 raw product timeliness (NRT-PT/NTC)"""

    product_group_id = Keyword()

    """Product group identifier grouping related S2 products (OData Attribute productGroupId)"""

    product_id = Keyword()

    """Product identifier from the PRIP interface (OData Id)"""

    product_name = Keyword()

    """Product file name from the PRIP interface (OData Name)"""

    production_service_name = Keyword()

    """Name of the PRIP production service instance providing the product"""

    production_service_type = Keyword()

    """Type of the production service providing the product (PRIP)"""

    publication_date = ZuluDate()

    """Date the product was published on the PRIP interface (OData PublicationDate)"""

    quality_status = Keyword()

    """Quality status of the product (OData Attribute qualityStatus)"""

    reportFolder = Keyword()

    """Folder or path of the source report file from which this record was extracted"""

    start_date = ZuluDate()

    """Product sensing start date (OData ContentDate.Start)"""


class ProductDeletion(MAASRawDocument):
    """
    Mapping class for index: raw-data-product-deletion

    Generated from: resources/templates/raw-data-product-deletion_template.json
    """

    class Index:
        "inner class for DSL"

        name = "raw-data-product-deletion"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("raw-data-product-deletion")

    _PARTITION_FIELD = "ingestionTime"

    _PARTITION_FIELD_FORMAT = "static"

    interface_type = Keyword()

    """Type of interface targeted by the deletion ('DD' for datahub, 'LTA' for long term archive)"""

    product_name = Keyword()

    """Name of the product to delete from the deletion list report"""

    reportFolder = Keyword()

    """Folder path of the source deletion list report file"""


class S3pMetricsCirculationAgent(MAASRawDocument):
    """
    Mapping class for index: raw-data-s3p-metrics-circulation-agent

    Generated from: resources/templates/raw-data-s3p-metrics-circulation-agent_template.json
    """

    class Index:
        "inner class for DSL"

        name = "raw-data-s3p-metrics-circulation-agent"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("raw-data-s3p-metrics-circulation-agent")

    _PARTITION_FIELD = "log_date"

    _PARTITION_FIELD_FORMAT = "%Y-%m"

    action = Keyword()

    """Action field of the M&C log line (e.g. OUT, IN)"""

    code = Keyword()

    """M&C message code from the log line (e.g. DC for Data Circulation)"""

    domain = Keyword()

    """M&C domain of the log line (e.g. Data Circulation)"""

    filename = Keyword()

    """Name of the circulated file referenced by the log line"""

    filesize = Long()

    """Size in bytes of the circulated file"""

    hostname = Keyword()

    """Host name of the S3P station server that emitted the log line"""

    log_date = ZuluDate()

    """Date the log line was emitted, used as the monthly partition field"""

    pid = Keyword()

    """Process identifier of the circulation agent from the log line"""

    queueid = Keyword()

    """Identifier of the circulation queue entry"""

    status = Keyword()

    """Status reported for the circulation of the file"""

    tourl = Keyword()

    """Destination URL the file was circulated to"""


class S3pMetricsRestCaduPollingAgent(MAASRawDocument):
    """
    Mapping class for index: raw-data-s3p-metrics-rest-cadu-polling-agent

    Generated from: resources/templates/raw-data-s3p-metrics-rest-cadu-polling-agent_template.json
    """

    class Index:
        "inner class for DSL"

        name = "raw-data-s3p-metrics-rest-cadu-polling-agent"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("raw-data-s3p-metrics-rest-cadu-polling-agent")

    _PARTITION_FIELD = "log_date"

    _PARTITION_FIELD_FORMAT = "%Y-%m"

    action = Keyword()

    """Action field of the M&C log line (e.g. IN, REF)"""

    code = Keyword()

    """M&C message code from the log line (e.g. IMP for Data Import, TL for Timeliness)"""

    creationtime = ZuluDate()

    """Creation time of the imported CADU session, used as the S3P session acquisition start time"""

    domain = Keyword()

    """M&C domain of the log line (e.g. Data Import, Timeliness)"""

    eventtime = ZuluDate()

    """Event time from the log line, used as the S3P session acquisition stop time"""

    filename = Keyword()

    """Name of the file or session referenced by the log line"""

    filesize = Long()

    """Size in bytes of the transferred file"""

    fromurl = Keyword()

    """Source URL the file was polled or transferred from"""

    host = Keyword()

    """Host referenced by the log line"""

    hostname = Keyword()

    """Host name of the S3P station server that emitted the log line"""

    jobid = Keyword()

    """Identifier of the CADU polling job from the log line"""

    log_date = ZuluDate()

    """Date the log line was emitted, used as the monthly partition field"""

    pid = Keyword()

    """Process identifier of the CADU polling agent from the log line"""

    queueid = Keyword()

    """Identifier of the processing queue entry"""

    reftime = ZuluDate()

    """Reference time reported in the log line"""

    status = Keyword()

    """Status reported for the file transfer or polling job"""

    timelinessKey = Keyword()

    """Downlink session timeliness key that identifies the S3P session"""

    tourl = Keyword()

    """Destination URL the file was transferred to"""


class S3pMetricsThinLayer(MAASRawDocument):
    """
    Mapping class for index: raw-data-s3p-metrics-thin-layer

    Generated from: resources/templates/raw-data-s3p-metrics-thin-layer_template.json
    """

    class Index:
        "inner class for DSL"

        name = "raw-data-s3p-metrics-thin-layer"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("raw-data-s3p-metrics-thin-layer")

    _PARTITION_FIELD = "log_date"

    _PARTITION_FIELD_FORMAT = "%Y-%m"

    check = Keyword()

    """Result of the timeliness check reported in the ThinLayer M&C log line (e.g. OK)"""

    day = Integer()

    """Day of the month parsed from the log timestamp"""

    env = Keyword()

    """Processing environment flag from the ThinLayer log (e.g. N for nominal)"""

    eventname = Keyword()

    """Name of the logged event (e.g. LOPP)"""

    eventtime = ZuluDate()

    """Timestamp of the event as reported in the ThinLayer log line"""

    filename = Keyword()

    """Name of the L0PP granule product referenced by the log line"""

    generationtime = ZuluDate()

    """Generation time of the product reported in the log line"""

    hostname = Keyword()

    """Host name of the S3P station server that emitted the log line"""

    level = Keyword()

    """Product processing level from the log line (e.g. 0)"""

    log_date = ZuluDate()

    """Date the log line was emitted, used as the monthly partition field"""

    message = Text()

    """Free-text message field of the log line"""

    month = Keyword()

    """Month parsed from the log timestamp"""

    pid = Keyword()

    """Process identifier of the ThinLayer agent from the log line"""

    pmode = Keyword()

    """Processing mode from the log line (e.g. N for nominal)"""

    process = Keyword()

    """Name of the process or agent that emitted the log line"""

    ptype = Keyword()

    """Product type code from the log line"""

    reftime = Keyword()

    """Reference time source of the product (e.g. ground)"""

    sat = Keyword()

    """Satellite unit the log line refers to (e.g. S3A)"""

    time = Keyword()

    """Time component parsed from the log timestamp"""

    timelinessKey = Keyword()

    """Downlink session timeliness key that identifies the S3P session"""

    validitystart = ZuluDate()

    """Start of the product validity period from the log line"""

    validitystop = ZuluDate()

    """Stop of the product validity period from the log line"""


class S3pSessionCaduFiles(InnerDoc):
    """
    Inner document class for parent class: S3pSession

    Generated from property: cadu_files
    """

    cadu_name = Keyword()

    """Name of the CADU file"""

    cadu_delivery_in = ZuluDate()

    """Time the CADU file was delivered in"""

    cadu_delivery_out = ZuluDate()

    """Time the CADU file was delivered out"""


class S3pSessionL0PpGranules(InnerDoc):
    """
    Inner document class for parent class: S3pSession

    Generated from property: l0pp_granules
    """

    product_name = Keyword()

    """Name of the L0PP granule product"""

    product_type = Keyword()

    """Type of the L0PP granule product"""

    delivery_date_to_eum = ZuluDate()

    """Delivery date of the granule to EUMETSAT"""

    delivery_start_date_to_eum = ZuluDate()

    """Start date of the granule delivery to EUMETSAT"""

    thin_layer_log_date = ZuluDate()

    """Date of the thin-layer log entry for the granule"""

    raw_data_generation_time = ZuluDate()

    """Generation time of the raw data granule"""

    validitystart = ZuluDate()

    """Validity start time of the granule"""

    validitystop = ZuluDate()

    """Validity stop time of the granule"""

    filesize = Long()

    """Size of the granule file in bytes"""

    transfer_bandwith_to_eum = Float()

    """Transfer bandwidth of the granule to EUMETSAT"""

    transfer_duration_to_eum = Long()

    """Transfer duration of the granule to EUMETSAT in seconds"""


class S3pSession(MAASDocument):
    """
    Mapping class for index: s3p-session

    Generated from: resources/templates/s3p-session_template.json
    """

    class Index:
        "inner class for DSL"

        name = "s3p-session"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("s3p-session")

    acquisition_start_time = ZuluDate()

    """Start time of the acquisition"""

    acquisition_stop_time = ZuluDate()

    """Stop time of the acquisition"""

    cadu_files = Object(S3pSessionCaduFiles)

    """CADU files received for the downlink session"""

    delivery_start_to_eum = ZuluDate()

    """Start time of the delivery to EUMETSAT"""

    delivery_stop_to_eum = ZuluDate()

    """Stop time of the delivery to EUMETSAT"""

    delivery_to_eum_completeness = Float()

    """Completeness ratio of L0PP granules delivered to EUMETSAT"""

    delivery_to_eum_timeliness = Long()

    """Timeliness of delivery to EUMETSAT from acquisition stop, in seconds"""

    delivery_to_eum_timeliness_from_acq_start = Long()

    """Timeliness of delivery to EUMETSAT from acquisition start, in seconds"""

    downlink_orbit = Keyword()

    """Downlink orbit number of the session"""

    downlink_session = Keyword()

    """Identifier of the downlink session"""

    generation_timeliness_from_acq_start = Long()

    """Timeliness of granule generation from acquisition start, in seconds"""

    hkraw_delivery_time = ZuluDate()

    """Delivery time of the HKRAW file"""

    hkraw_name = Keyword()

    """Name of the HKRAW file"""

    hkraw_size = Long()

    """Size of the HKRAW file in bytes"""

    l0pp_granules = Object(S3pSessionL0PpGranules)

    """L0PP granules produced for the downlink session"""

    satellite_id = Keyword()

    """Identifier of the satellite (e.g. S3A, S3B)"""

    timeliness_key = Keyword()

    """Timeliness key of the downlink session"""

    updateTime = ZuluDate()

    """Timestamp of the last update of this consolidated document"""


class SatUnavailabilityProduct(MAASRawDocument):
    """
    Mapping class for index: raw-data-sat-unavailability-product

    Generated from: resources/templates/raw-data-sat-unavailability-product_template.json
    """

    class Index:
        "inner class for DSL"

        name = "raw-data-sat-unavailability-product"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("raw-data-sat-unavailability-product")

    _PARTITION_FIELD = "ingestionTime"

    _PARTITION_FIELD_FORMAT = "static"

    category = Keyword()

    """Category classifying the unavailability record"""

    comment = Keyword()

    """Free-text comment describing the unavailability (Comment element)"""

    description = Text()

    """Free-text description of the unavailability record"""

    end_anx_offset = Integer()

    """Offset from the ascending node crossing at the end of the unavailability (EndAnxOffset element)"""

    end_doy = Integer()

    """Day of year corresponding to the end of the unavailability"""

    end_orbit = Keyword()

    """Orbit number at the end of the unavailability (EndOrbit element, normalized)"""

    end_time = Keyword()

    """End time of the unavailability period (EndTime element)"""

    file_class = Keyword()

    """File class of the source Earth Explorer file"""

    file_name = Keyword()

    """File name declared in the Earth Explorer header Fixed_Header/File_Name"""

    file_type = Keyword()

    """File type of the source Earth Explorer file"""

    file_version = Keyword()

    """Version of the source unavailability file"""

    interface_name = Keyword()

    """Interface that provided the product, set to the constant Satellite-Unavailability"""

    mission = Keyword()

    """Mission identifier from the Earth Explorer header Fixed_Header/Mission"""

    notes = Text()

    """Additional free-text notes attached to the unavailability record"""

    production_service_name = Keyword()

    """Production service name, set to the constant Exprivia"""

    production_service_type = Keyword()

    """Production service type, set to the constant AUXIP"""

    reportFolder = Keyword()

    """Source folder or path where the report file was collected"""

    source_creation_date = ZuluDate()

    """Creation date of the source file as declared by the producer"""

    source_creator = Keyword()

    """Identifier of the entity that created the source file"""

    source_system = Keyword()

    """System that produced the source file"""

    start_anx_offset = Integer()

    """Offset from the ascending node crossing at the start of the unavailability (StartAnxOffset element)"""

    start_doy = Integer()

    """Day of year corresponding to the start of the unavailability"""

    start_orbit = Keyword()

    """Orbit number at the start of the unavailability (StartOrbit element, normalized)"""

    start_time = Keyword()

    """Start time of the unavailability period (StartTime element)"""

    subsystem = Keyword()

    """Satellite subsystem affected by the unavailability (Subsystem element)"""

    type = Keyword()

    """Type of the unavailability entry (Type element)"""

    unavailability_reference = Keyword()

    """Unavailability reference from Data_Block/Unavailability_Reference"""

    unavailability_status = Keyword()

    """Status of the unavailability record"""

    unavailability_type = Keyword()

    """Unavailability type from Data_Block/Unavailability_Type"""

    unique_identifier = Keyword()

    """Unique identifier of the unavailability record"""

    validity_start = ZuluDate()

    """Start of the validity period declared in the source file"""

    validity_stop = ZuluDate()

    """End of the validity period declared in the source file"""
