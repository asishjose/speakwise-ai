
from speakwise.history.database import initialize_database
from speakwise.history.coaching_repository import (
    save_interaction,
    get_session_history,
    get_communication_scores,
)


def test_save_and_retrieve_interaction():
    initialize_database()

    session_id = "test-session-001"

    save_interaction(
        session_id=session_id,
        user_query="Improve my email",
        detected_intent="email_writing",
        selected_tools=["email_tool", "tone_tool"],
        generated_response="Here is your improved email.",
        communication_score={
            "overall_score": 8.5,
            "clarity_score": 9.0,
        },
    )

    history = get_session_history(session_id)

    assert len(history) >= 1

    latest = history[-1]

    assert latest["user_query"] == "Improve my email"
    assert latest["detected_intent"] == "email_writing"
    assert latest["selected_tools"] == ["email_tool", "tone_tool"]


def test_retrieve_communication_scores():
    session_id = "test-session-001"

    scores = get_communication_scores(session_id)

    assert len(scores) >= 1
    assert scores[-1]["score"]["overall_score"] == 8.5
