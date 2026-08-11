"""
session.py — lightweight session tracking.

No auth. No server. Just a UUID that lives for one run,
so reactions from the same sitting are grouped together.

Usage:
    from session import current_session
    session_id = current_session()
"""

import uuid

_session_id: str | None = None


def current_session() -> str:
    """Return the session ID for this run. Created once, reused throughout."""
    global _session_id
    if _session_id is None:
        _session_id = str(uuid.uuid4())
    return _session_id


def reset():
    """Force a new session. Call this if a user explicitly starts over."""
    global _session_id
    _session_id = str(uuid.uuid4())
    return _session_id