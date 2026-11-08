---
name: rap-boom-bap
description: "Recipe for 90s boom-bap rap beat — 88-95 BPM, punchy, dry, golden age."
version: 1.0.0
---

# Rap Boom-Bap Recipe

## Vibe
90s golden age hip-hop. Punchy, dry, no reverb. Think DJ Premier, Pete Rock, J Dilla.

## Specs
- **BPM:** 88-95
- **Drums (channel 10):** Kick on 1+3, snare on 2+4, no hats or sparse, slight swing on the snare
- **Swing:** Snare has a slight late swing (~55-58%)

## Drum pattern (1 bar, 16 steps)

| Step | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **Kick** | ● | | | | | | | | ● | | | | | | | |
| **Snare** | | | | | ● | | | | | | | | ● | | | |
| **HiHat** | ● | | | ● | | | ● | | | ● | | | ● | | | ● |

## Example drum_pattern call

```json
{
  "steps": [
    {"step": 0, "drums": ["kick", "hihat"]},
    {"step": 3, "drums": ["hihat"]},
    {"step": 4, "drums": ["snare"]},
    {"step": 7, "drums": ["hihat"]},
    {"step": 8, "drums": ["kick"]},
    {"step": 11, "drums": ["hihat"]},
    {"step": 12, "drums": ["snare"]},
    {"step": 15, "drums": ["hihat"]}
  ],
  "bpm": 90,
  "bars": 2,
  "channel": 10
}
```

## Variations
- **Sparse hats:** Remove hats entirely for a rawer feel
- **Ghost kick:** Add a soft kick on step 6 or 14 for a "false" bounce
- **Snare swing:** Delay the snare by a few milliseconds for Dilla-style swing
