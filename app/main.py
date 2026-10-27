from fastapi import FastAPI
from datetime import datetime, timezone
from app.schemas.incident import IncidentCreate, IncidentResponse

app = FastAPI(
    title="OpsFlow Core API",
    description="Backend de gestion d'incidents IT et suivi des SLA",
    version="0.1.0",
)

@app.post("/incident", response_model=IncidentResponse, status_code=201)
def create_incident(payload: IncidentCreate):
    now = datetime.now(timezone.utc)
    new_incident = payload.model_dump()
    new_incident["id"] = 1
    new_incident["status"] = "OPEN"
    new_incident["created_at"] = now
    new_incident["sla_due_at"] = now  
    
    return new_incident

@app.get("/health", tags=["System"])
def health_check():
    return {
        "status": "ok",
        "project": "OpsFlow Core",
        "version": "0.1.0",
    }