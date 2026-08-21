"""
Carga los datos de los CSV en la base de datos.

Usa el engine de SQLAlchemy en lugar de sqlite3 directamente, para que
el script funcione con cualquier motor (SQLite en local, PostgreSQL en
Docker) sin cambios: la URL la decide la variable de entorno.

El script es idempotente: vacía las tablas antes de cargarlas, así que
puede ejecutarse las veces que haga falta sin duplicar datos.

Uso:
    python scripts/load_data.py
"""

import sys
from pathlib import Path

from sqlalchemy import text

# Añadir la raíz del proyecto al path para poder importar src
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from src.data.loaders import load_prices, load_production, load_cushing
from src.db.connection import engine

# --- Cargar los DataFrames ---
prices = load_prices()
production = load_production()
inventories = load_cushing()

# --- Ajustar cada DataFrame a la estructura de su tabla ---
prices = prices[['date', 'price_usd_brent', 'price_usd_wti']]

production = production.rename(columns={'date_str': 'date'})
production = production[['date', 'country', 'production_kbd']]

inventories = inventories.rename(columns={'cushing_stocks_kb': 'stocks_kb'})
inventories['location'] = 'Cushing'
inventories = inventories[['date', 'location', 'stocks_kb']]

# --- Convertir fechas a fecha pura (sin la parte horaria) ---
prices['date'] = prices['date'].dt.date
production['date'] = production['date'].dt.date
inventories['date'] = inventories['date'].dt.date

# --- Volcar a la base de datos ---
with engine.begin() as conn:
    # Vaciar las tablas antes de cargar (idempotencia)
    conn.execute(text("DELETE FROM prices"))
    conn.execute(text("DELETE FROM production"))
    conn.execute(text("DELETE FROM inventories"))

    prices.to_sql('prices', conn, if_exists='append', index=False)
    production.to_sql('production', conn, if_exists='append', index=False)
    inventories.to_sql('inventories', conn, if_exists='append', index=False)

print("Datos cargados correctamente.")