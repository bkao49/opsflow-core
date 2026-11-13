from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.database import get_db
from app.models.incident import Incident
from app.models.audit import IncidentAuditLog
from app.schemas.incident import IncidentCreate, IncidentResponse, IncidentUpdate, IncidentAuditLogResponse
from app.services.sla import calculate_sla_deadline


router= APIRouter(
    prefix="/incidents",
    tags=["Incidents"]
)

@router.post("/", response_model=IncidentResponse, status_code=201)
def create_incident(payload: IncidentCreate, db: Session= Depends(get_db)):
    now= datetime.now(timezone.utc)
    deadline= calculate_sla_deadline(payload.severity.value, now)
    new_db_incident = Incident(
        title=payload.title,
        description=payload.description,
        severity=payload.severity.value, 
        reporter_id=payload.reporter_id,
        status="OPEN",
        sla_due_at=deadline
    )
    db.add(new_db_incident)
    db.commit()
    db.refresh(new_db_incident)
    return new_db_incident

@router.get("/", response_model=list[IncidentResponse])
def get_all_incidents(status: str | None = None, db: Session = Depends(get_db), skip: int =0, limit: int = Query(default=10, ge=1, le=100, description="Éléments par page")):

    
    # 1. On prépare la requête de base (qui sélectionne tout)
    query = select(Incident)
    query = query.where(Incident.is_deleted == False)
    
    # 2. SI l'utilisateur a fourni un statut, on ajoute le filtre (le WHERE)
    if status:
        query = query.where(Incident.status == status)
        
    query = query.offset(skip).limit(limit)
    incidents = db.scalars(query).all()
    
    return incidents
@router.get("/{incident_id}", response_model=IncidentResponse)
def get_incident(incident_id: int, db:Session= Depends(get_db)):
    incident=db.get(Incident, incident_id)
    if not incident:
        raise HTTPException(status_code=404, detail="Incident non trouvé")
    if incident.is_deleted:
        raise HTTPException(status_code=404, detail="Incident supprimé")
    return incident
@router.patch("/{incident_id}", response_model=IncidentResponse)
def update_incident(incident_id: int, payload: IncidentUpdate, db: Session = Depends(get_db)):
    db_incident = db.get(Incident, incident_id)

    if not db_incident:
        raise HTTPException(status_code=404, detail="Incident non trouvé")
    if db_incident.is_deleted:
        raise HTTPException(status_code=404, detail="Incident supprimé")

    if payload.status is not None and payload.status != db_incident.status:
        
        # TODO 3 : Crée un objet IncidentAuditLog (L'archive). 
        # Remplis les champs : incident_id, old_status, new_status, changed_by
        audit_log = IncidentAuditLog(
            incident_id=db_incident.id,
            old_status= db_incident.status,
            new_status= payload.status,
            changed_by= payload.updated_by

        )
        
        # TODO 4 : Ajoute ce log à la session de la base de données
        db.add(audit_log)
        
        # TODO 5 : Mets à jour le statut de l'incident (db_incident) avec le nouveau statut (payload)
        db_incident.status = payload.status

    # On vérifie si l'utilisateur a demandé à changer l'assignation
    if payload.assigned_to is not None:
        
        # TODO 6 : Mets à jour la personne assignée
        db_incident.assigned_to = payload.assigned_to

    # TODO 7 : Valide la transaction (commit) pour enregistrer l'incident ET le log en même temps
    db.commit()
    
    # TODO 8 : Rafraîchis l'incident (refresh)
    db.refresh(db_incident)
    
    # TODO 9 : Retourne l'incident mis à jour
    return db_incident
@router.get("/{incident_id}/audit", response_model=list[IncidentAuditLogResponse])
def get_incident_audit_logs(incident_id: int, db: Session = Depends(get_db)):
    
    # 1. On cherche l'incident
    db_incident = db.get(Incident, incident_id)
    if not db_incident:
        raise HTTPException(status_code=404, detail="Incident non trouvé")
    if db_incident.is_deleted:
        raise HTTPException(status_code=404, detail="Incident supprimé")
    
    # 2. La magie de SQLAlchemy : on renvoie directement l'attribut "audit_logs"
    # SQLAlchemy va secrètement faire un "SELECT * FROM incident_audit_logs WHERE incident_id = ..."
    return db_incident.audit_logs

@router.delete("/{incident_id}", status_code=204)
def delete_incident(incident_id: int, db: Session = Depends(get_db)):
    db_incident = db.get(Incident, incident_id)
    if not db_incident:
        raise HTTPException(status_code=404, detail="Incident non trouvé")
    if db_incident.is_deleted:
        raise HTTPException(status_code=404, detail="Incident supprimé")
    db_incident.is_deleted=True
    db.commit()
    return None