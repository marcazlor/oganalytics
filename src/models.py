from .db.connection import Base
from sqlalchemy import Column, Numeric, String, Boolean, Date, text

class Price(Base):
    __tablename__ = "prices"

    price_usd_brent = Column(Numeric)
    price_usd_wti = Column(Numeric)
    date = Column(Date, nullable=False, primary_key=True)

class Production(Base):
    __tablename__ = "production"

    date = Column(Date, nullable=False, primary_key=True)
    country = Column(String, nullable=False, primary_key=True)
    production_kbd = Column(Numeric)

class Inventory(Base):
    __tablename__ = "inventories"

    date = Column(Date, nullable=False, primary_key=True)
    location = Column(String, nullable=False, primary_key=True)
    stocks_kb = Column(Numeric)
