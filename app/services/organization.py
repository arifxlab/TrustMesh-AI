from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.authorization.roles import OrganizationRole
from app.models.organization import Organization
from app.repositories.organization import OrganizationRepository
from app.repositories.organization_member import OrganizationMemberRepository


class OrganizationService:
    def __init__(self, session: AsyncSession) -> None:
        self.repository = OrganizationRepository(session)
        self.membership_repository = OrganizationMemberRepository(session)

    async def create_organization(
        self,
        name: str,
        owner_user_id: UUID,
    ) -> Organization:
        organization = await self.repository.create(name)

        await self.membership_repository.create(
            organization_id=organization.id,
            user_id=owner_user_id,
            role=OrganizationRole.OWNER,
        )

        return organization

    async def get_organization_by_id(
        self,
        organization_id: UUID,
    ) -> Organization | None:
        return await self.repository.get_by_id(organization_id)

    async def get_organization_by_name(
        self,
        name: str,
    ) -> Organization | None:
        return await self.repository.get_by_name(name)
