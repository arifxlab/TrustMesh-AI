from uuid import uuid4

import pytest
from sqlalchemy import select

from app.db.session import async_session_factory
from app.models.user import User


@pytest.mark.asyncio
async def test_user_persistence() -> None:
    email = f"database-test-{uuid4()}@trustmesh.local"

    async with async_session_factory() as session:
        user = User(email=email)

        session.add(user)
        await session.commit()
        await session.refresh(user)

        assert user.id is not None
        assert user.email == email
        assert user.created_at is not None

        result = await session.execute(select(User).where(User.id == user.id))
        persisted_user = result.scalar_one()

        assert persisted_user.id == user.id
        assert persisted_user.email == email
