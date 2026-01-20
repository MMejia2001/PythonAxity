from __future__ import annotations

from typing import Protocol

from .domain import Order


class OrderRepo(Protocol):
    def add(self, order: Order) -> None: ...
    def get(self, order_id: int) -> Order | None: ...
