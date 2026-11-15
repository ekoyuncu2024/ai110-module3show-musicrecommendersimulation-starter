# Model Card: TuneMatch 1.0

## 1. Model Name

TuneMatch 1.0 — a basic music recommendation simulator.

## 2. Intended Use

This program recommends songs from a small sample catalog based on a person's genre, mood, and energy preferences. It is meant for a classroom project, not a real music streaming service. It assumes a user can describe their taste using a few simple values. It should not be used to measure someone's actual interests or to make important decisions about them.

## 3. How the Model Works

I used a content-based scoring system. Each song has a genre, mood, energy level, tempo, valence, danceability, and acousticness. The main score gives 2 points for a matching genre and 1 point for a matching mood. It also gives up to 1 point based on how close the song's energy is to the user's target. A perfect energy match gets the full point, rather than a higher-energy song automatically getting a better score. If an acoustic preference is provided, acousticness can add up to 0.25 points. The system sorts the songs by their final scores and shows the five highest ones along with the reasons.

Unlike Spotify or other large services, this program does not learn from listening history or compare users with each other. Real platforms can also use collaborative filtering, while this simulation only compares song attributes to the user's selected preferences.

## 4. Data

I kept the starter's 10 fictional songs and added 8 more, making 18 songs total. The new songs include folk, hip-hop, EDM, classical, Latin, country, metal, and indie. The catalog includes happy, chill, intense, focused, relaxed, sad, and other moods. Each row has a unique ID and numerical values for energy, tempo, valence, danceability, and acousticness. The program uses a small, made-up sample rather than actual listener data. Most genres still have only one song, so the available choices are limited.

## 5. Strengths

The system gave results that made sense for the main test profiles. Happy Pop ranked *Sunrise City* first, Chill Lofi ranked *Library Rain* first, and Intense Rock ranked *Storm Runner* first. The reasons also make it easy to see why each song was chosen. It is useful for understanding how changing a weight can change recommendations.

## 6. Limitations and Bias

The system gives matching genres twice as many points as matching moods, which can keep the recommendations too close to one genre. During the weight experiment, the Happy Pop profile ranked *Gym Hero* second at first, even though its mood was intense instead of happy. When energy mattered more and genre mattered less, it dropped to fourth. This shows how the weights can favor certain songs even when the mood is wrong. Most genres have only one song, so the system also cannot give much variety within those genres. It does not understand lyrics, personal history, sarcasm in song descriptions, or whether a person actually likes the artist. These gaps could create a filter bubble if a larger system kept reinforcing the same kinds of songs.

## 7. Evaluation

I tested the original 2/1/1 weights with Happy Pop, High-Energy Pop, Chill Lofi, Intense Rock, and a conflicting Sad EDM profile. Each time I looked at the top five song titles, scores, and explanations. I also ran 10 automated checks for CSV loading, score calculation, ranking, the object-based recommender, and edge cases. The full terminal output is in the README, and the experiment can be rerun with `python -m src.experiment`.

- **Happy Pop vs. High-Energy Pop:** *Sunrise City* led the happy profile, while *Gym Hero* led the intense profile. Changing the mood and target energy explained the switch.
- **Happy Pop vs. Chill Lofi:** *Sunrise City* was first for Happy Pop, but *Library Rain* was first for Chill Lofi. The lower energy and different genre changed the ranking.
- **Happy Pop vs. Intense Rock:** The rock profile put *Storm Runner* first. Both profiles preferred fairly energetic songs, but genre and mood changed which song ranked highest.
- **Happy Pop vs. Sad EDM:** *Sunrise City* matched both the pop genre and the happy mood for Happy Pop. Sad EDM ranked *Electric Summer* first because it matched the genre and was close in energy, even with a different mood.
- **High-Energy Pop vs. Chill Lofi:** *Gym Hero* fit the intense mood and high energy of the pop profile, while *Library Rain* fit the chill mood and much lower energy of the lofi profile.
- **High-Energy Pop vs. Intense Rock:** Both profiles had an intense mood and nearly the same energy target. *Gym Hero* and *Storm Runner* switched places near the top because their genres fit different profiles.
- **High-Energy Pop vs. Sad EDM:** Both profiles wanted high energy. High-Energy Pop found a track that matched all three preferences in *Gym Hero*. Sad EDM put *Electric Summer* first and *Last Train Home* second because one matched the genre and the other matched the mood.
- **Chill Lofi vs. Intense Rock:** Their top songs were different in both style and energy. *Library Rain* fit the low-energy chill preference, while *Storm Runner* fit the intense rock preference.
- **Chill Lofi vs. Sad EDM:** The conflicting profile ranked *Electric Summer* first even though it was marked happy, not sad, because EDM genre matched and the energy was close. That was an example of a technically valid result that might not feel right to a listener.
- **Intense Rock vs. Sad EDM:** Both preferred high energy, but the rock profile picked *Storm Runner* and the EDM profile picked *Electric Summer*. Genre matching had more influence than the difference in mood.

For the experiment, I changed genre weight from 2 to 1 and energy weight from 1 to 2, leaving mood at 1. In Happy Pop, *Rooftop Lights* moved from third to second, and *Gym Hero* moved from second to fourth. The top result stayed the same. This experiment changed the recommendations, but without real user feedback I cannot say whether it made them more accurate.

## 8. Future Work

1. Add more songs in each genre and mood so the recommendations are less repetitive.
2. Let users rate or skip songs, then update their preferences from that feedback.
3. Include a small amount of variety in the top results instead of only picking the closest matches.

## 9. Personal Reflection

The biggest thing I learned is how much the weights matter. I thought genre, mood, and energy would naturally work together, but changing one weight can move a song several spots. An AI assistant helped me plan the scoring formula and create test cases. I still had to check the actual output because a score can be mathematically correct without making a good recommendation. I was surprised that such a simple system could give results that mostly felt reasonable. If I kept working on it, I would start by adding more songs and using listening feedback to see if the suggestions really improve.
