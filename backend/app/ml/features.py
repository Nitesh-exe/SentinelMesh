from app.features.extractor import FeatureExtractor
from app.models.network import NetworkFlow


FEATURE_NAMES = (
    "packets",
    "bytes",
    "duration",
    "packets_per_second",
    "bytes_per_second",
    "bytes_per_packet",
    "destination_port",
)


def flow_to_vector(flow: NetworkFlow) -> list[float]:
    features = FeatureExtractor.extract(flow)

    return [
        float(features.packets),
        float(features.bytes),
        features.duration,
        features.packets_per_second,
        features.bytes_per_second,
        features.bytes_per_packet,
        float(features.destination_port),
    ]