from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app

PASSWORD = "CorrectHorseBatteryStaple123!"


def create_authenticated_client(client: TestClient) -> TestClient:
    email = f"organization-api-{uuid4()}@example.com"

    create_response = client.post(
        "/api/v1/users",
        json={
            "email": email,
            "password": PASSWORD,
        },
    )

    assert create_response.status_code == 201

    login_response = client.post(
        "/api/v1/auth/login",
        json={
            "email": email,
            "password": PASSWORD,
        },
    )

    assert login_response.status_code == 200

    access_token = login_response.json()["access_token"]

    client.headers.update(
        {"Authorization": f"Bearer {access_token}"},
    )

    return client


def test_create_organization() -> None:
    with TestClient(app) as client:
        create_authenticated_client(client)

        name = f"API Organization {uuid4()}"

        response = client.post(
            "/api/v1/organizations",
            json={"name": name},
        )

        assert response.status_code == 201

        data = response.json()

        assert data["name"] == name
        assert "id" in data
        assert "created_at" in data


def test_create_organization_requires_authentication() -> None:
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/organizations",
            json={"name": f"Unauthorized Organization {uuid4()}"},
        )

        assert response.status_code == 401


def test_get_organization() -> None:
    with TestClient(app) as client:
        create_authenticated_client(client)

        name = f"API Organization Lookup {uuid4()}"

        create_response = client.post(
            "/api/v1/organizations",
            json={"name": name},
        )

        assert create_response.status_code == 201

        organization_id = create_response.json()["id"]

        response = client.get(
            f"/api/v1/organizations/{organization_id}",
        )

        assert response.status_code == 200

        data = response.json()

        assert data["id"] == organization_id
        assert data["name"] == name


def test_get_organization_returns_404_for_unknown_id() -> None:
    with TestClient(app) as client:
        create_authenticated_client(client)

        response = client.get(
            f"/api/v1/organizations/{uuid4()}",
        )

        assert response.status_code == 404
        assert response.json() == {"detail": "Organization not found."}


def test_create_organization_rejects_empty_name() -> None:
    with TestClient(app) as client:
        create_authenticated_client(client)

        response = client.post(
            "/api/v1/organizations",
            json={"name": ""},
        )

        assert response.status_code == 422
