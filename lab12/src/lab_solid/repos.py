from __future__ import annotations

from typing import Dict

from .domain import Order


class InMemoryOrderRepo:
    def __init__(self) -> None:
        self._data: Dict[int, Order] = {}

    def add(self, order: Order) -> None:
        self._data[order.id] = order

    def get(self, order_id: int) -> Order | None:
        return self._data.get(order_id)


class FakeSqlOrderRepo:
    """
    Simula SQL.
    Igual cumple el mismo contrato: add/get.
    """

    def __init__(self) -> None:
        self._rows: Dict[int, dict] = {}

    def add(self, order: Order) -> None:
        # “Guardar” como si fuera fila en DB
        self._rows[order.id] = {
            "id": order.id,
            "customer": order.customer,
            "total": order.total,
        }

    def get(self, order_id: int) -> Order | None:
        row = self._rows.get(order_id)
        if not row:
            return None
        # Convertimos “fila” a entidad
        return Order(id=row["id"], customer=row["customer"], total=row["total"])
