from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.authorization.roles import OrganizationRole
from app.db.session import get_db_session
from app.dependencies.organization import (
    get_current_membership,
    require_organization_role,
)
from app.models.organization_member import OrganizationMember
from app.schemas.organization_member import (
    OrganizationMemberCreate,
    OrganizationMemberResponse,
)
from app.services.organization_member import OrganizationMemberService

router = APIRouter(
    prefix="/organizations/{organization_id}/members",
    tags=["organization-members"],
)

db_session = Depends(get_db_session)
current_membership_dependency = Depends(get_current_membership)
admin_or_owner_dependency = Depends(
    require_organization_role(
        OrganizationRole.OWNER,
        OrganizationRole.ADMIN,
    )
)


@router.post(
    "",
    response_model=OrganizationMemberResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_membership(
    organization_id: UUID,
    payload: OrganizationMemberCreate,
    _: OrganizationMember = admin_or_owner_dependency,
    session: AsyncSession = db_session,
) -> OrganizationMemberResponse:
    service = OrganizationMemberService(session)

    existing_membership = await service.get_membership_by_organization_and_user(
        organization_id=organization_id,
        user_id=payload.user_id,
    )

    if existing_membership is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User is already a member of this organization.",
        )

    membership = await service.create_membership(
        organization_id=organization_id,
        user_id=payload.user_id,
        role=payload.role,
    )

    await session.commit()

    return OrganizationMemberResponse.model_validate(membership)


@router.get(
    "",
    response_model=list[OrganizationMemberResponse],
)
async def list_memberships(
    organization_id: UUID,
    _: OrganizationMember = current_membership_dependency,
    session: AsyncSession = db_session,
) -> list[OrganizationMemberResponse]:
    service = OrganizationMemberService(session)

    memberships = await service.list_memberships_by_organization(
        organization_id,
    )

    return [OrganizationMemberResponse.model_validate(membership) for membership in memberships]


@router.get(
    "/{user_id}",
    response_model=OrganizationMemberResponse,
)
async def get_membership(
    organization_id: UUID,
    user_id: UUID,
    _: OrganizationMember = current_membership_dependency,
    session: AsyncSession = db_session,
) -> OrganizationMemberResponse:
    service = OrganizationMemberService(session)

    membership = await service.get_membership_by_organization_and_user(
        organization_id=organization_id,
        user_id=user_id,
    )

    if membership is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization membership not found.",
        )

    return OrganizationMemberResponse.model_validate(membership)
