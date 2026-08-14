from datetime import UTC, datetime, timedelta
from typing import Any

import jwt
from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerificationError, VerifyMismatchError
from jwt import InvalidTokenError

from app.core.config import get_settings


class PasswordSecurity:
    def __init__(self) -> None:
        self._hasher = PasswordHasher()

    def hash_password(self, password: str) -> str:
        return self._hasher.hash(password)

    def verify_password(self, password: str, password_hash: str) -> bool:
        try:
            return self._hasher.verify(password_hash, password)
        except (InvalidHashError, VerificationError, VerifyMismatchError):
            return False


class TokenSecurity:
    def __init__(self) -> None:
        self._settings = get_settings()

    def create_access_token(
        self,
        subject: str,
        expires_delta: timedelta | None = None,
    ) -> str:
        now = datetime.now(UTC)
        expires_at = now + (
            expires_delta
            or timedelta(
                minutes=self._settings.jwt_access_token_expire_minutes,
            )
        )

        payload: dict[str, Any] = {
            "sub": subject,
            "iat": now,
            "exp": expires_at,
        }

        return jwt.encode(
            payload,
            self._settings.jwt_secret_key,
            algorithm=self._settings.jwt_algorithm,
        )

    def decode_access_token(self, token: str) -> dict[str, Any] | None:
        try:
            payload = jwt.decode(
                token,
                self._settings.jwt_secret_key,
                algorithms=[self._settings.jwt_algorithm],
            )
        except InvalidTokenError:
            return None

        return payload


password_security = PasswordSecurity()
token_security = TokenSecurity()
