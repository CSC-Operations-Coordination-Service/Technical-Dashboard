"""Consolidation of Deletion ticket"""

from maas_cds.model import CdsDeletionIssue, DeletionIssue
from maas_engine.engine.replicate import ReplicatorEngine
from typing import Union


class DeletionIssueConsolidatorEngine(ReplicatorEngine):
    """Consolidate raw deletion tickets"""

    ENGINE_ID = "CONSOLIDATE_DELETION_TICKET"

    CONSOLIDATED_MODEL = CdsDeletionIssue

    def __init__(
        self,
        args=None,
        send_reports=False,
        min_doi=None,
        target_model="CdsDeletionIssue",
        exclude_fields=None,
        include_fields=None,
        interface_dict=None,
    ):

        super().__init__(
            args,
            target_model=target_model,
            include_fields=include_fields,
            exclude_fields=exclude_fields,
            send_reports=send_reports,
            min_doi=min_doi,
        )

        if interface_dict is None:
            self.interface_dict = {}
        else:
            self.interface_dict = interface_dict

    def get_consolidated_id(self, raw_document: DeletionIssue):
        return raw_document.meta.key

    def consolidate(
        self, raw_document: DeletionIssue, document: CdsDeletionIssue
    ) -> Union[CdsDeletionIssue, None]:
        """consolidate metrics data

        Args:
            raw_document (MetricsProduct): raw MetricsProduct extracted from metrics api
            document (CdsMetricsProduct): consolidated data

        Returns:
            CdsMetricsProduct: consolided data
        """
        document = super().consolidate(raw_document, document)

        if document.deletion_interfaces:
            unique_interfaces = {name.strip() for name in document.deletion_interfaces}

            document.deletion_interfaces = [
                self.interface_dict.get(interface.lower(), interface)
                for interface in unique_interfaces
            ]
        return document
