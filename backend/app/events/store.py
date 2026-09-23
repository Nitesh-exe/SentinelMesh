from app.models.network import NetworkFlow


class EventStore:
    def __init__(self) -> None:
        self._events: list[NetworkFlow] = []

    def add(self, event: NetworkFlow) -> NetworkFlow:
        self._events.append(event)
        return event

    def list(self) -> list[NetworkFlow]:
        return self._events.copy()

    def clear(self) -> None:
        self._events.clear()

    def count(self) -> int:
        return len(self._events)