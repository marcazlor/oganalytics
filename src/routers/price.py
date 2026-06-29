from .. import models, shcemas
from fastapi import status, HTTPException, Depends, APIRouter
from ..db.connection import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/price", tags=['Price'])

@router.get("/", response_model=shcemas.PriceOut)
def get_prices(db: Session = Depends(get_db)):
    prices = db.query(models.Price).all()
    if not prices:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No data was found")
    
    return prices