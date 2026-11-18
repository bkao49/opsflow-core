from fastapi import FastAPI
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from app.schemas.incident import IncidentCreate, IncidentResponse
from app.models import incident, audit
from app.routers import incident as incident_router
from fastapi import FastAPI, Depends 
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware   
from app.database import engine, Base, SessionLocal
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1. AVANT LE YIELD : S'exécute une seule fois au démarrage du serveur
    print("Démarrage : Création des tables...")
    Base.metadata.create_all(bind=engine)
    
    yield  # --- L'APPLICATION TOURNE ET REÇOIT LES CLIENTS ICI ---
    
    # 2. APRÈS LE YIELD : S'exécute quand on éteint le serveur
    print("Arrêt du serveur : Nettoyage...")

# On branche le lifespan à l'application

app = FastAPI(
    lifespan=lifespan,
    title="OpsFlow Core API",
    description="Backend de gestion d'incidents IT et suivi des SLA",
    version="0.1.0",
)
# Configuration du CORS
app.add_middleware(
    CORSMiddleware,
    # Ici, on listera les adresses web autorisées (ex: "http://localhost:3000" pour React)
    # Pour le développement, on autorise tout avec "*"
    allow_origins=["*"], 
    allow_credentials=True,
    # On autorise toutes les méthodes (GET, POST, PATCH, DELETE)
    allow_methods=["*"],
    # On autorise tous les en-têtes (Headers, ex: les tokens de sécurité)
    allow_headers=["*"],
)

app.include_router(incident_router.router)

@app.get("/health", tags=["System"])
def health_check():
    return {
        "status": "ok",
        "project": "OpsFlow Core",
        "version": "0.1.0",
    }