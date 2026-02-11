"""Custom CDS model definition for publication"""

import logging

from opensearchpy import Keyword
from maas_cds.model.anomaly_mixin import AnomalyMixin
from maas_cds.model.dynamic_partition_mixin import DynamicPartitionMixin
from maas_cds.model.product_datatake_mixin import ProductDatatakeMixin

from maas_cds.model import generated
import maas_cds.model.cds_completeness as cds_completeness_model


__all__ = ["CdsPublication"]


LOGGER = logging.getLogger("CdsPublication")


class CdsPublication(
    DynamicPartitionMixin, AnomalyMixin, ProductDatatakeMixin, generated.CdsPublication
):
    """CdsPublication custom"""

    cams_tickets = Keyword(multi=True)

    _PARTITION_FIELDS = [
        "publication_date",
    ]

    def mark_as_deleted(self, issue: "DeletionIssue", service_ids: dict = None):
        """Populate attributes to reflect deletion from the interface.

        Args:
            issue (DeletionIssue): issue
            service_ids (dict): Unused. Defaults to None
        """
        self.deletion_issue = issue.key
        self.deletion_date = issue.deletion_date
        self.deletion_cause = issue.deletion_cause

    @property
    def completeness_document_index(self):

        target_index = cds_completeness_model.CdsCompleteness(
            mission=self.mission,
            satellite_unit=self.satellite_unit,
            service_type=self.service_type,
            service_id=self.service_id,
        ).partition_index_name

        return target_index

    @property
    def completeness_document_class(self):

        target_model_class_name = f"CdsCompleteness{self.mission}"

        target_model_class = getattr(
            cds_completeness_model,
            target_model_class_name,
            cds_completeness_model.CdsCompleteness,
        )

        return target_model_class

    def get_completeness_document(self):

        target_model_class = f"CdsCompleteness{self.mission}"

        datatake_doc = getattr(
            cds_completeness_model,
            target_model_class,
            cds_completeness_model.CdsCompleteness,
        ).get_by_id(
            f"{self.satellite_unit}-{self.datatake_id}",
            [self.completeness_document_index],
        )

        return datatake_doc

    @property
    def completeness_key(self):
        """This is only made and tested for S1 and S2

        Returns:
            dict: a dict that contains all information to compute completeness
        """
        return {
            "index": self.completeness_document_index,
            "class": self.completeness_document_class,
            "key": "-".join(
                [
                    self.satellite_unit,
                    self.datatake_id,
                ]
            ),
            "satellite_unit": self.satellite_unit,
            "datatake_id": self.datatake_id,
            "product_type": self.product_type,
            "product_level": self.product_level,
            "service_type": self.service_type,
            "service_id": self.service_id,
        }

    @property
    def completeness_splitted_document_index(self):

        target_index = cds_completeness_model.CdsCompletenessSplitted(
            mission=self.mission,
            satellite_unit=self.satellite_unit,
            service_type=self.service_type,
            service_id=self.service_id,
        ).partition_index_name

        return target_index

    @property
    def completeness_splitted_document_class(self):

        target_model_class_name = f"CdsCompletenessSplitted{self.mission}"

        target_model_class = getattr(
            cds_completeness_model,
            target_model_class_name,
            cds_completeness_model.CdsCompletenessSplitted,
        )

        return target_model_class

    def get_completeness_splitted_document(self):

        target_model_class = f"CdsCompletenessSplitted{self.mission}"

        datatake_doc_id = self.completeness_splitted_key["key"]
        datatake_doc = getattr(
            cds_completeness_model,
            target_model_class,
            cds_completeness_model.CdsCompletenessSplitted,
        ).get_by_id(
            datatake_doc_id,
            [self.completeness_splitted_document_index],
        )

        return datatake_doc

    @property
    def completeness_splitted_key(self):
        """This is only made and tested for S3 and S5

        Returns:
            dict: a dict that contains all information to compute completeness grouped
        """
        return {
            "index": self.completeness_splitted_document_index,
            "class": self.completeness_splitted_document_class,
            "key": "-".join(
                [
                    self.datatake_id,  # Already prefixed by satellite
                    self.timeliness,
                    self.product_type,
                ]
            ),
            "mission": self.mission,
            "satellite_unit": self.satellite_unit,
            "datatake_id": self.datatake_id,
            "product_type": self.product_type,
            "product_level": self.product_level,
            "timeliness": self.timeliness,  # Needed for s3-s5
            "service_type": self.service_type,
            "service_id": self.service_id,
        }
