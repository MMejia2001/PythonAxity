from __future__ import annotations

from pydantic import BaseModel, Field, PositiveFloat, PositiveInt

from .entity import Order, OrderItem


class OrderItemIn(BaseModel):
    sku: str = Field(min_length=1)
    name: str = Field(min_length=1)
    unit_price: PositiveFloat
    qty: PositiveInt


class OrderIn(BaseModel):
    order_id: PositiveInt
    customer: str = Field(min_length=1)
    items: list[OrderItemIn]
    tax_rate: float = Field(default=0.16, ge=0.0, le=1.0)

    def to_entity(self) -> Order:
        """Convierte el modelo validado (entrada) a la entidad Order (dataclass)."""
        items = [
            OrderItem(
                sku=i.sku,
                name=i.name,
                unit_price=float(i.unit_price),
                qty=int(i.qty),
            )
            for i in self.items
        ]
        return Order(
            order_id=int(self.order_id),
            customer=self.customer,
            items=items,
            tax_rate=self.tax_rate,
        )


class OrderItemOut(BaseModel):
    sku: str
    name: str
    unit_price: float
    qty: int
    line_total: float


class OrderOut(BaseModel):
    order_id: int
    customer: str
    items: list[OrderItemOut]
    tax_rate: float
    subtotal: float
    tax: float
    total: float

    @classmethod
    def from_entity(cls, order: Order) -> "OrderOut":
        """Convierte entidad Order a modelo de salida serializable."""
        items_out = [
            OrderItemOut(
                sku=i.sku,
                name=i.name,
                unit_price=i.unit_price,
                qty=i.qty,
                line_total=i.line_total,
            )
            for i in order.items
        ]
        return cls(
            order_id=order.order_id,
            customer=order.customer,
            items=items_out,
            tax_rate=order.tax_rate,
            subtotal=order.subtotal,
            tax=order.tax,
            total=order.total,
        )
