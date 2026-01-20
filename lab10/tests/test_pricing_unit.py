from unittest.mock import Mock

import pytest

from lab_tdd.pricing import Item, discount_amount, order_total, shipping_cost, subtotal


@pytest.fixture
def sample_items():
    return [
        Item(sku="A1", unit_price=100.0, qty=2),  # 200
        Item(sku="B2", unit_price=50.0, qty=1),  # 50
    ]


def test_subtotal_ok(sample_items):
    assert subtotal(sample_items) == 250.0


@pytest.mark.parametrize(
    "sub,expected_shipping",
    [
        (0.0, 0.0),
        (10.0, 99.0),
        (999.99, 99.0),
        (1000.0, 0.0),
        (1500.0, 0.0),
    ],
)
def test_shipping_rules(sub, expected_shipping):
    assert shipping_cost(sub) == expected_shipping


@pytest.mark.parametrize(
    "sub,coupon,expected",
    [
        (0.0, None, 0.0),
        (0.0, "SAVE50", 0.0),
        (100.0, "SAVE50", 50.0),
        (100.0, "save10", 10.0),
        (5000.0, "SAVE10", 200.0),  # tope
        (100.0, "UNKNOWN", 0.0),
    ],
)
def test_discount_amount(sub, coupon, expected):
    assert discount_amount(sub, coupon) == expected


def test_order_total_uses_tax_provider_and_returns_breakdown(sample_items):
    tax_provider = Mock()
    tax_provider.get_tax_rate.return_value = 0.16

    result = order_total(
        items=sample_items,
        customer_country="MX",
        tax_provider=tax_provider,
        coupon=None,
    )

    tax_provider.get_tax_rate.assert_called_once_with("MX")

    assert result["subtotal"] == 250.0
    assert result["discount"] == 0.0
    assert result["shipping"] == 99.0
    assert result["tax"] == 40.0  # 250 * 0.16
    assert result["total"] == 389.0  # 250 + 40 + 99


def test_subtotal_rejects_negative_price():
    with pytest.raises(ValueError):
        subtotal([Item(sku="X", unit_price=-1.0, qty=1)])


def test_subtotal_rejects_non_positive_qty():
    with pytest.raises(ValueError):
        subtotal([Item(sku="X", unit_price=10.0, qty=0)])
