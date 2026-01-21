"""Publication consolidation"""

from maas_cds.engines.compute.compute_completeness import ComputeCompletenessEngine
from maas_cds.lib.parsing_name import utils
from maas_engine.engine.rawdata import DataEngine
from maas_cds.model.cds_completeness import CdsCompleteness

from maas_cds.model.enumeration import CompletenessScope

from maas_cds import model


class ComputeCompletenessEngineV2(ComputeCompletenessEngine):
    """Consolidate cds datatake"""

    ENGINE_ID = "COMPUTE_COMPLETENESS_V2"

    # When init from MP
    #  -> check from config what is needed on this periode / satellite
    # CdsPublication methode -> associate_completeness_index_name -> associate datatake_id doc reference
    #

    def load_datatake_doc(self, compute_key):
        """Load a datatake in the local cache

        Args:
            datatake_id (str): The datatake to load
            mission (str, optional): The mission of the datatake. Defaults to "".
        """

        self.logger.debug(
            "[CACHE] - Trying to add in cache: %s from %s as %s",
            compute_key["datatake_id"],
            compute_key["index"],
            compute_key["class"],
        )

        # ! TODO - Optimisation to reduce and group into a single query
        datatake_doc = compute_key["class"].get_by_id(
            f"{compute_key['satellite_unit']}-{compute_key['datatake_id']}",
            [compute_key["index"]],
        )

        original_datatake_doc = None

        if datatake_doc is not None:
            original_datatake_doc = datatake_doc.to_dict()

        else:
            self.logger.warning(
                "[CACHE] - Datatake id not found in %s index "
                "can't load it into local cache: %s",
                compute_key["index"],
                compute_key["datatake_id"],
            )

        self.local_cache_datatake[
            ComputeCompletenessEngineV2.compute_key_cache(compute_key)
        ] = (
            datatake_doc,
            original_datatake_doc,
        )

    @staticmethod
    def compute_key_cache(compute_key):
        # If this need to be refactor for s3-s5 we also need the product-type
        return f"{compute_key['index']}-{compute_key['datatake_id']}"

    def get_datatake_doc(self, compute_key):
        """Get a datatake doc from the local cache

        Args:
            datatake_id (str): _description_

        Returns:
            CdsDatatake: The cds-datatake doc associate to the asked datatake_id
        """

        key_in_cache = ComputeCompletenessEngineV2.compute_key_cache(compute_key)

        if key_in_cache not in self.local_cache_datatake:
            self.load_datatake_doc(compute_key)

        return self.local_cache_datatake[key_in_cache][0]

    def action_iterator(self):
        # get the specific bulk action iterator
        document_class = self.payload.document_class

        if document_class.startswith("CdsPublication"):
            iterator = self.action_iterator_from_publication()
        elif document_class.startswith("CdsCompleteness"):
            iterator = self.action_iterator_from_datatake()
        else:
            raise TypeError(
                f"Unexpected input document class for completeness: {document_class}"
            )

        # bulk feed
        for action in iterator:
            yield action

    def action_iterator_from_datatake(self):
        """Compute completeness from CdsDataTake

        Yields:
            dict: bulk action
        """

        self.logger.info("[ITER][Datatake] - start")

        # TODO add a cache to load completeness config

        for datatake_doc in self.input_documents:

            original_datatake_dict = datatake_doc.to_dict()

            # reset all field not mapped
            datatake_doc.purge_dynamic_fields()

            # TODO for s2
            yield from datatake_doc.load_data_before_compute()

            self.logger.debug("Instance are %s", type(datatake_doc))

            datatake_doc.compute_all_local_completeness()

            datatake_doc.compute_global_completeness()

            if original_datatake_dict != datatake_doc.to_dict():
                self.logger.info("[ITER][Datatake] - Pushing update %s", datatake_doc)

                yield datatake_doc.to_bulk_action()

            else:
                self.logger.info(
                    "[ITER][Datatake] - Nothing to do for %s", datatake_doc
                )

        self.logger.info("[ITER][Datatake] - end")

    def load_compute_keys_from_input_documents(self):
        """Load unique compute_key from input documents

        Yields:
            dict: bulk action with publications
        """

        self.logger.info("[ITER][Publication] - start")
        # input document can be CdsPublication or CdsPublication

        for publication_document in self.input_documents:
            self.logger.debug(
                "[ITER][Publication] - Compute completeness for %s",
                publication_document.name,
            )
            original_dict = publication_document.to_dict()

            # TODO for s2 mainly
            # Add the document in parrallel
            if original_dict != publication_document.to_dict():

                # Convert DAO to bulk payload
                publication_document_dict = publication_document.to_bulk_action()

                yield publication_document_dict

            # Group compute to avoid duplicate and save computation
            completeness_key = publication_document.completeness_key

            self.logger.debug("[ITER][Publication] - Key : %s", completeness_key)

            # Maybe here filter out not expected compute key
            if (
                completeness_key["product_type"] == "AMALFI_REPORT"
                or completeness_key["datatake_id"] == utils.DATATAKE_ID_MISSING_VALUE
            ):
                continue

            if not completeness_key:
                self.logger.warning(
                    "[ITER][Publication] - (%s) : No compute key",
                    publication_document.name,
                )
            elif completeness_key in self.tuples_to_compute:
                self.logger.debug(
                    "[ITER][Publication] - (%s) : Compute key already present",
                    publication_document.name,
                )
            else:
                # ! TODO refactor this in a single indentifier
                # ? TODO difference between datatake_id and this ?
                # datatake_id = publication_document.get_datatake_id()

                datatake_doc = self.get_datatake_doc(completeness_key)
                if datatake_doc is None:
                    self.logger.debug(
                        "[ITER][Publication] - Datatake is missing skip this key : %s",
                        completeness_key,
                    )
                    continue

                # TODO for S2
                # initially for retrieve_additional_fields_from_product
                datatake_doc.retrieve_additional_fields_from_publication(
                    publication_document
                )

                self.logger.debug(
                    "[ITER][Publication] - Added key to compute : %s",
                    completeness_key,
                )
                self.tuples_to_compute.append(completeness_key)

                other_calculations = datatake_doc.impact_other_calculation(
                    completeness_key
                )
                # TODO : Need to take in considertion the new format

                new_calculations = [
                    calc
                    for calc in other_calculations
                    if calc not in self.tuples_to_compute
                ]

                for new_calculation in new_calculations:
                    self.logger.debug(
                        "[ITER][Publication] - Added extra key to compute : %s",
                        new_calculation,
                    )
                    self.tuples_to_compute.append(new_calculation)

    def action_iterator_from_publication(self):
        """Compute completeness from CdsPublication

        Yields:
            dict: bulk action
        """

        # ! Verify this - Update publications sometime S2 ctx
        yield from self.load_compute_keys_from_input_documents()

        # compute local completeness
        for completeness_key in self.tuples_to_compute:

            datatake_doc = self.get_datatake_doc(completeness_key)

            datatake_id = completeness_key["datatake_id"]
            product_type = completeness_key["product_type"]

            if datatake_doc is None:
                self.logger.info(
                    "[ITER][Publication][%s][%s] - Datatake not find - skipping",
                    completeness_key["index"],
                    datatake_id,
                )
                continue

            related_publications = []

            local_value = datatake_doc.compute_local_value(
                product_type, related_publications
            )

            datatake_doc.set_completeness(
                CompletenessScope.LOCAL,
                product_type,
                local_value,
            )

            datatake_doc.compute_missing_production(product_type, related_publications)

            datatake_doc.compute_duplicated(product_type, related_publications)

            self.logger.info(
                "[ITER][Publication][%s] - Compute local value : %s -> %s",
                datatake_id,
                product_type,
                local_value,
            )

        # compute global completeness for all datatake in cache
        for completeness_cache_key, (
            datatake_doc,
            original_datatake_doc_dict,
        ) in self.local_cache_datatake.items():

            if datatake_doc is None:
                self.logger.info(
                    "[ITER][Publication][%s] - Datatake not find - skipping",
                    completeness_cache_key,
                )
                continue

            self.logger.info(
                "[ITER][Publication][%s] - Compute global value",
                datatake_doc.datatake_id,
            )

            datatake_doc.compute_global_completeness()

            new_doc_dict = datatake_doc.to_dict()

            # Detect if update was made
            if original_datatake_doc_dict != new_doc_dict:

                # Convert DAO to bulk payload
                datatake_doc_dict = datatake_doc.to_bulk_action()

                self.logger.info(
                    "[ITER][Publication][%s] - Pushing update", datatake_doc.datatake_id
                )

                # go feed parallel_bulk
                yield datatake_doc_dict

            else:
                self.logger.debug(
                    "[ITER][Publication][%s] - Nothing to do", datatake_doc.datatake_id
                )

        self.logger.info("[ITER][Publication] - end")
