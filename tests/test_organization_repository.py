from uuid import UUID

import pytest

from app.db.session import async_session_factory
from app.repositories.organization import OrganizationRepository


@pytest.mark.asyncio
async def test_create_and_get_organization() -> None:
    name = "Repository Test Organization"

    async with async_session_factory() as session:
        repository = OrganizationRepository(session)

        organization = await repository.create(name)
        await session.commit()

        organization_id = organization.id

    assert isinstance(organization_id, UUID)
    assert organization.name == name

    async with async_session_factory() as session:
        repository = OrganizationRepository(session)

        persisted = await repository.get_by_id(organization_id)

    assert persisted is not None
    assert persisted.id == organization_id
    assert persisted.name == name


@pytest.mark.asyncio
async def test_get_organization_by_name() -> None:
    name = "Repository Name Lookup"

    async with async_session_factory() as session:
        repository = OrganizationRepository(session)

        created = await repository.create(name)
        await session.commit()

        organization_id = created.id

    async with async_session_factory() as session:
        repository = OrganizationRepository(session)

        organization = await repository.get_by_name(name)

    assert organization is not None
    assert organization.id == organization_id
    assert organization.name == name


@pytest.mark.asyncio
async def test_get_organization_by_id_returns_none_for_unknown_id() -> None:
    unknown_id = UUID("00000000-0000-0000-0000-000000000000")

    async with async_session_factory() as session:
        repository = OrganizationRepository(session)

        organization = await repository.get_by_id(unknown_id)

    assert organization is None


@pytest.mark.asyncio
async def test_get_organization_by_name_returns_none_for_unknown_name() -> None:
    async with async_session_factory() as session:
        repository = OrganizationRepository(session)

        organization = await repository.get_by_name(
            "does-not-exist-organization",
        )

    assert organization is None


@pytest.mark.asyncio
async def test_organization_name_is_not_required_to_be_unique() -> None:
    name = "Duplicate Organization Name"

    async with async_session_factory() as session:
        repository = OrganizationRepository(session)

        first = await repository.create(name)
        second = await repository.create(name)
        await session.commit()

    assert first.id != second.id
    assert first.name == second.name
