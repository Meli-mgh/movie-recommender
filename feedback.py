"""
feedback.py — reaction storage for the recommendation loop.

Reaction types:
  accepted  — user chose this movie to watch
  rejected  — explicitly passed on it
  skipped   — scrolled past without engaging
  abandoned — started watching, stopped early
  rewatch   — watched again; strong positive signal
"""

import json
import os
from datetime import datetime, timezone

FEEDBACK_PATH = "cache/feedback.jsonl"
os.makedirs("cache", exist_ok=True)


def record(
    candidate_movie_id: int,
    reaction: str,
    *,
    session_id: str,
    seed_movie_id: int,
    position: int,
    score: float,
    mood_context: dict = None,
):
    valid_reactions = {"accepted", "rejected", "skipped", "abandoned", "rewatch"}
    if reaction not in valid_reactions:
        raise ValueError(f"Invalid reaction '{reaction}'. Must be one of: {valid_reactions}")

    event = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "session_id": session_id,
        "seed_movie_id": seed_movie_id,
        "candidate_movie_id": candidate_movie_id,
        "reaction": reaction,
        "position": position,       # 0 = top rec
        "score": round(score, 4),
        "mood_context": mood_context or {},
    }

    with open(FEEDBACK_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(event) + "\n")


def load_all() -> list[dict]:
    """Return all recorded reactions as a list of dicts, oldest first."""
    if not os.path.exists(FEEDBACK_PATH):
        return []
    with open(FEEDBACK_PATH, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def load_for_movie(movie_id: int) -> list[dict]:
    """Return all reactions where this movie was the candidate."""
    return [r for r in load_all() if r["candidate_movie_id"] == movie_id]


def load_for_session(session_id: str) -> list[dict]:
    """Return all reactions from a specific session."""
    return [r for r in load_all() if r["session_id"] == session_id]


def summary() -> dict:
    """Quick stats across all recorded feedback."""
    all_reactions = load_all()
    if not all_reactions:
        return {"total": 0}

    counts = {}
    for r in all_reactions:
        counts[r["reaction"]] = counts.get(r["reaction"], 0) + 1

    accepted = [r for r in all_reactions if r["reaction"] == "accepted"]
    rejected = [r for r in all_reactions if r["reaction"] == "rejected"]

    return {
        "total": len(all_reactions),
        "by_reaction": counts,
        "avg_position_accepted": (
            sum(r["position"] for r in accepted) / len(accepted) if accepted else None
        ),
        "avg_position_rejected": (
            sum(r["position"] for r in rejected) / len(rejected) if rejected else None
        ),
        "sessions": len(set(r["session_id"] for r in all_reactions)),  #distribution 
    }