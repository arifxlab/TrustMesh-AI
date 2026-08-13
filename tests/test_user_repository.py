from uuid import uuid4

import pytest

from app.db.session import async_session_factory
from app.repositories.user import UserRepository


@pytest.mark.asyncio
async def test_create_and_get_user() -> None:
    email = f"repository-test-{uuid4()}@trustmesh.local"

    async with async_session_factory() as session:
        repository = UserRepository(session)

        user = await repository.create(email)

        assert user.id is not None
        assert user.email == email
        assert user.created_at is not None

        await session.commit()

        persisted_user = await repository.get_by_id(user.id)

        assert persisted_user is not None
        assert persisted_user.id == user.id
        assert persisted_user.email == email


@pytest.mark.asyncio
async def test_get_user_by_email() -> None:
    email = f"email-test-{uuid4()}@trustmesh.local"

    async with async_session_factory() as session:
        repository = UserRepository(session)

        user = await repository.create(email)
        await session.commit()

        persisted_user = await repository.get_by_email(email)

        assert persisted_user is not None
        assert persisted_user.id == user.id
        assert persisted_user.email == email
