from app import app
from fastapi.testclient import TestClient


def test_create_order_endpoint():
    client = TestClient(app)

    r = client.post(
        "/orders",
        json={
            "order_id": 1,
            "customer": "Marco",
            "tax_rate": 0.16,
            "items": [{"sku": "A1", "unit_price": 100.0, "qty": 2}],
        },
    )
    assert r.status_code == 200
    data = r.json()
    assert data["order_id"] == 1
    assert data["total"] > 0
