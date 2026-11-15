"""Compare original weights with an energy-focused scoring experiment."""

from .main import CATALOG, PROFILES
from .recommender import load_songs, recommend_songs


def main() -> None:
    """Print top five songs before and after changing the scoring weights."""
    songs = load_songs(str(CATALOG))
    for name in ("Happy Pop", "Chill Lofi", "Intense Rock", "Conflicting Taste (Sad EDM)"):
        prefs = PROFILES[name]
        old = recommend_songs(prefs, songs, k=5)
        new = recommend_songs(prefs, songs, k=5, weights={"genre": 1.0, "energy": 2.0})
        print(f"\n{name}")
        print("Before (genre=2, mood=1, energy=1):")
        for i, (song, score, _) in enumerate(old, 1):
            print(f"  {i}. {song['title']} ({score:.2f})")
        print("After (genre=1, mood=1, energy=2):")
        for i, (song, score, _) in enumerate(new, 1):
            print(f"  {i}. {song['title']} ({score:.2f})")


if __name__ == "__main__":
    main()
