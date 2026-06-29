from typing import List
from .. import models, schemas
from fastapi import status, HTTPException, Depends, APIRouter
from ..db.connection import get_db
from sqlalchemy.orm import Session
from datetime import date

router = APIRouter(prefix="/price", tags=['Price'])

@router.get("/", response_model=List[schemas.PriceOut])
def get_prices(db: Session = Depends(get_db)):
    prices = db.query(models.Price).all()
    if not prices:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No data was found")
    
    return prices

@router.get("/spread", response_model=List[schemas.PriceSpreadOut])
def get_spread(db: Session = Depends(get_db)):
    spread = db.query(
        models.Price.date.label("date"),
        (models.Price.price_usd_brent - models.Price.price_usd_wti).label("spread")
    ).all()

    if not spread:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No data was found")
    
    return spread

@router.get("/spread/filter", response_model=List[schemas.PriceSpreadOut])
def get_spread_by_date(start_date: date | None = None, end_date: date | None = None, db: Session = Depends(get_db)):
    query = db.query(models.Price.date.label("date"),
        (models.Price.price_usd_brent - models.Price.price_usd_wti).label("spread"))
    
    if start_date is not None:
        query = query.filter(models.Price.date >= start_date)

    if end_date is not None:
        query = query.filter(models.Price.date <= end_date)

    spread = query.all()

    if not spread:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No data was found")
    
    return spread

@router.get("/latest", response_model=schemas.PriceOut)
def get_latest_price(db: Session = Depends(get_db)):
    latest = db.query(models.Price).order_by(models.Price.date.desc()).first()

    if not latest:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No data was found")
    
    return latest