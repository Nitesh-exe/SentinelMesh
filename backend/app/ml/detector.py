from pathlib import Path

from app.detection.models import DetectionResult, DetectionType
from app.ml.features import flow_to_vector
from app.ml.model import IntrusionModel
from app.models.network import NetworkFlow


class MLDetector:
    def __init__(self, model_path: Path) -> None:
        self._model = IntrusionModel()
        self._model.load(model_path)

    def detect(self, flow: NetworkFlow) -> DetectionResult:
        prediction, confidence = self._model.predict(
            [flow_to_vector(flow)]
        )

        detection_type = DetectionType.NORMAL

        if prediction == "PORT_SCAN":
            detection_type = DetectionType.PORT_SCAN
        elif prediction == "HIGH_RATE":
            detection_type = DetectionType.HIGH_RATE

        return DetectionResult(
            detection_type=detection_type,
            confidence=confidence,
            anomaly_score=(
                1.0 - confidence
                if detection_type is DetectionType.NORMAL
                else confidence
            ),
            reason=f"ML classifier predicted {prediction}",
        )