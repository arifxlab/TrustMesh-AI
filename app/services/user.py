from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.user import UserRepository
from app.security import password_security


class UserService:
    def __init__(self, session: AsyncSession) -> None:
        self.repository = UserRepository(session)

    async def create_user(self, email: str, password: str) -> User:
        password_hash = password_security.hash_password(password)

        return await self.repository.create(
            email=email,
            password_hash=password_hash,
        )

    async def get_user_by_id(self, user_id: UUID) -> User | None:
        return await self.repository.get_by_id(user_id)

    async def get_user_by_email(self, email: str) -> User | None:
        return await self.repository.get_by_email(email)
