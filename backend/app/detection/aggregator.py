from collections import defaultdict

from app.detection.models import DetectionResult, DetectionType
from app.models.network import NetworkFlow


class FlowAggregator:
    def detect_port_scan(
        self,
        flows: list[NetworkFlow],
        min_ports: int = 5,
    ) -> list[DetectionResult]:
        ports_by_source: dict[str, set[int]] = defaultdict(set)

        for flow in flows:
            ports_by_source[flow.source_ip].add(flow.destination_port)

        results: list[DetectionResult] = []

        for source_ip, ports in ports_by_source.items():
            if len(ports) < min_ports:
                continue

            results.append(
                DetectionResult(
                    detection_type=DetectionType.PORT_SCAN,
                    confidence=min(0.99, 0.70 + len(ports) / 100),
                    anomaly_score=min(0.99, 0.70 + len(ports) / 100),
                    reason=(
                        f"Source {source_ip} contacted "
                        f"{len(ports)} distinct destination ports"
                    ),
                )
            )

        return results