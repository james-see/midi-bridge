---
name: house-beat
description: "Recipe for 4-on-the-floor house beat — 124-130 BPM, steady, groovy, dancefloor."
version: 1.0.0
---

# House Beat Recipe

## Vibe
Steady, groovy, dancefloor. Classic Chicago house. Think Frankie Knuckles, Larry Levan.

## Specs
- **BPM:** 124-130
- **Drums (channel 10):** Kick on every beat (four-on-the-floor), claps on 2+4, hats on off-beats (the "and" between kicks)
- **Swing:** Hat between kicks can have slight swing for a groovier feel

## Drum pattern (1 bar, 16 steps)

| Step | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **Kick** | ● | | ● | | ● | | ● | | ● | | ● | | ● | | ● | |
| **Clap** | | | | | ● | | | | | | | | ● | | | |
| **HiHat** | | ● | | ● | | ● | | ● | | ● | | ● | | ● | | ● |

## Example drum_pattern call

```json
{
  "steps": [
    {"step": 0, "drums": ["kick"]},
    {"step": 2, "drums": ["kick", "hihat"]},
    {"step": 4, "drums": ["kick", "clap"]},
    {"step": 6, "drums": ["kick", "hihat"]},
    {"step": 8, "drums": ["kick"]},
    {"step": 10, "drums": ["kick", "hihat"]},
    {"step": 12, "drums": ["kick", "clap"]},
    {"step": 14, "drums": ["kick", "hihat"]}
  ],
  "bpm": 126,
  "bars": 1,
  "channel": 10
}
```

## Variations
- **Open hat:** Use hihat_open on off-beats for a splashier feel
- **Rim shot:** Add snare rimshot (side_stick=37) on step 14 for a break
- **Toms:** Replace kick on beat 4 with low_tom for a build-up fill
