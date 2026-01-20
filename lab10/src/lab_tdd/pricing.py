from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class Item:
    sku: str
    unit_price: float
    qty: int


class TaxProvider(Protocol):
    """Interface (contrato) para poder mockear fácilmente."""

    def get_tax_rate(self, customer_country: str) -> float: ...


def subtotal(items: list[Item]) -> float:
    if not items:
        return 0.0

    total = 0.0
    for it in items:
        if it.unit_price < 0:
            raise ValueError("unit_price no puede ser negativo")
        if it.qty <= 0:
            raise ValueError("qty debe ser > 0")
        total += it.unit_price * it.qty
    return round(total, 2)


def shipping_cost(subtotal_amount: float) -> float:
    """
    Reglas simples:
    - Si subtotal >= 1000 -> envío gratis
    - Si subtotal > 0 -> envío 99
    - Si subtotal == 0 -> envío 0
    """
    if subtotal_amount >= 1000:
        return 0.0
    if subtotal_amount > 0:
        return 99.0
    return 0.0


def discount_amount(subtotal_amount: float, coupon: str | None) -> float:
    """
    Cupones:
    - None o "" -> 0
    - "SAVE10" -> 10% del subtotal (máximo 200)
    - "SAVE50" -> 50 pesos (si subtotal > 0)
    """
    if not coupon:
        return 0.0

    code = coupon.strip().upper()

    if code == "SAVE10":
        disc = subtotal_amount * 0.10
        return round(min(disc, 200.0), 2)

    if code == "SAVE50":
        return 50.0 if subtotal_amount > 0 else 0.0

    # cupón desconocido -> no aplica
    return 0.0


def order_total(
    items: list[Item],
    customer_country: str,
    tax_provider: TaxProvider,
    coupon: str | None = None,
) -> dict:
    """
    Calcula total de orden.
    Devuelve desglose para facilitar test y debug.
    """
    sub = subtotal(items)
    ship = shipping_cost(sub)
    disc = discount_amount(sub, coupon)

    tax_rate = tax_provider.get_tax_rate(customer_country)
    if tax_rate < 0 or tax_rate > 1:
        raise ValueError("tax_rate fuera de rango (0..1)")

    taxable_base = max(sub - disc, 0.0)
    tax = round(taxable_base * tax_rate, 2)

    total = round(taxable_base + tax + ship, 2)

    return {
        "subtotal": sub,
        "shipping": ship,
        "discount": disc,
        "tax": tax,
        "total": total,
        "tax_rate": tax_rate,
    }
