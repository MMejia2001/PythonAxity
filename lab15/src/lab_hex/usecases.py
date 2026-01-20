from __future__ import annotations

from .domain import Order, OrderItem
from .ports import Notifier, OrderRepository


class CreateOrder:
    def __init__(self, repo: OrderRepository, notifier: Notifier) -> None:
        self._repo = repo
        self._notifier = notifier

    def execute(
        self,
        order_id: int,
        customer: str,
        items: list[dict],
        tax_rate: float = 0.16,
    ) -> Order:
        order_items = [
            OrderItem(
                sku=str(i["sku"]),
                unit_price=float(i["unit_price"]),
                qty=int(i["qty"]),
            )
            for i in items
        ]

        order = Order(
            order_id=order_id,
            customer=customer,
            items=order_items,
            tax_rate=tax_rate,
        )
        order.validate()

        self._repo.add(order)
        self._notifier.notify_order_created(order)

        return order
