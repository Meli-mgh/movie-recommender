import tmdb_client, scorer, llm_client, cache


def build_recommendations(seed, candidates, *, credits_by_id=None, mood_by_id=None, mood_context=None):
    """
    Build a ranked recommendation list from already-fetched movie data.

    This function is intentionally pure from the perspective of network I/O:
    it only consumes movie dictionaries and optional metadata lookups.
    """
    scored = []
    for candidate in candidates:
        candidate_data = dict(candidate)
        candidate_data["score"] = scorer.score(
            seed,
            candidate_data,
            credits_by_id=credits_by_id,
            mood_by_id=mood_by_id,
        )
        candidate_data["reason"] = scorer.explain(
            seed,
            candidate_data,
            credits_by_id=credits_by_id,
            mood_by_id=mood_by_id,
        )
        candidate_data["mood_context"] = mood_context or {}
        scored.append(candidate_data)

    sorted_results = sorted(scored, key=lambda x: x["score"], reverse=True)
    for i, movie in enumerate(sorted_results):
        movie["position"] = i
    return sorted_results


def get_recommendations(movie_id, mood_context=None):
    """
    Returns a list of candidate movies, sorted by score descending.
    Each movie dict includes:
      - score: raw weighted score
      - position: 0-indexed rank in this result set
      - reason: human-readable explanation string
      - mood_context: passed through for feedback recording
    """
    seed = tmdb_client.get_movie(movie_id)
    if not seed.get("mood"):
        scores, bins = llm_client.get_mood(seed)
        seed["mood"] = scores
        seed["mood_bins"] = bins
        cache.save(seed, seed["id"])

    candidates = tmdb_client.get_similar(movie_id)
    detailed_candidates = []

    print(f"Scoring {len(candidates)} candidates...")
    for i, candidate in enumerate(candidates):
        candidate_data = tmdb_client.get_movie(candidate["id"])
        if not candidate_data.get("mood"):
            scores, bins = llm_client.get_mood(candidate_data)
            candidate_data["mood"] = scores
            candidate_data["mood_bins"] = bins
            cache.save(candidate_data, candidate_data["id"])
        detailed_candidates.append(candidate_data)
        print(f"  {i + 1}/{len(candidates)} {candidate_data.get('title')}")

    return build_recommendations(
        seed,
        detailed_candidates,
        mood_context=mood_context,
    )
