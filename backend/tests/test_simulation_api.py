from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_normal_simulation() -> None:
    response = client.post("/api/v1/simulations/normal")

    assert response.status_code == 200

    flow = response.json()

    assert flow["source_ip"] == "192.168.1.10"
    assert flow["destination_ip"] == "192.168.1.20"


def test_port_scan_simulation() -> None:
    response = client.post("/api/v1/simulations/port-scan?count=10")

    assert response.status_code == 200

    flows = response.json()

    assert len(flows) == 10
    ports = [flow["destination_port"] for flow in flows]
    assert len(ports) == len(set(ports))
    assert all(1 <= port <= 65535 for port in ports)