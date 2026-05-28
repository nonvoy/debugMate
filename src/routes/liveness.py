from fastapi import APIRouter

router = APIRouter(tags=["liveness"])


@router.get("/live")
async def liveness_check() -> dict[str, str]:
    """Liveness check endpoint to verify that the application is running."""
    return {"status": "OK"}


@router.get("/ready")
async def readiness_check() -> dict[str, str]:
    """Readiness check endpoint to verify that the application is ready to handle requests."""
    # TODO: Check Celery worker status and other dependencies here
    return {"status": "OK"}
