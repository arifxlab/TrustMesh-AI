from datetime import UTC, datetime
from uuid import uuid4

import pytest
from pydantic import ValidationError

from app.schemas.user import UserCreate, UserResponse


def test_user_create_accepts_valid_email() -> None:
    schema = UserCreate(email="user@example.com")

    assert schema.email == "user@example.com"


def test_user_create_rejects_invalid_email() -> None:
    with pytest.raises(ValidationError):
        UserCreate(email="not-an-email")


def test_user_response_from_attributes() -> None:
    user_id = uuid4()
    created_at = datetime.now(UTC)

    user_object = type(
        "UserObject",
        (),
        {
            "id": user_id,
            "email": "user@example.com",
            "created_at": created_at,
        },
    )()

    response = UserResponse.model_validate(user_object)

    assert response.id == user_id
    assert response.email == "user@example.com"
    assert response.created_at == created_at
