from fastapi import APIRouter

from app.core.redis import redis_client

router = APIRouter(
    prefix="/redis",
    tags=["Redis"],
)


@router.get("/health")
async def redis_health():

    await redis_client.ping()

    return {
        "status": "Redis Connected"
    }