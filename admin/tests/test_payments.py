import requests
#from src.core.board import delete_payment

def test_member_paymets_api():
    response = requests.get("http://localhost:5000/api/me/payments/1")
    print(response)
    assert response.status_code == 200
    data = response.json()["data"]
    assert len(data) == 5
    assert data["name"] == "Juan"
    assert data["surname"] == "Perez"
    assert len(data["payments"]) == 1

def test_post_payments_api():
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
    #delete_payment(2)
    