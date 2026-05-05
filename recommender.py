import tmdb_client, scorer

def get_recommendations(movie_id):
    seed = tmdb_client.get_movie(movie_id)
    candidates = tmdb_client.get_similar(movie_id)
    
    scored = []
    print("Please wait...")
    for candidate in candidates:
        candidate = tmdb_client.get_movie(candidate["id"])
        candidate["score"] = scorer.score(seed, candidate)
        candidate["reason"] = scorer.explain(seed, candidate)
        scored.append(candidate)
    print("done!")
    scored_sorted = sorted(scored, key=lambda x : x["score"], reverse=True)
    
    return scored_sorted