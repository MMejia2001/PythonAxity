from __future__ import annotations

from lab_tipado.repo import InMemoryOrderRepo
from lab_tipado.schemas import OrderIn, OrderOut, OrderPayload


def main() -> None:
    payload: OrderPayload = {
        "order_id": 1,
        "customer": "Marco",
        "tax_rate": 0.16,
        "items": [
            {"sku": "A1", "name": "Mouse", "unit_price": 250.0, "qty": 1},
            {"sku": "B2", "name": "Teclado", "unit_price": 500, "qty": 2},
        ],
    }

    order_in = OrderIn.model_validate(payload)
    order_entity = order_in.to_entity()

    repo = InMemoryOrderRepo()
    repo.save(order_entity)

    loaded = repo.get(1)
    if loaded is None:
        print("No se encontró la orden")
        return

    out = OrderOut.from_entity(loaded, status=order_in.status)
    print(out.model_dump())


if __name__ == "__main__":
    main()
