import pytest


DONNEES_VALIDES = {
    "title": "Panne du Wi-Fi",
    "description": "Plus de connexion au 2e étage",
    "severity": "P1",
    "reporter_id": "kohy",
}
def test_create_incident(client):
    reponse=client.post("/incidents/",json=DONNEES_VALIDES)

    assert reponse.status_code==201
    assert reponse.json()["title"] == "Panne du Wi-Fi"
def test_liste_vide(client):
    reponse = client.get("/incidents/")
    assert reponse.json() == []
def test_title_incident(client):
    donnees={**DONNEES_VALIDES, "title":"te"}
    
    reponse=client.post("/incidents/",json=donnees)
    assert reponse.status_code==422
def test_status_invalide(client,creer_incident):
    incident = creer_incident()                       
    reponse = client.patch(
        f"/incidents/{incident.id}",                  
        json={"status": "BANANE", "updated_by": "kohy"}, 
    )
    assert reponse.status_code == 422
    assert "status" in str(reponse.json())
def test_status_valide(client,creer_incident):
    incident = creer_incident()                       
    reponse = client.patch(
        f"/incidents/{incident.id}",                  
        json={"status": "IN_PROGRESS", "updated_by": "kohy"}, 
    )
    assert reponse.status_code == 200
    audit = client.get(f"/incidents/{incident.id}/audit").json()
    assert len(audit) == 1                      
    assert audit[0]["old_status"] == "OPEN"
    assert audit[0]["new_status"] == "IN_PROGRESS"
    assert audit[0]["changed_by"] == "kohy"
    
@pytest.mark.parametrize(
    "limit, code_attendu",
    [(0, 422), (101, 422), (100, 200)],
)
def test_limit_bornes(client, limit, code_attendu):
    reponse = client.get(f"/incidents/?limit={limit}")
    assert reponse.status_code == code_attendu

def test_get_incident_supprime(client, creer_incident):
    incident = creer_incident(is_deleted=True)
    reponse = client.get(f"/incidents/{incident.id}")
    assert reponse.status_code == 404
    assert "supprimé" in reponse.json()["detail"] 
def test_incident_inconnu(client):
    reponse = client.get("/incidents/9999")
    assert reponse.status_code == 404