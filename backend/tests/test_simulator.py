from app.simulator.generator import TrafficGenerator


def test_normal_flow_is_valid() -> None:
    flow = TrafficGenerator(seed=42).normal_flow()

    assert flow.source_ip == "192.168.1.10"
    assert flow.destination_ip == "192.168.1.20"
    assert flow.protocol == "TCP"
    assert 0 <= flow.destination_port <= 65535


def test_port_scan_generates_distinct_destination_ports() -> None:
    flows = TrafficGenerator(seed=42).port_scan(20)

    assert len(flows) == 20
    ports = [flow.destination_port for flow in flows]
    assert len(ports) == len(set(ports))
    assert all(1 <= port <= 65535 for port in ports)
    assert all(flow.source_ip == "192.168.1.99" for flow in flows)