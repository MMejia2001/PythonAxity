from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class OrderItem:
    sku: str
    unit_price: float
    qty: int

    @property
    def line_total(self) -> float:
        return round(self.unit_price * self.qty, 2)


@dataclass(frozen=True)
class Order:
    order_id: int
    customer: str
    items: List[OrderItem]
    tax_rate: float = 0.16

    def validate(self) -> None:
        if self.order_id <= 0:
            raise ValueError("order_id debe ser > 0")
        if not self.customer:
            raise ValueError("customer requerido")
        if not self.items:
            raise ValueError("items requerido (mínimo 1)")
        if not (0 <= self.tax_rate <= 1):
            raise ValueError("tax_rate debe estar entre 0 y 1")
        for it in self.items:
            if not it.sku:
                raise ValueError("sku requerido")
            if it.unit_price < 0:
                raise ValueError("unit_price no puede ser negativo")
            if it.qty <= 0:
                raise ValueError("qty debe ser > 0")

    @property
    def subtotal(self) -> float:
        return round(sum(i.line_total for i in self.items), 2)

    @property
    def tax(self) -> float:
        return round(self.subtotal * self.tax_rate, 2)

    @property
    def total(self) -> float:
        return round(self.subtotal + self.tax, 2)
