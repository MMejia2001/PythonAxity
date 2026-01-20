def test_register_login_and_crud_orders(client):
    # register
    r = client.post(
        "/auth/register", json={"email": "ana@example.com", "password": "1234"}
    )
    assert r.status_code == 200
    token = r.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # create order
    r = client.post(
        "/orders",
        headers=headers,
        json={"items": [{"sku": "A1", "name": "Mouse", "unit_price": 100.0, "qty": 1}]},
    )
    assert r.status_code == 200
    order_id = r.json()["id"]

    # list
    r = client.get("/orders", headers=headers)
    assert r.status_code == 200
    assert len(r.json()) == 1

    # get
    r = client.get(f"/orders/{order_id}", headers=headers)
    assert r.status_code == 200
    assert r.json()["id"] == order_id

    # delete
    r = client.delete(f"/orders/{order_id}", headers=headers)
    assert r.status_code == 200
    assert r.json()["deleted"] is True
