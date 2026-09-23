from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class NetworkFlow(BaseModel):
    model_config = ConfigDict(extra="forbid")

    timestamp: datetime
    source_ip: str
    destination_ip: str
    source_port: int = Field(ge=0, le=65535)
    destination_port: int = Field(ge=0, le=65535)
    protocol: str = Field(min_length=1, max_length=16)
    packets: int = Field(ge=0)
    bytes: int = Field(ge=0)
    duration: float = Field(ge=0)