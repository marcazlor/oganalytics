Tabla 1: prices
    - date (DATE)
    - price_usd_brent (NUMERIC)
    - price_usd_wti (NUMERIC)
    
    Clave primaria: date
    El spread no se almacena; se calcula como diferencia en consulta para evitar redundancia

Tabla 2: production
    - date (DATE)
    - country (VARCHAR)
    - production_kbd (NUMERIC)

    Clave primaria: (date, country)

Tabla 3: inventories
    - date (DATE)
    - location (VARCHAR)
    - stocks_kb (NUMERIC)

    Clave primaria: (date, location)