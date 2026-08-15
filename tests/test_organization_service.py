from uuid import UUID, uuid4

import pytest

from app.db.session import async_session_factory
from app.models.user import User
from app.services.organization import OrganizationService


async def create_test_user() -> UUID:
    async with async_session_factory() as session:
        user = User(
            id=uuid4(),
            email=f"organization-service-{uuid4()}@example.com",
            password_hash="test-password-hash",
        )

        session.add(user)
        await session.commit()

        return user.id


@pytest.mark.asyncio
async def test_create_organization() -> None:
    name = f"Service Create {uuid4()}"
    owner_user_id = await create_test_user()

    async with async_session_factory() as session:
        service = OrganizationService(session)

        organization = await service.create_organization(
            name,
            owner_user_id,
        )
        await session.commit()

    assert isinstance(organization.id, UUID)
    assert organization.name == name


@pytest.mark.asyncio
async def test_get_organization_by_id() -> None:
    name = f"Service ID Lookup {uuid4()}"
    owner_user_id = await create_test_user()

    async with async_session_factory() as session:
        service = OrganizationService(session)

        created_organization = await service.create_organization(
            name,
            owner_user_id,
        )
        await session.commit()

    async with async_session_factory() as session:
        service = OrganizationService(session)

        organization = await service.get_organization_by_id(
            created_organization.id,
        )

    assert organization is not None
    assert organization.id == created_organization.id
    assert organization.name == name


@pytest.mark.asyncio
async def test_get_organization_by_id_returns_none_for_unknown_organization() -> None:
    async with async_session_factory() as session:
        service = OrganizationService(session)

        organization = await service.get_organization_by_id(uuid4())

    assert organization is None


@pytest.mark.asyncio
async def test_get_organization_by_name() -> None:
    name = f"Service Name Lookup {uuid4()}"
    owner_user_id = await create_test_user()

    async with async_session_factory() as session:
        service = OrganizationService(session)

        created_organization = await service.create_organization(
            name,
            owner_user_id,
        )
        await session.commit()

    async with async_session_factory() as session:
        service = OrganizationService(session)

        organization = await service.get_organization_by_name(name)

    assert organization is not None
    assert organization.id == created_organization.id
    assert organization.name == name


@pytest.mark.asyncio
async def test_get_organization_by_name_returns_none_for_unknown_name() -> None:
    async with async_session_factory() as session:
        service = OrganizationService(session)

        organization = await service.get_organization_by_name(
            f"does-not-exist-{uuid4()}",
        )

    assert organization is None
