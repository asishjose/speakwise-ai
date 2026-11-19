"""Rendering helpers for structured coaching feedback."""

from __future__ import annotations

from typing import Any

import streamlit as st


SCORE_FIELDS = ("grammar_score", "clarity_score", "tone_score", "relevance_score", "overall_score")


def find_score(results: list[dict[str, Any]]) -> dict[str, Any] | None:
    """Return a score object only when the backend actually supplied one."""
    for result in results:
        output = result.get("output")
        if isinstance(output, dict) and any(field in output for field in SCORE_FIELDS):
            return output
    return None


def render_score(score: dict[str, Any] | None) -> None:
    """Display communication scoring data without treating absent data as zero."""
    if not score:
        return
    st.markdown("#### Communication feedback")
    columns = st.columns(5)
    labels = ("Grammar", "Clarity", "Tone", "Relevance", "Overall")
    for column, label, field in zip(columns, labels, SCORE_FIELDS):
        value = score.get(field)
        if isinstance(value, (int, float)):
            column.metric(label, f"{value:.1f}/10")
            column.progress(min(max(float(value) / 10, 0.0), 1.0))

    for key, label in (("strengths", "Strengths"), ("weaknesses", "Areas to improve"), ("recommendations", "Recommendations")):
        items = score.get(key)
        if isinstance(items, list) and items:
            st.markdown(f"**{label}**")
            for item in items:
                st.write(f"• {item}")
    if score.get("evaluation_summary"):
        st.caption(str(score["evaluation_summary"]))
