from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "TrustMesh AI"
    app_version: str = "0.1.0"
    debug: bool = False

    database_url: str = ""
    redis_url: str = ""

    qdrant_url: str = "http://localhost:6333"
    qdrant_collection: str = "trustmesh_documents"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
