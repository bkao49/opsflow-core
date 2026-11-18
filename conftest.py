import os
os.environ["DATA_BASE_URL"] = "sqlite://"   # avant tout import de "app"

from datetime import datetime, timezone

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db
from app.models.incident import Incident
from app.services.sla import calculate_sla_deadline

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



@pytest.fixture
def creer_incident(db_session):

    # 1. La fonction d'aide, avec des valeurs par défaut pratiques
    def _creer_incident(titre="Panne du Wi-Fi", severity="P1", is_deleted=False):
        maintenant = datetime.now(timezone.utc)
        incident = Incident(
            title=titre,
            description="Plus de connexion au 2e étage",
            severity=severity,
            status="OPEN",
            reporter_id="kohy",
            # sla_due_at est OBLIGATOIRE en base : c'est l'API qui le calcule
            # d'habitude, ici on le calcule nous-mêmes avec la même fonction
            sla_due_at=calculate_sla_deadline(severity, maintenant),
            is_deleted=is_deleted,
        )
        db_session.add(incident)
        db_session.commit()
        db_session.refresh(incident)   # recharge l'objet : on récupère l'id attribué par la base
        return incident

    # 2. On retourne LA FONCTION ELLE-MÊME (sans parenthèses)
    return _creer_incident