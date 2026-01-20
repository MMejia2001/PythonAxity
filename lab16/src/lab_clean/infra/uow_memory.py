from __future__ import annotations

from lab_clean.application.ports import EventPublisher
from lab_clean.infra.repo_memory import InMemoryOrderRepo


class InMemoryEventPublisher(EventPublisher):
    def __init__(self) -> None:
        self.published: list[object] = []

    def publish(self, event: object) -> None:
        self.published.append(event)


class InMemoryUoW:
    def __init__(self) -> None:
        self.orders = InMemoryOrderRepo()
        self.events = InMemoryEventPublisher()

    def commit(self) -> None:
        # en memoria no hay transacción real, pero existe la idea
        return None

    def rollback(self) -> None:
        return None
