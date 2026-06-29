from typing import List
from .. import models, schemas
from fastapi import status, HTTPException, Depends, APIRouter
from ..db.connection import get_db
from sqlalchemy.orm import Session
from datetime import date

router = APIRouter(prefix="/production", tags=['Production'])

@router.get("/", response_model=List[schemas.ProductionOut])
def get_production(db: Session = Depends(get_db)):
    prod = db.query(models.Production).all()
    if not prod:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No data was found")
    
    return prod

@router.get("/filter", response_model=List[schemas.ProductionOut])
def get_production_by_country_and_date(country: str | None = None, start_date: date| None = None, end_date: date | None = None, db: Session = Depends(get_db)):
    query = db.query(models.Production)

    if country is not None:
        query = query.filter(models.Production.country == country)

    if start_date is not None:
        query = query.filter(models.Production.date >= start_date)

    if end_date is not None:
        query = query.filter(models.Production.date <= end_date)

    prod = query.all()
    
    if not prod:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No data was found")
    
    return prod

@router.get("/{country}", response_model=List[schemas.ProductionOut])
def get_production_by_country(country: str, db: Session = Depends(get_db)):
    prod = db.query(models.Production).filter(models.Production.country == country).all()
    if not prod:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No data was found")
    
    return prod