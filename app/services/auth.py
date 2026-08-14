from sqlalchemy.ext.asyncio import AsyncSession

from app.security import password_security, token_security
from app.services.user import UserService


class AuthService:
    def __init__(self, session: AsyncSession) -> None:
        self.user_service = UserService(session)

    async def authenticate_user(
        self,
        email: str,
        password: str,
    ) -> str | None:
        user = await self.user_service.get_user_by_email(email)

        if user is None:
            return None

        if not password_security.verify_password(
            password,
            user.password_hash,
        ):
            return None

        return token_security.create_access_token(str(user.id))
