from fastapi import status
from fastapi.testclient import TestClient


def test_liveness_check(client: TestClient):
    """Test the liveness check endpoint."""

    # When
    response = client.get("/health/live")

    # Then
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "OK"}


def test_readiness_check(client: TestClient):
    """Test the readiness check endpoint."""

    # When
    response = client.get("/health/ready")

    # Then
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "OK"}
