from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_product_not_found():
    response = client.get("/product/9999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Product not found"}


def test_create_product():
    response = client.post(
        "/product/",
        json={"html_content": "<html><h1>Test Product</h1><img src='http://example.com/image.jpg'><p class='comment'>Great product!</p></html>"}
    )
    assert response.status_code == 200
    assert "id" in response.json()
    assert response.json()["message"] == "Product created successfully"


def test_get_product():
    create_response = client.post(
        "/product/",
        json={"html_content": "<html><h1>Test Product</h1><img src='http://example.com/image.jpg'><p class='comment'>Great product!</p></html>"}
    )
    assert create_response.status_code == 200
    product_id = create_response.json()["id"]

    get_response = client.get(f"/product/{product_id}")
    assert get_response.status_code == 200
    product_data = get_response.json()
    assert product_data["title"] == "Test Product"
    assert "http://example.com/image.jpg" in product_data["image_urls"]
    assert "Great product!" in product_data["comments"] 
