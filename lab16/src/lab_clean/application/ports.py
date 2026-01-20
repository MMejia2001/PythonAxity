from __future__ import annotations

from typing import Protocol

from lab_clean.domain.entities import Order


class OrderRepo(Protocol):
    def add(self, order: Order) -> None: ...
    def get(self, order_id: int) -> Order | None: ...


class EventPublisher(Protocol):
    def publish(self, event: object) -> None: ...
