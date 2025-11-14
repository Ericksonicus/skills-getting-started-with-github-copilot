import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

ACTIVITY = "Chess Club"
EMAIL = "testuser@mergington.edu"


def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert ACTIVITY in response.json()


def test_signup_and_unregister():
    # Ensure user is not signed up
    client.post(f"/activities/{ACTIVITY}/unregister", params={"email": EMAIL})

    # Sign up
    signup_resp = client.post(f"/activities/{ACTIVITY}/signup", params={"email": EMAIL})
    assert signup_resp.status_code == 200
    assert "Signed up" in signup_resp.json()["message"]

    # Duplicate signup should fail
    dup_resp = client.post(f"/activities/{ACTIVITY}/signup", params={"email": EMAIL})
    assert dup_resp.status_code == 400
    assert "already signed up" in dup_resp.json()["detail"]

    # Unregister
    unsign_resp = client.post(f"/activities/{ACTIVITY}/unregister", params={"email": EMAIL})
    assert unsign_resp.status_code == 200
    assert "Unregistered" in unsign_resp.json()["message"]

    # Unregister again should fail
    unsign_again = client.post(f"/activities/{ACTIVITY}/unregister", params={"email": EMAIL})
    assert unsign_again.status_code == 400
    assert "not registered" in unsign_again.json()["detail"]
