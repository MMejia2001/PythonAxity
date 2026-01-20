from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, PositiveFloat, PositiveInt

app = FastAPI(title="Lab CLI API")

# “DB” en memoria (para lab)
ORDERS: dict[int, dict] = {}


class ItemIn(BaseModel):
    sku: str = Field(min_length=1)
    unit_price: PositiveFloat
    qty: PositiveInt


class OrderIn(BaseModel):
    order_id: PositiveInt
    customer: str = Field(min_length=1)
    items: list[ItemIn] = Field(min_length=1)


@app.get("/orders")
def list_orders():
    return list(ORDERS.values())


@app.post("/orders")
def create_order(payload: OrderIn):
    oid = int(payload.order_id)
    if oid in ORDERS:
        raise HTTPException(status_code=409, detail="order_id ya existe")

    order = payload.model_dump()
    ORDERS[oid] = order
    return order


@app.delete("/orders/{order_id}")
def delete_order(order_id: int):
    if order_id not in ORDERS:
        raise HTTPException(status_code=404, detail="No existe")
    del ORDERS[order_id]
    return {"deleted": order_id}
