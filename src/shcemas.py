from pydantic import BaseModel, ConfigDict
from datetime import date

class PriceOut(BaseModel):
    price_usd_brent : float
    price_usd_wti :float
    date : date

    model_config = ConfigDict(from_attributes=True)


