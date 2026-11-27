
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from speakwise.api.routes.communication import (
    router as communication_router,
)
from speakwise.history.database import initialize_database
from speakwise.observability.logging_config import (
    configure_logging,
)
from speakwise.observability.middleware import (
    request_logging_middleware,
)


configure_logging()

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI):
    initialize_database()

    logger.info("SpeakWise API starting")

    yield

    logger.info("SpeakWise API shutting down")


app = FastAPI(
    title="SpeakWise AI API",
    version="0.1.0",
    description="REST API for SpeakWise AI communication coaching.",
    lifespan=lifespan,
)


app.middleware("http")(request_logging_middleware)

app.include_router(communication_router)

Instrumentator().instrument(app).expose(
    app,
    endpoint="/metrics",
)


@app.get("/health", tags=["health"])
def health():
    return {"status": "ok"}
