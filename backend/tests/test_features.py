from datetime import datetime, timezone

from app.features.extractor import FeatureExtractor
from app.models.network import NetworkFlow
import pytest

def test_extracts_flow_features() -> None:
    flow = NetworkFlow(
        timestamp=datetime.now(timezone.utc),
        source_ip="192.168.1.10",
        destination_ip="192.168.1.20",
        source_port=50000,
        destination_port=443,
        protocol="TCP",
        packets=20,
        bytes=2000,
        duration=2.0,
    )

    features = FeatureExtractor.extract(flow)

    assert features.packets == 20
    assert features.bytes == 2000
    assert features.packets_per_second == 10.0
    assert features.bytes_per_second == 1000.0
    assert features.bytes_per_packet == 100.0
    assert features.destination_port == 443


def test_zero_duration_is_safe() -> None:
    flow = NetworkFlow(
        timestamp=datetime.now(timezone.utc),
        source_ip="192.168.1.10",
        destination_ip="192.168.1.20",
        source_port=50000,
        destination_port=22,
        protocol="TCP",
        packets=5,
        bytes=500,
        duration=0,
    )

    features = FeatureExtractor.extract(flow)

    assert features.packets_per_second == 5_000_000_000
    assert features.bytes_per_second == pytest.approx(500_000_000_000)