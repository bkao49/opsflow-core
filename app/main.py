from fastapi import FastAPI
from datetime import datetime, timezone
from app.schemas.incident import IncidentCreate, IncidentResponse
from app.models import incident, audit
from fastapi import FastAPI, Depends 
from sqlalchemy.orm import Session   
from app.database import engine, Base, SessionLocal
Base.metadata.create_all(bind=engine)
app = FastAPI(
    title="OpsFlow Core API",
    description="Backend de gestion d'incidents IT et suivi des SLA",
    version="0.1.0",
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/incidents", response_model=IncidentResponse, status_code=201, tags=["Incidents"])
def create_incident(payload: IncidentCreate, db: Session = Depends(get_db)):
    now = datetime.now(timezone.utc)
    
    new_db_incident = incident.Incident(
        title=payload.title,
        description=payload.description,
        severity=payload.severity,
        reporter_id=payload.reporter_id,
        status="OPEN",
        sla_due_at=now 
    )
    

    db.add(new_db_incident)
    
    db.commit()
    
    db.refresh(new_db_incident)
    
    return new_db_incident 

@app.get("/health", tags=["System"])
def health_check():
    return {
        "status": "ok",
        "project": "OpsFlow Core",
        "version": "0.1.0",
    }