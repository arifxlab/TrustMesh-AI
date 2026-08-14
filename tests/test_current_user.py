from fastapi.testclient import TestClient

from app.main import app


def test_get_current_user_with_valid_token() -> None:
    email = "current-user@example.com"
    password = "CorrectHorseBatteryStaple123!"

    with TestClient(app) as client:
        create_response = client.post(
            "/api/v1/users",
            json={
                "email": email,
                "password": password,
            },
        )

        assert create_response.status_code in {201, 409}

        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": email,
                "password": password,
            },
        )

        assert login_response.status_code == 200

        access_token = login_response.json()["access_token"]

        response = client.get(
            "/api/v1/users/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 200

        data = response.json()

        assert data["email"] == email
        assert "id" in data
        assert "created_at" in data


def test_get_current_user_without_token_is_rejected() -> None:
    with TestClient(app) as client:
        response = client.get("/api/v1/users/me")

        assert response.status_code == 401


def test_get_current_user_with_invalid_token_is_rejected() -> None:
    with TestClient(app) as client:
        response = client.get(
            "/api/v1/users/me",
            headers={"Authorization": "Bearer invalid-token"},
        )

        assert response.status_code == 401
