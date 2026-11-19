"""Frontend configuration loaded from environment variables."""

from __future__ import annotations

import os


BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000").rstrip("/")
REQUEST_TIMEOUT_SECONDS = float(os.getenv("BACKEND_TIMEOUT_SECONDS", "60"))
