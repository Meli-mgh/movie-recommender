import recommender, tmdb_client

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

def ask_next_action(recommendations, start):
    print("\nWhat would you like to do?")
    print("  1. See next 3")
    print("  2. Pick a recommendation as new seed")
    print("  3. Quit")
    
    choice = input("\nYour choice: ").strip()
    
    if choice == "1":
        return "next", None
    elif choice == "2":
        pick = input("Enter the number of the movie: ").strip()
        if pick.isdigit():
            index = int(pick) - 1
            if 0 <= index < len(recommendations):
                return "new_seed", recommendations[index]
    return "quit", None

def run():
    print("🎬 Movie Recommender")
    
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
        
        recommendations = recommender.get_recommendations(movie["id"])
        start = 0
        display_results(recommendations, start)
        
        while True:
            action, new_seed = ask_next_action(recommendations, start)
            
            if action == "next":
                start += 3
                if start >= len(recommendations):
                    print("No more recommendations.")
                    start -= 3
                else:
                    display_results(recommendations, start)
            
            elif action == "new_seed":
                recommendations = recommender.get_recommendations(new_seed["id"])
                start = 0
                display_results(recommendations, start)
            
            else:
                print("\nGoodbye! 🎬")
                return

if __name__ == "__main__":
    run()