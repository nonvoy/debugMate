from fastapi import status
from fastapi.testclient import TestClient


def test_create_event(client: TestClient):
    """Test the creation of an event via the /events/ endpoint."""

    # Given
    event_data = {
        "service": "auth-service",
        "severity": "error",
        "message": "User login failed due to invalid credentials",
        "environment": "production",
        "event_type": "authentication",
        "metadata": {"user_id": "12345"},
        "timestamp": "2024-06-01T12:00:00Z",
    }

    # When
    response = client.post("/api/v1/events/", json=event_data)

    # Then
    assert response.status_code == status.HTTP_201_CREATED

    response_data = response.json()
    assert "id" in response_data
    assert response_data["service"] == event_data["service"]
    assert response_data["severity"] == event_data["severity"]
    assert response_data["message"] == event_data["message"]
    assert response_data["environment"] == event_data["environment"]
    assert response_data["event_type"] == event_data["event_type"]
    assert response_data["metadata"] == event_data["metadata"]
    assert response_data["timestamp"] == event_data["timestamp"]
