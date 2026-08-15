from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.authorization.roles import OrganizationRole
from app.models.organization_member import OrganizationMember


class OrganizationMemberRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(
        self,
        organization_id: UUID,
        user_id: UUID,
        role: OrganizationRole = OrganizationRole.MEMBER,
    ) -> OrganizationMember:
        membership = OrganizationMember(
            id=uuid4(),
            organization_id=organization_id,
            user_id=user_id,
            role=role,
        )

        self.session.add(membership)
        await self.session.flush()

        return membership

    async def get_by_id(
        self,
        membership_id: UUID,
    ) -> OrganizationMember | None:
        result = await self.session.execute(
            select(OrganizationMember).where(OrganizationMember.id == membership_id)
        )

        return result.scalar_one_or_none()

    async def get_by_organization_and_user(
        self,
        organization_id: UUID,
        user_id: UUID,
    ) -> OrganizationMember | None:
        result = await self.session.execute(
            select(OrganizationMember).where(
                OrganizationMember.organization_id == organization_id,
                OrganizationMember.user_id == user_id,
            )
        )

        return result.scalar_one_or_none()

    async def list_by_organization(
        self,
        organization_id: UUID,
    ) -> list[OrganizationMember]:
        result = await self.session.execute(
            select(OrganizationMember)
            .where(OrganizationMember.organization_id == organization_id)
            .order_by(OrganizationMember.created_at.asc())
        )

        return list(result.scalars().all())
