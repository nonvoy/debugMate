from fastapi import status
from fastapi.testclient import TestClient


def test_publish_event(client: TestClient):
    """Test the publishing of an event via the /events/ endpoint."""

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
    assert response.status_code == status.HTTP_202_ACCEPTED

    response_data = response.json()
    assert "id" in response_data
    assert response_data["service"] == event_data["service"]
    assert response_data["severity"] == event_data["severity"]
    assert response_data["message"] == event_data["message"]
    assert response_data["environment"] == event_data["environment"]
    assert response_data["event_type"] == event_data["event_type"]
    assert response_data["metadata"] == event_data["metadata"]
    assert response_data["timestamp"] == event_data["timestamp"]


def test_publish_events_in_batch(client: TestClient):
    """Test the publishing of multiple events via the /events/batch endpoint."""

    # Given
    events_data = [
        {
            "service": "auth-service",
            "severity": "error",
            "message": "User login failed due to invalid credentials",
            "environment": "production",
            "event_type": "authentication",
            "metadata": {"user_id": "12345"},
            "timestamp": "2024-06-01T12:00:00Z",
        },
        {
            "service": "payment-service",
            "severity": "warning",
            "message": "Payment processing delayed due to network issues",
            "environment": "staging",
            "event_type": "payment",
            "metadata": {"transaction_id": "abcde"},
            "timestamp": "2024-06-01T12:05:00Z",
        },
    ]

    # When
    response = client.post("/api/v1/events/batch", json=events_data)

    # Then
    assert response.status_code == status.HTTP_202_ACCEPTED

    response_data = response.json()
    assert isinstance(response_data, list)
    assert len(response_data) == len(events_data)

    for i, event in enumerate(events_data):
        assert "id" in response_data[i]
        assert response_data[i]["service"] == event["service"]
        assert response_data[i]["severity"] == event["severity"]
        assert response_data[i]["message"] == event["message"]
        assert response_data[i]["environment"] == event["environment"]
        assert response_data[i]["event_type"] == event["event_type"]
        assert response_data[i]["metadata"] == event["metadata"]
        assert response_data[i]["timestamp"] == event["timestamp"]
        assert "batch_id" in response_data[i]

    assert response_data[0]["batch_id"] == response_data[1]["batch_id"]
