from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from lab_orm.crud import (
    add_item_to_order,
    create_order,
    create_user,
    list_orders_for_user,
)
from lab_orm.models import Base


def test_crud_flow_sqlite_in_memory():
    engine = create_engine("sqlite+pysqlite:///:memory:", future=True)
    TestingSessionLocal = sessionmaker(
        bind=engine, autoflush=False, autocommit=False, future=True
    )

    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        user = create_user(db, "ana@example.com", "Ana")
        order = create_order(db, user)
        add_item_to_order(db, order, "X1", "USB", 100.0, 1)

        orders = list_orders_for_user(db, user)

        assert len(orders) == 1
        assert len(orders[0].items) == 1
        assert orders[0].items[0].sku == "X1"
    finally:
        db.close()
