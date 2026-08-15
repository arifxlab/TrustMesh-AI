from uuid import uuid4

import pytest
from fastapi import HTTPException

from app.authorization.roles import OrganizationRole
from app.dependencies.organization import require_organization_role
from app.models.organization_member import OrganizationMember


def make_membership(role: OrganizationRole) -> OrganizationMember:
    return OrganizationMember(
        id=uuid4(),
        organization_id=uuid4(),
        user_id=uuid4(),
        role=role,
    )


@pytest.mark.asyncio
async def test_owner_is_allowed_for_owner_only_permission() -> None:
    dependency = require_organization_role(OrganizationRole.OWNER)
    membership = make_membership(OrganizationRole.OWNER)

    result = await dependency(membership)

    assert result is membership


@pytest.mark.asyncio
async def test_admin_is_allowed_for_admin_or_owner_permission() -> None:
    dependency = require_organization_role(
        OrganizationRole.OWNER,
        OrganizationRole.ADMIN,
    )
    membership = make_membership(OrganizationRole.ADMIN)

    result = await dependency(membership)

    assert result is membership


@pytest.mark.asyncio
async def test_member_is_rejected_from_admin_permission() -> None:
    dependency = require_organization_role(OrganizationRole.ADMIN)
    membership = make_membership(OrganizationRole.MEMBER)

    with pytest.raises(HTTPException) as exc_info:
        await dependency(membership)

    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == "You do not have permission to perform this action."


@pytest.mark.asyncio
async def test_viewer_is_rejected_from_admin_permission() -> None:
    dependency = require_organization_role(OrganizationRole.ADMIN)
    membership = make_membership(OrganizationRole.VIEWER)

    with pytest.raises(HTTPException) as exc_info:
        await dependency(membership)

    assert exc_info.value.status_code == 403


@pytest.mark.asyncio
async def test_multiple_roles_are_supported() -> None:
    dependency = require_organization_role(
        OrganizationRole.OWNER,
        OrganizationRole.ADMIN,
        OrganizationRole.MEMBER,
    )
    membership = make_membership(OrganizationRole.MEMBER)

    result = await dependency(membership)

    assert result is membership
