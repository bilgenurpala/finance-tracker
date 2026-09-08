import pytest
from httpx import AsyncClient

from app.core.dependencies import get_db, get_redis
from app.main import app
from tests.conftest import FakeRedis, FakeSession


class BrokenSession:
    async def execute(self, statement: object) -> object:
        raise RuntimeError("postgres is down")


class BrokenRedis:
    async def ping(self) -> bool:
        raise RuntimeError("redis is down")


@pytest.mark.usefixtures("healthy_dependencies")
async def test_health_returns_ok_when_all_dependencies_are_up(client: AsyncClient) -> None:
    response = await client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "checks": {"postgres": True, "redis": True},
    }


async def test_health_returns_503_when_postgres_is_down(client: AsyncClient) -> None:
    app.dependency_overrides[get_db] = lambda: BrokenSession()
    app.dependency_overrides[get_redis] = lambda: FakeRedis()
    try:
        response = await client.get("/health")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 503
    assert response.json() == {
        "status": "degraded",
        "checks": {"postgres": False, "redis": True},
    }


async def test_health_returns_503_when_redis_is_down(client: AsyncClient) -> None:
    app.dependency_overrides[get_db] = lambda: FakeSession()
    app.dependency_overrides[get_redis] = lambda: BrokenRedis()
    try:
        response = await client.get("/health")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 503
    assert response.json() == {
        "status": "degraded",
        "checks": {"postgres": True, "redis": False},
    }
