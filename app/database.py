import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

load_dotenv()


SQLALCHEMY_DATABASE_URL = os.getenv("DATA_BASE_URL")
if not SQLALCHEMY_DATABASE_URL:
    raise RuntimeError("ERREUR CRITIQUE : La variable DATA_BASE_URL est introuvable dans le .env !")


engine = create_engine(SQLALCHEMY_DATABASE_URL)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

# Nouvelle place pour le gestionnaire de connexion
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()