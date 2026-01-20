from lab_objetos.schemas import OrderIn, OrderOut


def main() -> None:
    # Simula un "JSON de entrada" (en Python es un dict)
    payload = {
        "order_id": 1,
        "customer": "Marco",
        "tax_rate": 0.16,
        "items": [
            {"sku": "A1", "name": "Mouse", "unit_price": 250.0, "qty": 1},
            {"sku": "B2", "name": "Teclado", "unit_price": 500.0, "qty": 2},
        ],
    }

    # 1) Validación con Pydantic (entrada)
    order_in = OrderIn.model_validate(payload)

    # 2) Convertir a entidad (dataclass)
    order_entity = order_in.to_entity()

    # 3) Convertir a salida (Pydantic)
    order_out = OrderOut.from_entity(order_entity)

    print(order_entity)  # usa __str__
    print("Items:", len(order_entity))  # usa __len__

    # 4) Serializar a dict “tipo JSON”
    print("\nSalida serializada:")
    print(order_out.model_dump())


if __name__ == "__main__":
    main()
