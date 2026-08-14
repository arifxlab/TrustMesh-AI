from fastapi import FastAPI

from app.api.organization_members import router as organization_members_router
from app.api.organizations import router as organizations_router
from app.api.users import router as users_router
from app.core.config import get_settings

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    description="AI-powered knowledge intelligence platform.",
    version=settings.app_version,
)

app.include_router(users_router, prefix="/api/v1")
app.include_router(organizations_router, prefix="/api/v1")
app.include_router(organization_members_router, prefix="/api/v1")


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}
