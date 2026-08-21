import pandas as pd
from ..config import RAW_DIR

# loaders.py está en src/data/, subo 3 niveles hasta la raíz del proyecto

def load_file(filename, skip=0, names=None, sep=',', decimal='.'):
    res = pd.read_csv(RAW_DIR / filename, skiprows=skip, names=names, sep=sep, decimal=decimal)
    return res

def load_prices():
    # Cargar datos de brent
    brent = load_file('brent_daily.csv', 3, ['date', 'price_usd'], ';', ',')
    
    # Diccionario de meses para establecer la date
    meses_es_en = {
    'ene': 'jan', 'feb': 'feb', 'mar': 'mar', 'abr': 'apr',
    'may': 'may', 'jun': 'jun', 'jul': 'jul', 'ago': 'aug',
    'sep': 'sep', 'oct': 'oct', 'nov': 'nov', 'dic': 'dec'
    }

    for es, en in meses_es_en.items():
        brent['date'] = brent['date'].str.replace(es, en, case=False)

    # Limpieza básica
    brent['date'] = pd.to_datetime(brent['date'], format='%b %d, %Y')
    brent = brent.dropna()
    brent = brent.sort_values('date').reset_index(drop=True)

    # Cargar datos de WTI
    wti = load_file('wti_daily.csv', 3, ['date', 'price_usd'], ';', ',')
    for es, en in meses_es_en.items():
        wti['date'] = wti['date'].str.replace(es, en, case=False)

    # Limpieza básica
    wti['date'] = pd.to_datetime(wti['date'], format='%b %d, %Y')
    wti = wti.dropna()
    wti = wti.sort_values('date').reset_index(drop=True)

    prices_brent_wti = brent.merge(wti, on='date', suffixes=('_brent', '_wti'))
    prices_brent_wti['spread'] = prices_brent_wti['price_usd_brent'] - prices_brent_wti['price_usd_wti']

    # Hacemos resample a Month End y cogemos la media de los valores del mes
    prices_brent_wti_monthly = prices_brent_wti.resample('ME', on='date').mean().reset_index()
    
    # Añadimos columna 'period' para unificar la fecha con las otras bases de datos
    prices_brent_wti_monthly['period'] = prices_brent_wti_monthly['date'].dt.to_period('M')

    return prices_brent_wti_monthly

def load_production():
    production = load_file('INT-Export-06-02-2026_12-44-43.csv', 1)

    # Limpieza de filas y columnas innecesarias
    production = production.drop(0)
    production = production.drop('API', axis=1)
    production = production.rename(columns={'Unnamed: 1':'country'})

    # Melt para pasar de formato ancho a formato largo, con un pais y fecha por fila
    production_long = production.melt(id_vars='country',var_name='date_str', value_name='production_kbd')
    production_long['date_str'] = pd.to_datetime(production_long['date_str'], format='%b %Y')
    production_long['production_kbd'] = pd.to_numeric(production_long['production_kbd'], errors='coerce')

    # Añadimos columna 'period' para unificar la fecha con las otras bases de datos
    production_long['period'] = production_long['date_str'].dt.to_period('M')
    production_long['country'] = production_long['country'].str.strip()

    return production_long

def load_cushing():
    cushing_weekly = load_file('Weekly_Cushing_OK_Ending_Stocks_excluding_SPR_of_Crude_Oil.csv', 4)
    cushing_weekly = cushing_weekly.rename(columns={'Week of':'date', 'Weekly Cushing OK Ending Stocks excluding SPR of Crude Oil  Thousand Barrels':'cushing_stocks_kb'})
    cushing_weekly['date'] = pd.to_datetime(cushing_weekly['date'])
    
    # Hacemos resample a Month End y cogemos la media de los valores del mes
    cushing_monthly = cushing_weekly.resample('ME', on='date').mean().reset_index()
    
    # Añadimos columna 'period' para unificar la fecha con las otras bases de datos
    cushing_monthly['period'] = cushing_monthly['date'].dt.to_period('M')

    return cushing_monthly