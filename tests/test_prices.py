from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_get_latest_price():
       response = client.get("/price/latest")
       assert response.status_code == 200