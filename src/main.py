from pathlib import Path
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .db.connection import engine
from .routers import price
from . import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(price.router)