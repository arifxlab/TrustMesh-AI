from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app


PASSWORD = "CorrectHorseBatteryStaple123!"


def test_create_user() -> None:
    with TestClient(app) as client:
        email = f"api-create-{uuid4()}@example.com"

        response = client.post(
            "/api/v1/users",
            json={
                "email": email,
                "password": PASSWORD,
            },
        )

    assert response.status_code == 201

    data = response.json()

    assert data["email"] == email
    assert "id" in data
    assert "created_at" in data
    assert "password" not in data
    assert "password_hash" not in data


def test_create_duplicate_user_returns_409() -> None:
    with TestClient(app) as client:
        email = f"api-duplicate-{uuid4()}@example.com"

        first_response = client.post(
            "/api/v1/users",
            json={
                "email": email,
                "password": PASSWORD,
            },
        )

        assert first_response.status_code == 201

        second_response = client.post(
            "/api/v1/users",
            json={
                "email": email,
                "password": PASSWORD,
            },
        )

    assert second_response.status_code == 409
    assert second_response.json() == {
        "detail": "A user with this email already exists.",
    }


def test_create_user_rejects_invalid_email() -> None:
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/users",
            json={
                "email": "not-an-email",
                "password": PASSWORD,
            },
        )

    assert response.status_code == 422


def test_create_user_rejects_short_password() -> None:
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/users",
            json={
                "email": f"api-short-password-{uuid4()}@example.com",
                "password": "short",
            },
        )

    assert response.status_code == 422


def test_create_user_rejects_password_over_maximum_length() -> None:
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/users",
            json={
                "email": f"api-long-password-{uuid4()}@example.com",
                "password": "A" * 129,
            },
        )

    assert response.status_code == 422


def test_get_user() -> None:
    with TestClient(app) as client:
        email = f"api-get-{uuid4()}@example.com"

        create_response = client.post(
            "/api/v1/users",
            json={
                "email": email,
                "password": PASSWORD,
            },
        )

        assert create_response.status_code == 201

        user_id = create_response.json()["id"]

        response = client.get(
            f"/api/v1/users/{user_id}",
        )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == user_id
    assert data["email"] == email
    assert "password" not in data
    assert "password_hash" not in data


def test_get_user_returns_404_for_unknown_id() -> None:
    with TestClient(app) as client:
        response = client.get(
            f"/api/v1/users/{uuid4()}",
        )

    assert response.status_code == 404
    assert response.json() == {"detail": "User not found."}


def test_get_user_by_email() -> None:
    with TestClient(app) as client:
        email = f"api-by-email-{uuid4()}@example.com"

        create_response = client.post(
            "/api/v1/users",
            json={
                "email": email,
                "password": PASSWORD,
            },
        )

        assert create_response.status_code == 201

        response = client.get(
            f"/api/v1/users/by-email/{email}",
        )

    assert response.status_code == 200

    data = response.json()

    assert data["email"] == email
    assert "id" in data
    assert "created_at" in data
    assert "password" not in data
    assert "password_hash" not in data


def test_get_user_by_email_returns_404_for_unknown_email() -> None:
    with TestClient(app) as client:
        email = f"does-not-exist-{uuid4()}@example.com"

        response = client.get(
            f"/api/v1/users/by-email/{email}",
        )

    assert response.status_code == 404
    assert response.json() == {"detail": "User not found."}
