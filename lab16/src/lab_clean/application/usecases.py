from __future__ import annotations

from lab_clean.domain.entities import Order, OrderItem
from lab_clean.domain.events import OrderCreated

from .handlers import PrintOrderCreatedHandler
from .uow import UnitOfWork


class CreateOrderUseCase:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow
        self._handler = PrintOrderCreatedHandler()

    def execute(
        self, order_id: int, customer: str, items: list[dict], tax_rate: float = 0.16
    ) -> Order:
        order_items = [
            OrderItem(
                sku=str(i["sku"]), unit_price=float(i["unit_price"]), qty=int(i["qty"])
            )
            for i in items
        ]

        order = Order(
            order_id=order_id, customer=customer, items=order_items, tax_rate=tax_rate
        )
        order.validate()

        self._uow.orders.add(order)
        order.mark_created()

        # “Commit” primero, luego publicar/manejar eventos
        self._uow.commit()

        # Publicar/manejar eventos en app (simple)
        for ev in order.events:
            self._uow.events.publish(ev)
            if isinstance(ev, OrderCreated):
                self._handler.handle(ev)

        return order
