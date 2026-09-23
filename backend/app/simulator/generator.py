from datetime import datetime, timezone
from random import Random

from app.models.network import NetworkFlow


class TrafficGenerator:
    def __init__(self, seed: int | None = None) -> None:
        self._random = Random(seed)

    def normal_flow(self) -> NetworkFlow:
        return NetworkFlow(
            timestamp=datetime.now(timezone.utc),
            source_ip="192.168.1.10",
            destination_ip="192.168.1.20",
            source_port=self._random.randint(49152, 65535),
            destination_port=self._random.choice([80, 443]),
            protocol="TCP",
            packets=self._random.randint(5, 50),
            bytes=self._random.randint(500, 10_000),
            duration=round(self._random.uniform(0.1, 3.0), 3),
        )

    def port_scan(self, count: int = 20) -> list[NetworkFlow]:
        source_port = self._random.randint(49152, 65535)

        ports = self._random.sample(
            range(1, 65536),
            count,
        )

        return [
            NetworkFlow(
                timestamp=datetime.now(timezone.utc),
                source_ip="192.168.1.99",
                destination_ip="192.168.1.20",
                source_port=source_port,
                destination_port=port,
                protocol="TCP",
                packets=1,
                bytes=60,
                duration=0.01,
            )
            for port in ports
        ]