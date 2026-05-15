import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert "Hive Mind" in response.json()["message"]

def test_hive_mind_endpoint_schema():
    """
    Test that the endpoint accepts the correct GameState schema 
    and returns a valid structure, even with a fallback.
    """
    payload = {
        "gameState": "Chamber_02",
        "session_metadata": {
            "tick_id": 442,
            "last_tactic_success": False,
            "difficulty_scaling": 0.85
        },
        "player": {
            "pos": [12.4, 0.0, 5.2],
            "vel": [2.1, 0.0, -0.5],
            "active_element": "Sulfur",
            "health": 45,
            "is_firing": True
        },
        "mummies": [
            {"id": 1, "pos": [2.0, 0.0, 2.1], "hp": 50, "state": "Stunned"},
            {"id": 2, "pos": [5.5, 0.0, 8.3], "hp": 100, "state": "Chasing"}
        ]
    }
    
    response = client.post("/api/v1/hive-mind", json=payload)
    
    # Even if API key is missing, it should return 200 with fallback tactics
    assert response.status_code == 200
    data = response.json()
    assert "hive_tactic" in data
    assert "instructions" in data
    assert len(data["instructions"]) == 2
    assert "agentic_negotiation" in data
