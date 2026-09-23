from enum import StrEnum

from pydantic import BaseModel, Field


class DetectionType(StrEnum):
    NORMAL = "NORMAL"
    PORT_SCAN = "PORT_SCAN"
    HIGH_RATE = "HIGH_RATE"


class DetectionResult(BaseModel):
    detection_type: DetectionType
    confidence: float = Field(ge=0.0, le=1.0)
    anomaly_score: float = Field(ge=0.0, le=1.0)
    reason: str