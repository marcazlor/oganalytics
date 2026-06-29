from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_get_latest_price():
       response = client.get("/price/latest")
       assert response.status_code == 200

def test_get_prices():
       response = client.get("/price/")
       assert response.status_code == 200

def test_get_spread():
       response = client.get("/price/spread")
       assert response.status_code == 200

def test_get_spread_by_date():
       response = client.get("/price/spread/filter?start_date=1990-08-31&end_date=1994-03-31")
       assert response.status_code == 200

def test_get_spread_content():
    response = client.get("/price/spread")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0          # devuelve datos, no lista vacía
    assert "spread" in data[0]     # cada elemento tiene el campo spread

def test_get_spread_by_date_invalid_range():
    response = client.get("/price/spread/filter?start_date=2050-08-31&end_date=1994-03-31")
    assert response.status_code == 404