import json
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    r = client.get("/healthz")
    assert r.status_code == 200
    assert "model" in r.json()

def test_analyze_positive():
    r = client.post("/analyze", json={"text": "Amazing quality, will buy again!"})
    assert r.status_code == 200
    body = r.json()
    assert body["label"] in ["Positive", "Neutral", "Negative"]
    assert len(body["scores"]) == 3

def test_batch():
    payload = {"items": [{"id":"1","text":"bad"}, {"id":"2","text":"great!"}]}
    r = client.post("/batch", json=payload)
    assert r.status_code == 200
    body = r.json()
    assert body["model"]
    assert len(body["results"]) == 2