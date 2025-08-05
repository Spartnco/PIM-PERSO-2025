from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_and_list_products() -> None:
    create_resp = client.post(
        "/products", json={"sku": "SKU001", "name": "Example"}
    )
    assert create_resp.status_code == 200
    product = create_resp.json()
    assert product["id"] is not None

    list_resp = client.get("/products")
    assert list_resp.status_code == 200
    data = list_resp.json()
    assert len(data) == 1
    assert data[0]["sku"] == "SKU001"