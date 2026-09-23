from uuid import UUID

from app.incidents.models import Incident


class IncidentStore:
    def __init__(self) -> None:
        self._incidents: list[Incident] = []

    def add(self, incident: Incident) -> Incident:
        self._incidents.append(incident)
        return incident

    def list(self) -> list[Incident]:
        return self._incidents.copy()

    def get(self, incident_id: UUID) -> Incident | None:
        return next(
            (incident for incident in self._incidents if incident.id == incident_id),
            None,
        )