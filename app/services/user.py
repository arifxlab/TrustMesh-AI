from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.user import UserRepository


class UserService:
    def __init__(self, session: AsyncSession) -> None:
        self.repository = UserRepository(session)

    async def create_user(self, email: str) -> User:
        return await self.repository.create(email)

    async def get_user_by_id(self, user_id: UUID) -> User | None:
        return await self.repository.get_by_id(user_id)

    async def get_user_by_email(self, email: str) -> User | None:
        return await self.repository.get_by_email(email)
