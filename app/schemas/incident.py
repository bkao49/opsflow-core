from enum import Enum
from enum import StrEnum
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional


class IncidentSeverity(StrEnum):
    CRITIQUE="P1"
    MAJEUR="P2"
    MINEUR="P3"


class IncidentStatus(StrEnum):
    OPEN="OPEN"
    IN_PROGRESS="IN_PROGRESS"
    RESOLVED="RESOLVED"
    CLOSED="CLOSED"

class IncidentCreate(BaseModel):
    title:str  = Field(...,min_length=5, max_length=150)
    description: str = Field(...,min_length=10)
    severity: IncidentSeverity
    reporter_id: str = Field (...,min_length=1)

class IncidentResponse(IncidentCreate):
    id: int
    status: IncidentStatus
    assigned_to: str | None = None
    created_at: datetime
    sla_due_at: datetime

class IncidentUpdate(BaseModel):
    # Tout est optionnel (Optional) car le technicien peut vouloir 
    # modifier seulement le statut, ou seulement l'assignation.
    status: Optional[str] = None
    assigned_to: Optional[str] = None
    
    # Pour simuler qui fait l'action (en vrai, ça viendrait du token de connexion)
    updated_by: str 

    model_config = {
        "json_schema_extra": {
            "example": {
                "status": "IN_PROGRESS",
                "assigned_to": "tech_bob",
                "updated_by": "tech_bob"
            }
        }
    }
class IncidentAuditLogResponse(BaseModel):
    id: int
    incident_id: int
    old_status: str
    new_status: str
    changed_by: str
    changed_at: datetime

    model_config = {
        # Cette ligne est cruciale : elle permet à Pydantic de lire un objet SQLAlchemy !
        "from_attributes": True
    }