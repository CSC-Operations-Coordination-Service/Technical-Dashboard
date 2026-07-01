"""Tests for the propagation of a datatake CAMS ticket down to its products.

When a CAMS ticket attachment changes on an S1 datatake, the engine mirrors the
datatake ``last_attached_ticket`` into the ``datatake_cams_ticket`` field of every
product and publication belonging to that datatake.
"""

from unittest.mock import patch

from maas_cds.engines.compute.anomaly_correlation_ticket import (
    CorrelateAnomalyTicketEngine,
)
from maas_cds.model import (
    CdsProduct,
    CdsPublication,
    CdsDatatakeS1,
    CdsDatatakeS2,
)


class FakeResults(list):
    """Minimal stand-in for an opensearch-dsl Response (iterable + hits.total)."""

    class _Hits:
        class _Total:
            def __init__(self, value):
                self.value = value

        def __init__(self, value):
            self.total = self._Total(value)

    def __init__(self, documents, total=None):
        super().__init__(documents)
        self.hits = self._Hits(total if total is not None else len(documents))


def _make_search_mock(results):
    """Build a chained search mock returning ``results`` on execute()."""

    def search(*_args, **_kwargs):
        from unittest.mock import MagicMock

        mock = MagicMock()
        mock.filter.return_value = mock
        mock.params.return_value = mock
        mock.execute.return_value = results
        return mock

    return search


def _datatake(datatake_id="123456-1", satellite_unit="S1A", ticket="GSANOM-1"):
    datatake = CdsDatatakeS1()
    datatake.datatake_id = datatake_id
    datatake.satellite_unit = satellite_unit
    datatake.last_attached_ticket = ticket
    return datatake


def _product(cls=CdsProduct, name="P1", current=None):
    product = cls()
    product.meta.id = name
    product.datatake_id = "123456-1"
    product.satellite_unit = "S1A"
    # partition field so to_bulk_action() can resolve the target index
    if cls is CdsPublication:
        product.publication_date = "2024-01-01T00:00:00.000Z"
    else:
        product.prip_publication_date = "2024-01-01T00:00:00.000Z"
    if current is not None:
        product.datatake_cams_ticket = current
    return product


def test_propagate_sets_ticket_on_products_and_publications():
    engine = CorrelateAnomalyTicketEngine()

    product = _product(CdsProduct, "prod-1")
    publication = _product(CdsPublication, "pub-1")

    with patch.object(
        CdsProduct, "search", _make_search_mock(FakeResults([product]))
    ), patch.object(
        CdsPublication, "search", _make_search_mock(FakeResults([publication]))
    ):
        actions = list(engine.propagate_ticket_to_products([_datatake(ticket="AN-42")]))

    assert product.datatake_cams_ticket == "AN-42"
    assert publication.datatake_cams_ticket == "AN-42"
    # one bulk action per impacted document
    assert len(actions) == 2


def test_propagate_skips_documents_already_up_to_date():
    engine = CorrelateAnomalyTicketEngine()

    up_to_date = _product(CdsProduct, "prod-ok", current="AN-42")

    with patch.object(
        CdsProduct, "search", _make_search_mock(FakeResults([up_to_date]))
    ), patch.object(CdsPublication, "search", _make_search_mock(FakeResults([]))):
        actions = list(engine.propagate_ticket_to_products([_datatake(ticket="AN-42")]))

    # nothing to write: value already matches
    assert actions == []


def test_propagate_clears_ticket_when_datatake_has_none():
    engine = CorrelateAnomalyTicketEngine()

    product = _product(CdsProduct, "prod-1", current="AN-42")

    with patch.object(
        CdsProduct, "search", _make_search_mock(FakeResults([product]))
    ), patch.object(CdsPublication, "search", _make_search_mock(FakeResults([]))):
        actions = list(engine.propagate_ticket_to_products([_datatake(ticket=None)]))

    assert product.datatake_cams_ticket is None
    assert len(actions) == 1


def test_only_s1_is_collected_for_propagation():
    # S1 is the only mission enabled for now
    assert CorrelateAnomalyTicketEngine.DATATAKE_TICKET_PROPAGATION_MISSIONS == ("S1",)
