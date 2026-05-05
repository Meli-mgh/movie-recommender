from dotenv import load_dotenv
import os

load_dotenv()

TMDB_KEY = os.getenv("TMDB_KEY")
if not TMDB_KEY:
    raise ValueError("TMDB API key not found. Add it to your .env file: TMDB_KEY=your_key_here")

WEIGHTS = {
    "genre": 3,
    "director": 4,
    "cast": 1,
    "keyword": 2,
    "decade": 1,
    "rating": 2,
}