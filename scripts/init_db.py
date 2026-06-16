import sqlite3
from pathlib import Path

# La raíz del proyecto: el script está en scripts/, subo un nivel
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_ROOT / 'data' / 'oganalytics.db'

conn = sqlite3.connect(DB_PATH)

cursor = conn.cursor()
cursor.executescript("""
    CREATE TABLE IF NOT EXISTS prices (
        date TEXT,
        price_usd_brent REAL,
        price_usd_wti REAL,
        PRIMARY KEY (date)
    );
    CREATE TABLE IF NOT EXISTS production (
        date TEXT,
        country TEXT,
        production_kbd REAL,
        PRIMARY KEY (date, country)
    );
    CREATE TABLE IF NOT EXISTS inventories (
        date TEXT,
        location TEXT,
        stocks_kb REAL,
        PRIMARY KEY (date, location)
    );
    """

)

conn.commit()
conn.close()