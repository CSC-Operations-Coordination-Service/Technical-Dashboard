"""Deletion tracking system"""

from typing import List

from maas_cds.model.generated import MaasConfigCollector
from maas_collector.rawdata.collector.credentialmixin import CredentialMixin

from maas_collector.rawdata.configuration import build_collector_configuration
from maas_collector.rawdata.implementation import (
    get_collector_class_by_config_classname,
)

from maas_engine.engine.rawdata import DataEngine
from maas_cds.model import (
    DeletionIssue,
    CdsInterfaceProductDeletion,
    CdsPublication,
)


from maas_cds.lib.parsing_name.utils import (
    generate_publication_names,
)


class TrackDeletionEngine(DataEngine, CredentialMixin):
    """Consolidate CdsInterfaceProductDeletion / DeletionIssue"""

    ENGINE_ID = "TRACK_DELETION"

    def __init__(
        self, args=None, send_reports=True, interface_dict=None, credential_dict=None
    ):
        super().__init__(args, send_reports=send_reports)
        if not interface_dict:
            self.logger.error("You must supply an interface dict")
            interface_dict = {}

        if not credential_dict:
            self.logger.error("You must supply an credentials dict")
            credential_dict = {}

        self.credential_dict = credential_dict
        self.interface_dict = interface_dict

    def translate_service_ids(self, names: List[str]) -> List[str]:
        """
        Translate user input to real service name using the engine parameter map

        Args:
            names (List[str]): service names from jira ticket

        Returns:
            List[str]: translated names
        """

        if isinstance(names, str):
            names = [names]
        return [self.interface_dict.get(name.lower(), name) for name in names]

    def action_iterator(self):
        """route the action iterator depending of the payload document class"""
        document_class = self.payload.document_class

        if document_class == "CdsInterfaceProductDeletion":
            yield from self.action_iterator_from_deletions(self.input_documents)

        elif document_class == "DeletionIssue":
            for issue in self.input_documents:
                products_deletion = (
                    CdsInterfaceProductDeletion.search()
                    .filter("term", jira_issue=issue.key)
                    .params(version=True, seq_no_primary_term=True, size=10000)
                    .execute()
                )

                yield from self.action_iterator_from_deletions(products_deletion)

        else:
            raise TypeError(
                f"Unexpected input document class to track deletion: {document_class}"
            )

    def action_iterator_from_deletions(
        self, products_deletion: List[CdsInterfaceProductDeletion]
    ):

        for deletion in products_deletion:

            # Init
            products_id_to_download = {}

            if deletion.interface_type not in products_id_to_download:
                products_id_to_download[deletion.interface_type] = {}

            # if hasattr(deletion, "effective_product_name") is not None:
            #     continue
            deletion_result = DeletionIssue.get_by_id(deletion.jira_issue)

            possible_name = list(generate_publication_names(deletion.product_name))

            service_ids = self.translate_service_ids(
                deletion_result.deletion_interfaces
            )

            self.logger.debug("Service IDs : %s", service_ids)

            for service_id in service_ids:
                # Init
                if service_id not in products_id_to_download[deletion.interface_type]:
                    products_id_to_download[deletion.interface_type][service_id] = []

                attr_name = (
                    self.local_attribute_prefix(deletion.interface_type, service_id)
                    + "_product_uuid"
                )
                if service_product_uuid := hasattr(deletion, attr_name) and getattr(
                    deletion, attr_name
                ):
                    self.logger.debug(
                        "[%s - %s] There is already a product uuid for %s : %s",
                        deletion.interface_type,
                        service_id,
                        deletion.product_name,
                        service_product_uuid,
                    )
                    products_id_to_download[deletion.interface_type][service_id].append(
                        service_product_uuid
                    )
                    continue

                publications_query = (
                    CdsPublication.search()
                    .filter(
                        "term",
                        service_type=deletion.interface_type,
                    )
                    .filter(
                        "term",
                        service_id=service_id,
                    )
                    .filter(
                        "terms",
                        name=possible_name,
                    )
                )

                publications = list(
                    publications_query.params(
                        version=True, seq_no_primary_term=True, ignore=404, size=10
                    ).execute()
                )

                nb_publication_find = len(publications)
                if nb_publication_find == 0:
                    self.logger.warning(
                        "[%s - %s] There is no product for %s",
                        deletion.interface_type,
                        service_id,
                        deletion.product_name,
                    )

                elif nb_publication_find > 1:
                    self.logger.warning(
                        "[%s - %s] There is no product for %s",
                        deletion.interface_type,
                        service_id,
                        deletion.product_name,
                    )
                else:
                    matched_publication = publications[0]
                    self.logger.debug(
                        "[%s - %s] There is a product for %s named : %s",
                        deletion.interface_type,
                        service_id,
                        deletion.product_name,
                        matched_publication.name,
                    )

                    deletion.effective_product_name = matched_publication.name
                    setattr(
                        deletion,
                        self.local_attribute_prefix(deletion.interface_type, service_id)
                        + "_product_uuid",
                        matched_publication.product_uuid,
                    )

                    products_id_to_download[deletion.interface_type][service_id].append(
                        matched_publication.product_uuid
                    )

            for interface_type, services in products_id_to_download.items():
                for service_id, product_uuids in services.items():
                    interface_name = f"{interface_type}_{service_id}"

                    # Exprivia_S1/S2/S3
                    if service_id == "Exprivia":
                        interface_name += f"_{deletion.product_name[0:2]}"

                    for product_uuid in product_uuids:

                        status = self.collect_product(interface_name, product_uuid)

                        if status is None:
                            # Fail to get a valid status
                            continue

                        attr_name = (
                            self.local_attribute_prefix(
                                deletion.interface_type, service_id
                            )
                            + "_deletion_history"
                        )

                        if not hasattr(deletion, attr_name):
                            setattr(deletion, attr_name, [])

                        getattr(deletion, attr_name).append(status)

                        attr_name = (
                            self.local_attribute_prefix(
                                deletion.interface_type, service_id
                            )
                            + "_is_available"
                        )

                        setattr(deletion, attr_name, status["available"])

            yield deletion.to_bulk_action()

    def local_attribute_prefix(self, service_id, service_name):
        return f"{service_id}_{service_name}"

    def collect_product(self, interface_name, product_uuid):

        self.logger.info(
            "[%s] - Trying to fetch product %s", interface_name, product_uuid
        )

        collect_conf = MaasConfigCollector.get_by_id(interface_name)

        if collect_conf is None:
            self.logger.warning("There is not collector config for %s", interface_name)
            return

        collect_conf_dict = collect_conf.to_dict()

        collector_class = get_collector_class_by_config_classname(
            collect_conf_dict["class"]
        )

        collector_config = build_collector_configuration(
            collect_conf_dict, collector_class.CONFIG_CLASS
        )

        self.set_credential_attributes(collector_config, self.credential_dict)

        item_status = collector_class.probe_item(collector_config, product_uuid)

        return item_status
