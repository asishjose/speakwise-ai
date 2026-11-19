"""HTTP handlers that adapt public API schemas to the existing workflow."""

from __future__ import annotations

import logging
import sqlite3
from typing import Any

from fastapi import APIRouter, HTTPException, status

from speakwise.agents import intent_classifier, workflow
from speakwise.api.schemas.requests import AnalyzeRequest, CoachRequest, ImproveRequest
from speakwise.api.schemas.responses import (
    AnalyzeResponse,
    CoachResponse,
    HistoryResponse,
    ImproveResponse,
    InteractionResponse,
    ToolResultResponse,
)
from speakwise.history import coaching_repository
from speakwise.memory.context_manager import ContextManager


logger = logging.getLogger(__name__)
router = APIRouter(tags=["communication"])


def _model_data(value: Any) -> Any:
    """Convert internal Pydantic outputs to JSON-compatible values."""
    return value.model_dump() if hasattr(value, "model_dump") else value


def _ensure_known_session(session_id: str | None) -> None:
    """Restore a persisted session into ephemeral workflow memory when needed."""
    if session_id is None:
        return
    if workflow.memory.get_session(session_id) is not None:
        return
    if not coaching_repository.session_exists(session_id):
        raise HTTPException(status_code=404, detail="Session not found")
    workflow.memory.restore_session(session_id)
    # Rebuild the ephemeral context from persisted interactions after a restart.
    for interaction in coaching_repository.get_session_history(session_id):
        workflow.memory.add_message(session_id, "user", interaction["user_query"])
        workflow.memory.add_message(session_id, "assistant", interaction["generated_response"])


def _raise_service_error(error: Exception) -> None:
    if isinstance(error, sqlite3.Error):
        logger.exception("Database operation failed")
        raise HTTPException(status_code=503, detail="Database service is unavailable") from error
    if isinstance(error, RuntimeError):
        logger.exception("Agent execution failed")
        raise HTTPException(status_code=502, detail="Coaching service is unavailable") from error
    if isinstance(error, ValueError):
        raise HTTPException(status_code=422, detail=str(error)) from error
    logger.exception("Unexpected API error")
    raise HTTPException(status_code=500, detail="Unable to process the request") from error


@router.post("/analyze", response_model=AnalyzeResponse)
def analyze_communication(request: AnalyzeRequest) -> AnalyzeResponse:
    """Classify a communication request without executing a coaching plan."""
    _ensure_known_session(request.session_id)
    try:
        history = workflow.memory.get_history(request.session_id) if request.session_id else []
        context = ContextManager(max_messages=10).build_context(history)
        result = intent_classifier.classify_intent(request.user_input, context)
        return AnalyzeResponse(**result.model_dump())
    except HTTPException:
        raise
    except Exception as error:
        _raise_service_error(error)


@router.post("/coach", response_model=CoachResponse)
def coach_communication(request: CoachRequest) -> CoachResponse:
    """Run the established intent, planning, tool, and persistence workflow."""
    _ensure_known_session(request.session_id)
    try:
        result = workflow.process_request(request.user_input, request.session_id)
        execution = result["execution"]
        results = [
            ToolResultResponse(tool_name=item["tool_name"], output=_model_data(item["output"]))
            for item in execution.get("results", [])
        ]
        return CoachResponse(
            session_id=result["session_id"],
            intent=result["intent"].intent,
            plan=result["plan"].model_dump(),
            status=execution["status"],
            response=result["response"],
            results=results,
        )
    except HTTPException:
        raise
    except Exception as error:
        _raise_service_error(error)


@router.post("/improve", response_model=ImproveResponse)
def improve_communication(request: ImproveRequest) -> ImproveResponse:
    """Use the existing coaching workflow to improve supplied communication."""
    _ensure_known_session(request.session_id)
    prompt = request.user_input
    if request.instructions and request.instructions.strip():
        prompt = f"{prompt}\n\nImprovement instructions: {request.instructions.strip()}"

    try:
        result = workflow.process_request(prompt, request.session_id)
        outputs = [_model_data(item["output"]) for item in result["execution"].get("results", [])]
        output = outputs[-1] if outputs else None
        improved_text = result["response"]
        explanation = None
        if isinstance(output, dict):
            improved_text = (
                output.get("improved_text")
                or output.get("corrected_text")
                or output.get("improved_response")
                or output.get("body")
                or improved_text
            )
            explanation = output.get("explanation") or output.get("evaluation_summary")
        return ImproveResponse(
            session_id=result["session_id"],
            improved_text=improved_text,
            explanation=explanation,
            selected_tools=[action.tool_name for action in result["plan"].actions],
        )
    except HTTPException:
        raise
    except Exception as error:
        _raise_service_error(error)


@router.get("/history/{session_id}", response_model=HistoryResponse)
def get_history(session_id: str) -> HistoryResponse:
    """Return a session's SQLite-backed coaching interactions chronologically."""
    try:
        if not coaching_repository.session_exists(session_id):
            raise HTTPException(status_code=404, detail="Session not found")
        history = coaching_repository.get_session_history(session_id)
        scores = coaching_repository.get_communication_scores(session_id)
        return HistoryResponse(
            session_id=session_id,
            interactions=[InteractionResponse(**item) for item in history],
            communication_scores=scores,
        )
    except HTTPException:
        raise
    except Exception as error:
        _raise_service_error(error)
