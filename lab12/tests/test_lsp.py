import pytest

from lab_solid.repos import FakeSqlOrderRepo, InMemoryOrderRepo
from lab_solid.service import OrderService


@pytest.mark.parametrize("repo_cls", [InMemoryOrderRepo, FakeSqlOrderRepo])
def test_service_works_with_any_repo(repo_cls):
    repo = repo_cls()
    svc = OrderService(repo)

    created = svc.create_order(1, "Ana", 10.0)
    fetched = svc.get_order(1)

    assert fetched == created


@pytest.mark.parametrize("repo_cls", [InMemoryOrderRepo, FakeSqlOrderRepo])
def test_get_unknown_returns_none(repo_cls):
    repo = repo_cls()
    svc = OrderService(repo)

    assert svc.get_order(999) is None
