import pytest
from app.services.sla import calculate_sla_deadline
from datetime import datetime, timedelta
now=datetime(2026,9,28,0,0)
@pytest.mark.parametrize("severity, resultat_attendu", [
    ("P1", now+timedelta(hours=4)),
    ("P2", now+timedelta(hours=24)),
    ("P3", now+timedelta(hours=48)),
    ("P4", now+timedelta(days=7))
])
def test_calculate_sla_deadline_depend_on_severity(severity:str, resultat_attendu: datetime):
    assert calculate_sla_deadline(severity,now)==resultat_attendu
