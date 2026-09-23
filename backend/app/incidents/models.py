from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from app.detection.models import DetectionResult
from app.models.network import NetworkFlow


class Incident(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    created_at: datetime
    source_ip: str
    detection: DetectionResult
    flow: NetworkFlow