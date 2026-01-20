from fastapi import Depends, FastAPI
from pydantic import BaseModel, Field, PositiveFloat, PositiveInt
from lab_clean.settings import settings

from lab_clean.adapters.presenter import OrderPresenter
from lab_clean.application.usecases import CreateOrderUseCase
from lab_clean.infra.uow_memory import InMemoryUoW

app = FastAPI(title="Lab Clean Architecture")

_uow = InMemoryUoW()
_presenter = OrderPresenter()


def get_usecase() -> CreateOrderUseCase:
    return CreateOrderUseCase(_uow)


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
def create_order(payload: CreateOrderIn, uc: CreateOrderUseCase = Depends(get_usecase)):
    order = uc.execute(
        order_id=int(payload.order_id),
        customer=payload.customer,
        items=[i.model_dump() for i in payload.items],
        tax_rate=float(payload.tax_rate),
    )
    return _presenter.to_dict(order)


# ejemplo: mostrar entorno en /health
@app.get("/health")
def health():
    return {"status": "ok", "env": settings.app_env}