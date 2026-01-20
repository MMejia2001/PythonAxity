from __future__ import annotations

from typing import Protocol

from .entity import Order


class OrderRepository(Protocol):
    def save(self, order: Order) -> None: ...
    def get(self, order_id: int) -> Order | None: ...


class InMemoryOrderRepo:
    def __init__(self) -> None:
        self._data: dict[int, Order] = {}

    def save(self, order: Order) -> None:
        self._data[order.order_id] = order

    def get(self, order_id: int) -> Order | None:
        return self._data.get(order_id)
