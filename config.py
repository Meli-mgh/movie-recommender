from dotenv import load_dotenv
import os

load_dotenv()

TMDB_KEY = os.getenv("TMDB_KEY")

WEIGHTS = {
    "genre": 3,
    "director": 4,
    "cast": 1,
    "keyword": 2,
    "decade": 1,
    "rating": 2,
}