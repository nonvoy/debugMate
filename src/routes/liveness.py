from fastapi import APIRouter, HTTPException, status
from fastapi.concurrency import run_in_threadpool

from src.services.celery.client import get_celery_client

router = APIRouter(tags=["liveness"])


@router.get("/live")
async def liveness_check() -> dict[str, str]:
    """Liveness check endpoint to verify that the application is running."""
    return {"status": "OK"}


@router.get("/ready")
async def readiness_check() -> dict[str, str]:
    """Readiness check endpoint to verify that the application is ready to handle requests."""
    celery_app = get_celery_client()
    try:
        response = await run_in_threadpool(celery_app.control.ping, timeout=5)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Celery broker/worker check failed: {exc}",
        ) from exc

    if not response:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="No Celery workers responded",
        )

    return {"status": "OK"}
