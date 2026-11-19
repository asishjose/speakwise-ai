
import json

from speakwise.history.database import get_connection


def create_session_record(session_id: str):
    with get_connection() as connection:
        connection.execute(
            """
            INSERT OR IGNORE INTO sessions (session_id)
            VALUES (?)
            """,
            (session_id,)
        )


def save_interaction(
    session_id: str,
    user_query: str,
    detected_intent: str,
    selected_tools: list[str],
    generated_response: str,
    communication_score: dict | None = None,
):
    create_session_record(session_id)

    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO coaching_history (
                session_id,
                user_query,
                detected_intent,
                selected_tools,
                generated_response,
                communication_score
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                session_id,
                user_query,
                detected_intent,
                json.dumps(selected_tools),
                generated_response,
                json.dumps(communication_score)
                if communication_score is not None else None,
            )
        )

        return cursor.lastrowid


def get_session_history(session_id: str):
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT *
            FROM coaching_history
            WHERE session_id = ?
            ORDER BY created_at, id
            """,
            (session_id,)
        ).fetchall()

        history = []

        for row in rows:
            record = dict(row)
            record["selected_tools"] = json.loads(record["selected_tools"])
            record["communication_score"] = (
                json.loads(record["communication_score"])
                if record["communication_score"] else None
            )
            history.append(record)

        return history


def session_exists(session_id: str) -> bool:
    """Return whether a session has been persisted in SQLite."""
    with get_connection() as connection:
        row = connection.execute(
            "SELECT 1 FROM sessions WHERE session_id = ?",
            (session_id,),
        ).fetchone()
        return row is not None


def get_communication_scores(session_id: str):
    history = get_session_history(session_id)

    return [
        {
            "interaction_id": item["id"],
            "score": item["communication_score"],
            "created_at": item["created_at"],
        }
        for item in history
        if item["communication_score"] is not None
    ]
