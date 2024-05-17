from fastapi.testclient import TestClient
from pythonpoetry.main import app
from pythonpoetry.com.github.dheerajhegde.api import build_pipeline

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_chat():
    response = client.get("/chat", params={"query": "test query"})
    assert response.status_code == 200
    assert "response" in response.json()
    assert "df" in response.json()