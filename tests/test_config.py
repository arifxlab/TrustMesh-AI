from app.core.config import get_settings


def test_settings_load_from_environment() -> None:
    settings = get_settings()

    assert settings.app_name == "TrustMesh AI"
    assert settings.app_version == "0.1.0"
    assert settings.database_url.startswith("postgresql+asyncpg://")
    assert settings.redis_url.startswith("redis://")
