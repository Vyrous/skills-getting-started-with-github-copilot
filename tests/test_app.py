from fastapi.testclient import TestClient

from src import app as app_module


client = TestClient(app_module.app)


def test_unregister_participant_removes_email_from_activity():
    original_participants = app_module.activities["Chess Club"]["participants"].copy()

    try:
        response = client.delete(
            "/activities/Chess Club/unregister?email=michael@mergington.edu"
        )

        assert response.status_code == 200
        assert "michael@mergington.edu" not in app_module.activities["Chess Club"]["participants"]
        assert response.json()["message"] == "Removed michael@mergington.edu from Chess Club"
    finally:
        app_module.activities["Chess Club"]["participants"] = original_participants


def test_unregister_participant_returns_404_for_unknown_activity():
    response = client.delete("/activities/Unknown/unregister?email=test@example.com")

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
