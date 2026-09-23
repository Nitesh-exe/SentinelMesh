from datetime import datetime, timezone

from app.detection.rules import RuleDetector
from app.incidents.store import IncidentStore
from app.models.network import NetworkFlow
from app.pipeline.processor import EventProcessor


def make_flow(
    packets: int,
    bytes: int,
    duration: float,
) -> NetworkFlow:
    return NetworkFlow(
        timestamp=datetime.now(timezone.utc),
        source_ip="192.168.1.99",
        destination_ip="192.168.1.20",
        source_port=50000,
        destination_port=22,
        protocol="TCP",
        packets=packets,
        bytes=bytes,
        duration=duration,
    )


def test_suspicious_flow_creates_incident() -> None:
    store = IncidentStore()
    processor = EventProcessor(RuleDetector(), store)

    incident = processor.process(
        make_flow(packets=1, bytes=60, duration=0.01)
    )

    assert incident is not None
    assert store.list() == [incident]


def test_normal_flow_does_not_create_incident() -> None:
    store = IncidentStore()
    processor = EventProcessor(RuleDetector(), store)

    incident = processor.process(
        make_flow(packets=10, bytes=1000, duration=1)
    )

    assert incident is None
    assert store.list() == []