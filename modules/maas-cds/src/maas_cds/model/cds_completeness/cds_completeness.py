"""Custom CDS model definition"""

import logging

from maas_cds.model.datatake import CdsDatatake

from maas_cds.model import generated

__all__ = ["CdsCompleteness"]


LOGGER = logging.getLogger("CdsModelCompleteness")


class CdsCompleteness(generated.CdsCompleteness, CdsDatatake):

    DATAFLOW_CACHE = None

    def find_brother_products_scan(self, product_type, indices=None):
        """Find products with the same datatake and the same product_type

        Note: Common method to extract publication associated on the same completeness key

        Args:
            product_type (str): product_type searched
            indices (): list of indices generated to find with more precision

        Returns:
            list(CdsPublication): list of products matching datatake_id and product_type
        """

        # TODO MAAS_CDS-1236: make a single query to find all the whole brotherhood
        # with list of datatake / product types later post-processed to be grouped by
        # tuple (datatake_id, product_type) in a dict

        search_request = (
            generated.CdsPublication.search()
            .filter("term", datatake_id=self.datatake_id)
            .filter("term", satellite_unit=self.satellite_unit)
            .filter("term", product_type=product_type)
            .filter("term", service_type=self.service_type)
            .filter("term", service_id=self.service_id)
            .params(ignore=404)
        )

        query_scan = search_request.scan()

        return query_scan

    def retrieve_additional_fields_from_publication(
        self, product: generated.CdsPublication
    ):
        """Abstract function which allow to fill additional
        datatake fields during completeness calculation"""
        pass

    def get_all_product_types(self):
        nominal_expected = super().get_all_product_types()
        applicable_config = self.get_applicable_configuration()

        applicable_product_type = [
            dataflow_item.product_type for dataflow_item in applicable_config
        ]

        return [
            product_type
            for product_type in nominal_expected
            if product_type in applicable_product_type
        ]

    def get_applicable_configuration(self):
        if self.DATAFLOW_CACHE is None:
            self.DATAFLOW_CACHE = (
                generated.MaasConfigDataflow.search()
                .filter("term", latest=True)
                .execute()[0]
            )

        # Filter DATAFLOW_CACHE records to match mission, satellite_unit, and service_type
        filtered_records = [
            record
            for record in self.DATAFLOW_CACHE.records
            if record.mission == self.mission
            and self.satellite_unit in record.satellites
            and self.service_type in record.services_config
            and record.services_config[self.service_type]
            and any(
                item.startswith(("C", "P"))
                for item in record.services_config[self.service_type]
            )
        ]

        return filtered_records
