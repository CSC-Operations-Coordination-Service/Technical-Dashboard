from maas_cds.engines.compute.anomaly_correlation_ticket import (
    CorrelateAnomalyTicketEngine,
)
from maas_cds.model import (
    CamsCloudAnomalyCorrelation,
    CdsCamsTickets,
    CdsAnomalyCorrelation,
)


# def test_cams_cloud_ticket_created_before():
#     report = CamsCloudAnomalyCorrelation(
#         **{
#             "reportName": "Jira_CAMS_Cloud_Anomaly_Correlation_20240207_142434086673_1.json",
#             "created": "2024-02-01T03:18:38.354Z",
#             "description": "Missing S2A datatstrip data due to antenna acquisition issue at Svalbard Station",
#             "impacted_passes": ["44974"],
#             "impacted_observations": ["S2A-44973-3"],
#             "issue": "GSANOM-14445",
#             "key": "AN-192",
#             "origin": "Acquisition",
#             "summary": "GSANOM-14445 - anomaly correlation",
#             "sattelite_unit": "S2A",
#             "station_type": "X-Band",
#             "station": "SGS",
#             "status": "Done",
#             "title": "GSANOM-14445 - anomaly correlation",
#             "updated": "2024-02-01T15:20:34.397Z",
#             "interface_name": "Jira_CAMS_Cloud_Anomaly_Correlation",
#             "ingestionTime": "2024-02-01T22:38:39.185Z",
#         }
#     )
#     report.meta.id = "AN-192"
#     report.meta.index = "raw-data-cams-cloud-anomaly-correlation-static"
#     report.full_clean()

#     ticket = CdsCamsTickets(
#         **{
#             "created": "2024-02-01T03:18:31.763Z",
#             "occurence_date": "2024-02-01T03:00:00.000Z",
#             "title": "CGS-SGS: S2A: 44974: Data missing, FER above threshold",
#             "url": "https://esa-cams.atlassian.net/browse/GSANOM-14445",
#             "datatake_ids": ["S2A-44973-3"],
#             "linked_issues": "AN-192",
#             "updated": "2024-02-14T14:47:50.207Z",
#             "key": "GSANOM-14445",
#             "status": "Closed",
#             "affected_systems": "S-2",
#             "assigned_element": ["ATOS", "ESA S-2", "OMCS", "Svalbard Station"],
#             "criticality": "Blocking",
#             "entity": "Svalbard Station",
#             "involved_entities": ["ATOS", "ESA S-2", "OMCS", "Svalbard Station"],
#             "originating_entity": "Svalbard Station",
#             "reporter": "sentinel-cams@ksat.no",
#             "review_board_dispositions": "Coorddesk(jnschmidt)@2024-02-01: delegated to Svalbard station for investigation",
#             "urgency": "Low",
#         }
#     )
#     ticket.meta.id = ""
#     ticket.meta.index = ""
#     ticket.full_clean()
#     engine = CorrelateAnomalyTicketEngine()
#     engine.consolidate_cams_cloud_ticket(report, ticket)

#     assert "origin" in ticket
#     assert "description" in ticket
#     assert ticket.correlation_file_id == "AN-192"

#     assert ticket.acquisition_pass == ["S2A_X-Band_44974_SGS"]


# def test_cams_cloud_ticket_created_after_failed():
#     report = CdsAnomalyCorrelation(
#         **{
#             "reportName": "Jira_CAMS_Cloud_Anomaly_Correlation_20240207_142434086673_1.json",
#             "created": "2025-02-01T03:18:38.354Z",
#             "description": "Missing S2A datatstrip data due to antenna acquisition issue at Svalbard Station",
#             "impacted_passes": ["44974"],
#             "impacted_observations": ["S2A-44973-3"],
#             "issue": "GSANOM-14445",
#             "key": "AN-192",
#             "origin": "Acquisition",
#             "summary": "GSANOM-14445 - anomaly correlation",
#             "sattelite_unit": "S2A",
#             "station_type": "X-Band",
#             "station": "SGS",
#             "status": "Done",
#             "title": "GSANOM-14445 - anomaly correlation",
#             "updated": "2024-02-01T15:20:34.397Z",
#             "interface_name": "Jira_CAMS_Cloud_Anomaly_Correlation",
#             "ingestionTime": "2024-02-01T22:38:39.185Z",
#         }
#     )
#     report.meta.id = "AN-192"
#     report.meta.index = "cds-anomaly-correlation"
#     report.full_clean()

