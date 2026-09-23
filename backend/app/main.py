from uuid import UUID

from fastapi import FastAPI, HTTPException

from app.detection.rules import RuleDetector
from app.events.service import EventService
from app.events.store import EventStore
from app.incidents.models import Incident
from app.incidents.store import IncidentStore
from app.models.network import NetworkFlow
from app.pipeline.processor import EventProcessor
from app.simulator.generator import TrafficGenerator

app = FastAPI(
    title="SentinelMesh API",
    version="0.1.0",
)

generator = TrafficGenerator()

event_service = EventService(EventStore())
incident_store = IncidentStore()
processor = EventProcessor(
    detector=RuleDetector(),
    incidents=incident_store,
)


@app.get("/api/v1/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/v1/flows", response_model=NetworkFlow, status_code=201)
def ingest_flow(flow: NetworkFlow) -> NetworkFlow:
    event_service.ingest(flow)
    processor.process(flow)
    return flow


@app.get("/api/v1/flows", response_model=list[NetworkFlow])
def list_flows() -> list[NetworkFlow]:
    return event_service.list_events()


@app.get("/api/v1/incidents", response_model=list[Incident])
def list_incidents() -> list[Incident]:
    return incident_store.list()


@app.get("/api/v1/incidents/{incident_id}", response_model=Incident)
def get_incident(incident_id: UUID) -> Incident:
    incident = incident_store.get(incident_id)

    if incident is None:
        raise HTTPException(status_code=404, detail="Incident not found")

    return incident


@app.post("/api/v1/simulations/normal", response_model=NetworkFlow)
def simulate_normal() -> NetworkFlow:
    flow = generator.normal_flow()
    event_service.ingest(flow)
    processor.process(flow)
    return flow


@app.post("/api/v1/simulations/port-scan", response_model=list[NetworkFlow])
def simulate_port_scan(count: int = 20) -> list[NetworkFlow]:
    flows = generator.port_scan(count)

    for flow in flows:
        event_service.ingest(flow)
        processor.process(flow)

    return flows