from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db_session
from app.schemas.user import UserCreate, UserResponse
from app.services.user import UserService

router = APIRouter(prefix="/users", tags=["users"])

db_session = Depends(get_db_session)


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    payload: UserCreate,
    session: AsyncSession = db_session,
) -> UserResponse:
    service = UserService(session)

    existing_user = await service.get_user_by_email(str(payload.email))

    if existing_user is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this email already exists.",
        )

    user = await service.create_user(str(payload.email))

    await session.commit()

    return UserResponse.model_validate(user)


@router.get(
    "/{user_id}",
    response_model=UserResponse,
)
async def get_user(
    user_id: UUID,
    session: AsyncSession = db_session,
) -> UserResponse:
    service = UserService(session)

    user = await service.get_user_by_id(user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )

    return UserResponse.model_validate(user)


@router.get(
    "/by-email/{email}",
    response_model=UserResponse,
)
async def get_user_by_email(
    email: str,
    session: AsyncSession = db_session,
) -> UserResponse:
    service = UserService(session)

    user = await service.get_user_by_email(email)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )

    return UserResponse.model_validate(user)
