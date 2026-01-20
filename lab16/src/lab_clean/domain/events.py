from dataclasses import dataclass


@dataclass(frozen=True)
class OrderCreated:
    order_id: int
    customer: str
    total: float
