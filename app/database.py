from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase


SQLALCHEMY_DATABASE_URL = "postgresql+psycopg://opsflow_user:supersecretpassword@localhost:5432/opsflow_db"


engine = create_engine(SQLALCHEMY_DATABASE_URL)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Nouvelle syntaxe SQLAlchemy 2.0
class Base(DeclarativeBase):
    pass