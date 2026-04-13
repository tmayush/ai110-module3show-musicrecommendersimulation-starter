# Model Card: Music Recommender Simulation

## 1. Model Name

VibeFinder 1.0

---

## 2. Intended use

This is a classroom simulation. It recommends songs from a small catalog based on what genre, mood, and energy level a user prefers. It exists for learning how content-based recommenders work. Not for production, not for real users, not for anything where recommendations could actually shape someone's listening habits.

---

## 3. How the model works

The system goes through every song in the catalog and compares it to the user's preferences. Genre match gets the most points (2.0), mood match gets 1.5, and energy similarity can add up to 1.0 depending on how close the song's energy is to what the user wants. There's also a small 0.5 bonus if the user likes acoustic music and the song is fairly acoustic.

Every song gets a total score, the list gets sorted high to low, and the top picks come back. Each recommendation comes with a breakdown of why it scored the way it did, which is actually one of the more useful parts of the system since you can immediately tell if the logic is doing something weird.

---

## 4. Data

20 songs in a CSV file. Started with 10 and I added 10 more because the original set was missing entire genres (no edm, folk, or metal) and moods (no sad or relaxed tracks).

Current genres: pop, lofi, rock, ambient, jazz, synthwave, indie pop, edm, folk, metal. Moods: happy, chill, intense, sad, relaxed, focused, moody.

Still pretty skewed though. No hip-hop, classical, R&B, or country anywhere. The whole catalog reads like it was put together by someone who mostly listens to electronic and indie music, which means anyone outside that space is going to get mediocre results no matter what.

---

## 5. Strengths

Works well when the user has a clear, single-genre preference. The "Chill Lofi Listener" profile got a perfect 5.0 on its top pick (Library Rain) because it matched on literally every factor. The "Happy Pop Fan" got sensible results too, with Sunrise City on top since it hit both genre and mood while being close on energy.

The explanations are probably the best part. You don't just get a ranked list, you get "genre match (+2.0); mood match (+1.5); energy similarity (+0.98)" so you can actually see what's happening. Makes debugging the scoring logic way easier than staring at raw numbers.

---

## 6. Limitations and bias

Genre dominates everything. At 2.0 points it's the heaviest weight, so a song that nails mood and energy but is the wrong genre will almost always lose to a so-so song in the right genre. I proved this to myself during the weight experiment: cutting genre in half immediately pushed better-fitting songs from other genres into the top results.

The catalog is small and lopsided. Four lofi tracks, one folk song, one metal song. If your favorite genre has more entries you just get better recommendations by default. A metal fan has exactly one option (Rage Circuit) and that's it.

There's also no way to have mixed preferences. You can't say "I like chill lofi AND intense rock depending on my mood." You pick one profile, which isn't how anyone actually listens to music.

---

## 7. Evaluation

I tested three profiles. The Happy Pop Fan (pop, happy, energy 0.8) got Sunrise City on top at 4.48, and the whole top 5 was upbeat stuff. Felt right. The Chill Lofi Listener (lofi, chill, energy 0.35, likes acoustic) got Library Rain at a perfect 5.0. The acoustic bonus was what separated it from the other lofi tracks.

The most interesting result was the Intense Rock Enthusiast (rock, intense, energy 0.9). Storm Runner topped at 4.49, but Rage Circuit, which is metal/intense at 0.97 energy, only came in 5th. It's arguably the most "intense" song in the whole catalog, but missing the rock genre match held it back. That felt wrong to me and was probably the clearest sign that genre weight was too high.

For the experiment I doubled energy weight (1.0 to 2.0) and halved genre (2.0 to 1.0). Biggest shift was the Pop profile: Bonfire Night (rock/happy) jumped from #3 to #2 because its perfect energy match suddenly mattered more than genre. For Rock, Gym Hero (pop/intense) moved ahead of Bonfire Night since high energy was worth more than being rock. The system is pretty sensitive to weight changes. Small tweaks reshuffled the lists more than I expected.

---

## 8. Future work

- Let users have multi-genre or blended profiles instead of forcing one genre choice.
- Add a diversity penalty so the top results aren't all from the same artist or genre.
- Actually use tempo and valence in the scoring. They're already in the dataset but the scoring logic ignores them right now.

---

## 9. Personal reflection

I didn't expect genre to dominate as hard as it did. Going in, I figured energy and mood would matter more for whether a recommendation "felt" right, but at 2.0 points genre basically decides the top half of every list before anything else gets a say. Cutting genre weight in half during the experiment was when it clicked for me. The results went from "songs in your genre" to "songs that match your vibe," which felt way more like what an actual recommendation should be.

This project changed how I think about what Spotify is doing under the hood. They probably have hundreds of features and are constantly adjusting weights, but the basic idea is the same thing I built here: turn preferences into numbers, compare them against song attributes, sort by score. The big difference is feedback. My system never learns whether someone liked what it suggested, so it will keep pushing the same types of songs forever. That's basically a filter bubble, and it was kind of uncomfortable seeing how easily even 20 songs and four scoring rules can create one.

The other thing that stuck with me is that this system has zero concept of surprise. If your profile says "happy" it will never suggest a sad song, even if that's exactly what you need after a rough day. Real recommendation has to include some randomness or discovery, and I honestly don't know how you'd code that without it feeling forced.
