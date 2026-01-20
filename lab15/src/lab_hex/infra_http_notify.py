from __future__ import annotations

from typing import Protocol

from .domain import Order
from .ports import Notifier


class HttpClient(Protocol):
    def post(self, url: str, json: dict) -> None: ...


class HttpNotifier(Notifier):
    def __init__(self, client: HttpClient, url: str) -> None:
        self._client = client
        self._url = url

    def notify_order_created(self, order: Order) -> None:
        payload = {
            "order_id": order.order_id,
            "customer": order.customer,
            "total": order.total,
        }
        self._client.post(self._url, json=payload)


class FakeHttpClient:
    """Para pruebas: no hace red, solo guarda lo que “hubiera enviado”."""

    def __init__(self) -> None:
        self.calls: list[tuple[str, dict]] = []

    def post(self, url: str, json: dict) -> None:
        self.calls.append((url, json))
