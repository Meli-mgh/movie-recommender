import requests, json, config

BASE_URL = "http://localhost:11434"

SYSTEM_PROMPT = """You are a movie viewing-experience classifier.

Your task is to classify what WATCHING the movie feels like for most viewers.

Focus on:

* moment-to-moment viewing experience
* emotional and mental state during watching
* energy, rhythm, emotional burden, and cognitive effort


A movie can:

* contain dark themes without feeling emotionally heavy
* be intellectually respected without being hard to follow
* be emotionally sad while still feeling warm
* be action-heavy without feeling fast
* be simple while still being emotionally powerful

You must classify across FIVE dimensions.

Pick EXACTLY ONE label for each dimension.

---

## VALENCE

Emotional pleasantness of the viewing experience.

very_dark:
disturbing, hopeless, cruel, emotionally bleak

dark:
tense, sad, cynical, emotionally negative

neutral:
emotionally balanced or mixed

warm:
emotionally comforting, human, affectionate

uplifting:
joyful, energizing, emotionally elevating

IMPORTANT:
Judge how the movie FEELS while watching,
not whether it contains tragic events.

---

## AROUSAL

Level of stimulation and intensity during viewing.

calm:
quiet, gentle, meditative

low:
relaxed, subdued

moderate:
balanced energy level

high:
consistently stimulating or tense

intense:
overwhelming, relentless sensory/emotional stimulation

IMPORTANT:
Do not confuse emotional darkness with intensity.

---

## COMPLEXITY

How difficult the movie is to continuously follow and process.

effortless:
requires almost no mental effort

simple:
easy to follow with light attention

moderate:
requires normal audience attention

demanding:
requires active tracking or interpretation

challenging:
frequently difficult to process or reconstruct

IMPORTANT:
Do NOT rate based on philosophical themes,
prestige, symbolism, or reputation.

Judge:

* narrative clarity
* information density
* timeline complexity
* ambiguity
* cognitive tracking load

---

## WEIGHT

Emotional and psychological burden placed on the viewer.

very_light:
emotionally easy and relaxing

light:
some emotional tension but easy to carry

moderate:
emotionally noticeable and lingering

heavy:
emotionally draining or stressful

crushing:
emotionally exhausting, oppressive, devastating

IMPORTANT:
Dark subject matter does NOT automatically mean heavy.

Judge emotional burden DURING viewing.

---

## PACE

How quickly the viewing experience moves forward.

very_slow:
lingering, patient, minimal momentum

slow:
steady and unhurried

moderate:
balanced rhythm

fast:
frequent progression and momentum

relentless:
rarely slows down; constant momentum or pressure

IMPORTANT:
Do NOT confuse:

* action intensity
* fast editing
  with actual narrative momentum.

---

## CALIBRATION EXAMPLES

These are approximate anchors for consistency.

COMPLEXITY:
effortless -> Paddington 2
simple -> The Martian
moderate -> Knives Out
demanding -> The Prestige
challenging -> Mulholland Drive

WEIGHT:
very_light -> School of Rock
light -> Ocean's Eleven
moderate -> Her
heavy -> Manchester by the Sea
crushing -> Requiem for a Dream

PACE:
very_slow -> Paterson
slow -> Lost in Translation
moderate -> The Martian
fast -> Inception
relentless -> Mad Max: Fury Road

Respond ONLY with valid JSON.

Example:
{
"valence": "warm",
"arousal": "moderate",
"complexity": "simple",
"weight": "light",
"pace": "moderate"
}
"""


def _build_user_prompt(movie):
    genres = ", ".join(g["name"] for g in movie.get("genres", []))
    keywords = ", ".join(k["name"] for k in movie.get("keywords", []))
    return f"""Title: {movie.get("title")}
Overview: {movie.get("overview")}
Genres: {genres}
Keywords: {keywords}
Runtime: {movie.get("runtime")} minutes"""


def _parse_response(content):
    content = content.strip()
    if content.startswith("```"):
        content = content.split("```")[1]
        if content.startswith("json"):
            content = content[4:]

    try:
        bins = json.loads(content.strip())
        scores = {
            dim: config.MOOD_SCORES[dim].get(bins.get(dim, "moderate"), 0.0)
            for dim in config.MOOD_SCORES
        }
        return scores, bins
    except (json.JSONDecodeError, KeyError):
        print(f"\n⚠ Could not parse model response. Raw output:\n{content}\n")
        return {dim: 0.0 for dim in config.MOOD_SCORES}, {}


def get_mood(movie, debug=False):
    payload = {
        "model": config.MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": _build_user_prompt(movie)},
        ],
        "stream": False,
    }
    response = requests.post(f"{BASE_URL}/api/chat", json=payload)
    if response.status_code != 200:
        response.raise_for_status()

    content = response.json()["message"]["content"]
    scores, bins = _parse_response(content)

    if debug:
        print(f"\n── Mood: {movie.get('title')} ──")
        print(f"Bins:   {bins}")
        print(f"Scores: {scores}\n")

    return scores, bins