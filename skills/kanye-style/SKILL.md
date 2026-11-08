---
name: kanye-style
description: "Recipe for a Kanye-style heavy beat — 138-142 BPM, 808 tail, reverb snare, emotional."
version: 1.0.0
---

# Kanye-Style Beat Recipe

## Vibe
Heavy, emotional, 808-forward. Think "808s & Heartbreak", "Yeezus" era. Big low-end, dramatic snare.

## Specs
- **BPM:** 138-142
- **Drums (channel 10):** Kick on 1 with long 808 tail, snare on 3 with reverb, fast hats (32nd notes), pitched 808 slides
- **Swing:** Straight, no swing — mechanical precision

## Drum pattern (1 bar, 16 steps)

| Step | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **Kick** | ● | | | | | | | | ● | | | | | | | |
| **Snare** | | | | | | | | ● | | | | | | | | ● |
| **HiHat** | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● |
| **808** | ●~~ | | | | | | | | | | | | | | | |

(●~~ = long tail, holds through step 1-2)

## Example drum_pattern call

```json
{
  "steps": [
    {"step": 0, "drums": ["kick", "hihat"]},
    {"step": 1, "drums": ["hihat"]},
    {"step": 2, "drums": ["hihat"]},
    {"step": 3, "drums": ["hihat"]},
    {"step": 4, "drums": ["hihat"]},
    {"step": 5, "drums": ["hihat"]},
    {"step": 6, "drums": ["hihat"]},
    {"step": 7, "drums": ["snare"]},
    {"step": 8, "drums": ["kick", "hihat"]},
    {"step": 9, "drums": ["hihat"]},
    {"step": 10, "drums": ["hihat"]},
    {"step": 11, "drums": ["hihat"]},
    {"step": 12, "drums": ["hihat"]},
    {"step": 13, "drums": ["hihat"]},
    {"step": 14, "drums": ["hihat"]},
    {"step": 15, "drums": ["snare"]}
  ],
  "bpm": 140,
  "bars": 1,
  "channel": 10
}
```

## Variations
- **808 glides:** Add a low bass note on step 0 with long duration that bends down
- **Reverb snare:** Send a CC message (controller=91, value=127) before the snare for reverb on
- **32nd hats:** Double every hihat to 32nd-note speed for the "Yeezus" feel
- **Missing kick:** Remove kick on step 8 for a breakdown feel
