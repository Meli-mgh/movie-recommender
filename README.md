# 🎬 Movie Recommender

A content-based recommendation engine built in Python. Give it a movie, it finds you more!

---

## How It Works

When you pick a seed movie, the engine scores a pool of candidates across six features:

| Feature | Signal |
|---|---|
| **Genre** | Overlapping genres |
| **Director** | Same director |
| **Cast** | Shared actors |
| **Keywords** | Thematic tags from TMDB |
| **Decade** | Same era of filmmaking |
| **Rating** | Proximity of TMDB scores |

Each feature has a configurable weight. The final score is a weighted sum (fully transparent, fully yours to tune)

---

## Project Structure

```
movie_recommender/
├── recommender.py      # orchestration — fetch, score, return results
├── ui.py               # all user interaction
├── tmdb_client.py      # TMDB API calls
├── scorer.py           # scoring algorithm
├── cache.py            # local JSON cache
├── config.py           # API key + scoring weights
├── .env                # your TMDB key (gitignored)
├── .env.example        # safe to commit
└── README.md
```

---

## Getting Started

**1. Clone the repo**
```bash
git clone https://github.com/Meli-mgh/movie-recommender.git
cd movie-recommender
```

**2. Set up your environment**
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**3. Add your TMDB API key**
```bash
cp .env.example .env
```
Get a free key at [themoviedb.org](https://www.themoviedb.org/settings/api), then add it to `.env`:
```
TMDB_KEY=your_key_here
```

**4. Run**
```bash
python ui.py
```

---

## Configuration

Weights live in `config.py`:

```python
WEIGHTS = {
    "genre": 3,
    "director": 4,
    "cast": 1,
    "keyword": 2,
    "decade": 1,
    "rating": 2,
}
```

Want director to matter more than genre? Change the numbers. The algorithm is yours.

---

## Caching

API responses are cached locally under `cache/` as JSON. Repeat lookups are instant and don't burn API calls. Cache is gitignored.

---

## Roadmap

### Near-term
- Cognitively-informed scoring — a weighting system grounded in how people actually form taste preferences, informed by psychology and cognitive science research
- Richer recommendation explanations beyond feature overlap
- Paginated results — "give me the next 3"
- Bearer token auth (newer TMDB standard)

### Personalization
- Local user accounts with persistent profiles
- Personal watch history and library
- Per-user scoring weights tuned to individual taste
- Mood-based recommendations

### Social
- Shareable profiles
- Combined profile matching — find movies two people will both enjoy
- IMDb account integration

### Long-term
- Web UI
- Cloud deployment
- Collaborative filtering layered on top of content-based engine

---

## Why I Built This

Most recommendation systems are a black box. I wanted to understand what's actually inside — and building the scoring engine from scratch forced me to think carefully about what makes two movies *feel* similar. That turns out to be a more interesting question than it sounds.

Every decision in this codebase has a reason behind it.

---

## Tech Stack

- Python 3
- [TMDB API](https://developer.themoviedb.org/)
- `requests`, `python-dotenv`

---

## License

MIT