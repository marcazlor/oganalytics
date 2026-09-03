from pathlib import Path

import joblib
import pandas as pd
from fastapi import APIRouter, HTTPException, status

from .. import schemas
from ..data.loaders import load_prices, load_production
from ..ml.features import build_features, FEATURE_COLS
from ..config import MODEL_PATH

router = APIRouter(prefix="/predictions", tags=['Predictions'])

# El modelo se carga una sola vez al importar el módulo, no en cada
# petición: no cambia entre llamadas y leer el .pkl del disco cada vez
# sería innecesario.
try:
    modelo = joblib.load(MODEL_PATH)
except FileNotFoundError:
    modelo = None

@router.get("/spread", response_model=schemas.PredictionsOut)
def get_spread_prediction():
    """
    Predice el spread Brent-WTI del mes siguiente al último con datos
    completos de todas las features.

    Se devuelve también la predicción del baseline naive (persistencia
    del valor actual), que en la validación con TimeSeriesSplit resultó
    tan preciso como el modelo. La fecha objetivo puede ir por detrás
    del mes actual por el retraso de publicación de la producción de
    la EIA.
    """

    if modelo is None:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='modelo no disponible; ejecute scripts/train_model.py')
    # dropna=False conserva la última fila, que es justo sobre la que
    # queremos predecir (no tiene objetivo, pero sí todas las features).
    df = build_features(
        load_prices(),
        load_production(),
        incluir_objetivo=False,
        dropna=False,
    )
    df = df.dropna(subset=FEATURE_COLS)

    if df.empty:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No hay datos suficientes para generar una predicción",
        )

    ultima = df.tail(1)
    ultimo_mes = ultima.index[0]

    return {
        'predicted_date': (ultimo_mes + pd.DateOffset(months=1)).date(),
        'model_prediction': float(modelo.predict(ultima[FEATURE_COLS])[0]),
        'baseline_prediction': float(ultima['spread'].iloc[0]),
        'last_complete_month': ultimo_mes.date(),
    }