import pytest
from pydantic import ValidationError

from app.core.config import Settings

REQUIRED_VARS = ["DATABASE_URL", "REDIS_URL", "SECRET_KEY", "ENVIRONMENT"]

VALID_CONFIG = {
    "DATABASE_URL": "postgresql+asyncpg://user:pass@localhost:5432/fintrack",
    "REDIS_URL": "redis://localhost:6379/0",
    "SECRET_KEY": "a" * 32,
    "ENVIRONMENT": "development",
}


@pytest.fixture
def clean_env(monkeypatch: pytest.MonkeyPatch) -> None:
    for name in [*REQUIRED_VARS, "ANTHROPIC_API_KEY", "DEBUG"]:
        monkeypatch.delenv(name, raising=False)


def build(**overrides: str) -> Settings:
    values = {**VALID_CONFIG, **overrides}
    return Settings(_env_file=None, **values)


@pytest.mark.usefixtures("clean_env")
def test_valid_configuration_is_accepted() -> None:
    settings = build()

    assert settings.ENVIRONMENT == "development"
    assert settings.SECRET_KEY.get_secret_value() == "a" * 32


@pytest.mark.usefixtures("clean_env")
@pytest.mark.parametrize("missing", REQUIRED_VARS)
def test_missing_required_field_raises(missing: str) -> None:
    values = {k: v for k, v in VALID_CONFIG.items() if k != missing}

    with pytest.raises(ValidationError) as exc_info:
        Settings(_env_file=None, **values)

    errors = exc_info.value.errors()
    assert [e for e in errors if e["loc"] == (missing,) and e["type"] == "missing"]


@pytest.mark.usefixtures("clean_env")
def test_short_secret_key_is_rejected() -> None:
    with pytest.raises(ValidationError, match="at least 32 characters"):
        build(SECRET_KEY="too-short")


@pytest.mark.usefixtures("clean_env")
def test_sync_database_url_is_rejected() -> None:
    with pytest.raises(ValidationError, match="postgresql\\+asyncpg://"):
        build(DATABASE_URL="postgresql://user:pass@localhost:5432/fintrack")


@pytest.mark.usefixtures("clean_env")
def test_invalid_environment_is_rejected() -> None:
    with pytest.raises(ValidationError):
        build(ENVIRONMENT="staging-2")
