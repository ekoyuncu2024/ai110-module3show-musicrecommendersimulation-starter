# Music Recommender Simulation

I made a small music recommendation program that ranks songs based on a user's genre, mood, and energy preferences. It reads a CSV file, gives every song a score, then prints the top five with short explanations. I also tested several different preferences to see when the rankings make sense and when the scoring rules cause problems.

## How The System Works

Each song has an ID, title, artist, genre, mood, energy, tempo, valence, danceability, and acousticness. The user gives a preferred genre, mood, and target energy between 0 and 1. The object-oriented `UserProfile` also includes whether the user likes acoustic music.

My algorithm recipe is:

- **Genre match:** +2.0 points.
- **Mood match:** +1.0 point.
- **Energy similarity:** `1 - abs(song_energy - target_energy)` points (up to +1.0). This rewards being close to the target, rather than being as energetic as possible.
- **Optional acoustic preference:** up to +0.25 points when the user supplies `likes_acoustic`; it does not affect the default CLI profiles.
- **Rank:** calculate a score for every song, sort from highest to lowest, and return the top `k`. Ties go to the lower song ID.

`score_song()` returns both the number and a list of reasons. `recommend_songs()` scores every song and ranks them. The `Song`, `UserProfile`, and `Recommender` classes provide an object-oriented version that shares the same scoring rules. The CLI uses the dictionary-based functions. The design stays simple on purpose.

```text
songs.csv + user preferences
            |
      score each song
            |
   sort highest to lowest
            |
     show top 5 + reasons
```

This is **content-based filtering** because it compares song attributes with a user's preferences. Real services can also use **collaborative filtering**, which looks at patterns among listeners, such as likes, skips, and playlists. Our version does not collect those interactions or train a machine learning model. A possible bias is that genre matches receive more points than mood, so songs from the same genre can be ranked above songs that fit a user's mood better.

## Getting Started

Requires Python 3.9 or later. From the project root:

```bash
python -m pip install -r requirements.txt
python -m src.main
```

To run the scoring experiment:

```bash
python -m src.experiment
```

To run the tests:

```bash
python -m pytest -q
```

## Sample Recommendation Output

The following is actual terminal output from `python -m src.main`, with 18 songs loaded. Each profile shows its five highest-scoring songs.

```text
Loaded songs: 18
```

### Happy Pop

```text
Happy Pop (genre=pop, mood=happy, energy=0.80)
  1. Sunrise City - Score: 3.98
     Because: genre match (+2.00); mood match (+1.00); energy gap 0.02 (+0.98)
  2. Gym Hero - Score: 2.87
     Because: genre match (+2.00); energy gap 0.13 (+0.87)
  3. Rooftop Lights - Score: 1.96
     Because: mood match (+1.00); energy gap 0.04 (+0.96)
  4. Street Festival - Score: 1.91
     Because: mood match (+1.00); energy gap 0.09 (+0.91)
  5. Electric Summer - Score: 1.85
     Because: mood match (+1.00); energy gap 0.15 (+0.85)
```

### High-Energy Pop

```text
High-Energy Pop (genre=pop, mood=intense, energy=0.93)
  1. Gym Hero - Score: 4.00
     Because: genre match (+2.00); mood match (+1.00); energy gap 0.00 (+1.00)
  2. Sunrise City - Score: 2.89
     Because: genre match (+2.00); energy gap 0.11 (+0.89)
  3. Storm Runner - Score: 1.98
     Because: mood match (+1.00); energy gap 0.02 (+0.98)
  4. Steel Horizon - Score: 1.95
     Because: mood match (+1.00); energy gap 0.05 (+0.95)
  5. Electric Summer - Score: 0.98
     Because: energy gap 0.02 (+0.98)
```

### Chill Lofi

```text
Chill Lofi (genre=lofi, mood=chill, energy=0.35)
  1. Library Rain - Score: 4.00
     Because: genre match (+2.00); mood match (+1.00); energy gap 0.00 (+1.00)
  2. Midnight Coding - Score: 3.93
     Because: genre match (+2.00); mood match (+1.00); energy gap 0.07 (+0.93)
  3. Focus Flow - Score: 2.95
     Because: genre match (+2.00); energy gap 0.05 (+0.95)
  4. Spacewalk Thoughts - Score: 1.93
     Because: mood match (+1.00); energy gap 0.07 (+0.93)
  5. Coffee Shop Stories - Score: 0.98
     Because: energy gap 0.02 (+0.98)
```

### Intense Rock

