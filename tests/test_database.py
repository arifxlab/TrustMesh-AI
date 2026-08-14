from uuid import uuid4

import pytest

from app.db.session import async_session_factory
from app.models.user import User


@pytest.mark.asyncio
async def test_user_persistence() -> None:
    email = f"database-test-{uuid4()}@trustmesh.local"

    async with async_session_factory() as session:
        user = User(
            email=email,
            password_hash="test-password-hash",
        )

        session.add(user)
        await session.commit()
        await session.refresh(user)

        assert user.id is not None
        assert user.email == email
        assert user.password_hash == "test-password-hash"
        assert user.created_at is not None
