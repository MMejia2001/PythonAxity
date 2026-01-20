from __future__ import annotations

from sqlalchemy import ForeignKey, create_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    sessionmaker,
)

from .domain import Order, OrderItem
from .ports import OrderRepository


class Base(DeclarativeBase):
    pass


class OrderRow(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True)
    customer: Mapped[str]
    tax_rate: Mapped[float]

    items: Mapped[list["OrderItemRow"]] = relationship(
        back_populates="order", cascade="all, delete-orphan"
    )


class OrderItemRow(Base):
    __tablename__ = "order_items"
    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    sku: Mapped[str]
    unit_price: Mapped[float]
    qty: Mapped[int]

    order: Mapped["OrderRow"] = relationship(back_populates="items")


class SqlAlchemyOrderRepo(OrderRepository):
    def __init__(self, db_url: str = "sqlite:///lab.db") -> None:
        self._engine = create_engine(
            db_url, connect_args={"check_same_thread": False}, future=True
        )
        Base.metadata.create_all(bind=self._engine)
        self._Session = sessionmaker(bind=self._engine, future=True)

    def add(self, order: Order) -> None:
        with self._Session() as s:
            row = OrderRow(
                id=order.order_id, customer=order.customer, tax_rate=order.tax_rate
            )
            for it in order.items:
                row.items.append(
                    OrderItemRow(sku=it.sku, unit_price=it.unit_price, qty=it.qty)
                )
            s.add(row)
            s.commit()

    def get(self, order_id: int) -> Order | None:
        with self._Session() as s:
            row = s.get(OrderRow, order_id)
            if not row:
                return None

            items = [
                OrderItem(sku=i.sku, unit_price=i.unit_price, qty=i.qty)
                for i in row.items
            ]
            return Order(
                order_id=row.id,
                customer=row.customer,
                items=items,
                tax_rate=row.tax_rate,
            )
