from fastapi import FastAPI
from .db.connection import engine
from .routers import price, production, inventory
from . import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(price.router)
app.include_router(production.router)
app.include_router(inventory.router)