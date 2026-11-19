"""API tests: all agent/LLM boundaries are mocked; no Gemini request is made."""

import os
import sqlite3

os.environ.setdefault("GEMINI_API_KEY", "test-key-not-used-for-network-calls")

import pytest
from fastapi.testclient import TestClient

from speakwise.agents.workflow import memory
from speakwise.api.main import app
from speakwise.api.routes import communication
from speakwise.history import database
from speakwise.history.coaching_repository import create_session_record, save_interaction
from speakwise.schemas.intent import IntentClassification
from speakwise.schemas.plan import CommunicationPlan, PlannedAction
from speakwise.schemas.tools.tone import ToneImprovement


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setattr(database, "DATABASE_PATH", tmp_path / "api-test.db")
    memory.sessions.clear()
    with TestClient(app) as test_client:
        yield test_client
    memory.sessions.clear()


def _workflow_result(session_id="new-session"):
    return {
        "session_id": session_id,
        "intent": IntentClassification(intent="tone_improvement", confidence=0.93, reasoning="Tone request."),
        "plan": CommunicationPlan(
            user_goal="Improve tone",
            primary_intent="tone_improvement",
            actions=[PlannedAction(tool_name="tone_tool", action="Improve tone", required_information=[])],
            execution_strategy="single",
            missing_information=[],
            needs_clarification=False,
            clarification_question=None,
            reasoning="A tone tool is appropriate.",
        ),
        "execution": {
            "status": "success",
            "results": [{
                "tool_name": "tone_tool",
                "output": ToneImprovement(
                    original_text="Send it now",
                    detected_tone="direct",
                    target_tone="professional",
                    improved_text="Please send it at your earliest convenience.",
                    explanation="Uses a polite request.",
                    changes_made=["Added politeness"],
                ),
            }],
        },
        "response": "Please send it at your earliest convenience.",
    }


def test_health_and_analyze_are_successful(client, monkeypatch):
    monkeypatch.setattr(
        communication.intent_classifier,
        "classify_intent",
        lambda *_: IntentClassification(intent="grammar_correction", confidence=0.98, reasoning="Correction requested."),
    )
    assert client.get("/health").json() == {"status": "ok"}
    response = client.post("/analyze", json={"user_input": "Correct this sentence."})
    assert response.status_code == 200
    assert response.json()["intent"] == "grammar_correction"


def test_coach_and_improve_use_mocked_workflow(client, monkeypatch):
    monkeypatch.setattr(communication.workflow, "process_request", lambda *_: _workflow_result())
    coached = client.post("/coach", json={"user_input": "Make it professional."})
    improved = client.post("/improve", json={"user_input": "Send it now", "instructions": "professional"})
    assert coached.status_code == 200
    assert coached.json()["results"][0]["tool_name"] == "tone_tool"
    assert improved.status_code == 200
    assert improved.json()["improved_text"] == "Please send it at your earliest convenience."


def test_history_and_nonexistent_session(client):
    create_session_record("history-session")
    save_interaction(
        session_id="history-session", user_query="Score this", detected_intent="communication_evaluation",
        selected_tools=["scoring_tool"], generated_response="Feedback",
        communication_score={"overall_score": 8.0},
    )
    response = client.get("/history/history-session")
    assert response.status_code == 200
    assert response.json()["interactions"][0]["communication_score"]["overall_score"] == 8.0
    assert client.get("/history/missing-session").status_code == 404
    assert client.post("/coach", json={"user_input": "Hello", "session_id": "missing-session"}).status_code == 404


def test_validation_and_service_errors(client, monkeypatch):
    assert client.post("/analyze", json={"user_input": "   "}).status_code == 422
    monkeypatch.setattr(communication.intent_classifier, "classify_intent", lambda *_: (_ for _ in ()).throw(RuntimeError("mock failure")))
    assert client.post("/analyze", json={"user_input": "Help"}).status_code == 502
    monkeypatch.setattr(communication.coaching_repository, "session_exists", lambda _: (_ for _ in ()).throw(sqlite3.OperationalError("offline")))
    assert client.get("/history/any-session").status_code == 503
