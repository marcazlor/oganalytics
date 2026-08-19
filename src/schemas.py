from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import date

class PriceOut(BaseModel):
    price_usd_brent : float
    price_usd_wti : float
    date : date

    model_config = ConfigDict(from_attributes=True)


class PriceSpreadOut(BaseModel):
    spread : float
    date : date

    model_config = ConfigDict(from_attributes=True)
    

class ProductionOut(BaseModel):
    date : date
    country : str
    production_kbd : Optional[float]

    model_config = ConfigDict(from_attributes=True)

class InventoryOut(BaseModel):
    date : date
    location : str
    stocks_kb : float
    
    model_config = ConfigDict(from_attributes=True)

class PredictionsOut(BaseModel):
    predicted_date : date
    model_prediction: float
    baseline_prediction: float
    last_complete_month: date

    model_config = ConfigDict(from_attributes=True)