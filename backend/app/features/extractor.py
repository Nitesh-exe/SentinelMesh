from dataclasses import dataclass

from app.models.network import NetworkFlow


@dataclass(frozen=True)
class FlowFeatures:
    packets: int
    bytes: int
    duration: float
    packets_per_second: float
    bytes_per_second: float
    bytes_per_packet: float
    destination_port: int


class FeatureExtractor:
    @staticmethod
    def extract(flow: NetworkFlow) -> FlowFeatures:
        duration = max(flow.duration, 1e-9)

        return FlowFeatures(
            packets=flow.packets,
            bytes=flow.bytes,
            duration=flow.duration,
            packets_per_second=flow.packets / duration,
            bytes_per_second=flow.bytes / duration,
            bytes_per_packet=flow.bytes / max(flow.packets, 1),
            destination_port=flow.destination_port,
        )