from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.organization import Organization
from app.repositories.organization import OrganizationRepository


class OrganizationService:
    def __init__(self, session: AsyncSession) -> None:
        self.repository = OrganizationRepository(session)

    async def create_organization(self, name: str) -> Organization:
        return await self.repository.create(name)

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
