from datetime import datetime, timezone

from app.detection.models import DetectionType
from app.detection.rules import RuleDetector
from app.models.network import NetworkFlow


def make_flow(
    packets: int = 10,
    bytes: int = 1000,
    duration: float = 1.0,
) -> NetworkFlow:
    return NetworkFlow(
        timestamp=datetime.now(timezone.utc),
        source_ip="192.168.1.99",
        destination_ip="192.168.1.20",
        source_port=50000,
        destination_port=443,
        protocol="TCP",
        packets=packets,
        bytes=bytes,
        duration=duration,
    )


def test_normal_flow() -> None:
    result = RuleDetector().detect(make_flow())

    assert result.detection_type is DetectionType.NORMAL


def test_high_rate_flow() -> None:
    result = RuleDetector().detect(
        make_flow(packets=1000, bytes=100_000, duration=1)
    )

    assert result.detection_type is DetectionType.HIGH_RATE
    assert result.confidence > 0.9


def test_scan_like_flow() -> None:
    result = RuleDetector().detect(
        make_flow(packets=1, bytes=60, duration=0.01)
    )

    assert result.detection_type is DetectionType.PORT_SCAN