"""add password hash to users

Revision ID: b88c9d32a540
Revises: d3cc1dadddf6
Create Date: 2026-08-14 20:27:37.149772

"""

import secrets
from collections.abc import Sequence

import sqlalchemy as sa
from argon2 import PasswordHasher

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "b88c9d32a540"
down_revision: str | Sequence[str] | None = "d3cc1dadddf6"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""

    # Phase 1: Add the column as nullable so existing users remain valid.
    op.add_column(
        "users",
        sa.Column(
            "password_hash",
            sa.String(length=255),
            nullable=True,
        ),
    )

    # Phase 2: Give existing development users unusable password hashes.
    #
    # These users were created before password authentication existed.
    # A unique random password is generated for each user, hashed with
    # Argon2, and immediately discarded. Therefore nobody knows the
    # corresponding plaintext password.
    connection = op.get_bind()
    password_hasher = PasswordHasher()

    users = connection.execute(
        sa.text("SELECT id FROM users WHERE password_hash IS NULL")
    ).fetchall()

    for user in users:
        unusable_password = secrets.token_urlsafe(64)
        password_hash = password_hasher.hash(unusable_password)

        connection.execute(
            sa.text(
                """
                UPDATE users
                SET password_hash = :password_hash
                WHERE id = :user_id
                """
            ),
            {
                "password_hash": password_hash,
                "user_id": user.id,
            },
        )

    # Phase 3: Enforce the invariant for all future users.
    op.alter_column(
        "users",
        "password_hash",
        existing_type=sa.String(length=255),
        nullable=False,
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column("users", "password_hash")
