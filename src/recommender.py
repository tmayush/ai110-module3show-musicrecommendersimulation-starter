from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def _score(self, user: UserProfile, song: Song) -> float:
        """Computes a score for a song given a user profile."""
        score = 0.0
        if song.genre.lower() == user.favorite_genre.lower():
            score += 2.0
        if song.mood.lower() == user.favorite_mood.lower():
            score += 1.5
        score += 1.0 - abs(song.energy - user.target_energy)
        if user.likes_acoustic and song.acousticness > 0.7:
            score += 0.5
        return round(score, 2)

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Returns the top k songs ranked by score for the given user."""
        ranked = sorted(self.songs, key=lambda s: self._score(user, s), reverse=True)
        return ranked[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Returns a human-readable explanation of why a song was recommended."""
        parts = []
        if song.genre.lower() == user.favorite_genre.lower():
            parts.append("genre match (+2.0)")
        if song.mood.lower() == user.favorite_mood.lower():
            parts.append("mood match (+1.5)")
        energy_score = round(1.0 - abs(song.energy - user.target_energy), 2)
        parts.append(f"energy similarity (+{energy_score})")
        if user.likes_acoustic and song.acousticness > 0.7:
            parts.append("acoustic bonus (+0.5)")
        total = self._score(user, song)
        return f"Score: {total} — " + "; ".join(parts)

def load_songs(csv_path: str) -> List[Dict]:
    """Loads songs from a CSV file and converts numeric fields to floats."""
    import csv

    songs = []
    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["id"] = int(row["id"])
            row["energy"] = float(row["energy"])
            row["tempo_bpm"] = float(row["tempo_bpm"])
            row["valence"] = float(row["valence"])
            row["danceability"] = float(row["danceability"])
            row["acousticness"] = float(row["acousticness"])
            songs.append(row)

    print(f"Loaded songs: {len(songs)}")
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Scores a single song against user preferences and returns (score, reasons)."""
    score = 0.0
    reasons = []

    # Genre match: +2.0
    if song["genre"].lower() == user_prefs["genre"].lower():
        score += 2.0
        reasons.append("genre match (+2.0)")

    # Mood match: +1.5
    if song["mood"].lower() == user_prefs["mood"].lower():
        score += 1.5
        reasons.append("mood match (+1.5)")

    # Energy similarity: up to +1.0 (closer to target = more points)
    energy_diff = abs(song["energy"] - user_prefs["energy"])
    energy_score = round(1.0 - energy_diff, 2)
    score += energy_score
    reasons.append(f"energy similarity (+{energy_score})")

    # Acousticness bonus: +0.5 if user likes acoustic and song is acoustic
    if user_prefs.get("likes_acoustic") and song["acousticness"] > 0.7:
        score += 0.5
        reasons.append("acoustic bonus (+0.5)")

    return round(score, 2), reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Scores all songs, ranks them, and returns the top k with explanations."""
    scored = []
    for song in songs:
        song_score, reasons = score_song(user_prefs, song)
        explanation = "; ".join(reasons)
        scored.append((song, song_score, explanation))

    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:k]
