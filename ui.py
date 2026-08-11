import recommender, tmdb_client, feedback, session


def get_user_input():
    return input("\nEnter a movie title: ").strip()


def disambiguate(results):
    print("\nFound multiple matches:")
    for i, movie in enumerate(results):
        year = movie.get("release_date", "")[:4]
        print(f"  {i + 1}. {movie['title']} ({year})")
    print("  0. None of these")

    choice = input("\nPick a number: ").strip()
    if not choice.isdigit() or int(choice) == 0:
        return None
    index = int(choice) - 1
    if index >= len(results):
        return None
    return results[index]


def confirm(movie):
    year = movie.get("release_date", "")[:4]
    answer = input(f"\nFound: {movie['title']} ({year}). Is this the one? (y/n): ").strip().lower()
    return answer == "y"


def display_results(recommendations, start=0):
    batch = recommendations[start:start + 3]
    print("\n🎬 Recommendations:")
    for i, movie in enumerate(batch):
        year = movie.get("release_date", "")[:4]
        print(f"\n  {start + i + 1}. {movie['title']} ({year})")
        print(f"     Score: {movie['score']:.2f}")
        print(f"     Why: {movie['reason']}")


def ask_next_action(recommendations, start, seed_id, session_id):
    print("\nWhat would you like to do?")
    print("  1. See next 3")
    print("  2. Pick a recommendation to watch")
    print("  3. Quit")

    choice = input("\nYour choice: ").strip()

    if choice == "1":
        # Mark the current batch as skipped
        batch = recommendations[start:start + 3]
        for movie in batch:
            feedback.record(
                candidate_movie_id=movie["id"],
                reaction="skipped",
                session_id=session_id,
                seed_movie_id=seed_id,
                position=movie["position"],
                score=movie["score"],
                mood_context=movie.get("mood_context", {}),
            )
        return "next", None

    elif choice == "2":
        pick = input("Enter the number of the movie: ").strip()
        if pick.isdigit():
            index = int(pick) - 1
            if 0 <= index < len(recommendations):
                chosen = recommendations[index]
                feedback.record(
                    candidate_movie_id=chosen["id"],
                    reaction="accepted",
                    session_id=session_id,
                    seed_movie_id=seed_id,
                    position=chosen["position"],
                    score=chosen["score"],
                    mood_context=chosen.get("mood_context", {}),
                )
                return "new_seed", chosen

    return "quit", None


def run():
    print("🎬 Movie Recommender")
    session_id = session.current_session()

    while True:
        title = get_user_input()
        results = tmdb_client.search_movies(title)

        if not results:
            print("No movies found. Try a different title.")
            continue

        if len(results) == 1:
            movie = results[0]
            if not confirm(movie):
                continue
        else:
            movie = disambiguate(results)
            if not movie:
                continue

        seed_id = movie["id"]
        recommendations = recommender.get_recommendations(seed_id)
        start = 0
        display_results(recommendations, start)

        while True:
            action, new_seed = ask_next_action(recommendations, start, seed_id, session_id)

            if action == "next":
                start += 3
                if start >= len(recommendations):
                    print("No more recommendations.")
                    start -= 3
                else:
                    display_results(recommendations, start)

            elif action == "new_seed":
                seed_id = new_seed["id"]
                recommendations = recommender.get_recommendations(seed_id)
                start = 0
                display_results(recommendations, start)

            else:
                print("\nGoodbye! 🎬")
                return


if __name__ == "__main__":
    run()
