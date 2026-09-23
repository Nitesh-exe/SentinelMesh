from datetime import datetime, timezone

from app.events.service import EventService
from app.events.store import EventStore
from app.models.network import NetworkFlow


def make_flow() -> NetworkFlow:
    return NetworkFlow(
        timestamp=datetime.now(timezone.utc),
        source_ip="192.168.1.10",
        destination_ip="192.168.1.20",
        source_port=50000,
        destination_port=443,
        protocol="TCP",
        packets=10,
        bytes=1000,
        duration=1.0,
    )


def test_ingest_stores_event() -> None:
    service = EventService(EventStore())
    flow = make_flow()

    service.ingest(flow)

    assert service.count() == 1
    assert service.list_events() == [flow]


def test_list_returns_copy() -> None:
    service = EventService(EventStore())
    service.ingest(make_flow())

    events = service.list_events()
    events.clear()

    assert service.count() == 1