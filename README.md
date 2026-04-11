# 🎵 Music Recommender Simulation

## Project Summary

This project is a content-based music recommender that scores songs from a small CSV catalog against a user's taste profile. Each song gets points for matching genre, mood, and having similar energy levels. The system then ranks all songs and returns the top picks with explanations of why each song was recommended.

---

## How The System Works

Real streaming platforms like Spotify use a mix of **collaborative filtering** (looking at what similar users listen to) and **content-based filtering** (matching song attributes to your taste). Collaborative filtering is powerful at scale but needs tons of user data. Our simulation focuses on content-based filtering since we're working with a small catalog and a single user profile.

### Song Features

Each `Song` in our system has these attributes:
- **genre** — categorical label (pop, lofi, rock, edm, etc.)
- **mood** — categorical label (happy, chill, intense, sad, relaxed, focused, moody)
- **energy** — numerical score from 0.0 to 1.0
- **tempo_bpm** — beats per minute
- **valence** — musical positivity from 0.0 to 1.0
- **danceability** — how danceable, from 0.0 to 1.0
- **acousticness** — how acoustic, from 0.0 to 1.0

### User Profile

A `UserProfile` stores:
- `favorite_genre` — the genre the user prefers
- `favorite_mood` — the mood the user gravitates toward
- `target_energy` — their ideal energy level (0.0–1.0)
- `likes_acoustic` — whether they prefer acoustic-heavy tracks

### Algorithm Recipe

The scoring logic awards points per song:
- **+2.0 points** for a genre match
- **+1.5 points** for a mood match
- **Up to +1.0 point** for energy similarity (closer = more points, calculated as `1.0 - abs(song_energy - target_energy)`)
- **+0.5 points** for acousticness bonus (if the user likes acoustic and the song's acousticness > 0.7)

Songs are scored individually, sorted highest-to-lowest, and the top K are returned.

### Data Flow

```
Input (User Preferences) → Score each song in CSV → Sort by score → Output top K recommendations
```

### Potential Biases

This system might over-prioritize genre since it carries the heaviest weight (+2.0). A great song that matches mood and energy perfectly but is in the wrong genre will score lower than a mediocre genre match. The small dataset also means some genres are overrepresented (e.g., multiple lofi tracks).

---

## Getting Started

### Setup

1. Install dependencies with UV:

```bash
uv sync
```

2. Run the app:

```bash
uv run python -m src.main
```

### Running Tests

```bash
uv run pytest
```

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this


---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}  

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

Give your recommender a name, for example:

> VibeFinder 1.0

---

## 2. Intended Use

- What is this system trying to do
- Who is it for

Example:

> This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

---

## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

- What features of each song does it consider
- What information about the user does it use
- How does it turn those into a number

Try to avoid code in this section, treat it like an explanation to a non programmer.

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

---

## 5. Strengths

Where does your recommender work well

You can think about:
- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:
- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

---

## 7. Evaluation

How did you check your system

Examples:
- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"

