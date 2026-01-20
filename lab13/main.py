from lab_patterns.adapter import ShippingAdapter
from lab_patterns.domain import CartItem, Customer
from lab_patterns.provider_external import ExternalShippingApi
from lab_patterns.service import CheckoutService
from lab_patterns.strategies import RegularPricing, VipPricing


def main() -> None:
    items = [CartItem("A1", 100.0, 2), CartItem("B2", 50.0, 1)]
    customer = Customer("C1", "vip")

    pricing = VipPricing() if customer.tier == "vip" else RegularPricing()
    shipping = ShippingAdapter(ExternalShippingApi())

    svc = CheckoutService(pricing=pricing, shipping=shipping)
    print("Total:", svc.total(items, customer, zip_code="64000"))


if __name__ == "__main__":
    main()
