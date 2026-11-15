"""Functional and object-oriented tests for the recommender."""

from pathlib import Path
import pytest
from src.recommender import Song, UserProfile, Recommender, load_songs, score_song, recommend_songs

CATALOG = Path(__file__).resolve().parent.parent / "data" / "songs.csv"


def make_small_recommender() -> Recommender:
    songs = [
        Song(1, "Test Pop Track", "Test Artist", "pop", "happy", 0.8, 120, 0.9, 0.8, 0.2),
        Song(2, "Chill Lofi Loop", "Test Artist", "lofi", "chill", 0.4, 80, 0.6, 0.5, 0.9),
    ]
    return Recommender(songs)


def test_recommend_returns_songs_sorted_by_score():
    user = UserProfile("pop", "happy", 0.8, False)
    results = make_small_recommender().recommend(user, k=2)
    assert len(results) == 2
    assert results[0].genre == "pop"
    assert results[0].mood == "happy"


def test_explain_recommendation_returns_non_empty_string():
    user = UserProfile("pop", "happy", 0.8, False)
    rec = make_small_recommender()
    explanation = rec.explain_recommendation(user, rec.songs[0])
    assert "genre match" in explanation
    assert "energy gap" in explanation


def test_catalog_loads_typed_numbers():
    songs = load_songs(str(CATALOG))
    assert len(songs) == 18
    assert isinstance(songs[0]["id"], int)
    assert all(isinstance(s[field], float) for s in songs for field in ("energy", "tempo_bpm", "valence", "danceability", "acousticness"))
    assert len({song["id"] for song in songs}) == len(songs)


def test_exact_match_outscores_wrong_genre_and_mood():
    songs = load_songs(str(CATALOG))
    user = {"genre": "pop", "mood": "happy", "energy": 0.82}
    match = next(s for s in songs if s["title"] == "Sunrise City")
    mismatch = next(s for s in songs if s["title"] == "Storm Runner")
    score, reasons = score_song(user, match)
    assert score == pytest.approx(4.0)
    assert len(reasons) == 3
    assert score > score_song(user, mismatch)[0]


def test_energy_closeness_increases_score():
    songs = load_songs(str(CATALOG))
    song = songs[0]
    prefs = {"genre": "other", "mood": "other", "energy": 0.82}
    exact, _ = score_song(prefs, song)
    far, _ = score_song({**prefs, "energy": 0.12}, song)
    assert exact > far


def test_ranking_sorted_and_catalog_unchanged():
    songs = load_songs(str(CATALOG))
    before = [s["id"] for s in songs]
    results = recommend_songs({"genre": "lofi", "mood": "chill", "energy": 0.35}, songs, k=5)
    assert len(results) == 5
    assert [item[1] for item in results] == sorted((item[1] for item in results), reverse=True)
    assert [s["id"] for s in songs] == before
    assert results[0][0]["title"] == "Library Rain"
    assert all(reason for _, _, reason in results)


def test_k_limits_and_missing_matches():
    songs = load_songs(str(CATALOG))
    prefs = {"genre": "opera", "mood": "mysterious", "energy": 0.5}
    assert recommend_songs(prefs, songs, k=0) == []
    assert len(recommend_songs(prefs, songs, k=100)) == len(songs)
    assert len(recommend_songs(prefs, songs, k=5)) == 5


def test_alternative_weights_change_scores():
    songs = load_songs(str(CATALOG))
    prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}
    baseline = recommend_songs(prefs, songs)
    shifted = recommend_songs(prefs, songs, weights={"genre": 1.0, "energy": 2.0})
    assert shifted[0][1] != baseline[0][1]


def test_acoustic_preference_used_in_oop():
    rec = make_small_recommender()
    user = UserProfile("pop", "happy", 0.8, True)
    assert "acoustic fit" in rec.explain_recommendation(user, rec.songs[0])


def test_invalid_energy_is_rejected():
    songs = load_songs(str(CATALOG))
    with pytest.raises(ValueError):
        score_song({"genre": "pop", "mood": "happy", "energy": 1.5}, songs[0])
