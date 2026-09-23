from datetime import datetime, timezone

from app.detection.aggregator import FlowAggregator
from app.detection.models import DetectionType
from app.models.network import NetworkFlow


def make_flow(port: int, source_ip: str = "192.168.1.99") -> NetworkFlow:
    return NetworkFlow(
        timestamp=datetime.now(timezone.utc),
        source_ip=source_ip,
        destination_ip="192.168.1.20",
        source_port=50000,
        destination_port=port,
        protocol="TCP",
        packets=1,
        bytes=60,
        duration=0.01,
    )


def test_multiple_ports_create_port_scan_detection() -> None:
    flows = [make_flow(port) for port in range(1, 11)]

    results = FlowAggregator().detect_port_scan(flows)

    assert len(results) == 1
    assert results[0].detection_type is DetectionType.PORT_SCAN
    assert "10 distinct destination ports" in results[0].reason


def test_few_ports_do_not_trigger_scan() -> None:
    flows = [make_flow(port) for port in range(1, 4)]

    results = FlowAggregator().detect_port_scan(flows)

    assert results == []


def test_sources_are_evaluated_independently() -> None:
    flows = [
        *(make_flow(port, "192.168.1.99") for port in range(1, 6)),
        *(make_flow(port, "192.168.1.50") for port in range(1, 4)),
    ]

    results = FlowAggregator().detect_port_scan(flows)

    assert len(results) == 1
    assert "192.168.1.99" in results[0].reason