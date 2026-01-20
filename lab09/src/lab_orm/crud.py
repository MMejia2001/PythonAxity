from __future__ import annotations

from sqlalchemy.orm import Session

from .models import Order, OrderItem, User


def create_user(db: Session, email: str, name: str) -> User:
    user = User(email=email, name=name)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def create_order(db: Session, user: User) -> Order:
    order = Order(user_id=user.id)
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


def add_item_to_order(
    db: Session,
    order: Order,
    sku: str,
    name: str,
    unit_price: float,
    qty: int,
) -> OrderItem:
    item = OrderItem(
        order_id=order.id, sku=sku, name=name, unit_price=unit_price, qty=qty
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def list_orders_for_user(db: Session, user: User) -> list[Order]:
    return db.query(Order).filter(Order.user_id == user.id).all()


def delete_user(db: Session, user: User) -> None:
    db.delete(user)
    db.commit()
