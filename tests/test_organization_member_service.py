from uuid import uuid4

import pytest

from app.db.session import async_session_factory
from app.services.organization import OrganizationService
from app.services.organization_member import OrganizationMemberService
from app.services.user import UserService


@pytest.mark.asyncio
async def test_create_membership() -> None:
    organization_name = f"Service Membership Organization {uuid4()}"
    owner_email = f"service-owner-{uuid4()}@trustmesh.local"
    member_email = f"service-membership-{uuid4()}@trustmesh.local"

    async with async_session_factory() as session:
        organization_service = OrganizationService(session)
        user_service = UserService(session)
        membership_service = OrganizationMemberService(session)

        owner = await user_service.create_user(
            owner_email,
            "TestPassword123!",
        )

        member = await user_service.create_user(
            member_email,
            "TestPassword123!",
        )

        organization = await organization_service.create_organization(
            organization_name,
            owner.id,
        )

        membership = await membership_service.create_membership(
            organization_id=organization.id,
            user_id=member.id,
        )

        await session.commit()

    assert membership.organization_id == organization.id
    assert membership.user_id == member.id
    assert membership.role == "member"


@pytest.mark.asyncio
async def test_get_membership_by_id() -> None:
    organization_name = f"Service Membership Lookup {uuid4()}"
    owner_email = f"service-owner-id-{uuid4()}@trustmesh.local"
    member_email = f"service-membership-id-{uuid4()}@trustmesh.local"

    async with async_session_factory() as session:
        organization_service = OrganizationService(session)
        user_service = UserService(session)
        membership_service = OrganizationMemberService(session)

        owner = await user_service.create_user(
            owner_email,
            "TestPassword123!",
        )

        member = await user_service.create_user(
            member_email,
            "TestPassword123!",
        )

        organization = await organization_service.create_organization(
            organization_name,
            owner.id,
        )

        created_membership = await membership_service.create_membership(
            organization.id,
            member.id,
        )

        await session.commit()

    async with async_session_factory() as session:
        membership_service = OrganizationMemberService(session)

        membership = await membership_service.get_membership_by_id(
            created_membership.id,
        )

    assert membership is not None
    assert membership.id == created_membership.id
    assert membership.organization_id == organization.id
    assert membership.user_id == member.id


@pytest.mark.asyncio
async def test_get_membership_by_id_returns_none_for_unknown_membership() -> None:
    async with async_session_factory() as session:
        membership_service = OrganizationMemberService(session)

        membership = await membership_service.get_membership_by_id(uuid4())

    assert membership is None


@pytest.mark.asyncio
async def test_get_membership_by_organization_and_user() -> None:
    organization_name = f"Service Membership Pair {uuid4()}"
    owner_email = f"service-owner-pair-{uuid4()}@trustmesh.local"
    member_email = f"service-membership-pair-{uuid4()}@trustmesh.local"

    async with async_session_factory() as session:
        organization_service = OrganizationService(session)
        user_service = UserService(session)
        membership_service = OrganizationMemberService(session)

        owner = await user_service.create_user(
            owner_email,
            "TestPassword123!",
        )

        member = await user_service.create_user(
            member_email,
            "TestPassword123!",
        )

        organization = await organization_service.create_organization(
            organization_name,
            owner.id,
        )

        created_membership = await membership_service.create_membership(
            organization.id,
            member.id,
        )

        await session.commit()

    async with async_session_factory() as session:
        membership_service = OrganizationMemberService(session)

        membership = await membership_service.get_membership_by_organization_and_user(
            organization.id,
            member.id,
        )

    assert membership is not None
    assert membership.id == created_membership.id


@pytest.mark.asyncio
async def test_get_membership_by_organization_and_user_returns_none_when_missing() -> None:
    async with async_session_factory() as session:
        membership_service = OrganizationMemberService(session)

        membership = await membership_service.get_membership_by_organization_and_user(
            uuid4(),
            uuid4(),
        )

    assert membership is None


@pytest.mark.asyncio
async def test_list_memberships_by_organization() -> None:
    organization_name = f"Service Membership List {uuid4()}"
    first_email = f"service-membership-list-1-{uuid4()}@trustmesh.local"
    second_email = f"service-membership-list-2-{uuid4()}@trustmesh.local"

    async with async_session_factory() as session:
        organization_service = OrganizationService(session)
        user_service = UserService(session)
        membership_service = OrganizationMemberService(session)

        first_user = await user_service.create_user(
            first_email,
            "TestPassword123!",
        )
        second_user = await user_service.create_user(
            second_email,
            "TestPassword123!",
        )

        organization = await organization_service.create_organization(
            organization_name,
            first_user.id,
        )

        first_membership = await membership_service.get_membership_by_organization_and_user(
            organization.id,
            first_user.id,
        )

        assert first_membership is not None

        second_membership = await membership_service.create_membership(
            organization.id,
            second_user.id,
        )

        await session.commit()

    async with async_session_factory() as session:
        membership_service = OrganizationMemberService(session)

        memberships = await membership_service.list_memberships_by_organization(organization.id)

    membership_ids = {membership.id for membership in memberships}

    assert first_membership.id in membership_ids
    assert second_membership.id in membership_ids
    assert len(memberships) == 2


@pytest.mark.asyncio
async def test_list_memberships_by_organization_returns_empty_list() -> None:
    async with async_session_factory() as session:
        membership_service = OrganizationMemberService(session)

        memberships = await membership_service.list_memberships_by_organization(uuid4())

    assert memberships == []
