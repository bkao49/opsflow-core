from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone
from app.database import Base


class IncidentAuditLog(Base):
    __tablename__ = "incident_audit_logs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    
    # La clé étrangère
    incident_id: Mapped[int] = mapped_column(ForeignKey("incidents.id"))
    
    old_status: Mapped[str] = mapped_column(String(20))
    new_status: Mapped[str] = mapped_column(String(20))
    
    changed_by: Mapped[str] = mapped_column(String(100))
    changed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    incident: Mapped["Incident"] = relationship(back_populates="audit_logs")