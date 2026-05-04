import config, tmdb_client



def score(seed, candidate):
    total = sum([
    _genre_score(seed, candidate),
    _director_score(seed, candidate),
    _cast_score(seed, candidate),
    _keyword_score(seed, candidate),
    _decade_score(seed, candidate),
    _rating_score(seed, candidate),
    ])
    return total


def _genre_score(seed, candidate):
    seed_ids = set(g["id"] for g in seed["genres"])
    candidate_ids = set(g["id"] for g in candidate["genres"])
    overlap = seed_ids & candidate_ids
    return len(overlap) * config.WEIGHTS["genre"]           
              

def _director_score(seed, candidate):
    seed_dirs = _get_director(seed)
    candidate_dirs = _get_director(candidate)
    if seed_dirs & candidate_dirs:
        return config.WEIGHTS["director"]
    return 0


def _cast_score(seed, candidate):
    seed_cast = set(p["name"] for p in tmdb_client.get_credits(seed["id"])["cast"][:5])
    candidate_cast = set(p["name"] for p in tmdb_client.get_credits(candidate["id"])["cast"][:5])
    overlap = seed_cast & candidate_cast
    return len(overlap) * config.WEIGHTS["cast"] 


def _keyword_score(seed, candidate):
    seed_keywords = set(k["id"] for k in tmdb_client.get_keywords(seed["id"]))
    candidate_keywords = set(k["id"] for k in tmdb_client.get_keywords(candidate["id"]))
    overlap = seed_keywords & candidate_keywords
    return len(overlap) * config.WEIGHTS["keyword"]


def _decade_score(seed, candidate):
    seed_year = int(seed["release_date"].split("-")[0])
    candidate_year = int(candidate["release_date"].split("-")[0])
    if seed_year//10 == candidate_year//10:
        return config.WEIGHTS["decade"]
    return 0


def _rating_score(seed, candidate):
    seed_rating = seed.get("vote_average", 0)
    candidate_rating = candidate.get("vote_average", 0)
    diff = abs(seed_rating - candidate_rating)
    return max(0, 1 - (diff / 10)) * config.WEIGHTS["rating"]


def _get_director(movie):
    credits = tmdb_client.get_credits(movie["id"])
    return set(p["name"] for p in credits["crew"] if p["job"] == "director")
    
    
def explain(seed, candidate):
    reasons = []
    
    if _genre_score(seed, candidate) > 0:
        reasons.append("genre")
    if _director_score(seed, candidate) > 0:
        reasons.append("director")
    if _cast_score(seed, candidate) > 0:
        reasons.append("cast")
    if _keyword_score(seed, candidate) > 0:
        reasons.append("keywords")
    if _decade_score(seed, candidate) > 0:
        reasons.append("decade")
    if _rating_score(seed, candidate) > 0:
        reasons.append("rating")
        
    return "Strong match on "+ ", ".join(reasons) if reasons else "General match"