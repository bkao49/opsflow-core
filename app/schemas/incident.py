from enum import Enum
from enum import StrEnum
from datetime import datetime
from pydantic import BaseModel, Field


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


