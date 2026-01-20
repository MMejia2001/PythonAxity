from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable


@dataclass(frozen=True)  #crea init automático, inmutable
class OrderItem:
    """Item de una orden."""

    sku: str
    name: str
    unit_price: float
    qty: int

    def __post_init__(self) -> None:
        if not self.sku or not self.name:
            raise ValueError("sku y name no pueden estar vacíos")
        if self.unit_price < 0:
            raise ValueError("unit_price no puede ser negativo")
        if self.qty <= 0:
            raise ValueError("qty debe ser mayor que 0")

    @property
    def line_total(self) -> float:
        return round(self.unit_price * self.qty, 2)


@dataclass
class Order:
    """
    Entidad Order (dataclass).
    - Tiene cálculos derivados: subtotal, tax, total
    - Soporta comparaciones (ordenamiento) por total y luego por id
    """

    order_id: int
    customer: str
    items: list[OrderItem] = field(default_factory=list)
    tax_rate: float = 0.16  # 16% por defecto

    def __post_init__(self) -> None:
        if self.order_id <= 0:
            raise ValueError("order_id debe ser mayor que 0")
        if not self.customer:
            raise ValueError("customer no puede estar vacío")
        if not (0 <= self.tax_rate <= 1):
            raise ValueError("tax_rate debe estar entre 0 y 1")
        if len(self.items) == 0:
            raise ValueError("Una orden debe tener al menos 1 item")

    # ---- dunder methods ----
    def __str__(self) -> str:
        return (
            f"Order(id={self.order_id}, customer={self.customer}, total={self.total})"
        )

    def __len__(self) -> int:
        """Cantidad de items."""
        return len(self.items)

    # Comparaciones: ordena por total, luego por order_id
    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Order):
            return NotImplemented
        if self.total != other.total:
            return self.total < other.total
        return self.order_id < other.order_id

    # ---- cálculos derivados ----
    @property
    def subtotal(self) -> float:
        return round(sum(i.line_total for i in self.items), 2)

    @property
    def tax(self) -> float:
        return round(self.subtotal * self.tax_rate, 2)

    @property
    def total(self) -> float:
        return round(self.subtotal + self.tax, 2)

    # ---- helpers “pythonic” ----
    @classmethod
    def from_items(
        cls,
        order_id: int,
        customer: str,
        items: Iterable[OrderItem],
        tax_rate: float = 0.16,
    ) -> "Order":
        return cls(
            order_id=order_id, customer=customer, items=list(items), tax_rate=tax_rate
        )
