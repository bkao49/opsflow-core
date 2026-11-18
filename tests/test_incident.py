def test_create_incident(client):
    donnees = {
        "title": "Panne du Wi-Fi",
        "description": "Plus de connexion au 2e étage",
        "severity": "P1",
        "reporter_id": "kohy",
    }
    reponse=client.post("/incidents/",json=donnees)

    assert reponse.status_code==200
    assert reponse.json()["title"] == "Panne du Wi-Fi"
def test_liste_vide(client):
    reponse = client.get("/incidents/")
    assert reponse.json() == []