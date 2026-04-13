"""
Command line runner for the Music Recommender Simulation.

Loads songs from CSV, runs the recommender against multiple user profiles,
and prints ranked results with explanations.
"""

import os

from recommender import load_songs, recommend_songs

# Resolve paths relative to project root (parent of src/)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def print_recommendations(profile_name: str, user_prefs: dict, songs: list, weights: dict = None) -> None:
    """Prints the top 5 recommendations for a given profile."""
    print(f"\n{'='*60}")
    print(f"  Profile: {profile_name}")
    print(f"  Prefs: genre={user_prefs['genre']}, mood={user_prefs['mood']}, "
          f"energy={user_prefs['energy']}, acoustic={user_prefs.get('likes_acoustic', False)}")
    if weights:
        print(f"  Weights: {weights}")
    print(f"{'='*60}")

    recommendations = recommend_songs(user_prefs, songs, k=5, weights=weights)

    for i, (song, score, explanation) in enumerate(recommendations, 1):
        print(f"\n  {i}. {song['title']} by {song['artist']}")
        print(f"     Genre: {song['genre']} | Mood: {song['mood']} | Energy: {song['energy']}")
        print(f"     Score: {score:.2f}")
        print(f"     Because: {explanation}")

    print()


def main() -> None:
    songs = load_songs(os.path.join(PROJECT_ROOT, "data", "songs.csv"))

    # Profile 1: Happy Pop Fan
    pop_happy = {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.8,
        "likes_acoustic": False,
    }

    # Profile 2: Chill Lofi Listener
    chill_lofi = {
        "genre": "lofi",
        "mood": "chill",
        "energy": 0.35,
        "likes_acoustic": True,
    }

    # Profile 3: Intense Rock Enthusiast
    intense_rock = {
        "genre": "rock",
        "mood": "intense",
        "energy": 0.9,
        "likes_acoustic": False,
    }

    profiles = [
        ("Happy Pop Fan", pop_happy),
        ("Chill Lofi Listener", chill_lofi),
        ("Intense Rock Enthusiast", intense_rock),
    ]

    for name, prefs in profiles:
        print_recommendations(name, prefs, songs)

    # --- Experiment: Weight Shift ---
    # Double energy weight, halve genre weight to test sensitivity
    experimental_weights = {"genre": 1.0, "mood": 1.5, "energy": 2.0, "acoustic": 0.5}

    print("\n" + "#" * 60)
    print("  EXPERIMENT: Energy x2, Genre /2")
    print("#" * 60)

    for name, prefs in profiles:
        print_recommendations(f"{name} [experimental]", prefs, songs, weights=experimental_weights)


if __name__ == "__main__":
    main()
