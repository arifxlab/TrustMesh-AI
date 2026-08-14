from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.organization import Organization


class OrganizationRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, name: str) -> Organization:
        organization = Organization(
            id=uuid4(),
            name=name,
        )

        self.session.add(organization)
        await self.session.flush()

        return organization

    async def get_by_id(self, organization_id: UUID) -> Organization | None:
        result = await self.session.execute(
            select(Organization).where(Organization.id == organization_id)
        )

        return result.scalar_one_or_none()

    async def get_by_name(self, name: str) -> Organization | None:
        result = await self.session.execute(
            select(Organization)
            .where(Organization.name == name)
            .order_by(Organization.created_at.desc())
            .limit(1)
        )

        return result.scalar_one_or_none()
