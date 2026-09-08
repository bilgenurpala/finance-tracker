from collections.abc import AsyncIterator

import redis.asyncio as aioredis
from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession


async def get_db(request: Request) -> AsyncIterator[AsyncSession]:
    factory = request.app.state.session_factory
    async with factory() as session:
        yield session


async def get_redis(request: Request) -> AsyncIterator[aioredis.Redis]:
    client = aioredis.Redis(connection_pool=request.app.state.redis_pool)
    try:
        yield client
    finally:
        await client.aclose()
