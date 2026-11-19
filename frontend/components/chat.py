"""Chat transcript rendering."""

from __future__ import annotations

from typing import Any

import streamlit as st

from components.feedback import render_score


def render_messages(messages: list[dict[str, Any]]) -> None:
    for message in messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            tools = message.get("tools")
            if tools:
                st.caption("Tools used: " + ", ".join(tools))
            render_score(message.get("score"))
