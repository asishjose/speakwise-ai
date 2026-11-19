"""ASGI application entry point for SpeakWise AI."""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from speakwise.api.routes.communication import router as communication_router
from speakwise.history.database import initialize_database


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Ensure SQLite tables exist without invoking any LLM service."""
    initialize_database()
    yield


app = FastAPI(
    title="SpeakWise AI API",
    version="0.1.0",
    description="REST API for SpeakWise AI communication coaching.",
    lifespan=lifespan,
)
app.include_router(communication_router)


@app.get("/health", tags=["health"])
def health() -> dict[str, str]:
    """Return service availability; this endpoint never calls an LLM."""
    return {"status": "ok"}
