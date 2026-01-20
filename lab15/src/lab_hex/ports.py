from __future__ import annotations

from typing import Protocol

from .domain import Order


class OrderRepository(Protocol):
    def add(self, order: Order) -> None: ...
    def get(self, order_id: int) -> Order | None: ...


class Notifier(Protocol):
    def notify_order_created(self, order: Order) -> None: ...
