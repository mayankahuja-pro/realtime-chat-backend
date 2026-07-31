import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.api import api_router
from app.core.config import settings
from app.core.logger import logger
from app.db.session import engine
from app.exceptions.handlers import register_exception_handlers
from app.websocket.redis_pubsub import subscribe

from app.websocket.redis_pubsub import subscribe

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        # Database connection check
        async with engine.begin() as conn:
            await conn.run_sync(lambda conn: None)

        logger.info("✅ Database Connected Successfully")

        # Start Redis subscriber
        asyncio.create_task(subscribe())
        logger.info("🚀 Redis Subscriber Task Started")

        yield

    except Exception as e:
        logger.error(f"❌ Startup Error: {e}")
        raise

    finally:
        logger.info("🛑 Shutting Down...")

        await engine.dispose()

        logger.info("✅ Database Connection Closed")

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    debug=settings.DEBUG,
    lifespan=lifespan,
)

@app.on_event("startup")
async def startup():

    asyncio.create_task(
        subscribe()
    )

register_exception_handlers(app)

app.include_router(api_router)