"""Maintain cams anomalies impact over entities"""

from typing import Any, Dict, Iterator
from collections import defaultdict

from opensearchpy import NotFoundError, Keyword

from maas_model import MAASDocument

from maas_engine.engine.rawdata import DataEngine


from maas_cds.model import (
    CdsCamsTickets,
    CdsDatatakeS1,
    CdsDatatakeS2,
    CdsS3Completeness,
    CdsS5Completeness,
    CdsAcquisitionPassStatus,
    CdsCadipAcquisitionPassStatus,
    CdsEdrsAcquisitionPassStatus,
    CdsHktmAcquisitionCompleteness,
    CdsHktmProductionCompleteness,
    CdsProduct,
    CdsPublication,
)


class CorrelateAnomalyTicketEngine(DataEngine):
    """Consolidate anomaly correlation info to various entities"""

    ENGINE_ID = "CORRELATE_ANOMALY_TICKET"

    IMPACTED_CLASSES = (
        CdsDatatakeS1,
        CdsDatatakeS2,
        CdsS3Completeness,
        CdsS5Completeness,
        CdsAcquisitionPassStatus,
        CdsCadipAcquisitionPassStatus,
        CdsEdrsAcquisitionPassStatus,
        CdsHktmAcquisitionCompleteness,
        CdsHktmProductionCompleteness,
        CdsProduct,
        CdsPublication,
    )

    # To ease the extendability of these we maybe need to
    # add a custom Mixin to put the attachement strategy in different impactedclasses
    # Other strategy can be to pre compile the query, but avoiding this splitted strategy over multiple dict

    # this dictionnary maps mission to document class and retrieval method: direct
    # document identifiers for S1 & S2, or search on the datatake_id field for S3 & S5
    DATATAKE_ENTITY_DICT = {
        "S1": (CdsDatatakeS1, "ids"),
        "S2": (CdsDatatakeS2, "ids"),
        "S3": (CdsS3Completeness, "search"),
        "S5": (CdsS5Completeness, "search"),
    }

    # pylint: disable=C0301
    # black formatting makes lambda lines too long
    ACQUISITION_QUERY_DICT = {
        "EDRS": [
            {
                "class": CdsEdrsAcquisitionPassStatus,
                "search": lambda satellite_id, identifier, ground_station: CdsEdrsAcquisitionPassStatus.search()
                .query()
                .filter("term", satellite_id=satellite_id.upper())
                .filter("term", link_session_id=identifier)
                .filter("term", ground_station=ground_station.upper()),
            },
            {
                "class": CdsHktmAcquisitionCompleteness,
                "search": lambda satellite_id, identifier, ground_station: CdsHktmAcquisitionCompleteness.search()
                .query()
                .filter("term", satellite_unit=satellite_id.upper())
                .filter("term", session_id=identifier)
                .filter("term", ground_station=ground_station.upper()),
            },
            {
                "class": CdsHktmProductionCompleteness,
                "search": lambda satellite_id, identifier, ground_station: CdsHktmProductionCompleteness.search()
                .query()
                .filter("term", satellite_unit=satellite_id.upper())
                .filter("term", downlink_absolute_orbit=identifier)
                .filter(
                    "prefix", station="EDRS"
                ),  # Mp are created with station like EDRS-A not the receptor like HDGS
            },
        ],
        "X-Band": [
            {
                "class": CdsAcquisitionPassStatus,
                "search": lambda satellite_id, identifier, ground_station: CdsAcquisitionPassStatus.search()
                .query()
                .filter("term", satellite_id=satellite_id.upper())
                .filter("term", downlink_orbit=identifier)
                .filter("term", ground_station=ground_station.upper()),
            },
            {
                "class": CdsCadipAcquisitionPassStatus,
                "search": lambda satellite_id, identifier, ground_station: CdsCadipAcquisitionPassStatus.search()
                .query()
                .filter("term", satellite_id=satellite_id.upper())
                .filter("term", downlink_orbit=identifier)
                .filter("term", station_id=f"{ground_station.upper()}_"),
            },
            {
                "class": CdsHktmAcquisitionCompleteness,
                "search": lambda satellite_id, identifier, ground_station: CdsHktmAcquisitionCompleteness.search()
                .query()
                .filter("term", satellite_unit=satellite_id.upper())
                .filter("term", session_id=identifier)
                .filter("term", ground_station=ground_station.upper()),
            },
            {
                "class": CdsHktmProductionCompleteness,
                "search": lambda satellite_id, identifier, ground_station: CdsHktmProductionCompleteness.search()
                .query()
                .filter("term", satellite_unit=satellite_id.upper())
                .filter("term", downlink_absolute_orbit=identifier)
                .filter("term", station=ground_station.upper()),
            },
        ],
    }

    # pylint: enable=C0301

    PRODUCT_IMPACTED = (CdsProduct, CdsPublication)

    def action_iterator(self) -> Iterator[Dict[str, Any]]:

        self.logger.debug("START ACTION ITERATR")
        # Retrieve all ticket impact by the AN
        ticket_with_an_payloads = {}
        for report in self.input_documents:
            ticket_id = report.ticket_id
            if ticket_id not in ticket_with_an_payloads:
                ticket_with_an_payloads[ticket_id] = []
            ticket_with_an_payloads[ticket_id].append(report)

        # Next get the tickets to avoid duplicated impact and centralize information
        self.logger.debug(
            "Load %s tickets",
            len(ticket_with_an_payloads.keys()),
        )

        tickets = CdsCamsTickets.mget_by_ids(list(ticket_with_an_payloads.keys()))

        for ticket, ticket_id in zip(tickets, ticket_with_an_payloads.keys()):

            if ticket is None:
                self.logger.warning(
                    "[%s] - Can't find ticket for the following %s",
                    ticket_id,
                    ticket_with_an_payloads[ticket_id],
                )
                continue

            self.logger.info(
                "Consolidating file %s for updated anomalies %s",
                ticket_id,
                ticket_with_an_payloads[ticket_id],
            )

            for an_payload in ticket_with_an_payloads[ticket_id]:
                # Field to aggregate
                fields_to_merge = [
                    "products",
                    "publications",
                    "datatake_ids",
                    "acquisition_pass",
                ]

                for field in fields_to_merge:

                    # Merge and avoid duplicates
                    setattr(
                        ticket,
                        field,
                        list(
                            set(
                                list(getattr(ticket, field, []) or [])
                                + list(getattr(an_payload, field, []) or [])
                            )
                        ),
                    )

                # Correlate ticket from report (keep origin and description of the latest ingested)
                ticket.origin = an_payload.origin
                ticket.description = an_payload.description

            yield from self.correlate_ticket(ticket)

            yield ticket.to_bulk_action()

    def correlate_ticket(self, ticket: CdsCamsTickets) -> Iterator[Dict[str, Any]]:
        """Correlate all entities described in the ticket

        Args:
            ticket (CdsCamsTickets): ticket to correlate

        Yields:
            Iterator[Dict[str, Any]]: bulk action
        """
        # get already linked documents
        linked_documents = self.get_linked_documents(ticket.key)

        for correlate_method, identifiers in [
            (self.correlate_datatakes, ticket.datatake_ids),
            (self.correlate_acquisitions, ticket.acquisition_pass),
            (self.correlate_products, ticket.products),
        ]:
            self.logger.debug(
                "Calling %s with args: ids=%s, linked_documents=%s",
                correlate_method.__name__,
                identifiers,
                linked_documents,
            )

            yield from correlate_method(ticket, linked_documents)

    def get_linked_documents(self, ticket_id: str | Keyword) -> dict:
        """Search all impacted entities that are linked to a ticket

        Args:
            ticket_id (str): ticket identifier

        Returns:
            dict: a dictionnary where keys are class names and values are documents
        """

        document_dict = {}

        for document_class in self.IMPACTED_CLASSES:
            self.logger.debug("%s: searching for linked %s", ticket_id, document_class)

            try:
                documents = (
                    document_class.search()
                    .query("term", cams_tickets=ticket_id)
                    .params(version=True, seq_no_primary_term=True, size=10000)
                    .execute()
                )

                if documents:
                    self.logger.debug("%s: found %s", ticket_id, documents)

                    document_dict[document_class.__name__] = documents

                else:
                    self.logger.debug(
                        "%s: no %s were found (%s)",
                        ticket_id,
                        document_class,
                        documents,
                    )

            except NotFoundError as error:
                self.logger.debug("%s: %s", error.__class__.__name__, error)

        self.logger.debug("Found linked documents for %s: %s", ticket_id, document_dict)

        return document_dict

    def apply_correlation(
        self,
        ticket: CdsCamsTickets,
        class_obj,
        linked_documents: list[MAASDocument],
        target_ids_or_documents: list,
    ) -> Iterator[Dict[str, Any]]:
        """
        Correlate ticket to document from a given class

        Args:
            ticket.key (str): ticket identifier
            class_obj (_type_): the impacted document class object
            linked_documents (list[MAASDocument]): list of documents ob
            target_ids_or_documents (list): a list of documents or
                indentifiers to impact

        Yields:
            Dict[str, Any]: bulk actions
        """

        self.logger.debug(
            "apply correlation for ticket %s to %s. linked: %s target: %s",
            ticket.key,
            class_obj.__name__,
            linked_documents,
            target_ids_or_documents,
        )

        if not (linked_documents or target_ids_or_documents):
            self.logger.warning(
                "No modification to apply to %s for %s", class_obj.__name__, ticket.key
            )
            return

        existing_ids = {document.meta.id for document in linked_documents}

        has_documents_arg = False

        if target_ids_or_documents:
            if isinstance(target_ids_or_documents[0], MAASDocument):
                # a list of instances have been provided
                target_ids = {document.meta.id for document in target_ids_or_documents}
                has_documents_arg = True
            elif isinstance(target_ids_or_documents[0], str):
                target_ids = set(target_ids_or_documents)
            else:
                raise TypeError(
                    f"Cannot use "
                    f"{target_ids_or_documents[0].__class__.__name__}"
                    " as target_ids_or_documents argument"
                )
        else:
            target_ids = set()

        # systematic update
        to_link_ids = target_ids

        to_unlink_ids = existing_ids - target_ids

        self.logger.debug("to link: %s ; to unlink: %s", to_link_ids, to_unlink_ids)

        if has_documents_arg:
            target_documents = [
                document
                for document in target_ids_or_documents
                if document.meta.id in to_link_ids
            ]
        elif to_link_ids:
            to_link_ids_list = list(to_link_ids)

            target_documents = list(
                class_obj.mget_by_ids(to_link_ids_list, ignore_missing_index=True)
            )

            if not all(target_documents):
                self.logger.warning(
                    "Some %s are missing in %s", class_obj.__name__, to_link_ids
                )
                # recover to known documents
                target_documents = [
                    document for document in target_documents if document
                ]
                self.logger.debug("target restricted to %s", target_documents)
        else:
            target_documents = []

        for to_link_document in target_documents:
            if not ticket.key in to_link_document.cams_tickets:
                self.logger.debug("Linking %s to %s", ticket.key, to_link_document)
                to_link_document.cams_tickets.append(ticket.key)
            else:
                self.logger.debug(
                    "%s Already linked to %s", ticket.key, to_link_document
                )

            to_link_document.set_last_attached_ticket(ticket)

            yield to_link_document.to_bulk_action()

        for to_unlink_document in [
            document
            for document in linked_documents
            if document.meta.id in to_unlink_ids
        ]:
            self.logger.debug("Unlinking %s from %s", ticket.key, to_unlink_document)

            to_unlink_document.cams_tickets.remove(ticket.key)

            to_unlink_document.unset_last_attached_ticket()

            yield to_unlink_document.to_bulk_action()

    def correlate_datatakes(
        self, ticket: CdsCamsTickets, linked_documents: list[MAASDocument]
    ) -> Iterator[Dict[str, Any]]:
        """
        Handle correlation for datatakes from any mission

        Args:
            report (CamsAnomalyCorrelation): raw data
            linked_documents (dict): current impact of the anomaly

        Yields:
            Iterator[typing.Generator]: bulk actions
        """

        mission_datatake_dict = defaultdict(list)

        if ticket.datatake_ids:
            # group by mission for robustness
            for datatake_id in ticket.datatake_ids:
                mission = datatake_id[:2]
                mission_datatake_dict[mission].append(datatake_id)

        self.logger.debug("mission_datatake_dict: %s", mission_datatake_dict)

        for (
            mission,
            (class_obj, retrieve_method_type),
        ) in self.DATATAKE_ENTITY_DICT.items():
            existing_documents = []

            if class_obj.__name__ in linked_documents:
                mission_linked_list = linked_documents[class_obj.__name__]

                # filter by mission because of S1 / S2 datatakes are in the same index
                existing_documents.extend(
                    [
                        document
                        for document in mission_linked_list
                        if document.meta.id.startswith(mission)
                    ]
                )
                if existing_documents:
                    self.logger.debug("Found linked: %s", existing_documents)

            target_ids = mission_datatake_dict.get(mission, [])

            if not (existing_documents or target_ids):
                self.logger.debug("nothing to do for mission %s", mission)
                # nothing to do for this mission
                continue

            if retrieve_method_type == "ids":
                correlate_arg = target_ids

            elif retrieve_method_type == "search":
                search = class_obj.search().filter("terms", datatake_id=target_ids)

                results = search.params(
                    version=True,
                    seq_no_primary_term=True,
                    size=10000,
                ).execute()

                correlate_arg = list(results)

            else:
                raise ValueError(
                    f"Invalid retrieve_method_type:  {retrieve_method_type}"
                )

            yield from self.apply_correlation(
                ticket,
                class_obj,
                existing_documents,
                correlate_arg,
            )

    def correlate_acquisitions(
        self, ticket: CdsCamsTickets, linked_documents: dict
    ) -> Iterator[Dict[str, Any]]:
        """
        Handle correlation for x-band, edrs acquisition pass status.

        Args:
            report (CamsAnomalyCorrelation): raw data
            linked_documents (dict): current impact of the anomaly

        Yields:
            Iterator[typing.Generator]: bulk actions
        """

        target_documents = {"EDRS": {}, "X-Band": {}}

        if ticket.acquisition_pass:
            for pass_key in ticket.acquisition_pass:
                satellite_id, station_type, identifier, ground_station = pass_key.split(
                    "_"
                )

                if not station_type in self.ACQUISITION_QUERY_DICT:
                    self.logger.warning("Unknown station type: %s", station_type)
                    continue

                if not isinstance(identifier, str):
                    if isinstance(identifier, float):
                        identifier = f"{int(identifier)}"
                    elif identifier:
                        identifier = str(identifier)
                    else:
                        self.logger.warning(
                            "No identifier found in %s",
                            (satellite_id, station_type, identifier, ground_station),
                        )
                        continue

                for interface in self.ACQUISITION_QUERY_DICT[station_type]:
                    search = interface["search"](
                        satellite_id,
                        identifier,
                        ground_station,
                    )

                    results = search.params(
                        version=True,
                        seq_no_primary_term=True,
                        size=10000,
                    ).execute()

                    if not results:
                        self.logger.warning(
                            "No results for Acquisition: %s %s %s %s",
                            satellite_id,
                            station_type,
                            identifier,
                            ground_station,
                        )
                        continue

                    classname = interface["class"].__name__

                    if classname not in target_documents[station_type]:
                        target_documents[station_type][classname] = []

                    target_documents[station_type][classname].extend(results)

        for station_type, station_type_documents in target_documents.items():
            for interface in self.ACQUISITION_QUERY_DICT[station_type]:
                class_obj = interface["class"]

                linked_acquisitions = linked_documents.get(class_obj.__name__, [])

                target_documents = station_type_documents.get(class_obj.__name__, [])

                yield from self.apply_correlation(
                    ticket,
                    class_obj,
                    linked_acquisitions,
                    target_documents,
                )

    def correlate_products(
        self, ticket: CdsCamsTickets, linked_documents: dict
    ) -> Iterator[Dict[str, Any]]:
        """
        Handle correlation for products and publication.

        Args:
            report (CamsAnomalyCorrelation): raw data
            linked_documents (dict): current impact of the anomaly

        Yields:
            Iterator[typing.Generator]: bulk actions
        """

        for class_obj in self.PRODUCT_IMPACTED:
            self.logger.debug(
                "Correlate %s:  %s - %s",
                class_obj.__name__,
                ticket.products,
                ticket.publications,
            )

            # Search through all publication name combinations
            if ticket.publications:
                results = (
                    class_obj.search()
                    .query()
                    .filter("terms", name=ticket.publications)
                    .params(
                        version=True,
                        seq_no_primary_term=True,
                        size=10000,
                    )
                    .execute()
                )
            else:
                results = []

            linked_products = linked_documents.get(class_obj.__name__, [])

            yield from self.apply_correlation(
                ticket,
                class_obj,
                linked_products,
                results,
            )
