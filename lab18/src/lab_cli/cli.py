from __future__ import annotations

import json
from typing import Optional

import typer

from .client import OrdersClient

app = typer.Typer(help="CLI para gestionar Orders consumiendo una API")


@app.command()
def list(api_url: Optional[str] = typer.Option(None, help="URL base de la API")):
    """Lista orders."""
    client = OrdersClient(api_url)
    orders = client.list_orders()
    typer.echo(json.dumps(orders, indent=2, ensure_ascii=False))


@app.command()
def create(
    order_id: int = typer.Option(..., help="ID de la orden"),
    customer: str = typer.Option(..., help="Cliente"),
    sku: str = typer.Option(..., help="SKU (un item simple)"),
    unit_price: float = typer.Option(..., help="Precio unitario"),
    qty: int = typer.Option(..., help="Cantidad"),
    api_url: Optional[str] = typer.Option(None, help="URL base de la API"),
):
    """Crea una order (simple: 1 item)."""
    client = OrdersClient(api_url)

    payload = {
        "order_id": order_id,
        "customer": customer,
        "items": [{"sku": sku, "unit_price": unit_price, "qty": qty}],
    }

    created = client.create_order(payload)
    typer.echo(json.dumps(created, indent=2, ensure_ascii=False))


@app.command()
def delete(
    order_id: int = typer.Argument(..., help="ID a borrar"),
    api_url: Optional[str] = typer.Option(None, help="URL base de la API"),
):
    """Borra una order por ID."""
    client = OrdersClient(api_url)
    result = client.delete_order(order_id)
    typer.echo(json.dumps(result, indent=2, ensure_ascii=False))


def main():
    app()


if __name__ == "__main__":
    main()
