from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db_session
from app.schemas.organization import OrganizationCreate, OrganizationResponse
from app.services.organization import OrganizationService

router = APIRouter(prefix="/organizations", tags=["organizations"])

db_session = Depends(get_db_session)


@router.post(
    "",
    response_model=OrganizationResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_organization(
    payload: OrganizationCreate,
    session: AsyncSession = db_session,
) -> OrganizationResponse:
    service = OrganizationService(session)

    organization = await service.create_organization(payload.name)

    await session.commit()

    return OrganizationResponse.model_validate(organization)


@router.get(
    "/{organization_id}",
    response_model=OrganizationResponse,
)
async def get_organization(
    organization_id: UUID,
    session: AsyncSession = db_session,
) -> OrganizationResponse:
    service = OrganizationService(session)

    organization = await service.get_organization_by_id(organization_id)

    if organization is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found.",
        )

    return OrganizationResponse.model_validate(organization)
