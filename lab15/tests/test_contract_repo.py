import pytest

from lab_hex.domain import Order, OrderItem
from lab_hex.infra_memory import InMemoryOrderRepo
from lab_hex.infra_sqlalchemy import SqlAlchemyOrderRepo


@pytest.mark.parametrize(
    "repo_factory",
    [
        lambda: InMemoryOrderRepo(),
        lambda: SqlAlchemyOrderRepo("sqlite+pysqlite:///:memory:"),
    ],
)
def test_repo_contract_add_get(repo_factory):
    repo = repo_factory()
    order = Order(
        order_id=1,
        customer="Ana",
        items=[OrderItem("A", 10.0, 1)],
    )
    order.validate()

    repo.add(order)
    fetched = repo.get(1)

    assert fetched is not None
    assert fetched.order_id == 1
    assert fetched.customer == "Ana"
    assert fetched.total == order.total
