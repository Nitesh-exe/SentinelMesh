from pathlib import Path

from app.ml.features import flow_to_vector
from app.ml.model import IntrusionModel
from app.ml.trainer import generate_training_data
from app.models.network import NetworkFlow


def test_flow_vector_has_expected_dimensions() -> None:
    flow = NetworkFlow(
        timestamp="2026-01-01T00:00:00Z",
        source_ip="192.168.1.10",
        destination_ip="192.168.1.20",
        source_port=50000,
        destination_port=443,
        protocol="TCP",
        packets=20,
        bytes=2000,
        duration=2,
    )

    assert len(flow_to_vector(flow)) == 7


def test_training_data_contains_multiple_classes() -> None:
    x, y = generate_training_data(samples_per_class=10)

    assert len(x) == 30
    assert set(y) == {"NORMAL", "PORT_SCAN", "HIGH_RATE"}


def test_model_trains_and_predicts(tmp_path: Path) -> None:
    x, y = generate_training_data(samples_per_class=30)

    model = IntrusionModel()
    model.fit(x, y)

    path = tmp_path / "model.joblib"
    model.save(path)

    loaded = IntrusionModel()
    loaded.load(path)

    prediction, confidence = loaded.predict([x[0]])

    assert prediction in {"NORMAL", "PORT_SCAN", "HIGH_RATE"}
    assert 0 <= confidence <= 1