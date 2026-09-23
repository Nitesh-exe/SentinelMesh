from app.detection.models import DetectionResult, DetectionType
from app.features.extractor import FeatureExtractor
from app.models.network import NetworkFlow


class RuleDetector:
    def detect(self, flow: NetworkFlow) -> DetectionResult:
        features = FeatureExtractor.extract(flow)

        if features.packets == 1 and features.bytes <= 100:
            return DetectionResult(
                detection_type=DetectionType.PORT_SCAN,
                confidence=0.85,
                anomaly_score=0.85,
                reason="Single low-payload connection consistent with scanning activity",
            )

        if features.packets_per_second >= 100:
            return DetectionResult(
                detection_type=DetectionType.HIGH_RATE,
                confidence=0.95,
                anomaly_score=0.95,
                reason=(
                    f"High packet rate: "
                    f"{features.packets_per_second:.2f} packets/sec"
                ),
            )

        return DetectionResult(
            detection_type=DetectionType.NORMAL,
            confidence=0.90,
            anomaly_score=0.05,
            reason="No known suspicious flow pattern detected",
        )