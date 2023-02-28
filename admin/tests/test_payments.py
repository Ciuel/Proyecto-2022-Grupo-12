import requests
import pytest
from src.web import create_app

@pytest.fixture()
def app():
    app = create_app()
    app.config.update(
        {
            "TESTING": True,
        }
    )
    yield app

@pytest.fixture()
def client(app):
    return app.test_client()

def test_member_paymets_api():
    response = requests.get("http://localhost:5000/api/me/payments/1")
    print(response)
    assert response.status_code == 200
    data = response.json()["data"]
    assert len(data) == 5
    assert data["name"] == "Juan"
    assert data["surname"] == "Perez"
    assert len(data["payments"]) == 1

def test_post_payments_api(app):
    response = requests.get("http://localhost:5000/api/me/payments/1")
    print(response)
    assert response.status_code == 200
    data = response.json()["data"]
    assert len(data["payments"]) == 1
    requests.post("http://localhost:5000/api/me/payments/1")
    response = requests.get("http://localhost:5000/api/me/payments/1")
    print(response)
    assert response.status_code == 200
    data = response.json()["data"]
    assert len(data["payments"]) == 2
    print(data["payments"][-1]["id"])
    with app.app_context():
        from src.core.board import delete_payment
        delete_payment(data["payments"][-1]["id"])
    