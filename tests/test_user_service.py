from uuid import UUID, uuid4

import pytest

from app.db.session import async_session_factory
from app.security import password_security
from app.services.user import UserService

PASSWORD = "CorrectHorseBatteryStaple123!"


@pytest.mark.asyncio
async def test_create_user() -> None:
    email = f"service-create-{uuid4()}@trustmesh.local"

    async with async_session_factory() as session:
        service = UserService(session)

        user = await service.create_user(email, PASSWORD)
        await session.commit()

    assert isinstance(user.id, UUID)
    assert user.email == email
    assert user.password_hash != PASSWORD
    assert user.password_hash.startswith("$argon2")
    assert password_security.verify_password(PASSWORD, user.password_hash)


@pytest.mark.asyncio
async def test_get_user_by_email() -> None:
    email = f"service-email-{uuid4()}@trustmesh.local"

    async with async_session_factory() as session:
        service = UserService(session)

        created_user = await service.create_user(email, PASSWORD)
        await session.commit()

    async with async_session_factory() as session:
        service = UserService(session)

        user = await service.get_user_by_email(email)

    assert user is not None
    assert user.id == created_user.id
    assert user.email == email
    assert user.password_hash == created_user.password_hash


@pytest.mark.asyncio
async def test_get_user_by_id() -> None:
    email = f"service-id-{uuid4()}@trustmesh.local"

    async with async_session_factory() as session:
        service = UserService(session)

        created_user = await service.create_user(email, PASSWORD)
        await session.commit()

    async with async_session_factory() as session:
        service = UserService(session)

        user = await service.get_user_by_id(created_user.id)

    assert user is not None
    assert user.id == created_user.id
    assert user.email == email


@pytest.mark.asyncio
async def test_get_user_by_id_returns_none_for_unknown_user() -> None:
    async with async_session_factory() as session:
        service = UserService(session)

        user = await service.get_user_by_id(
            UUID("00000000-0000-0000-0000-000000000000"),
        )

    assert user is None


@pytest.mark.asyncio
async def test_get_user_by_email_returns_none_for_unknown_email() -> None:
    async with async_session_factory() as session:
        service = UserService(session)

        user = await service.get_user_by_email(
            f"does-not-exist-{uuid4()}@trustmesh.local",
        )

    assert user is None
