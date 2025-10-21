from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)


def test_get_activities_contains_known_activity():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert "Chess Club" in data


def test_signup_and_unregister_flow():
    activity = "Chess Club"
    email = "pytest.user@mergington.edu"

    # Ensure not present
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    # Signup
    resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp.status_code == 200
    assert email in activities[activity]["participants"]

    # Duplicate signup should fail
    resp_dup = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp_dup.status_code == 400

    # Unregister
    resp_del = client.delete(f"/activities/{activity}/participants/{email}")
    assert resp_del.status_code == 200
    assert email not in activities[activity]["participants"]


def test_unregister_nonexistent_participant():
    activity = "Chess Club"
    email = "not.present@mergington.edu"

    # Ensure not present
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    resp = client.delete(f"/activities/{activity}/participants/{email}")
    assert resp.status_code == 404
