from collections.abc import Callable
from uuid import UUID

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.authorization.roles import OrganizationRole
from app.db.session import get_db_session
from app.dependencies.auth import get_current_user
from app.models.organization_member import OrganizationMember
from app.models.user import User
from app.repositories.organization_member import OrganizationMemberRepository

db_session_dependency = Depends(get_db_session)
current_user_dependency = Depends(get_current_user)


async def get_current_membership(
    organization_id: UUID,
    current_user: User = current_user_dependency,
    session: AsyncSession = db_session_dependency,
) -> OrganizationMember:
    repository = OrganizationMemberRepository(session)

    membership = await repository.get_by_organization_and_user(
        organization_id=organization_id,
        user_id=current_user.id,
    )

    if membership is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a member of this organization.",
        )

    return membership


current_membership_dependency = Depends(get_current_membership)


def require_organization_role(
    *allowed_roles: OrganizationRole,
) -> Callable:
    async def dependency(
        membership: OrganizationMember = current_membership_dependency,
    ) -> OrganizationMember:
        if membership.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this action.",
            )

        return membership

    return dependency
