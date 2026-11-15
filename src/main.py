"""Command-line demonstration of the music recommendation system."""

from pathlib import Path
from .recommender import load_songs, recommend_songs

CATALOG = Path(__file__).resolve().parent.parent / "data" / "songs.csv"

PROFILES = {
    "Happy Pop": {"genre": "pop", "mood": "happy", "energy": 0.80},
    "High-Energy Pop": {"genre": "pop", "mood": "intense", "energy": 0.93},
    "Chill Lofi": {"genre": "lofi", "mood": "chill", "energy": 0.35},
    "Intense Rock": {"genre": "rock", "mood": "intense", "energy": 0.92},
    "Conflicting Taste (Sad EDM)": {"genre": "edm", "mood": "sad", "energy": 0.90},
}


def main() -> None:
    """Print top-five recommendations for several different music tastes."""
    songs = load_songs(str(CATALOG))
    print(f"Loaded songs: {len(songs)}")
    for name, prefs in PROFILES.items():
        print(f"\n{name} (genre={prefs['genre']}, mood={prefs['mood']}, energy={prefs['energy']:.2f})")
        for index, (song, score, reasons) in enumerate(recommend_songs(prefs, songs, k=5), start=1):
            print(f"  {index}. {song['title']} - Score: {score:.2f}")
            print(f"     Because: {reasons}")


if __name__ == "__main__":
    main()
