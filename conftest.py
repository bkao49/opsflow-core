import os

# DOIT rester avant tout import de "app" (voir plus haut)
os.environ["DATA_BASE_URL"] = "sqlite://"

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db   # get_db vient de app.database
# Configuration du moteur SQLite en mémoire RAM
engine_test = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
SessionTest = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)


# --- FIXTURE 1 : La base de données propre à chaque test ---
@pytest.fixture(scope="function")
def db_session():
    # 1. AVANT LE TEST : On crée toutes les tables à neuf
    Base.metadata.create_all(bind=engine_test)
    db = SessionTest()
    
    try:
        yield db  # On donne la session de test
    finally:
        # 2. APRÈS LE TEST : On ferme la session et on détruit toutes les tables
        db.close()
        Base.metadata.drop_all(bind=engine_test)


# --- FIXTURE 2 : Le TestClient branché sur la base de test ---
@pytest.fixture(scope="function")
def client(db_session): # <-- Elle réclame la fixture db_session juste au-dessus !
    
    # On crée notre faux videur qui renvoie la session de test
    def override_get_db():
        try:
            yield db_session
        finally:
            pass # La fermeture est déjà gérée par la fixture db_session

    # 1. AVANT LE TEST : On remplace la dépendance
    app.dependency_overrides[get_db] = override_get_db
    
    # 2. PENDANT LE TEST : On livre le TestClient prêt à l'emploi
    with TestClient(app) as c:
        yield c
        
    # 3. APRÈS LE TEST : On nettoie les overrides
    app.dependency_overrides.clear()