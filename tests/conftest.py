from collections.abc import AsyncIterator

import pytest
from httpx import ASGITransport, AsyncClient

from app.core.dependencies import get_db, get_redis
from app.main import app


class FakeResult:
    def scalar_one(self) -> int:
        return 1


class FakeSession:
    async def execute(self, statement: object) -> FakeResult:
        return FakeResult()


class FakeRedis:
    async def ping(self) -> bool:
        return True


@pytest.fixture
def healthy_dependencies() -> AsyncIterator[None]:
    app.dependency_overrides[get_db] = lambda: FakeSession()
    app.dependency_overrides[get_redis] = lambda: FakeRedis()
    yield
    app.dependency_overrides.clear()


@pytest.fixture
async def client() -> AsyncIterator[AsyncClient]:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
