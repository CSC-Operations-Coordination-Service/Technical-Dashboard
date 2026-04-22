"""Engine to compute all duplication indicator for a given datatake, using a product or a deletion ticket"""

from maas_engine.engine.rawdata import DataEngine

from maas_cds import model


class ComputeDuplicationEngine(DataEngine):
    """Consolidate cds datatake"""

    ENGINE_ID = "COMPUTE_DUPLICATION"

    def action_iterator(self):
        # get the specific bulk action iterator
        document_class = self.payload.document_class

        if document_class.startswith("CdsProduct"):
            iterator = self.action_iterator_from_product()

        elif document_class.startswith("CdsDatatake"):
            iterator = self.action_iterator_from_datatake()

        elif document_class.startswith("CdsDuplication"):
            iterator = self.action_iterator_from_duplication()

        else:
            raise TypeError(
                f"Unexpected input document class for completeness: {document_class}"
            )

        yield from iterator

    def action_iterator_from_datatake(self):
        """Compute duplication indicator from CdsDatatake

        Yields:
            dict: bulk action
        """
        # By using a data engine all document in the message will be laod in self.input_documents
        for datatake in self.input_documents:

            pass

        if False:
            yield

    def action_iterator_from_product(self):
        """Compute duplication indicator from CdsProduct

        Yields:
            dict: bulk action
        """

        if False:
            yield

    def action_iterator_from_duplication(self):
        """Compute duplication indicator from CdsDuplication

        Yields:
            dict: bulk action
        """

        if False:
            yield
