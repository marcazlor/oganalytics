def test_get_production(client, sample_data):
    response = client.get("/production/")
    assert response.status_code == 200
    assert len(response.json()) == 3


def test_get_production_by_country(client, sample_data):
    response = client.get("/production/Russia")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert all(item["country"] == "Russia" for item in data)


def test_get_production_country_not_found(client, sample_data):
    """Un país que no existe en los datos debe devolver 404."""
    response = client.get("/production/Atlantis")
    assert response.status_code == 404