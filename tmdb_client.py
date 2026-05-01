import config, cache
import requests

BASE_URL= f"https://api.themoviedb.org/3"

def search_movies(query):
    params = {
        "api_key": config.TMDB_KEY,
        "query": query
    }
    response = requests.get(f"{BASE_URL}/search/movie", params=params)
    data = response.json()
    return data.get("results", [])


def get_movie(movie_id):
    cached = cache.get(movie_id)
    if cached:
        return cached
    response = requests.get(f"{BASE_URL}/movie/{movie_id}", params={"api_key": config.TMDB_KEY})
    data = response.json()
    cache.save(data, movie_id)
    return data


def get_keywords(movie_id):
    response = requests.get(f"{BASE_URL}/movie/{movie_id}/keywords", params={"api_key": config.TMDB_KEY})
    data = response.json()
    return data.get("keywords", [])
    
    
def get_similar(movie_id):
    response= requests.get(f"{BASE_URL}/movie/{movie_id}/similar", params={"api_key": config.TMDB_KEY})
    data = response.json()
    return data.get("results", [])



