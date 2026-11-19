"""Sidebar controls for session and backend state."""

from __future__ import annotations

from typing import Callable

import streamlit as st


def render_sidebar(
    session_ids: list[str],
    current_session_id: str | None,
    backend_online: bool,
    on_new_conversation: Callable[[], None],
    on_load_session: Callable[[str], None],
) -> None:
    with st.sidebar:
        st.title("SpeakWise AI")
        st.caption("Your Intelligent AI Communication Coach")
        if st.button("+ New conversation", width="stretch"):
            on_new_conversation()

        st.divider()
        st.markdown("**Backend status**")
        if backend_online:
            st.success("Connected")
        else:
            st.error("Unavailable")

        st.markdown("**Current session**")
        st.caption(current_session_id or "A session will be created with your first message.")

        st.divider()
        st.markdown("**Conversation history**")
        if session_ids:
            chosen = st.selectbox("Recent sessions", session_ids, index=None, placeholder="Choose a session")
            if chosen and st.button("Load selected session", width="stretch"):
                on_load_session(chosen)
        else:
            st.caption("Sessions used in this browser appear here.")
        entered = st.text_input("Load by session ID", placeholder="Paste an existing session ID")
        if st.button("Load session ID", width="stretch", disabled=not entered.strip()):
            on_load_session(entered.strip())
