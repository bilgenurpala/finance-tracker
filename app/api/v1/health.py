import logging

import redis.asyncio as aioredis
from fastapi import APIRouter, Depends, Response, status
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db, get_redis

logger = logging.getLogger(__name__)

router = APIRouter(tags=["system"])


async def _check_postgres(session: AsyncSession) -> bool:
    try:
        result = await session.execute(text("SELECT 1"))
        return result.scalar_one() == 1
    except Exception:
        logger.exception("Postgres health check failed")
        return False


async def _check_redis(client: aioredis.Redis) -> bool:
    try:
        return bool(await client.ping())
    except Exception:
        logger.exception("Redis health check failed")
        return False


@router.get("/health")
async def health(
    response: Response,
    session: AsyncSession = Depends(get_db),
    redis_client: aioredis.Redis = Depends(get_redis),
) -> dict[str, object]:
    checks = {
        "postgres": await _check_postgres(session),
        "redis": await _check_redis(redis_client),
    }
    healthy = all(checks.values())
    if not healthy:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    return {"status": "ok" if healthy else "degraded", "checks": checks}
