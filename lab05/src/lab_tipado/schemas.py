from __future__ import annotations

from typing import Literal, TypedDict, Union

from pydantic import BaseModel, Field, PositiveFloat, PositiveInt

from .entity import Order, OrderItem


# --- TypedDict: “shape” del payload tipo JSON (dict) ---
class OrderItemPayload(TypedDict):
    sku: str
    name: str
    unit_price: Union[int, float, str]  # Union: puede venir como "40"
    qty: int


class OrderPayload(TypedDict):
    order_id: int
    customer: str
    items: list[OrderItemPayload]
    tax_rate: float


# --- Literal: valores permitidos (ejemplo simple) ---
OrderStatus = Literal["new", "paid", "cancelled"]


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
    status: OrderStatus = "new"

    def to_entity(self) -> Order:
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
    status: OrderStatus

    @classmethod
    def from_entity(cls, order: Order, status: OrderStatus = "new") -> "OrderOut":
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
            status=status,
        )
