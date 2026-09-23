from random import Random

from app.ml.features import flow_to_vector
from app.ml.model import IntrusionModel
from app.models.network import NetworkFlow
from pathlib import Path

def generate_training_data(
    samples_per_class: int = 200,
    seed: int = 42,
) -> tuple[list[list[float]], list[str]]:
    random = Random(seed)

    x: list[list[float]] = []
    y: list[str] = []

    for _ in range(samples_per_class):
        packets = random.randint(5, 50)
        bytes_count = random.randint(500, 10_000)
        duration = random.uniform(0.5, 5.0)

        flow = NetworkFlow(
            timestamp="2026-01-01T00:00:00Z",
            source_ip="192.168.1.10",
            destination_ip="192.168.1.20",
            source_port=random.randint(49152, 65535),
            destination_port=random.choice([80, 443]),
            protocol="TCP",
            packets=packets,
            bytes=bytes_count,
            duration=duration,
        )

        x.append(flow_to_vector(flow))
        y.append("NORMAL")

    for _ in range(samples_per_class):
        packets = random.randint(1, 3)
        bytes_count = random.randint(40, 100)
        duration = random.uniform(0.001, 0.05)

        flow = NetworkFlow(
            timestamp="2026-01-01T00:00:00Z",
            source_ip="192.168.1.99",
            destination_ip="192.168.1.20",
            source_port=random.randint(49152, 65535),
            destination_port=random.randint(1, 65535),
            protocol="TCP",
            packets=packets,
            bytes=bytes_count,
            duration=duration,
        )

        x.append(flow_to_vector(flow))
        y.append("PORT_SCAN")

    for _ in range(samples_per_class):
        packets = random.randint(500, 5000)
        bytes_count = random.randint(50_000, 500_000)
        duration = random.uniform(0.1, 2.0)

        flow = NetworkFlow(
            timestamp="2026-01-01T00:00:00Z",
            source_ip="192.168.1.99",
            destination_ip="192.168.1.20",
            source_port=random.randint(49152, 65535),
            destination_port=random.choice([80, 443]),
            protocol="TCP",
            packets=packets,
            bytes=bytes_count,
            duration=duration,
        )

        x.append(flow_to_vector(flow))
        y.append("HIGH_RATE")

    return x, y


def train_model(path: str | Path = "models/intrusion.joblib") -> None:
    path = Path(path)

    x, y = generate_training_data()

    model = IntrusionModel()
    model.fit(x, y)
    model.save(path)