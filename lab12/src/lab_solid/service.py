from __future__ import annotations

from .domain import Order
from .ports import OrderRepo


class OrderService:
    def __init__(self, repo: OrderRepo) -> None:
        self._repo = repo

    def create_order(self, order_id: int, customer: str, total: float) -> Order:
        if order_id <= 0:
            raise ValueError("order_id debe ser > 0")
        if not customer:
            raise ValueError("customer requerido")
        if total < 0:
            raise ValueError("total no puede ser negativo")

        order = Order(id=order_id, customer=customer, total=round(total, 2))
        self._repo.add(order)
        return order

    def get_order(self, order_id: int) -> Order | None:
        return self._repo.get(order_id)
