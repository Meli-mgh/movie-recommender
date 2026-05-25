import config, cache
import requests

BASE_URL = "https://api.themoviedb.org/3"

def _handle_response(response):
    if response.status_code == 401:
        raise ValueError("Invalid TMDB API key. Check your .env file.")
    if response.status_code != 200:
        response.raise_for_status()
    return response.json()

def _params(**kwargs):
    return {"api_key": config.TMDB_KEY, **kwargs}

def search_movies(query):
    response = requests.get(f"{BASE_URL}/search/movie", params=_params(query=query))
    data = _handle_response(response)
    return data.get("results", [])

def get_movie(movie_id):
    cached = cache.get(movie_id)
    if cached:
        return cached
    response = requests.get(f"{BASE_URL}/movie/{movie_id}", params=_params())
    data = _handle_response(response)
    data["keywords"] = get_keywords(movie_id)
    cache.save(data, movie_id)
    return data

def get_keywords(movie_id):
    response = requests.get(f"{BASE_URL}/movie/{movie_id}/keywords", params=_params())
    data = _handle_response(response)
    return data.get("keywords", []) if data else []

def get_similar(movie_id):
    response = requests.get(f"{BASE_URL}/movie/{movie_id}/similar", params=_params())
    data = _handle_response(response)
    return data.get("results", [])

def get_credits(movie_id):
    response = requests.get(f"{BASE_URL}/movie/{movie_id}/credits", params=_params())
    return _handle_response(response)