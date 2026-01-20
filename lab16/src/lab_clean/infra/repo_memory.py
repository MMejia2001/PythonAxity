from __future__ import annotations

from lab_clean.domain.entities import Order


class InMemoryOrderRepo:
    def __init__(self) -> None:
        self._data: dict[int, Order] = {}

    def add(self, order: Order) -> None:
        self._data[order.order_id] = order

    def get(self, order_id: int) -> Order | None:
        return self._data.get(order_id)
