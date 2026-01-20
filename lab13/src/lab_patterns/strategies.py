from __future__ import annotations

from typing import Protocol

from .domain import CartItem, Customer


class PricingStrategy(Protocol):
    def price(self, items: list[CartItem], customer: Customer) -> float: ...


class RegularPricing:
    def price(self, items: list[CartItem], customer: Customer) -> float:
        return round(sum(i.unit_price * i.qty for i in items), 2)


class VipPricing:
    """VIP tiene 10% descuento en subtotal."""

    def price(self, items: list[CartItem], customer: Customer) -> float:
        subtotal = sum(i.unit_price * i.qty for i in items)
        return round(subtotal * 0.90, 2)
