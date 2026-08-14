from uuid import uuid4

import pytest

from app.db.session import async_session_factory
from app.repositories.organization import OrganizationRepository
from app.repositories.organization_member import OrganizationMemberRepository
from app.repositories.user import UserRepository


@pytest.mark.asyncio
async def test_create_and_get_membership() -> None:
    organization_name = f"Membership Organization {uuid4()}"
    email = f"membership-{uuid4()}@trustmesh.local"

    async with async_session_factory() as session:
        organization_repository = OrganizationRepository(session)
        user_repository = UserRepository(session)
        membership_repository = OrganizationMemberRepository(session)

        organization = await organization_repository.create(organization_name)
        user = await user_repository.create(email)

        membership = await membership_repository.create(
            organization.id,
            user.id,
        )

        await session.commit()

        membership_id = membership.id

    async with async_session_factory() as session:
        membership_repository = OrganizationMemberRepository(session)

        found = await membership_repository.get_by_id(membership_id)

    assert found is not None
    assert found.id == membership_id
    assert found.role == "member"


@pytest.mark.asyncio
async def test_get_membership_by_organization_and_user() -> None:
    organization_name = f"Membership Lookup {uuid4()}"
    email = f"membership-lookup-{uuid4()}@trustmesh.local"

    async with async_session_factory() as session:
        organization_repository = OrganizationRepository(session)
        user_repository = UserRepository(session)
        membership_repository = OrganizationMemberRepository(session)

        organization = await organization_repository.create(organization_name)
        user = await user_repository.create(email)

        membership = await membership_repository.create(
            organization.id,
            user.id,
            role="admin",
        )

        await session.commit()

        membership_id = membership.id

    async with async_session_factory() as session:
        membership_repository = OrganizationMemberRepository(session)

        found = await membership_repository.get_by_organization_and_user(
            organization.id,
            user.id,
        )

    assert found is not None
    assert found.id == membership_id
    assert found.organization_id == organization.id
    assert found.user_id == user.id
    assert found.role == "admin"


@pytest.mark.asyncio
async def test_get_membership_by_id_returns_none_for_unknown_id() -> None:
    async with async_session_factory() as session:
        repository = OrganizationMemberRepository(session)

        membership = await repository.get_by_id(uuid4())

    assert membership is None


@pytest.mark.asyncio
async def test_get_membership_by_organization_and_user_returns_none_when_missing() -> None:
    async with async_session_factory() as session:
        repository = OrganizationMemberRepository(session)

        membership = await repository.get_by_organization_and_user(
            uuid4(),
            uuid4(),
        )

    assert membership is None


@pytest.mark.asyncio
async def test_list_memberships_by_organization() -> None:
    organization_name = f"Membership List {uuid4()}"
    first_email = f"membership-first-{uuid4()}@trustmesh.local"
    second_email = f"membership-second-{uuid4()}@trustmesh.local"

    async with async_session_factory() as session:
        organization_repository = OrganizationRepository(session)
        user_repository = UserRepository(session)
        membership_repository = OrganizationMemberRepository(session)

        organization = await organization_repository.create(organization_name)
        first_user = await user_repository.create(first_email)
        second_user = await user_repository.create(second_email)

        first_membership = await membership_repository.create(
            organization.id,
            first_user.id,
        )
        second_membership = await membership_repository.create(
            organization.id,
            second_user.id,
            role="admin",
        )

        await session.commit()

        first_membership_id = first_membership.id
        second_membership_id = second_membership.id

    async with async_session_factory() as session:
        membership_repository = OrganizationMemberRepository(session)

        memberships = await membership_repository.list_by_organization(
            organization.id,
        )

    membership_ids = [membership.id for membership in memberships]

    assert first_membership_id in membership_ids
    assert second_membership_id in membership_ids
    assert len(memberships) == 2


@pytest.mark.asyncio
async def test_list_memberships_by_organization_returns_empty_list() -> None:
    async with async_session_factory() as session:
        repository = OrganizationMemberRepository(session)

        memberships = await repository.list_by_organization(uuid4())

    assert memberships == []
