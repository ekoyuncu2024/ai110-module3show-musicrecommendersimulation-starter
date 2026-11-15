"""Simple, explainable content-based music recommendations."""

import csv
from dataclasses import asdict, dataclass
from math import isfinite
from typing import Dict, List, Optional, Tuple

DEFAULT_WEIGHTS = {"genre": 2.0, "mood": 1.0, "energy": 1.0, "acoustic": 0.25}
NUMERIC_FIELDS = ("energy", "tempo_bpm", "valence", "danceability", "acousticness")


@dataclass
class Song:
    """Store the attributes for one song."""

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
    """Store a user's genre, mood, energy, and acoustic preferences."""

    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


class Recommender:
    """Object-oriented interface that uses the same scoring rules as the CLI."""

    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top k Song objects, highest scoring first."""
        prefs = asdict(user)
        ranked = sorted(
            self.songs,
            key=lambda song: (-score_song(prefs, asdict(song))[0], song.id),
        )
        return ranked[:max(0, k)]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Describe why a song received its score."""
        _, reasons = score_song(asdict(user), asdict(song))
        return "; ".join(reasons)


def load_songs(csv_path: str) -> List[Dict]:
    """Load a song CSV, converting ID and all numeric features."""
    songs = []
    with open(csv_path, newline="", encoding="utf-8-sig") as handle:
        for row in csv.DictReader(handle):
            row["id"] = int(row["id"])
            for field in NUMERIC_FIELDS:
                row[field] = float(row[field])
            songs.append(row)
    return songs


def score_song(
    user_prefs: Dict, song: Dict, weights: Optional[Dict[str, float]] = None
) -> Tuple[float, List[str]]:
    """Score one song and list the reasons for its score."""
    w = DEFAULT_WEIGHTS.copy()
    if weights is not None:
        w.update(weights)

    genre = user_prefs.get("genre", user_prefs.get("favorite_genre", ""))
    mood = user_prefs.get("mood", user_prefs.get("favorite_mood", ""))
    energy = float(user_prefs.get("energy", user_prefs.get("target_energy", 0.5)))
    if not isfinite(energy) or not 0 <= energy <= 1:
        raise ValueError("Target energy must be between 0 and 1")

    score = 0.0
    reasons = []
    if str(song["genre"]).casefold() == str(genre).casefold():
        score += w["genre"]
        reasons.append(f"genre match (+{w['genre']:.2f})")
    if str(song["mood"]).casefold() == str(mood).casefold():
        score += w["mood"]
        reasons.append(f"mood match (+{w['mood']:.2f})")

    gap = abs(float(song["energy"]) - energy)
    energy_points = max(0.0, 1.0 - gap) * w["energy"]
    score += energy_points
    reasons.append(f"energy gap {gap:.2f} (+{energy_points:.2f})")

    if "likes_acoustic" in user_prefs:
        acoustic = float(song["acousticness"])
        acoustic_fit = acoustic if user_prefs["likes_acoustic"] else 1.0 - acoustic
        acoustic_points = max(0.0, min(1.0, acoustic_fit)) * w["acoustic"]
        score += acoustic_points
        reasons.append(f"acoustic fit (+{acoustic_points:.2f})")

    return round(score, 4), reasons


def recommend_songs(
    user_prefs: Dict,
    songs: List[Dict],
    k: int = 5,
    weights: Optional[Dict[str, float]] = None,
) -> List[Tuple[Dict, float, str]]:
    """Score all songs, rank them, and return the top k with reasons."""
    results = []
    for song in songs:
        score, reasons = score_song(user_prefs, song, weights)
        results.append((song, score, "; ".join(reasons)))
    # sorted() produces a new list, leaving the original catalog alone.
    ranked = sorted(results, key=lambda item: (-item[1], int(item[0]["id"])))
    return ranked[:max(0, k)]
