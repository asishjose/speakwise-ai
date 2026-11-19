"""Small HTTP client for the SpeakWise FastAPI contract."""

from __future__ import annotations

from typing import Any

import requests

from config import REQUEST_TIMEOUT_SECONDS


class BackendError(RuntimeError):
    """A safe, user-facing backend error."""


class SpeakWiseApiClient:
    """Calls SpeakWise's HTTP API without accessing agents or SQLite directly."""

    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    def _request(self, method: str, path: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        try:
            response = requests.request(
                method,
                f"{self.base_url}{path}",
                json=payload,
                timeout=REQUEST_TIMEOUT_SECONDS,
            )
        except requests.RequestException as error:
            raise BackendError("Cannot reach the SpeakWise backend. Check that FastAPI is running.") from error

        try:
            body = response.json()
        except ValueError as error:
            raise BackendError("The backend returned an invalid response.") from error

        if not response.ok:
            detail = body.get("detail") if isinstance(body, dict) else None
            message = detail if isinstance(detail, str) else "The backend could not process this request."
            if response.status_code == 404:
                message = "That session could not be found."
            raise BackendError(message)
        if not isinstance(body, dict):
            raise BackendError("The backend returned an unexpected response format.")
        return body

    def health(self) -> bool:
        try:
            return self._request("GET", "/health").get("status") == "ok"
        except BackendError:
            return False

    def coach(self, user_input: str, session_id: str | None) -> dict[str, Any]:
        payload: dict[str, Any] = {"user_input": user_input}
        if session_id:
            payload["session_id"] = session_id
        return self._request("POST", "/coach", payload)

    def analyze(self, user_input: str, session_id: str | None) -> dict[str, Any]:
        payload: dict[str, Any] = {"user_input": user_input}
        if session_id:
            payload["session_id"] = session_id
        return self._request("POST", "/analyze", payload)

    def improve(self, user_input: str, instructions: str | None, session_id: str | None) -> dict[str, Any]:
        payload: dict[str, Any] = {"user_input": user_input}
        if instructions:
            payload["instructions"] = instructions
        if session_id:
            payload["session_id"] = session_id
        return self._request("POST", "/improve", payload)

    def history(self, session_id: str) -> dict[str, Any]:
        return self._request("GET", f"/history/{session_id}")
