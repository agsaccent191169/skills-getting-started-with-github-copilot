import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Basketball" in data

def test_signup_for_activity():
    email = "testuser@mergington.edu"
    activity = "Basketball"
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert f"Signed up {email} for {activity}" in response.json()["message"]
    # Clean up: remove test user
    client.delete(f"/activities/{activity}/participants/{email}")

def test_remove_participant():
    email = "removeuser@mergington.edu"
    activity = "Tennis Club"
    # First, add the user
    client.post(f"/activities/{activity}/signup?email={email}")
    # Now, remove
    response = client.delete(f"/activities/{activity}/participants/{email}")
    assert response.status_code == 200
    assert f"Removed {email} from {activity}" in response.json()["message"]
    # Try removing again (should 404)
    response = client.delete(f"/activities/{activity}/participants/{email}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
