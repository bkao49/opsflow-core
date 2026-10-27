from datetime import datetime, timedelta

def calculate_sla_deadline(severity: str, created_at: datetime) -> datetime:
    """
    Calcule la date limite de résolution (SLA) selon la gravité de l'incident.
    """
    match severity:
        case "P1": # Critique (Résolution en 4 heures)
            return created_at + timedelta(hours=4)
        case "P2": # Élevée (Résolution en 24 heures)
            return created_at + timedelta(hours=24)
        case "P3": # Moyenne (Résolution en 48 heures)
            return created_at + timedelta(hours=48)
        case _:    # P4 ou par défaut (Résolution en 7 jours)
            return created_at + timedelta(days=7)