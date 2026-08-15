from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.authorization.roles import OrganizationRole


class OrganizationMemberCreate(BaseModel):
    user_id: UUID
    role: OrganizationRole = Field(default=OrganizationRole.MEMBER)


class OrganizationMemberResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    user_id: UUID
    role: OrganizationRole
    created_at: datetime
