from lab_clean.application.usecases import CreateOrderUseCase
from lab_clean.domain.events import OrderCreated
from lab_clean.infra.uow_memory import InMemoryUoW


def test_create_order_publishes_event_and_saves_order():
    uow = InMemoryUoW()
    uc = CreateOrderUseCase(uow)

    order = uc.execute(
        order_id=1,
        customer="Marco",
        items=[{"sku": "A1", "unit_price": 100.0, "qty": 2}],
        tax_rate=0.16,
    )

    saved = uow.orders.get(1)
    assert saved is not None
    assert saved.total == order.total

    assert any(isinstance(e, OrderCreated) for e in uow.events.published)
