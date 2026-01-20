from __future__ import annotations

from .adapter import ShippingProvider
from .cache_decorator import simple_cache
from .domain import CartItem, Customer
from .strategies import PricingStrategy


@simple_cache
def _calc_weight(items: tuple[CartItem, ...]) -> float:
    # ejemplo simple: cada item pesa 0.2kg por unidad
    return round(sum(i.qty * 0.2 for i in items), 2)


class CheckoutService:
    def __init__(self, pricing: PricingStrategy, shipping: ShippingProvider) -> None:
        self._pricing = pricing
        self._shipping = shipping

    def total(self, items: list[CartItem], customer: Customer, zip_code: str) -> float:
        subtotal = self._pricing.price(items, customer)

        weight = _calc_weight(tuple(items))
        shipping_cost = self._shipping.get_shipping_cost(zip_code, weight)

        return round(subtotal + shipping_cost, 2)
