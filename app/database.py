from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase


SQLALCHEMY_DATABASE_URL = "postgresql+psycopg://opsflow_user:supersecretpassword@localhost:5432/opsflow_db"


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