from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app


def test_register_and_login() -> None:
    email = f"auth-{uuid4()}@example.com"
    password = "CorrectHorseBatteryStaple123!"

    with TestClient(app) as client:
        create_response = client.post(
            "/api/v1/users",
            json={
                "email": email,
                "password": password,
            },
        )

        assert create_response.status_code == 201

        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": email,
                "password": password,
            },
        )

        assert login_response.status_code == 200

        data = login_response.json()

        assert data["token_type"] == "bearer"
        assert isinstance(data["access_token"], str)
        assert len(data["access_token"]) > 0
