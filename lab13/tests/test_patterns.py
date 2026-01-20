from lab_patterns.adapter import ShippingAdapter
from lab_patterns.domain import CartItem, Customer
from lab_patterns.provider_external import ExternalShippingApi
from lab_patterns.service import CheckoutService, _calc_weight
from lab_patterns.strategies import RegularPricing, VipPricing


def test_strategy_regular_vs_vip():
    items = [CartItem("A", 100.0, 1)]
    c = Customer("1", "regular")

    reg = RegularPricing().price(items, c)
    vip = VipPricing().price(items, c)

    assert reg == 100.0
    assert vip == 90.0  # 10% off


def test_adapter_returns_float_cost():
    api = ExternalShippingApi()
    adapter = ShippingAdapter(api)

    cost = adapter.get_shipping_cost("64000", 2.0)
    assert isinstance(cost, float)
    assert cost > 0


def test_cache_decorator_reuses_result():
    items = (CartItem("A", 10.0, 2),)
    w1 = _calc_weight(items)
    w2 = _calc_weight(items)
    assert w1 == w2  # misma salida, y la segunda fue cacheada internamente


def test_checkout_total_works():
    items = [CartItem("A", 100.0, 2)]  # subtotal 200
    cust = Customer("1", "regular")
    svc = CheckoutService(RegularPricing(), ShippingAdapter(ExternalShippingApi()))

    total = svc.total(items, cust, "64000")
    assert total > 200.0  # subtotal + shipping
