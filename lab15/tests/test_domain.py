import pytest

from lab_hex.domain import Order, OrderItem


def test_order_validation_fails_without_items():
    with pytest.raises(ValueError):
        o = Order(order_id=1, customer="X", items=[])
        o.validate()


def test_order_totals():
    o = Order(
        order_id=1,
        customer="X",
        items=[OrderItem("A", 100.0, 2)],
        tax_rate=0.16,
    )
    o.validate()
    assert o.subtotal == 200.0
    assert o.tax == 32.0
    assert o.total == 232.0
