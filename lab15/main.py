from lab_hex.infra_http_notify import FakeHttpClient, HttpNotifier
from lab_hex.infra_memory import InMemoryOrderRepo
from lab_hex.usecases import CreateOrder


def main() -> None:
    repo = InMemoryOrderRepo()
    fake_http = FakeHttpClient()
    notifier = HttpNotifier(fake_http, url="http://notify.local/order-created")

    uc = CreateOrder(repo, notifier)

    order = uc.execute(
        order_id=1,
        customer="Marco",
        items=[
            {"sku": "A1", "unit_price": 100.0, "qty": 2},
            {"sku": "B2", "unit_price": 50.0, "qty": 1},
        ],
    )

    print("Order total:", order.total)
    print("HTTP calls:", fake_http.calls)


if __name__ == "__main__":
    main()
