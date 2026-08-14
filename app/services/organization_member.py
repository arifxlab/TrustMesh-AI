from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.organization_member import OrganizationMember
from app.repositories.organization_member import OrganizationMemberRepository


class OrganizationMemberService:
    def __init__(self, session: AsyncSession) -> None:
        self.repository = OrganizationMemberRepository(session)

    async def create_membership(
        self,
        organization_id: UUID,
        user_id: UUID,
        role: str = "member",
    ) -> OrganizationMember:
        return await self.repository.create(
            organization_id=organization_id,
            user_id=user_id,
            role=role,
        )

    async def get_membership_by_id(
        self,
        membership_id: UUID,
    ) -> OrganizationMember | None:
        return await self.repository.get_by_id(membership_id)

    async def get_membership_by_organization_and_user(
        self,
        organization_id: UUID,
        user_id: UUID,
    ) -> OrganizationMember | None:
        return await self.repository.get_by_organization_and_user(
            organization_id=organization_id,
            user_id=user_id,
        )

    async def list_memberships_by_organization(
        self,
        organization_id: UUID,
    ) -> list[OrganizationMember]:
        return await self.repository.list_by_organization(organization_id)
