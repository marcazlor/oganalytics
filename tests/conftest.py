"""
Configuración común de los tests.

Los tests no usan la base de datos real: se sustituye la dependencia
get_db de FastAPI por una que apunta a una base SQLite de prueba, que
se crea vacía antes de cada test y se destruye al terminar. Así los
tests son reproducibles y no dependen del estado de la máquina ni de
que los datos estén cargados.
"""

from datetime import date

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.db.connection import Base, get_db
from src.main import app
from src.models import Price, Production, Inventory

SQLALCHEMY_TEST_URL = "sqlite:///./test.db"

engine_test = create_engine(
    SQLALCHEMY_TEST_URL,
    connect_args={"check_same_thread": False},
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)


def override_get_db():
    """Sustituye a get_db durante los tests. No es una fixture: FastAPI
    la llama directamente al resolver la dependencia."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def session():
    """Base de datos limpia para cada test."""
    Base.metadata.create_all(bind=engine_test)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine_test)


@pytest.fixture
def client(session):
    """Cliente HTTP contra la app, con las tablas ya creadas."""
    yield TestClient(app)


@pytest.fixture
def sample_data(session):
    """Datos mínimos y controlados para los tests que necesitan contenido.

    Los valores son inventados y redondos a propósito: permiten afirmar
    resultados exactos sin depender de los datos reales, que cambian
    cada vez que se recargan las fuentes.
    """
    prices = [
        Price(date=date(2020, 1, 31), price_usd_brent=100.0, price_usd_wti=98.0),
        Price(date=date(2020, 2, 29), price_usd_brent=102.0, price_usd_wti=99.0),
        Price(date=date(2020, 3, 31), price_usd_brent=105.0, price_usd_wti=100.0),
    ]
    production = [
        Production(date=date(2020, 1, 31), country="Russia", production_kbd=10000.0),
        Production(date=date(2020, 2, 29), country="Russia", production_kbd=10100.0),
        Production(date=date(2020, 1, 31), country="United States", production_kbd=13000.0),
    ]
    inventories = [
        Inventory(date=date(2020, 1, 31), location="Cushing", stocks_kb=40000.0),
        Inventory(date=date(2020, 2, 29), location="Cushing", stocks_kb=41000.0),
    ]

    session.add_all(prices + production + inventories)
    session.commit()

    yield