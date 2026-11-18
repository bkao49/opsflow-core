from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db

moteur_test = create_engine(
    "sqlite://", # 2 slashs = En mémoire (aucun fichier créé sur le PC)
    connect_args={"check_same_thread": False}, # Toujours requis par FastAPI + SQLite
    poolclass=StaticPool, # Force le maintien d'une seule connexion en vie
)
SessionTest = sessionmaker(bind=moteur_test)
Base.metadata.create_all(bind=moteur_test)
def override_get_db():
    db = SessionTest() 
    try:
        yield db       
    finally:
        db.close()    
app.dependency_overrides[get_db] = override_get_db


def test_health_check():
    client = TestClient(app)
    response = client.get("/health")
    
    assert response.status_code==200
