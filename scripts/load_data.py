import sys
import sqlite3
from pathlib import Path

# Añadir la raíz del proyecto al path para poder importar src
sys.path.append(str(Path(__file__).resolve().parent.parent))
from src.data.loaders import load_prices, load_production, load_cushing

# Ruta a la base de datos
DB_PATH = Path(__file__).resolve().parent.parent / 'data' / 'oganalytics.db'

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

# --- Convertir fechas a fecha pura (sin la parte horaria 00:00:00) ---
prices['date'] = prices['date'].dt.date
production['date'] = production['date'].dt.date
inventories['date'] = inventories['date'].dt.date

# --- Volcar a la base de datos ---
conn = sqlite3.connect(DB_PATH)

# Vaciar las tablas antes de cargar (idempotencia)
cursor = conn.cursor()
cursor.execute("DELETE FROM prices")
cursor.execute("DELETE FROM production")
cursor.execute("DELETE FROM inventories")

prices.to_sql('prices', conn, if_exists='append', index=False)
production.to_sql('production', conn, if_exists='append', index=False)
inventories.to_sql('inventories', conn, if_exists='append', index=False)

conn.commit()
conn.close()

print("Datos cargados correctamente.")