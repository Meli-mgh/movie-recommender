from dotenv import load_dotenv
import os

load_dotenv()

TMDB_KEY = os.getenv("TMDB_KEY", "")

MODEL = "gemma3:4b"


WEIGHTS = {
    "genre": 1.0,
    "director": 0.5,
    "cast": 0.25,
    "keyword": 1.0,
    "decade": 0.25,
    "rating": 0.5,
    "mood": 25.0,
}

MOOD_LABELS = {
    "valence": [
        "very_dark",
        "dark",
        "neutral",
        "warm",
        "uplifting",
    ],
    "arousal": [
        "calm",
        "low",
        "moderate",
        "high",
        "intense",
    ],
    "complexity": [
        "effortless",
        "simple",
        "moderate",
        "demanding",
        "challenging",
    ],
    "weight": [
        "very_light",
        "light",
        "moderate",
        "heavy",
        "crushing",
    ],
    "pace": [
        "very_slow",
        "slow",
        "moderate",
        "fast",
        "relentless",
    ],
}

# Helper values used ONLY during scoring.
MOOD_SCORES = {
    "valence": {
        "very_dark": -1.0,
        "dark": -0.5,
        "neutral": 0.0,
        "warm": 0.5,
        "uplifting": 1.0,
    },
    "arousal": {
        "calm": -1.0,
        "low": -0.5,
        "moderate": 0.0,
        "high": 0.5,
        "intense": 1.0,
    },
    "complexity": {
        "effortless": -1.0,
        "simple": -0.4,
        "moderate": 0.0,
        "demanding": 0.6,
        "challenging": 1.0,
    },
    "weight": {
        "very_light": -1.0,
        "light": -0.4,
        "moderate": 0.0,
        "heavy": 0.6,
        "crushing": 1.0,
    },
    "pace": {
        "very_slow": -1.0,
        "slow": -0.5,
        "moderate": 0.0,
        "fast": 0.5,
        "relentless": 1.0,
    },
}

MOOD_DIMENSION_WEIGHTS = {
    "valence": 1.0,
    "arousal": 1.5,
    "complexity": 2.5,
    "weight": 3.0,
    "pace": 1.0,
}