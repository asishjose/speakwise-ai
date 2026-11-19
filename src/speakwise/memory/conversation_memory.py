
from uuid import uuid4
from typing import Literal

from pydantic import BaseModel, Field


class ConversationMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class ConversationSession(BaseModel):
    session_id: str
    messages: list[ConversationMessage] = Field(
        default_factory=list
    )


class ConversationMemory:

    def __init__(self, max_messages: int = 20):

        self.sessions: dict[str, ConversationSession] = {}
        self.max_messages = max_messages

    def create_session(self) -> str:

        session_id = str(uuid4())

        self.sessions[session_id] = ConversationSession(
            session_id=session_id
        )

        return session_id

    def restore_session(self, session_id: str) -> None:
        """Make a persisted session available to the in-process memory store.

        Conversation memory is intentionally ephemeral; the API uses this when
        a client continues a session stored in SQLite after an app restart.
        """
        if session_id not in self.sessions:
            self.sessions[session_id] = ConversationSession(session_id=session_id)

    def get_session(self, session_id: str):

        return self.sessions.get(session_id)

    def add_message(
        self,
        session_id: str,
        role: Literal["user", "assistant"],
        content: str
    ):

        session = self.get_session(session_id)

        if session is None:
            raise ValueError("Invalid session ID")

        session.messages.append(
            ConversationMessage(
                role=role,
                content=content
            )
        )

        # Keep only the most recent messages
        session.messages = session.messages[-self.max_messages:]

    def get_history(self, session_id: str):

        session = self.get_session(session_id)

        if session is None:
            raise ValueError("Invalid session ID")

        return session.messages

    def clear_session(self, session_id: str):

        if session_id not in self.sessions:
            raise ValueError("Invalid session ID")

        self.sessions[session_id].messages.clear()

    def delete_session(self, session_id: str):

        if session_id not in self.sessions:
            raise ValueError("Invalid session ID")

        del self.sessions[session_id]
