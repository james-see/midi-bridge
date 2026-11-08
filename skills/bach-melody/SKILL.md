---
name: bach-melody
description: "Recipe for a Bachian melody — counterpoint, arpeggios, diatonic, baroque style."
version: 1.0.0
---

# Bach Melody Recipe

## Vibe
Baroque counterpoint, elegant arpeggios, sequences, passing tones. Think J.S. Bach inventions, two-part counterpoint.

## Specs
- **BPM:** 60-80 (classical tempo, andante-allegro moderato)
- **Notes:** Diatonic arpeggios over I-IV-V-vi chord progression
- **Scales:** Major or minor, church modes (Dorian, Phrygian, etc.)
- **Channel:** 1 (melody instrument — harpsichord, piano, strings)

## Chord progression (C major, 4 bars)

| Bar | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| **Chord** | C major (I) | A minor (vi) | F major (IV) | G major (V) |
| **Arpeggio** | C4-E4-G4 | A3-C4-E4 | F3-A3-C4 | G3-B3-D4 |

## Example play_pattern call (4-bar melody)

```json
{
  "pattern": [
    {"note": "C4", "time": 0.0, "duration": 0.5, "velocity": 80},
    {"note": "E4", "time": 0.5, "duration": 0.5, "velocity": 75},
    {"note": "G4", "time": 1.0, "duration": 0.5, "velocity": 80},
    {"note": "C5", "time": 1.5, "duration": 0.5, "velocity": 85},
    {"note": "A3", "time": 2.0, "duration": 0.5, "velocity": 70},
    {"note": "C4", "time": 2.5, "duration": 0.5, "velocity": 75},
    {"note": "E4", "time": 3.0, "duration": 0.5, "velocity": 80},
    {"note": "F3", "time": 4.0, "duration": 0.5, "velocity": 70},
    {"note": "A3", "time": 4.5, "duration": 0.5, "velocity": 75},
    {"note": "C4", "time": 5.0, "duration": 0.5, "velocity": 80},
    {"note": "G3", "time": 6.0, "duration": 0.5, "velocity": 85},
    {"note": "B3", "time": 6.5, "duration": 0.5, "velocity": 80},
    {"note": "D4", "time": 7.0, "duration": 0.5, "velocity": 90}
  ],
  "bpm": 72,
  "channel": 1
}
```

## Variations
- **Two-part counterpoint:** Add a second `play_pattern` call for a bass line (down a third or sixth from the melody)
- **Passing tones:** Insert chromatic notes between arpeggio tones (e.g. C#4 between C4 and D4)
- **Sequences:** Repeat a fragment up or down a step (baroque sequence technique)
- **Ornamentation:** Add trills (rapid alternation between two adjacent notes) using `send_note` with very short duration