#     ticket = CdsCamsTickets(
#         **{
#             "created": "2024-02-01T03:18:31.763Z",
#             "occurence_date": "2024-02-01T03:00:00.000Z",
#             "title": "CGS-SGS: S2A: 44974: Data missing, FER above threshold",
#             "url": "https://esa-cams.atlassian.net/browse/GSANOM-14445",
#             "datatake_ids": ["S2A-44973-3"],
#             "linked_issues": "AN-192",
#             "updated": "2024-02-14T14:47:50.207Z",
#             "key": "GSANOM-14445",
#             "status": "Closed",
#             "affected_systems": "S-2",
#             "assigned_element": ["ATOS", "ESA S-2", "OMCS", "Svalbard Station"],
#             "criticality": "Blocking",
#             "entity": "Svalbard Station",
#             "involved_entities": ["ATOS", "ESA S-2", "OMCS", "Svalbard Station"],
#             "originating_entity": "Svalbard Station",
#             "reporter": "sentinel-cams@ksat.no",
#             "review_board_dispositions": "Coorddesk(jnschmidt)@2024-02-01: delegated to Svalbard station for investigation",
#             "urgency": "Low",
#         }
#     )
#     ticket.meta.id = ""
#     ticket.meta.index = ""
#     ticket.full_clean()
#     engine = CorrelateAnomalyTicketEngine()
#     engine.consolidate_cams_cloud_ticket(report, ticket)

#     assert "origin" in ticket
#     assert "description" in ticket
#     assert ticket.correlation_file_id == "AN-192"

#     assert ticket.acquisition_pass == []


# def test_cams_cloud_ticket_created_after_failed():
#     report = CamsCloudAnomalyCorrelation(
#         **{
#             "reportName": "Jira_CAMS_Cloud_Anomaly_Correlation_20240207_142434086673_1.json",
#             "created": "2025-02-01T03:18:38.354Z",
#             "description": "Missing S2A datatstrip data due to antenna acquisition issue at Svalbard Station",
#             "impacted_passes": ["S2A-44974"],
#             "impacted_observations": ["S2A-44973-3"],
#             "issue": "GSANOM-14445",
#             "key": "AN-192",
#             "origin": "Acquisition",
#             "summary": "GSANOM-14445 - anomaly correlation",
#             "sattelite_unit": "S2A",
#             "station_type": "X-Band",
#             "station": "SGS",
#             "status": "Done",
#             "title": "GSANOM-14445 - anomaly correlation",
#             "updated": "2024-02-01T15:20:34.397Z",
#             "interface_name": "Jira_CAMS_Cloud_Anomaly_Correlation",
#             "ingestionTime": "2024-02-01T22:38:39.185Z",
#         }
#     )
#     report.meta.id = "AN-192"
#     report.meta.index = "raw-data-cams-cloud-anomaly-correlation-static"
#     report.full_clean()

#     ticket = CdsCamsTickets(
#         **{
#             "created": "2024-02-01T03:18:31.763Z",
#             "occurence_date": "2024-02-01T03:00:00.000Z",
#             "title": "CGS-SGS: S2A: 44974: Data missing, FER above threshold",
#             "url": "https://esa-cams.atlassian.net/browse/GSANOM-14445",
#             "datatake_ids": ["S2A-44973-3"],
#             "linked_issues": "AN-192",
#             "updated": "2024-02-14T14:47:50.207Z",
#             "key": "GSANOM-14445",
#             "status": "Closed",
#             "affected_systems": "S-2",
#             "assigned_element": ["ATOS", "ESA S-2", "OMCS", "Svalbard Station"],
#             "criticality": "Blocking",
#             "entity": "Svalbard Station",
#             "involved_entities": ["ATOS", "ESA S-2", "OMCS", "Svalbard Station"],
#             "originating_entity": "Svalbard Station",
#             "reporter": "sentinel-cams@ksat.no",
#             "review_board_dispositions": "Coorddesk(jnschmidt)@2024-02-01: delegated to Svalbard station for investigation",
#             "urgency": "Low",
#         }
#     )
#     ticket.meta.id = ""
#     ticket.meta.index = ""
#     ticket.full_clean()
#     engine = CorrelateAnomalyTicketEngine()
#     engine.consolidate_cams_cloud_ticket(report, ticket)

#     assert "origin" in ticket
#     assert "description" in ticket
#     assert ticket.correlation_file_id == "AN-192"

#     assert ticket.acquisition_pass == ["S2A_X-Band_44974_SGS"]


# def test_cams_cloud_ticket_created_after_failed():
#     report = CamsCloudAnomalyCorrelation(
#         **{
#             "reportName": "Jira_CAMS_Cloud_Anomaly_Correlation_20240207_142434086673_1.json",
#             "created": "2025-02-01T03:18:38.354Z",
#             "description": "Missing S2A datatstrip data due to antenna acquisition issue at Svalbard Station",
#             "impacted_passes": ["44974"],
#             "impacted_observations": ["S2A-44973-3"],
#             "issue": "GSANOM-14445",
#             "key": "AN-192",
#             "origin": "Acquisition",
#             "summary": "GSANOM-14445 - anomaly correlation",
#             "sattelite_unit": "S2A",
#             "station_type": "X-Band",
#             "station": "SGS",
#             "status": "Done",
#             "title": "GSANOM-14445 - anomaly correlation",
#             "updated": "2024-02-01T15:20:34.397Z",
#             "interface_name": "Jira_CAMS_Cloud_Anomaly_Correlation",
#             "ingestionTime": "2024-02-01T22:38:39.185Z",
#         }
#     )
#     report.meta.id = "AN-192"
#     report.meta.index = "raw-data-cams-cloud-anomaly-correlation-static"
#     report.full_clean()

