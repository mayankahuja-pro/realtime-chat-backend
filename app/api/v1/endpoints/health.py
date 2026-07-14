from fastapi import APIRouter

router = APIRouter(tags=["Health"])


@router.get("/")
async def root():
    return {
        "status": "success",
        "message": "Realtime Chat Backend Running 🚀"
    }


@router.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "Realtime Chat Backend"
    }


@router.get("/health/live")
async def liveness():
    return {
        "status": "alive"
    }


@router.get("/health/ready")
async def readiness():
    return {
        "status": "ready"
    }