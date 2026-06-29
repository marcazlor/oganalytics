from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_et_inventories():
    response = client.get("/inventory")
    assert response.status_code == 200

def test_get_inventories_by_date():
    response = client.get("/inventory/filter?start_date=2004-10-31&end_date=2005-05-31")
    assert response.status_code == 200

def test_get_inventories_by_date_invalid_date_range():
    response = client.get("/inventory/filter?start_date=2004-10-31&end_date=1999-05-31")
    assert response.status_code == 404

