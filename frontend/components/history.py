"""Rendering for persisted coaching interactions."""

from __future__ import annotations

from typing import Any

import streamlit as st

from components.feedback import render_score


def render_history(interactions: list[dict[str, Any]]) -> None:
    if not interactions:
        st.info("This session has no saved interactions yet.")
        return
    for item in interactions:
        timestamp = item.get("created_at", "Unknown time")
        with st.expander(f"{timestamp} · {item.get('detected_intent', 'communication')}"):
            st.markdown("**You**")
            st.write(item.get("user_query", ""))
            st.markdown("**SpeakWise AI**")
            st.write(item.get("generated_response", ""))
            tools = item.get("selected_tools")
            if isinstance(tools, list) and tools:
                st.caption("Tools used: " + ", ".join(tools))
            score = item.get("communication_score")
            render_score(score if isinstance(score, dict) else None)
