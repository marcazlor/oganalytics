from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from ..config import settings

SQLALCHEMY_DATABASE_URL = settings.database_url

# check_same_thread es un parámetro exclusivo de SQLite (permite usar
# la conexión desde varios hilos, como hace FastAPI). PostgreSQL no lo
# reconoce y fallaría, así que solo se aplica cuando toca.
connect_args = (
    {"check_same_thread": False}
    if SQLALCHEMY_DATABASE_URL.startswith("sqlite")
    else {}
)

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args=connect_args)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()