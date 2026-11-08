---
name: trap-beat
description: "Recipe for a trap beat — 140+ BPM, 808 sub-bass, fast hats, dark vibe."
version: 1.0.0
---

# Trap Beat Recipe

## Vibe
Dark, heavy, sub-bass-driven. Modern trap/hip-hop production style.

## Specs
- **BPM:** 140-150
- **Drums (channel 10):** Kick on 1+3, snare on 2+4, fast hats on every 16th, 808 sub-bass on 1
- **Swing:** Hats can have slight swing (16th swing ~54-58%)

## Drum pattern (1 bar, 16 steps)

| Step | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **Kick** | ● | | | | | | | | ● | | | | | | | |
| **Snare** | | | | | ● | | | | | | | | ● | | | |
| **HiHat** | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● |
| **808** | ● | | | | | | | | | | | | | | | | |

## Example drum_pattern call

```json
{
  "steps": [
    {"step": 0, "drums": ["kick", "hihat"]},
    {"step": 2, "drums": ["hihat"]},
    {"step": 4, "drums": ["snare", "hihat"]},
    {"step": 6, "drums": ["hihat"]},
    {"step": 8, "drums": ["kick", "hihat"]},
    {"step": 10, "drums": ["hihat"]},
    {"step": 12, "drums": ["snare", "hihat"]},
    {"step": 14, "drums": ["hihat"]}
  ],
  "bpm": 140,
  "bars": 1,
  "channel": 10
}
```

## Variations
- **Fast hats:** Add 32nd-note hats by doubling the hihat steps
- **808 glides:** Add a low bass note (e.g. C2=36) on step 0 with long duration
- **Snare roll:** Add ghost snares on steps 7, 15