#     ticket = CdsCamsTickets(
#         **{
#             "created": "2024-02-01T03:18:31.763Z",
#             "occurence_date": "2024-02-01T03:00:00.000Z",
#             "title": "CGS-SGS: S2A: 44974: Data missing, FER above threshold",
#             "url": "https://esa-cams.atlassian.net/browse/GSANOM-14445",
#             "datatake_ids": ["S2A-44973-3"],
#             "linked_issues": "AN-192",
#             "updated": "2024-02-14T14:47:50.207Z",
#             "key": "GSANOM-14445",
#             "status": "Closed",
#             "affected_systems": "S-2",
#             "assigned_element": ["ATOS", "ESA S-2", "OMCS", "Svalbard Station"],
#             "criticality": "Blocking",
#             "entity": "Svalbard Station",
#             "involved_entities": ["ATOS", "ESA S-2", "OMCS", "Svalbard Station"],
#             "originating_entity": "Svalbard Station",
#             "reporter": "sentinel-cams@ksat.no",
#             "review_board_dispositions": "Coorddesk(jnschmidt)@2024-02-01: delegated to Svalbard station for investigation",
#             "urgency": "Low",
#         }
#     )
#     ticket.meta.id = ""
#     ticket.meta.index = ""
#     ticket.full_clean()
#     engine = CorrelateAnomalyTicketEngine()
#     engine.consolidate_cams_cloud_ticket(report, ticket)

#     assert "origin" in ticket
#     assert "description" in ticket
#     assert ticket.correlation_file_id == "AN-192"

#     assert ticket.acquisition_pass == []


# def test_cams_cloud_ticket_edrs_new_station_format():
#     report = CamsCloudAnomalyCorrelation(
#         **{
#             "reportName": "Jira_CAMS_Cloud_Anomaly_Correlation_20250723_131915863672_1.json",
#             "created": "2025-07-22T07:31:18.162Z",
#             "issue": "GSANOM-19558",
#             "key": "AN-4655",
#             "summary": "GSANOM-19558 - anomaly correlation",
#             "status": "Created",
#             "title": "GSANOM-19558 - anomaly correlation",
#             "updated": "2025-07-23T13:09:24.399Z",
#             "interface_name": "Jira_CAMS_Cloud_Anomaly_Correlation",
#             "ingestionTime": "2025-07-23T13:19:16.572Z",
#             "description": "GS1_SC-328.\r\nImpact in completeness: 1 DT",
#             "impacted_passes": ["S1A-L20250527142528290000209"],
#             "impacted_observations": ["S1A-490112", "S1A-490114"],
#             "sattelite_unit": "S1A",
#             "station_type": "EDRS",
#             "station": "RDGS + HDGS + notec",  # Custom edit to fully test whitelsit station
#         }
#     )
#     report.meta.id = "AN-4655"
#     report.meta.index = "raw-data-cams-cloud-anomaly-correlation-static"
#     report.full_clean()

#     ticket = CdsCamsTickets(
#         **{
#             "affected_systems": "S-1",
#             "assigned_element": ["EDRS", "ESA S-1", "S-1A Production - SERCO"],
#             "created": "2025-07-22T07:31:16.293Z",
#             "criticality": "Critical",
#             "involved_entities": ["EDRS", "ESA S-1", "S-1A Production - SERCO"],
#             "key": "GSANOM-19558",
#             "linked_issues": "AN-4655",
#             "occurence_date": "2025-07-21T14:30:00.000Z",
#             "originating_entity": "S-1A Production - SERCO",
#             "reporter": "cscs1s3pf-EXPR",
#             "status": "Closed",
#             "title": "[S1A] DTs 077A80 077A82 for EDR session L20250527142528290000209 partially extracted",
#             "updated": "2025-07-23T14:09:15.905Z",
#             "urgency": "Medium",
#             "correlation_file_id": "AN-4655",
#             "url": "https://esa-cams.atlassian.net/browse/GSANOM-19558",
#             "entity": "EDRS",
#             "review_board_dispositions": "OCS(F.Cerreti)@2025-07-22 Assigned as first line to EDRS team in order to assess if communication to FOS is needed",
#         }
#     )
#     ticket.meta.id = "GSANOM-19558"
#     ticket.meta.index = "cds-cams-tickets-static"
#     ticket.full_clean()
#     engine = CorrelateAnomalyTicketEngine()
#     engine.consolidate_cams_cloud_ticket(report, ticket)

#     # "acquisition_pass": ["S1A_EDRS_L20250527142528290000209_RDGS + HDGS"],
#     assert ticket.acquisition_pass == [
#         "S1A_EDRS_L20250527142528290000209_HDGS",
#         "S1A_EDRS_L20250527142528290000209_RDGS",
#     ]
