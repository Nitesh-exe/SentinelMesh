from pathlib import Path

from app.detection.models import DetectionResult, DetectionType
from app.detection.rules import RuleDetector
from app.ml.detector import MLDetector
from app.models.network import NetworkFlow


class DetectionEngine:
    def __init__(self, model_path: Path) -> None:
        self._rules = RuleDetector()
        self._ml = MLDetector(model_path)

    def detect(self, flow: NetworkFlow) -> DetectionResult:
        rule_result = self._rules.detect(flow)

        # Deterministic security rules take precedence over ML.
        if rule_result.detection_type is not DetectionType.NORMAL:
            return rule_result

        return self._ml.detect(flow)