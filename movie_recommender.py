import os
import requests
import random
import json

API_KEY = os.getenv("OMDB_KEY")
if not API_KEY:
    raise ValueError("OMDB_KEY not set. Please set your environment variable.")

def get_movie_data(title):
    url = f"http://www.omdbapi.com/?t={title}&apikey={API_KEY}"
    response = requests.get(url)
    return response.json()

def search_by_keyword(keyword):
    url = f"http://www.omdbapi.com/?s={keyword}&apikey={API_KEY}"
    response = requests.get(url)
    return response.json()

user_movie = input("Enter a movie you like: ")

movie_data = get_movie_data(user_movie)

# Save JSON to file to inspect
with open("movie_data.json", "w", encoding="utf-8") as f:
    json.dump(movie_data, f, indent=2)

if movie_data.get("Response") == "True":
    genre = movie_data.get("Genre", "").split(",")[0]
    if genre:
        print(f"Detected genre: {genre}")
        results = search_by_keyword(genre)
        if results.get("Response") == "True":
            candidates = results["Search"]
            recommendation = random.choice(candidates)
            print("\nYou might also like:")
            print(recommendation["Title"], "-", recommendation["Year"])
        else:
            print("Couldn't find recommendations.")
    else:
        print("Genre information not available.")
else:
    print(f"Movie not found: {movie_data.get('Error')}")