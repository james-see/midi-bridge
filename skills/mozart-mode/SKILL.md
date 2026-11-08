---
name: mozart-mode
description: "Recipe for a Mozart-style melody — elegant, alberti bass, balanced phrases, classical."
version: 1.0.0
---

# Mozart Mode Recipe

## Vibe
Elegant, balanced, graceful. Think W.A. Mozart piano sonatas — clear melody over alberti bass, balanced 4-bar phrases, grace notes.

## Specs
- **BPM:** 100-120 (allegro)
- **Notes:** Elegant melodies with balanced phrasing, alberti bass accompaniment
- **Scales:** Major, focused on elegance and simplicity
- **Channel:** 1 (piano)

## Structure (4-bar phrase, C major)

| Bar | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| **Melody** | E4-D4-C4 | D4-E4-F4 | E4-D4-C4 | G4-F4-E4 |
| **Alberti Bass** | C3-G3-E3-G3 | C3-G3-E3-G3 | C3-G3-E3-G3 | G3-D3-B2-D3 |

## Example play_pattern call (melody, 4 bars)

```json
{
  "pattern": [
    {"note": "E4", "time": 0.0, "duration": 0.5, "velocity": 75},
    {"note": "D4", "time": 0.5, "duration": 0.5, "velocity": 70},
    {"note": "C4", "time": 1.0, "duration": 0.5, "velocity": 80},
    {"note": "D4", "time": 1.5, "duration": 0.5, "velocity": 72},
    {"note": "E4", "time": 2.0, "duration": 0.5, "velocity": 75},
    {"note": "F4", "time": 2.5, "duration": 0.5, "velocity": 78},
    {"note": "E4", "time": 3.0, "duration": 0.5, "velocity": 70},
    {"note": "D4", "time": 3.5, "duration": 0.5, "velocity": 72},
    {"note": "C4", "time": 4.0, "duration": 0.5, "velocity": 80},
    {"note": "G4", "time": 5.0, "duration": 0.5, "velocity": 85},
    {"note": "F4", "time": 5.5, "duration": 0.5, "velocity": 78},
    {"note": "E4", "time": 6.0, "duration": 0.5, "velocity": 75}
  ],
  "bpm": 112,
  "channel": 1
}
```

## Example play_pattern call (alberti bass, 4 bars)

Play simultaneously with the melody:

```json
{
  "pattern": [
    {"note": "C3", "time": 0.0, "duration": 0.5, "velocity": 60},
    {"note": "G3", "time": 0.5, "duration": 0.5, "velocity": 55},
    {"note": "E3", "time": 1.0, "duration": 0.5, "velocity": 58},
    {"note": "G3", "time": 1.5, "duration": 0.5, "velocity": 55},
    {"note": "C3", "time": 2.0, "duration": 0.5, "velocity": 60},
    {"note": "G3", "time": 2.5, "duration": 0.5, "velocity": 55},
    {"note": "E3", "time": 3.0, "duration": 0.5, "velocity": 58},
    {"note": "G3", "time": 3.5, "duration": 0.5, "velocity": 55},
    {"note": "C3", "time": 4.0, "duration": 0.5, "velocity": 60},
    {"note": "G3", "time": 5.0, "duration": 0.5, "velocity": 55},
    {"note": "B2", "time": 5.5, "duration": 0.5, "velocity": 58},
    {"note": "D3", "time": 6.0, "duration": 0.5, "velocity": 55}
  ],
  "bpm": 112,
  "channel": 1
}
```

## Variations
- **Grace notes:** Add quick notes just before main notes (e.g. D#4 before E4) using very short duration
- **Ornamentation:** Trills — rapid alternation between two adjacent notes
- **Major/minor shift:** Switch to A minor for bars 5-8 for a darker section
- **Rubato:** Vary BPM slightly during the piece for expressive timing
