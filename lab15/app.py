from fastapi import Depends, FastAPI
from pydantic import BaseModel, Field, PositiveFloat, PositiveInt

from lab_hex.infra_http_notify import FakeHttpClient, HttpNotifier
from lab_hex.infra_memory import InMemoryOrderRepo
from lab_hex.usecases import CreateOrder

app = FastAPI(title="Lab Hexagonal")

# “Wiring” simple: creamos adapters acá (para el lab)
_repo = InMemoryOrderRepo()
_http_client = FakeHttpClient()
_notifier = HttpNotifier(_http_client, url="http://notify.local/order-created")


def get_usecase() -> CreateOrder:
    return CreateOrder(repo=_repo, notifier=_notifier)


class ItemIn(BaseModel):
    sku: str = Field(min_length=1)
    unit_price: PositiveFloat
    qty: PositiveInt


class CreateOrderIn(BaseModel):
    order_id: PositiveInt
    customer: str = Field(min_length=1)
    tax_rate: float = Field(default=0.16, ge=0.0, le=1.0)
    items: list[ItemIn] = Field(min_length=1)


@app.post("/orders")
def create_order(payload: CreateOrderIn, uc: CreateOrder = Depends(get_usecase)):
    order = uc.execute(
        order_id=int(payload.order_id),
        customer=payload.customer,
        items=[i.model_dump() for i in payload.items],
        tax_rate=float(payload.tax_rate),
    )
    return {
        "order_id": order.order_id,
        "customer": order.customer,
        "subtotal": order.subtotal,
        "tax": order.tax,
        "total": order.total,
    }
