def test_get_latest_price(client, sample_data):
    response = client.get("/price/latest")
    assert response.status_code == 200
    data = response.json()
    # El más reciente de los datos de prueba es marzo de 2020
    assert data["price_usd_brent"] == 105.0


def test_get_prices(client, sample_data):
    response = client.get("/price/")
    assert response.status_code == 200
    assert len(response.json()) == 3


def test_get_prices_empty_database(client):
    """Sin sample_data la base está vacía: el endpoint debe devolver 404."""
    response = client.get("/price/")
    assert response.status_code == 404


def test_get_spread(client, sample_data):
    response = client.get("/price/spread")
    assert response.status_code == 200


def test_get_spread_content(client, sample_data):
    response = client.get("/price/spread")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    assert "spread" in data[0]
    # Primer registro: 100.0 - 98.0
    assert data[0]["spread"] == 2.0


def test_get_spread_by_date(client, sample_data):
    response = client.get("/price/spread/filter?start_date=2020-01-01&end_date=2020-02-29")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_spread_by_date_invalid_range(client, sample_data):
    """Rango sin datos: el endpoint devuelve 404."""
    response = client.get("/price/spread/filter?start_date=2050-01-01&end_date=2050-12-31")
    assert response.status_code == 404