from datetime import datetime, timezone

from app.detection.engine import DetectionEngine
from app.detection.models import DetectionType
from app.incidents.models import Incident
from app.incidents.store import IncidentStore
from app.models.network import NetworkFlow


class EventProcessor:
    def __init__(
        self,
        detector: DetectionEngine,
        incidents: IncidentStore,
    ) -> None:
        self._detector = detector
        self._incidents = incidents

    def process(self, flow: NetworkFlow) -> Incident | None:
        detection = self._detector.detect(flow)

        if detection.detection_type is DetectionType.NORMAL:
            return None

        return self._incidents.add(
            Incident(
                created_at=datetime.now(timezone.utc),
                source_ip=flow.source_ip,
                detection=detection,
                flow=flow,
            )
        )