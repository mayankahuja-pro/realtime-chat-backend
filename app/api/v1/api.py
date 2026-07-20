from fastapi import APIRouter

from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.health import router as health_router
from app.websocket.chat import router as websocket_router
from app.api.v1.endpoints.messages import router as message_router
from app.api.v1.endpoints.redis import router as redis_router

api_router = APIRouter()

api_router.include_router(health_router)
api_router.include_router(auth_router)
api_router.include_router(websocket_router)

api_router.include_router(message_router)

api_router.include_router(redis_router)