def test_get_inventories(client, sample_data):
    response = client.get("/inventory/")
    assert response.status_code == 200
    assert len(response.json()) == 2
 
 
def test_get_inventories_by_date(client, sample_data):
    response = client.get("/inventory/filter?start_date=2020-01-01&end_date=2020-01-31")
    assert response.status_code == 200
    assert len(response.json()) == 1
 
 
def test_get_inventories_by_date_invalid_range(client, sample_data):
    response = client.get("/inventory/filter?start_date=2020-10-31&end_date=1999-05-31")
    assert response.status_code == 404
