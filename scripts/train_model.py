"""
Entrena el modelo final de predicción del spread Brent-WTI y lo serializa.

A diferencia de la validación (que entrena con el train de cada split),
aquí se entrena con toda la serie disponible: en producción interesa que
el modelo use toda la información hasta la fecha.

Uso:
    python scripts/train_model.py
"""

import sys
from pathlib import Path

import joblib
from sklearn.linear_model import Ridge
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

# Añadir la raíz del proyecto al path para poder importar src
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from src.data.loaders import load_prices, load_production
from src.ml.features import build_features, FEATURE_COLS, TARGET_COL

MODEL_PATH = PROJECT_ROOT / 'models' / 'ridge_spread.pkl'

# --- Datos y features ---
df = build_features(load_prices(), load_production())

X = df[FEATURE_COLS]
y = df[TARGET_COL]

# --- Entrenamiento ---
# Ridge va dentro de un Pipeline con StandardScaler: la penalización de
# Ridge depende de la escala de las features, y aquí conviven variables
# de magnitudes muy distintas (spread ~1, produccion ~10.000).
# Se serializa el Pipeline completo para que la API aplique el mismo
# escalado que se usó al entrenar.
# alpha=1: valores mayores no mejoraron el rendimiento de forma
# consistente en la validación con TimeSeriesSplit.
modelo = Pipeline([
    ('scaler', StandardScaler()),
    ('ridge', Ridge(alpha=1)),
])
modelo.fit(X, y)

# --- Serialización ---
MODEL_PATH.parent.mkdir(exist_ok=True)
joblib.dump(modelo, MODEL_PATH)

print(f"Modelo entrenado con {len(X)} observaciones y guardado en {MODEL_PATH}")