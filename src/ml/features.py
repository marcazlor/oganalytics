"""
Construcción de features para la predicción del spread Brent-WTI.

Este módulo es la única fuente de verdad de la lógica de features:
lo usan tanto el notebook (para entrenar) como la API (para predecir).
Duplicar esta lógica provocaría training-serving skew.
"""

import pandas as pd

# Parámetros de las features
LAGS = (3, 6, 12)
VENTANAS = (3, 6, 12)
LAG_PRODUCCION = 3  # meses de retraso en la publicación de la EIA International

# Columnas que entran al modelo. Fuente de verdad compartida
# entre entrenamiento y predicción.
FEATURE_COLS = [
    'price_usd_brent',
    'price_usd_wti',
    'spread',
    'spread_lag_3',
    'spread_lag_6',
    'spread_lag_12',
    'spread_ma_3',
    'spread_ma_6',
    'spread_ma_12',
    'spread_std_3',
    'spread_std_6',
    'spread_std_12',
    'spread_dev_ma6',
    'production_kbd',
]

TARGET_COL = 'next_month_spread'


def build_features(prices_monthly, production, incluir_objetivo=True, dropna=True):
    """
    Construye el conjunto de features a partir de los precios mensuales
    y la producción de crudo de EE. UU.

    Parameters
    ----------
    prices_monthly : DataFrame
        Salida de load_prices(): date, price_usd_brent, price_usd_wti,
        spread, period.
    production : DataFrame
        Salida de load_production(), sin filtrar por país.
    incluir_objetivo : bool
        Si True, añade la columna next_month_spread (spread de t+1).
        Se usa en entrenamiento; en predicción no procede.
    dropna : bool
        Si True, elimina las filas incompletas. Poner a False al predecir,
        para conservar la última fila (que no tiene objetivo pero sí features).

    Returns
    -------
    DataFrame indexado por fecha, con las columnas de FEATURE_COLS
    (y el objetivo si se pidió).
    """
    df = prices_monthly.copy()

    # Objetivo: el spread del mes siguiente
    if incluir_objetivo:
        df[TARGET_COL] = df['spread'].shift(-1)

    # Lags del spread (miran al pasado)
    for lag in LAGS:
        df[f'spread_lag_{lag}'] = df['spread'].shift(lag)

    # Medias móviles y volatilidad. rolling() es trailing por defecto:
    # la ventana en t cubre t, t-1... t-N+1, todo información conocida en t.
    for ventana in VENTANAS:
        df[f'spread_ma_{ventana}'] = df['spread'].rolling(ventana).mean()
        df[f'spread_std_{ventana}'] = df['spread'].rolling(ventana).std()

    # Desviación respecto a la media móvil: codifica la reversión a la media
    df['spread_dev_ma6'] = df['spread'] - df['spread_ma_6']

    # Producción de EE. UU. con lag realista de publicación
    production_usa = production[production['country'] == 'United States']
    df = df.merge(production_usa, how='inner', on='period')
    df['production_kbd'] = df['production_kbd'].shift(LAG_PRODUCCION)

    # Limpieza y formato final
    df = df.drop(columns=['date_str'])
    if dropna:
        df = df.dropna()
    df = df.set_index('date')

    columnas = FEATURE_COLS + [TARGET_COL] if incluir_objetivo else FEATURE_COLS
    return df[columnas]