from fastapi import FastAPI

from src.routes.events import router as events_router
from src.routes.liveness import router as liveness_router

app = FastAPI()

app.include_router(liveness_router, prefix="/health")
app.include_router(events_router, prefix="/api/v1")
