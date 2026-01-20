from lab_orm.crud import (
    add_item_to_order,
    create_order,
    create_user,
    list_orders_for_user,
)
from lab_orm.db import SessionLocal, engine
from lab_orm.models import Base


def main() -> None:
    # Crear tablas (solo demo; en real usarás Alembic)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        user = create_user(db, "marco@example.com", "Marco")
        order = create_order(db, user)

        add_item_to_order(db, order, "A1", "Mouse", 250.0, 1)
        add_item_to_order(db, order, "B2", "Teclado", 500.0, 2)

        orders = list_orders_for_user(db, user)
        print("Órdenes del usuario:", len(orders))
        print("Items de la primera orden:", len(orders[0].items))

    finally:
        db.close()


if __name__ == "__main__":
    main()
