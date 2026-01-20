from dataclasses import dataclass


@dataclass(frozen=True)
class CartItem:
    sku: str
    unit_price: float
    qty: int


@dataclass(frozen=True)
class Customer:
    customer_id: str
    tier: str  # "regular" | "vip"
