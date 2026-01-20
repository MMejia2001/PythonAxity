from dataclasses import dataclass, field

from .events import OrderCreated


@dataclass
class OrderItem:
    sku: str
    unit_price: float
    qty: int

    @property
    def line_total(self) -> float:
        return round(self.unit_price * self.qty, 2)


@dataclass
class Order:
    order_id: int
    customer: str
    items: list[OrderItem]
    tax_rate: float = 0.16
    events: list[object] = field(default_factory=list)

    def validate(self) -> None:
        if self.order_id <= 0:
            raise ValueError("order_id debe ser > 0")
        if not self.customer:
            raise ValueError("customer requerido")
        if not self.items:
            raise ValueError("mínimo 1 item")

    @property
    def subtotal(self) -> float:
        return round(sum(i.line_total for i in self.items), 2)

    @property
    def tax(self) -> float:
        return round(self.subtotal * self.tax_rate, 2)

    @property
    def total(self) -> float:
        return round(self.subtotal + self.tax, 2)

    def mark_created(self) -> None:
        self.events.append(OrderCreated(self.order_id, self.customer, self.total))
