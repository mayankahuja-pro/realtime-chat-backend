from contextlib import asynccontextmanager
from app.exceptions.handlers import register_exception_handlers
from fastapi import FastAPI

from app.api.v1.api import api_router
from app.core.config import settings
from app.db.session import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        async with engine.begin() as conn:
            await conn.run_sync(lambda conn: None)
        print("✅ Database Connected Successfully")
    except Exception as e:
        print(f"❌ Database Connection Failed: {e}")
    yield
    await engine.dispose()


app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    debug=settings.DEBUG,
    lifespan=lifespan,
)

register_exception_handlers(app)

app.include_router(api_router)