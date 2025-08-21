"""Update hktm completeness after related products are ingested"""

from typing import Callable, List, Dict, Tuple, Generator
from datetime import timedelta, datetime

from opensearchpy import Q, MultiSearch

from maas_engine.engine.rawdata import DataEngine

from maas_cds.model import (
    CdsHktmProductionCompleteness,
    CdsHktmAcquisitionCompleteness,
    CdsProduct,
)
from maas_cds import model


class ComputeHktmRelatedEngine(DataEngine):
    """Update documents related to hktm creation or update"""

    ENGINE_ID = "COMPUTE_HKTM_RELATED"

    SESSION_ID_META = {
        "CdsEdrsAcquisitionPassStatus": {
            "hktm_completeness": "edrs_completeness",
        },
        "CdsCadipAcquisitionPassStatus": {
            "hktm_completeness": "cadip_completeness",
        },
    }

    def __init__(
        self,
        args=None,
        target_model: str = None,
        send_reports=False,
        tolerance_value: int = 30,
    ):
        """constructor

        Args:
            args (namespace, optional): cli options. Defaults to None.
            target_model (str, optional): Model class name. Defaults to None.
            send_reports (bool, optional): flag. Defaults to False.
        """
        super().__init__(args, send_reports=send_reports)

        self.target_model: (
            CdsHktmAcquisitionCompleteness | CdsHktmProductionCompleteness
        ) = target_model

        self.tolerance_value = tolerance_value

    def update_hktm_factory(self) -> Callable:
        """
        Factory that returns the hktm update method for each
        valid target model

        Args:
            document : target document that need to be updated

        Returns:
            callable: update hktm method
        """
        if self.target_model == "CdsHktmProductionCompleteness":
            return self.update_hktm_production
        elif self.target_model == "CdsHktmAcquisitionCompleteness":
            return self.update_hktm_acquisition
        else:
            raise ValueError(f"Unexpected target model : {self.target_model}")

    def search_hktm_factory(self) -> Callable:
        """
        Factory that returns the hktm search method for each
        valid target model

        Args:
            document : target document that need to be updated

        Returns:
            callable: search hktm method
        """
        if self.target_model == "CdsHktmProductionCompleteness":
            return self.search_hktm_production
        elif self.target_model == "CdsHktmAcquisitionCompleteness":
            return self.search_hktm_acquisition
        else:
            raise ValueError(f"Unexpected target model : {self.target_model}")

    def update_hktm_production(
        self, document: CdsHktmProductionCompleteness
    ) -> CdsHktmProductionCompleteness:
        """Sets the completeness attribute to 1

        Args:
            document (CdsHktmProductionCompleteness): input document

        Returns:
            CdsHktmProductionCompleteness: updated document
        """
        setattr(document, "completeness", 1)

        return document

    def update_hktm_acquisition(
        self, document: CdsHktmAcquisitionCompleteness
    ) -> CdsHktmAcquisitionCompleteness:
        """Sets the completeness attribute to 1

        Args:
            document (CdsHktmAcquisitionCompleteness): input document

        Returns:
            CdsHktmAcquisitionCompleteness: updated document
        """
        setattr(
            document,
            self.SESSION_ID_META[self.input_model.__name__]["hktm_completeness"],
            1,
        )

        return document

    def search_hktm_production(
        self, documents: CdsProduct
    ) -> Tuple[MultiSearch, List[Dict]]:
        """
        Search for HKTM information within a tolerance window.

        This method performs an HKTM search based on a list of input documents and applies
        a tolerance window to match effective downlink start dates.

        Args:
        - documents: A list of raw documents for HKTM search.

        Returns:
        - msearch: An Elasticsearch MultiSearch object containing search queries.
        - valid_input_documents: A list of valid input documents used for the search.
        """
        msearch = MultiSearch()

        tolerance_value = timedelta(minutes=self.tolerance_value)

        valid_input_documents = []
        for cds_product in documents:
            sensing_start_date = getattr(cds_product, "sensing_start_date")

            # ? Use of orbit but only for S1 usage of CdsProductSX can be usefull
            search = (
                CdsHktmProductionCompleteness.search()
                .filter("term", satellite_unit=cds_product.satellite_unit)
                .filter(
                    "range",
                    effective_downlink_start={
                        "lte": sensing_start_date + tolerance_value
                    },
                )
                .filter(
                    "range",
                    effective_downlink_start={
                        "gte": sensing_start_date - tolerance_value
                    },
                )
            )

            if cds_product.mission == "S1":
                search = search.filter(
                    "term", downlink_absolute_orbit=cds_product.absolute_orbit
                )

            msearch = msearch.add(search)

            valid_input_documents.append(cds_product)

        return msearch, valid_input_documents

    def search_hktm_acquisition(self, documents) -> Tuple[MultiSearch, List[Dict]]:
        """
        Search for HKTM information within a tolerance window.

        This method performs an HKTM search based on a list of input documents and applies
        a tolerance window to match effective downlink start dates.

        Args:
        - documents: A list of raw documents for HKTM search.

        Returns:
        - msearch: An Elasticsearch MultiSearch object containing search queries.
        - valid_input_documents: A list of valid input documents used for the search.
        """
        msearch = MultiSearch()

        valid_input_documents = []

        for raw_document in documents:
            # To improve : associated the product event the status is KO
            if raw_document.get_status() == "OK":

                msearch = msearch.add(
                    raw_document.search_acquistion_completeness_document()
                )

                valid_input_documents.append(raw_document)

        return msearch, valid_input_documents

    def action_iterator(self) -> Generator:
        """overridee

        Iter throught input documents and find products who are inside
        Then add informations on these products

        Yields:
            Iterator[Generator]: bulk actions
        """
        search_method = self.search_hktm_factory()
        msearch, valid_input_documents = search_method(self.input_documents)

        self.logger("[%s] - Running engine", self.input_model)

        if valid_input_documents:
            # contained identifier to container instance as MultiSearch does not support
            # metadata like params(version=True, seq_no_primary_term=True)
            result_map = {}

            for raw_document, response in zip(valid_input_documents, msearch.execute()):
                if not response:
                    self.logger.warning("No hktm found %s", raw_document)
                    continue

                for document in response:
                    # store link between content and container
                    result_map[document.meta.id] = raw_document

            # retrieve again targeted documents as msearch does not support versionning :'(
            for hktm_completeness_document, proof_document in zip(
                getattr(model, self.target_model).mget_by_ids(list(result_map.keys())),
                result_map.values(),
            ):
                initial_dict = hktm_completeness_document.to_dict()

                update_method = self.update_hktm_factory()
                hktm_completeness_document = update_method(hktm_completeness_document)

                if (
                    getattr(hktm_completeness_document, "related_document_id")
                    and proof_document.meta.id
                    != hktm_completeness_document.related_document_id
                ):
                    self.logger.warning(
                        "[%s] - This document was already completed by : %s (%s)",
                        hktm_completeness_document.meta.id,
                        hktm_completeness_document.related_document_name,
                        hktm_completeness_document.related_document_id,
                    )

                setattr(
                    hktm_completeness_document,
                    "related_document_id",
                    proof_document.meta.id,
                )

                fields_to_keep = [
                    # CdsProduct
                    ["name", "related_document_name"],
                    ["fos_pushing_date_backup"],
                    ["fos_pushing_date_nominal"],
                    # CdsCadipAcquisitionPassStatus
                    ["acquisition_id", "related_cadip_acquisition_id"],
                ]

                for field in fields_to_keep:
                    if hasattr(proof_document, field[0]) and (
                        value := getattr(proof_document, field[0], None)
                    ):
                        setattr(
                            hktm_completeness_document,
                            field[-1],
                            value,
                        )

                if initial_dict | hktm_completeness_document.to_dict() != initial_dict:

                    self.logger.info(
                        "[%s] - Update (%s) with %s",
                        hktm_completeness_document.meta.id,
                        hktm_completeness_document.reportName,
                        proof_document,
                    )
                    yield hktm_completeness_document.to_bulk_action()

                else:
                    self.logger.debug(
                        "[%s] - Nothing to do : %s",
                        hktm_completeness_document.meta.id,
                        document.reportName,
                    )
            else:
                self.logger.info(
                    "[%s] - Nothing to do : no hktm found",
                    valid_input_documents,
                )
        else:
            self.logger.debug(
                "[SKIPPING] - Nothing to do : no acquisition have an OK status",
            )
