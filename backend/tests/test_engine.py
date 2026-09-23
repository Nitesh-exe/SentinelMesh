from pathlib import Path

from app.detection.engine import DetectionEngine
from app.detection.models import DetectionType
from app.ml.trainer import train_model
from app.models.network import NetworkFlow


def make_flow(
    packets: int,
    bytes: int,
    duration: float,
) -> NetworkFlow:
    return NetworkFlow(
        timestamp="2026-01-01T00:00:00Z",
        source_ip="192.168.1.99",
        destination_ip="192.168.1.20",
        source_port=50000,
        destination_port=443,
        protocol="TCP",
        packets=packets,
        bytes=bytes,
        duration=duration,
    )


def test_engine_uses_rule_detection_first(tmp_path: Path) -> None:
    model_path = tmp_path / "model.joblib"
    train_model(model_path)

    engine = DetectionEngine(model_path)

    result = engine.detect(
        make_flow(
            packets=1,
            bytes=60,
            duration=0.01,
        )
    )

    assert result.detection_type is DetectionType.PORT_SCAN


def test_engine_uses_ml_for_unmatched_flow(tmp_path: Path) -> None:
    model_path = tmp_path / "model.joblib"
    train_model(model_path)

    engine = DetectionEngine(model_path)

    result = engine.detect(
        make_flow(
            packets=20,
            bytes=2000,
            duration=2,
        )
    )

    assert result.detection_type is DetectionType.NORMAL
    assert 0 <= result.confidence <= 1