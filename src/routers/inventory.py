from typing import List
from .. import models, schemas
from fastapi import status, HTTPException, Depends, APIRouter
from ..db.connection import get_db
from sqlalchemy.orm import Session
from datetime import date

router = APIRouter(prefix="/inventory", tags=['Inventory'])

@router.get("/", response_model=List[schemas.InventoryOut])
def get_inventories(db: Session = Depends(get_db)):
    inventory = db.query(models.Inventory).all()
    if not inventory:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No data was found")
    
    return inventory

@router.get("/filter", response_model=List[schemas.InventoryOut])
def get_inventories_by_date(start_date: date | None = None, end_date: date | None = None, db: Session = Depends(get_db)):
    query = db.query(models.Inventory)

    if start_date is not None:
        query = query.filter(models.Inventory.date >= start_date)
    
    if end_date is not None:
        query = query.filter(models.Inventory.date <= end_date)

    inventory = query.all()

    if not inventory:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No data was found")
    
    return inventory
