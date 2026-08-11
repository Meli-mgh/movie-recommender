import config, tmdb_client
from math import sqrt


def score(seed, candidate, credits_by_id=None, mood_by_id=None):
    return sum([
        _genre_score(seed, candidate),
        _director_score(seed, candidate, credits_by_id=credits_by_id),
        _cast_score(seed, candidate, credits_by_id=credits_by_id),
        _keyword_score(seed, candidate),
        _decade_score(seed, candidate),
        _rating_score(seed, candidate),
        _mood_score(seed, candidate, mood_by_id=mood_by_id),
    ])


def _genre_score(seed, candidate):
    seed_ids = set(g["id"] for g in seed.get("genres", []))
    candidate_ids = set(g["id"] for g in candidate.get("genres", []))
    return len(seed_ids & candidate_ids) * config.WEIGHTS["genre"]


def _get_director(credits):
    if not credits:
        return set()
    return set(p["name"] for p in credits.get("crew", []) if p.get("job") == "Director")


def _get_credits(movie, credits_by_id=None):
    if credits_by_id is not None and movie.get("id") in credits_by_id:
        return credits_by_id[movie["id"]]
    return tmdb_client.get_credits(movie["id"])


def _director_score(seed, candidate, credits_by_id=None):
    seed_credits = _get_credits(seed, credits_by_id=credits_by_id)
    candidate_credits = _get_credits(candidate, credits_by_id=credits_by_id)
    if _get_director(seed_credits) & _get_director(candidate_credits):
        return config.WEIGHTS["director"]
    return 0


def _cast_score(seed, candidate, credits_by_id=None):
    seed_credits = _get_credits(seed, credits_by_id=credits_by_id)
    candidate_credits = _get_credits(candidate, credits_by_id=credits_by_id)
    seed_cast = set(p["name"] for p in seed_credits.get("cast", [])[:5])
    candidate_cast = set(p["name"] for p in candidate_credits.get("cast", [])[:5])
    return len(seed_cast & candidate_cast) * config.WEIGHTS["cast"]


def _keyword_score(seed, candidate):
    seed_keywords = set(k["id"] for k in seed.get("keywords", []))
    candidate_keywords = set(k["id"] for k in candidate.get("keywords", []))
    return len(seed_keywords & candidate_keywords) * config.WEIGHTS["keyword"]


def _get_year(movie):
    date = movie.get("release_date", "")
    return date.split("-")[0] if date else None


def _decade_score(seed, candidate):
    seed_year = _get_year(seed)
    candidate_year = _get_year(candidate)
    if not seed_year or not candidate_year:
        return 0
    if int(seed_year) // 10 == int(candidate_year) // 10:
        return config.WEIGHTS["decade"]
    return 0


def _rating_score(seed, candidate):
    seed_rating = seed.get("vote_average", 0)
    candidate_rating = candidate.get("vote_average", 0)
    diff = abs(seed_rating - candidate_rating)
    return max(0, 1 - (diff / 10)) * config.WEIGHTS["rating"]


def _get_mood(movie, mood_by_id=None):
    if mood_by_id is not None and movie.get("id") in mood_by_id:
        return mood_by_id[movie["id"]]
    return movie.get("mood", {})


def _mood_score(seed, candidate, mood_by_id=None):
    dims = ["valence", "arousal", "complexity", "weight", "pace"]
    seed_mood = _get_mood(seed, mood_by_id=mood_by_id)
    candidate_mood = _get_mood(candidate, mood_by_id=mood_by_id)
    distance = sqrt(sum(
    config.MOOD_DIMENSION_WEIGHTS[d] *
    (seed_mood.get(d, 0) - candidate_mood.get(d, 0)) ** 2
    for d in dims
    ))
    similarity = 1 - (distance / sqrt(len(dims) * 4))
    return similarity * config.WEIGHTS["mood"]


def _mood_explanation(seed, candidate, mood_by_id=None):
    dims = ["valence", "arousal", "complexity", "weight", "pace"]
    seed_bins = seed.get("mood_bins", {})
    candidate_bins = candidate.get("mood_bins", {})

    matches = []
    drifts = []

    for dim in dims:
        s = seed_bins.get(dim)
        c = candidate_bins.get(dim)
        if not s or not c:
            continue
        if s == c:
            matches.append(dim)
        else:
            seed_labels = config.MOOD_LABELS[dim]
            s_idx = seed_labels.index(s) if s in seed_labels else -1
            c_idx = seed_labels.index(c) if c in seed_labels else -1
            if s_idx != -1 and c_idx != -1 and abs(s_idx - c_idx) == 1:
                matches.append(dim)
            else:
                drifts.append(f"{dim}: {s}→{c}")

    parts = []
    if matches:
        parts.append(f"mood match on {', '.join(matches)}")
    if drifts:
        parts.append(f"differs in {'; '.join(drifts)}")
    return parts


def explain(seed, candidate, credits_by_id=None, mood_by_id=None):
    seed_credits = _get_credits(seed, credits_by_id=credits_by_id)
    candidate_credits = _get_credits(candidate, credits_by_id=credits_by_id)
    reasons = []

    if _genre_score(seed, candidate) > 0:
        reasons.append("genre")
    if _get_director(seed_credits) & _get_director(candidate_credits):
        reasons.append("director")
    seed_cast = set(p["name"] for p in seed_credits.get("cast", [])[:5])
    candidate_cast = set(p["name"] for p in candidate_credits.get("cast", [])[:5])
    if seed_cast & candidate_cast:
        reasons.append("cast")
    if _keyword_score(seed, candidate) > 0:
        reasons.append("keywords")
    if _decade_score(seed, candidate) > 0:
        reasons.append("decade")

    mood_parts = _mood_explanation(seed, candidate, mood_by_id=mood_by_id)
    reasons.extend(mood_parts)

    return "Strong match on " + ", ".join(reasons) if reasons else "General match"
