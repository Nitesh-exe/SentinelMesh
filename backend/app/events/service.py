from app.events.store import EventStore
from app.models.network import NetworkFlow


class EventService:
    def __init__(self, store: EventStore) -> None:
        self._store = store

    def ingest(self, event: NetworkFlow) -> NetworkFlow:
        return self._store.add(event)

    def list_events(self) -> list[NetworkFlow]:
        return self._store.list()

    def count(self) -> int:
        return self._store.count()