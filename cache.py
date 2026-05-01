import json
import os

os.makedirs("cache/movies", exist_ok=True)

def get(movie_id):
    path = f"cache/movies/{movie_id}.json"
    try:
        with open(path, "r") as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        return None
    
                
def save(movie, movie_id):
    path = f"cache/movies/{movie_id}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(movie, f, indent=2)

