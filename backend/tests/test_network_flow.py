from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from app.models.network import NetworkFlow


def valid_flow() -> dict:
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "source_ip": "192.168.1.10",
        "destination_ip": "192.168.1.20",
        "source_port": 51000,
        "destination_port": 443,
        "protocol": "TCP",
        "packets": 25,
        "bytes": 4812,
        "duration": 1.42,
    }


def test_network_flow_accepts_valid_data() -> None:
    flow = NetworkFlow.model_validate(valid_flow())

    assert flow.source_ip == "192.168.1.10"
    assert flow.destination_port == 443


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("source_port", -1),
        ("destination_port", 65536),
        ("packets", -1),
        ("bytes", -1),
        ("duration", -0.1),
    ],
)
def test_network_flow_rejects_invalid_ranges(
    field: str, value: object
) -> None:
    data = valid_flow()
    data[field] = value

    with pytest.raises(ValidationError):
        NetworkFlow.model_validate(data)


def test_network_flow_rejects_unknown_fields() -> None:
    data = valid_flow()
    data["unexpected"] = "nope"

    with pytest.raises(ValidationError):
        NetworkFlow.model_validate(data)