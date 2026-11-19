"""Streamlit interface for SpeakWise AI's FastAPI backend."""

from __future__ import annotations

from typing import Any

import streamlit as st

# Streamlit runs this file with ``frontend/`` on sys.path, so these imports
# intentionally stay local rather than requiring the repository root package.
from api_client import BackendError, SpeakWiseApiClient
from components.chat import render_messages
from components.feedback import find_score
from components.history import render_history
from components.sidebar import render_sidebar
from config import BACKEND_URL


st.set_page_config(page_title="SpeakWise AI", page_icon="💬", layout="wide")


def _initialize_state() -> None:
    defaults: dict[str, Any] = {
        "current_session_id": None,
        "messages": [],
        "known_session_ids": [],
        "loaded_history": None,
    }
    for key, value in defaults.items():
        st.session_state.setdefault(key, value)


def _remember_session(session_id: str | None) -> None:
    if session_id and session_id not in st.session_state.known_session_ids:
        st.session_state.known_session_ids.insert(0, session_id)


def _new_conversation() -> None:
    st.session_state.current_session_id = None
    st.session_state.messages = []
    st.session_state.loaded_history = None


def _load_session(client: SpeakWiseApiClient, session_id: str) -> None:
    try:
        history = client.history(session_id)
    except BackendError as error:
        st.sidebar.error(str(error))
        return

    messages: list[dict[str, Any]] = []
    for interaction in history.get("interactions", []):
        messages.append({"role": "user", "content": interaction.get("user_query", "")})
        messages.append(
            {
                "role": "assistant",
                "content": interaction.get("generated_response", ""),
                "tools": interaction.get("selected_tools", []),
                "score": interaction.get("communication_score"),
            }
        )
    st.session_state.current_session_id = session_id
    st.session_state.messages = messages
    st.session_state.loaded_history = history
    _remember_session(session_id)
    st.rerun()


def _submit_coaching(client: SpeakWiseApiClient, user_input: str) -> None:
    st.session_state.messages.append({"role": "user", "content": user_input})
    try:
        with st.spinner("SpeakWise AI is preparing your coaching feedback…"):
            result = client.coach(user_input, st.session_state.current_session_id)
    except BackendError as error:
        st.session_state.messages.pop()
        st.error(str(error))
        return

    st.session_state.current_session_id = result.get("session_id")
    _remember_session(st.session_state.current_session_id)
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": result.get("response", "No coaching response was returned."),
            "tools": [item.get("tool_name", "") for item in result.get("results", []) if item.get("tool_name")],
            "score": find_score(result.get("results", [])),
        }
    )
    st.session_state.loaded_history = None
    st.rerun()


def _render_tools(client: SpeakWiseApiClient) -> None:
    with st.expander("Analyze communication", expanded=False):
        analysis_text = st.text_area("Text to analyze", key="analysis_text", height=100)
        if st.button("Analyze", key="analyze_button"):
            if not analysis_text.strip():
                st.warning("Enter some text to analyze.")
            else:
                try:
                    with st.spinner("Analyzing communication…"):
                        result = client.analyze(analysis_text, st.session_state.current_session_id)
                    st.success(f"Intent: {result.get('intent', 'Unavailable')}")
                    confidence = result.get("confidence")
                    if isinstance(confidence, (int, float)):
                        st.progress(min(max(float(confidence), 0.0), 1.0), text=f"Confidence: {confidence:.0%}")
                    if result.get("reasoning"):
                        st.write(result["reasoning"])
                except BackendError as error:
                    st.error(str(error))

    with st.expander("Improve a message", expanded=False):
        improve_text = st.text_area("Original message", key="improve_text", height=100)
        instructions = st.text_input("Preferences (optional)", key="improve_instructions", placeholder="e.g. Polite and professional")
        if st.button("Improve message", key="improve_button"):
            if not improve_text.strip():
                st.warning("Enter a message to improve.")
            else:
                try:
                    with st.spinner("Improving your message…"):
                        result = client.improve(improve_text, instructions, st.session_state.current_session_id)
                    session_id = result.get("session_id")
                    if session_id:
                        st.session_state.current_session_id = session_id
                        _remember_session(session_id)
                    st.markdown("#### Improved response")
                    st.code(result.get("improved_text", "No improved text was returned."), language=None)
                    if result.get("explanation"):
                        st.caption(result["explanation"])
                    tools = result.get("selected_tools")
                    if isinstance(tools, list) and tools:
                        st.caption("Tools used: " + ", ".join(tools))
                except BackendError as error:
                    st.error(str(error))


def main() -> None:
    _initialize_state()
    client = SpeakWiseApiClient(BACKEND_URL)
    backend_online = client.health()

    render_sidebar(
        st.session_state.known_session_ids,
        st.session_state.current_session_id,
        backend_online,
        _new_conversation,
        lambda session_id: _load_session(client, session_id),
    )

    st.title("SpeakWise AI")
    st.caption("Your Intelligent AI Communication Coach")
    if not st.session_state.messages:
        st.info("Start a conversation and I’ll help you communicate with clarity and confidence.")

    render_messages(st.session_state.messages)
    _render_tools(client)

    if st.session_state.loaded_history:
        with st.expander("Loaded session details", expanded=False):
            render_history(st.session_state.loaded_history.get("interactions", []))

    user_input = st.chat_input("Ask for communication coaching…", disabled=not backend_online)
    if user_input and user_input.strip():
        _submit_coaching(client, user_input.strip())


if __name__ == "__main__":
    main()
