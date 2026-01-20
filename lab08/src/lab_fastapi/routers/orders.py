from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..deps import get_current_user, get_db
from ..models import Order, OrderItem, User
from ..schemas import OrderCreate, OrderItemOut, OrderOut

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("", response_model=OrderOut)
def create_order(
    payload: OrderCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    order = Order(user_id=user.id)
    db.add(order)
    db.commit()
    db.refresh(order)

    for item in payload.items:
        db.add(
            OrderItem(
                order_id=order.id,
                sku=item.sku,
                name=item.name,
                unit_price=float(item.unit_price),
                qty=int(item.qty),
            )
        )
    db.commit()
    db.refresh(order)

    return OrderOut(
        id=order.id,
        items=[
            OrderItemOut(sku=i.sku, name=i.name, unit_price=i.unit_price, qty=i.qty)
            for i in order.items
        ],
    )


@router.get("", response_model=list[OrderOut])
def list_orders(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    orders = db.query(Order).filter(Order.user_id == user.id).all()
    return [
        OrderOut(
            id=o.id,
            items=[
                OrderItemOut(sku=i.sku, name=i.name, unit_price=i.unit_price, qty=i.qty)
                for i in o.items
            ],
        )
        for o in orders
    ]


@router.get("/{order_id}", response_model=OrderOut)
def get_order(
    order_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    order = (
        db.query(Order).filter(Order.id == order_id, Order.user_id == user.id).first()
    )
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    return OrderOut(
        id=order.id,
        items=[
            OrderItemOut(sku=i.sku, name=i.name, unit_price=i.unit_price, qty=i.qty)
            for i in order.items
        ],
    )


@router.delete("/{order_id}")
def delete_order(
    order_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    order = (
        db.query(Order).filter(Order.id == order_id, Order.user_id == user.id).first()
    )
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    db.delete(order)
    db.commit()
    return {"deleted": True}
