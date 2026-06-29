from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_get_production():
       response = client.get("/production/")
       assert response.status_code == 200

def test_get_production_by_country():
       response = client.get("/production/Russia")
       assert response.status_code == 200
       data = response.json()
       assert len(data) > 0                                
       assert all(item["country"] == "Russia" for item in data)