```text
Intense Rock (genre=rock, mood=intense, energy=0.92)
  1. Storm Runner - Score: 3.99
     Because: genre match (+2.00); mood match (+1.00); energy gap 0.01 (+0.99)
  2. Gym Hero - Score: 1.99
     Because: mood match (+1.00); energy gap 0.01 (+0.99)
  3. Steel Horizon - Score: 1.94
     Because: mood match (+1.00); energy gap 0.06 (+0.94)
  4. Electric Summer - Score: 0.97
     Because: energy gap 0.03 (+0.97)
  5. Sunrise City - Score: 0.90
     Because: energy gap 0.10 (+0.90)
```

### Conflicting Taste (Sad EDM)

```text
Conflicting Taste (Sad EDM) (genre=edm, mood=sad, energy=0.90)
  1. Electric Summer - Score: 2.95
     Because: genre match (+2.00); energy gap 0.05 (+0.95)
  2. Last Train Home - Score: 1.49
     Because: mood match (+1.00); energy gap 0.51 (+0.49)
  3. Storm Runner - Score: 0.99
     Because: energy gap 0.01 (+0.99)
  4. Gym Hero - Score: 0.97
     Because: energy gap 0.03 (+0.97)
  5. Sunrise City - Score: 0.92
     Because: energy gap 0.08 (+0.92)
```

## Experiments You Tried

I tested the default Happy Pop profile, High-Energy Pop, Chill Lofi, Intense Rock, and an unusual combination of sad mood with high-energy EDM. The last one was useful because the best-scoring song did not actually have a sad mood. It ranked first because it matched the genre and had similar energy.

I also tested a weight change: **genre from 2.0 to 1.0** and **energy from 1.0 to 2.0**, with mood staying at 1.0. This makes the energy fit more important than before. The experiment is repeatable with `python -m src.experiment`.

```text
Happy Pop
Before (genre=2, mood=1, energy=1):
  1. Sunrise City (3.98)
  2. Gym Hero (2.87)
  3. Rooftop Lights (1.96)
  4. Street Festival (1.91)
  5. Electric Summer (1.85)
After (genre=1, mood=1, energy=2):
  1. Sunrise City (3.96)
  2. Rooftop Lights (2.92)
  3. Street Festival (2.82)
  4. Gym Hero (2.74)
  5. Electric Summer (2.70)

Chill Lofi
Before (genre=2, mood=1, energy=1):
  1. Library Rain (4.00)
  2. Midnight Coding (3.93)
  3. Focus Flow (2.95)
  4. Spacewalk Thoughts (1.93)
  5. Coffee Shop Stories (0.98)
After (genre=1, mood=1, energy=2):
  1. Library Rain (4.00)
  2. Midnight Coding (3.86)
  3. Focus Flow (2.90)
  4. Spacewalk Thoughts (2.86)
  5. Coffee Shop Stories (1.96)

Intense Rock
Before (genre=2, mood=1, energy=1):
  1. Storm Runner (3.99)
  2. Gym Hero (1.99)
  3. Steel Horizon (1.94)
  4. Electric Summer (0.97)
  5. Sunrise City (0.90)
After (genre=1, mood=1, energy=2):
  1. Storm Runner (3.98)
  2. Gym Hero (2.98)
  3. Steel Horizon (2.88)
  4. Electric Summer (1.94)
  5. Sunrise City (1.80)

Conflicting Taste (Sad EDM)
Before (genre=2, mood=1, energy=1):
  1. Electric Summer (2.95)
  2. Last Train Home (1.49)
  3. Storm Runner (0.99)
  4. Gym Hero (0.97)
  5. Sunrise City (0.92)
After (genre=1, mood=1, energy=2):
  1. Electric Summer (2.90)
  2. Storm Runner (1.98)
  3. Last Train Home (1.98)
  4. Gym Hero (1.94)
  5. Sunrise City (1.84)
```

For Happy Pop, the top song stayed *Sunrise City*, but *Gym Hero* fell from second to fourth, while *Rooftop Lights* moved up from third to second. The new results pay more attention to energy and less to an exact genre match. That makes the rankings different, but I cannot say they are more accurate without real listener feedback.

## Limitations and Risks

The catalog has just 18 made-up songs, with most genres represented by only one track. This means some profiles have few good matches. The system can also favor the wrong mood if a song matches the genre and energy. It ignores lyrics, listening history, favorite artists, and whether someone likes discovering new genres. Recommending more of the same music could create a filter bubble over time.

## Reflection

I learned that a recommendation system is not just about calculating a score. The weights decide what matters most, and changing them can make the same songs appear in a different order. Testing multiple profiles helped me see that a result can be mathematically correct and still seem strange for a real listener.

I used an AI assistant to help plan the scoring formula and organize tests, but I checked the actual program output and the experiment results. If I expanded this project, I would add more songs and let users give feedback so the scores could reflect what they really enjoy.

For the full evaluation, bias discussion, intended use, and future improvements, see [the Model Card](model_card.md).
