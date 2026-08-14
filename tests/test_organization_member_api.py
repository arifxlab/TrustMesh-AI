from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app


def test_create_organization_membership() -> None:
    with TestClient(app) as client:
        organization_response = client.post(
            "/api/v1/organizations",
            json={"name": f"API Membership Organization {uuid4()}"},
        )

        assert organization_response.status_code == 201

        organization_id = organization_response.json()["id"]

        user_email = f"api-membership-{uuid4()}@example.com"

        user_response = client.post(
            "/api/v1/users",
            json={"email": user_email},
        )

        assert user_response.status_code == 201

        user_id = user_response.json()["id"]

        response = client.post(
            f"/api/v1/organizations/{organization_id}/members",
            json={
                "user_id": user_id,
                "role": "admin",
            },
        )

    assert response.status_code == 201

    data = response.json()

    assert data["organization_id"] == organization_id
    assert data["user_id"] == user_id
    assert data["role"] == "admin"
    assert "id" in data
    assert "created_at" in data


def test_get_organization_membership() -> None:
    with TestClient(app) as client:
        organization_response = client.post(
            "/api/v1/organizations",
            json={"name": f"API Membership Lookup {uuid4()}"},
        )

        organization_id = organization_response.json()["id"]

        user_response = client.post(
            "/api/v1/users",
            json={"email": f"api-lookup-{uuid4()}@example.com"},
        )

        user_id = user_response.json()["id"]

        create_response = client.post(
            f"/api/v1/organizations/{organization_id}/members",
            json={"user_id": user_id},
        )

        assert create_response.status_code == 201

        response = client.get(
            f"/api/v1/organizations/{organization_id}/members/{user_id}",
        )

    assert response.status_code == 200

    data = response.json()

    assert data["organization_id"] == organization_id
    assert data["user_id"] == user_id
    assert data["role"] == "member"


def test_get_organization_membership_returns_404_when_missing() -> None:
    with TestClient(app) as client:
        response = client.get(
            f"/api/v1/organizations/{uuid4()}/members/{uuid4()}",
        )

    assert response.status_code == 404
    assert response.json() == {"detail": "Organization membership not found."}


def test_list_organization_memberships() -> None:
    with TestClient(app) as client:
        organization_response = client.post(
            "/api/v1/organizations",
            json={"name": f"API Membership List {uuid4()}"},
        )

        organization_id = organization_response.json()["id"]

        first_user_response = client.post(
            "/api/v1/users",
            json={"email": f"api-list-1-{uuid4()}@example.com"},
        )

        second_user_response = client.post(
            "/api/v1/users",
            json={"email": f"api-list-2-{uuid4()}@example.com"},
        )

        first_user_id = first_user_response.json()["id"]
        second_user_id = second_user_response.json()["id"]

        first_membership_response = client.post(
            f"/api/v1/organizations/{organization_id}/members",
            json={"user_id": first_user_id},
        )

        second_membership_response = client.post(
            f"/api/v1/organizations/{organization_id}/members",
            json={"user_id": second_user_id},
        )

        assert first_membership_response.status_code == 201
        assert second_membership_response.status_code == 201

        response = client.get(
            f"/api/v1/organizations/{organization_id}/members",
        )

    assert response.status_code == 200

    data = response.json()

    membership_user_ids = {membership["user_id"] for membership in data}

    assert first_user_id in membership_user_ids
    assert second_user_id in membership_user_ids
    assert len(data) == 2


def test_list_organization_memberships_returns_empty_list() -> None:
    with TestClient(app) as client:
        organization_response = client.post(
            "/api/v1/organizations",
            json={"name": f"API Empty Members {uuid4()}"},
        )

        organization_id = organization_response.json()["id"]

        response = client.get(
            f"/api/v1/organizations/{organization_id}/members",
        )

    assert response.status_code == 200
    assert response.json() == []


def test_create_duplicate_membership_returns_409() -> None:
    with TestClient(app) as client:
        organization_response = client.post(
            "/api/v1/organizations",
            json={"name": f"API Duplicate Membership {uuid4()}"},
        )

        organization_id = organization_response.json()["id"]

        user_response = client.post(
            "/api/v1/users",
            json={"email": f"api-duplicate-{uuid4()}@example.com"},
        )

        user_id = user_response.json()["id"]

        first_response = client.post(
            f"/api/v1/organizations/{organization_id}/members",
            json={"user_id": user_id},
        )

        assert first_response.status_code == 201

        second_response = client.post(
            f"/api/v1/organizations/{organization_id}/members",
            json={"user_id": user_id},
        )

    assert second_response.status_code == 409
    assert second_response.json() == {"detail": "User is already a member of this organization."}


def test_create_membership_rejects_empty_role() -> None:
    with TestClient(app) as client:
        organization_response = client.post(
            "/api/v1/organizations",
            json={"name": f"API Role Validation {uuid4()}"},
        )

        organization_id = organization_response.json()["id"]

        user_response = client.post(
            "/api/v1/users",
            json={"email": f"api-role-{uuid4()}@example.com"},
        )

        user_id = user_response.json()["id"]

        response = client.post(
            f"/api/v1/organizations/{organization_id}/members",
            json={
                "user_id": user_id,
                "role": "",
            },
        )

    assert response.status_code == 422
