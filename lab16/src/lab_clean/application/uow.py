from __future__ import annotations

from typing import Protocol

from .ports import EventPublisher, OrderRepo


class UnitOfWork(Protocol):
    orders: OrderRepo
    events: EventPublisher

    def commit(self) -> None: ...
    def rollback(self) -> None: ...
