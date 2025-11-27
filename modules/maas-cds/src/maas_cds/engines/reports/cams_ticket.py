"""GSANOM consolidation"""

from maas_engine.engine.replicate import ReplicatorEngine
from maas_cds.model import CdsCamsTickets, CamsCloudTickets
from typing import Union


class CamsTicketConsolidatorEngine(ReplicatorEngine):
    """Consolidate Cams Ticket"""

    ENGINE_ID = "CONSOLIDATE_CAMS_TICKET"

    CONSOLIDATED_MODEL = CdsCamsTickets

    # Configuration information this can be located in the database or config json
    INUVIK_STATION = "Inuvik Station"
    NEUSTRELITZ_STATION = "Neustrelitz Station"
    SVALBARD_STATION = "Svalbard Station"

    def __init__(
        self,
        args=None,
        send_reports=False,
        min_doi=None,
        target_model="CdsCamsTickets",
        exclude_fields=None,
        include_fields=None,
        base_url=None,
    ):
        if base_url is None:
            raise ValueError("base_url argument must be provided and cannot be None")

        # Add some default configuration for this replciator engine
        # if include_fields is None:
        #     include_fields = []
        if exclude_fields is None:
            exclude_fields = [
                "reportName",
                "ingestionTime",
                "interface_name",
                "reportFolder",
            ]
        super().__init__(
            args,
            target_model=target_model,
            include_fields=include_fields,
            exclude_fields=exclude_fields,
            send_reports=send_reports,
            min_doi=min_doi,
        )

        self.base_url = base_url

    def get_consolidated_id(self, raw_document: CamsCloudTickets):
        return raw_document.meta.id

    def consolidate(
        self, raw_document: CamsCloudTickets, document: CdsCamsTickets
    ) -> Union[CdsCamsTickets]:
        """consolidate jira document data

        Args:
            raw_document (CdsCamsTickets): raw CdsCamsTickets extracted from jira api
            document (CdsCamsTickets): consolidated data

        Returns:
            CdsCamsTickets: consolided data
        """
        document = super().consolidate(raw_document, document)

        # Extra replicate assignation

        document.url = self.base_url + document.meta.id

        # Some dashboard use this previous field, filter also here in case of futur updateé
        if raw_document.linked_issues is not None:

            document.correlation_file_id = [
                issue for issue in raw_document.linked_issues if issue.startswith("AN")
            ]
        else:
            document.correlation_file_id = []

        if (
            "DLR Acquisition Service" == document.entity
            and not self.NEUSTRELITZ_STATION in document.assigned_element
        ):
            document.assigned_element.append(self.NEUSTRELITZ_STATION)

        if (
            "SSC Acquisition Service" == document.entity
            and not self.INUVIK_STATION in document.assigned_element
        ):
            document.assigned_element.append(self.INUVIK_STATION)

        if isinstance(document.affected_systems, str):
            document.affected_systems = [document.affected_systems]

        if "S-5p" in document.affected_systems:
            if (
                "INU" in document.title
                and self.INUVIK_STATION not in document.assigned_element
            ):
                document.assigned_element.append(self.INUVIK_STATION)
            if (
                "SGS" in document.title
                and self.SVALBARD_STATION not in document.assigned_element
            ):
                document.assigned_element.append(self.SVALBARD_STATION)

        document.assigned_element = list(set(document.assigned_element))

        return document
