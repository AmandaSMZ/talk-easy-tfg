from fastapi.testclient import TestClient
from main import app 

client = TestClient(app)

def test_tag_message_ok():
    data = {
        "text": "El servidor necesita soporte urgente.",
        "labels": ["soporte", "urgente", "infraestructura", "recordatorio"]
    }
    response = client.post("/tag-message", json=data)
    print(response.json())  
    assert response.status_code == 200
    assert "predicted_labels" in response.json()
    assert "probabilities" in response.json()
    assert len(response.json()["probabilities"]) == 4

def test_tag_message_empty_text():
    data = {
        "text": "",
        "labels": ["soporte", "urgente"]
    }
    response = client.post("/tag-message", json=data)
    assert response.status_code == 422
    assert "text" in response.json()["detail"].lower() or "vacío" in response.json()["detail"].lower()

def test_tag_message_empty_labels():
    data = {
        "text": "Un mensaje cualquiera.",
        "labels": []
    }
    response = client.post("/tag-message", json=data)
    assert response.status_code == 422
    assert "labels" in response.json()["detail"].lower()
    
def test_tag_message_no_relevant_labels():
    data = {
        "text": "Esto es irrelevante para los labels posibles.",
        "labels": ["a", "b", "c"]
    }
    response = client.post("/tag-message", json=data)
    # Puede devolver 200 con detail, según cómo gestiones el 'no labels'
    # O puede devolver predicted_labels vacío y probabilities llenas
    # Ajusta según tu lógica, aquí se ilustra una comprobación genérica:
    assert response.status_code in [200, 422, 404, 204]