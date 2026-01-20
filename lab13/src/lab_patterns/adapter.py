from __future__ import annotations

from typing import Protocol

from .provider_external import ExternalShippingApi


class ShippingProvider(Protocol):
    def get_shipping_cost(self, zip_code: str, weight_kg: float) -> float: ...


class ShippingAdapter:
    """
    Adapter: adapta ExternalShippingApi a nuestra interfaz ShippingProvider.
    """

    def __init__(self, api: ExternalShippingApi) -> None:
        self._api = api

    def get_shipping_cost(self, zip_code: str, weight_kg: float) -> float:
        data = self._api.quote(zip_code, weight_kg)
        return float(data["cost_mxn"])
