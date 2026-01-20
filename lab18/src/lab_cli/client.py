from __future__ import annotations

import os
from typing import Any

import httpx


def get_base_url() -> str:
    # variable de entorno: ORDERS_API_URL
    return os.getenv("ORDERS_API_URL", "http://127.0.0.1:8000").rstrip("/")


class OrdersClient:
    def __init__(self, base_url: str | None = None) -> None:
        self.base_url = (base_url or get_base_url()).rstrip("/")

    def list_orders(self) -> list[dict[str, Any]]:
        r = httpx.get(f"{self.base_url}/orders", timeout=10.0)
        r.raise_for_status()
        return r.json()

    def create_order(self, order: dict[str, Any]) -> dict[str, Any]:
        r = httpx.post(f"{self.base_url}/orders", json=order, timeout=10.0)
        r.raise_for_status()
        return r.json()

    def delete_order(self, order_id: int) -> dict[str, Any]:
        r = httpx.delete(f"{self.base_url}/orders/{order_id}", timeout=10.0)
        r.raise_for_status()
        return r.json()
