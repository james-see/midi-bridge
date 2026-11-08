# MIDI Bridge — Plugin Design Plan

## Concept

**MIDI Bridge** is a Hermes Agent plugin that gives the agent the ability to send live MIDI events to a local DAW (Logic Pro, Bitwig, Ableton, GarageBand, or any MIDI-capable app). The agent can play notes, drum patterns, control changes, and program changes in real time through whatever instrument track the user has armed.

**The core insight:** A prompt cannot send MIDI. Generating music requires a real tool with hardware access to the MIDI subsystem (CoreMIDI on macOS, ALSA on Linux). This is genuinely impossible without a plugin.

## Who needs this

- **Music producers** — generate beats, basslines, chord progressions from natural language
- **Songwriters** — audition melodies and harmonies without leaving the chat
- **Sound designers** — trigger program changes and CC sweeps on synths
- **Anyone who makes music** — automate tedious MIDI programming via conversation

## Architecture

```
You: "Play a 4-bar drum pattern at 120 BPM — kick on 1+3, snare on 2+4, hats on every 8th"
        │
        ▼
┌──────────────────────────────────┐
│  Agent calls play_pattern         │
│  Builds MIDI note sequence        │
│  with timing + channel             │
└──────────┬───────────────────────┘
           │ MIDI events (mido)
           ▼
┌──────────────────────────────────┐
│  CoreMIDI (macOS) /              │
│  ALSA (Linux)                    │
└──────────┬───────────────────────┘
           │
           ▼
┌──────────────────────────────────┐
│  Logic Pro / Bitwig /            │  ← plays through armed track
│  Ableton / GarageBand /          │
│  any DAW with an instrument       │
└──────────────────────────────────┘
```

## Plugin Surfaces Used

| Surface | API | Purpose |
|---|---|---|
| Custom tools | `ctx.register_tool()` | 8 MIDI tools the agent can call |
| Bundled skill | `ctx.register_skill()` | Teaches agent music theory + DAW setup |
| Slash command | `ctx.register_command()` | `/midi` for port listing + test |

## Tools

| Tool | Description | Key Parameters |
|---|---|---|
| `send_note` | Play a single MIDI note | `note` (0-127), `velocity` (0-127), `duration` (seconds), `channel` (1-16, default 1) |
| `send_notes` | Play multiple notes simultaneously (a chord) | `notes` (list of 0-127), `velocity`, `duration`, `channel` |
| `send_cc` | Send control change (knobs, mod wheel) | `controller` (0-127), `value` (0-127), `channel` |
| `send_program_change` | Switch instrument preset | `program` (0-127), `channel` |
| `send_pitch_bend` | Send pitch bend message | `value` (-8192 to 8191), `channel` |
| `play_pattern` | Play a timed sequence of notes | `pattern` (list of {note, time, duration, velocity}), `bpm` (default 120), `channel` |
| `drum_pattern` | Play a drum pattern from a step grid | `steps` (list of {step, drums}), `bpm`, `bars` (default 1), `channel` (default 10) |
| `list_midi_ports` | Show available MIDI output ports | (none) |
| `set_output` | Route MIDI to a specific port | `port_name` |

## Note Number Reference (bundled in skill)

Standard MIDI note mapping (middle C = 60):

| Note | Octave 0 | Octave 1 | Octave 2 | Octave 3 | Octave 4 | Octave 5 |
|---|---|---|---|---|---|---|
| C | 12 | 24 | 36 | 48 | **60** | 72 |
| C# | 13 | 25 | 37 | 49 | 61 | 73 |
| D | 14 | 26 | 38 | 50 | 62 | 74 |
| D# | 15 | 27 | 39 | 51 | 63 | 75 |
| E | 16 | 28 | 40 | 52 | 64 | 76 |
| F | 17 | 29 | 41 | 53 | 65 | 77 |
| F# | 18 | 30 | 42 | 54 | 66 | 78 |
| G | 19 | 31 | 43 | 55 | 67 | 79 |
| G# | 20 | 32 | 44 | 56 | 68 | 80 |
| A | 21 | 33 | 45 | 57 | 69 | 81 |
| A# | 22 | 34 | 46 | 58 | 70 | 82 |
| B | 23 | 35 | 47 | 59 | 71 | 83 |

## Drum Map (GM standard, channel 10)

| Drum | MIDI Note |
|---|---|
| Kick / Bass Drum | 36 |
| Snare | 38 |
| Side Stick | 37 |
| Hi-Hat (closed) | 42 |
| Hi-Hat (open) | 46 |
| Low Tom | 41 |
| Mid Tom | 47 |
| High Tom | 48 |
| Crash Cymbal | 49 |
| Ride Cymbal | 51 |
| Cowbell | 56 |

## Bundled Skill (skill/SKILL.md)

Teaches the agent:

### DAW setup instructions
1. Open your DAW (Logic Pro, Bitwig, Ableton, GarageBand)
2. Arm a track with an instrument (Drum Machine Designer, EXS24, a synth, a piano)
3. Set the track's MIDI input to the Chat Shield virtual port (use `list_midi_ports` to find it)
4. Hit play so the DAW is listening
5. Then ask the agent to play something

### If the user says "I don't hear anything"
- Run `list_midi_ports` to check available outputs
- Run `set_output` to route to the correct port
- Check: is a track armed? Is the DAW playing?
- Try `send_note` with note=60, velocity=100, duration=1 to test

### Music theory basics
- Note names → MIDI numbers (C4=60, D4=62, E4=64, etc.)
- Scales: major (W-W-H-W-W-W-W-H), minor (W-H-W-W-H-W-W-H), pentatonic (5 notes)
- Intervals: octave (12), fifth (7), third (4), etc.
- Tempo: BPM → seconds per beat = 60/BPM

### Drum pattern construction
- A bar = 4 beats at default
- 16th notes = 4 per beat = 16 steps per bar
- Kick on 1 and 3 (steps 0 and 8)
- Snare on 2 and 4 (steps 4 and 12)
- Hats on every 16th (all even steps) or every 8th (every other step)
- Trap: kick on 1, snare on 3, hats on every 16th, faster BPM (140+)

### Pattern format for `play_pattern`
```json
{
  "pattern": [
    {"note": 60, "time": 0.0, "duration": 0.5, "velocity": 100},
    {"note": 64, "time": 0.5, "duration": 0.5, "velocity": 90},
    {"note": 67, "time": 1.0, "duration": 0.5, "velocity": 80}
  ],
  "bpm": 120,
  "channel": 1
}
```

### Drum format for `drum_pattern`
```json
{
  "steps": [
    {"step": 0, "drums": ["kick"]},
    {"step": 4, "drums": ["snare"]},
    {"step": 8, "drums": ["kick"]},
    {"step": 12, "drums": ["snare"]},
    {"step": 0, "drums": ["hihat"],  {"step": 2, "drums": ["hihat"]},
    {"step": 4, "drums": ["hihat"]}, {"step": 6, "drums": ["hihat"]}
  ],
  "bpm": 120,
  "bars": 1,
  "channel": 10
}
```

## Plugin File Structure

```
midi-bridge/
├── plugin.yaml              # Manifest
├── __init__.py               # register(ctx) — registers tools + slash command + all skills
├── schemas.py                 # Tool schemas (what the LLM sees)
├── tools.py                   # Tool handlers (MIDI logic via mido)
├── midi_utils.py              # Note name↔MIDI conversion, port management
├── pattern_player.py           # Timing engine for play_pattern / drum_pattern
├── skills/
│   ├── SKILL.md              # Core skill: music theory + DAW setup + troubleshooting
│   ├── trap-beat.md           # Recipe: trap beat (140+ BPM, 808s, fast hats)
│   ├── rap-boom-bap.md         # Recipe: 90s boom-bap rap (90 BPM, punchy)
│   ├── house-beat.md            # Recipe: 4-on-the-floor house (128 BPM)
│   ├── kanye-style.md          # Recipe: Kanye-style heavy beat (140 BPM, 808 tail)
│   ├── bach-melody.md          # Recipe: Bachian counterpoint + arpeggios
│   └── mozart-mode.md           # Recipe: Mozart elegant melodies + alberti bass
└── README.md                   # User-facing docs
```

## plugin.yaml

```yaml
name: midi-bridge
version: 1.0.0
description: "Send live MIDI events to a local DAW from Hermes Agent. Play notes, chords, drum patterns, control changes, and program changes in real time through any armed instrument track. Uses CoreMIDI (macOS) / ALSA (Linux) via the mido Python library. No cloud, no API keys — everything is local."
author: "@james-see"
license: MIT
homepage: https://github.com/james-see/midi-bridge
requires_hermes: ">=0.22.0"
provides_tools:
  - send_note
  - send_notes
  - send_cc
  - send_program_change
  - send_pitch_bend
  - play_pattern
  - drum_pattern
  - list_midi_ports
  - set_output
python_dependencies:
  - "mido>=1.3,<2.0"
  - "numpy>=1.24,<3.0"
config_schema:
  default_channel:
    type: int
    default: 1
    label: "Default MIDI channel"
    description: "MIDI channel for send_note and play_pattern (1-16)"
  default_velocity:
    type: int
    default: 100
    label: "Default velocity"
    description: "Default note velocity (0-127)"
  default_bpm:
    type: int
    default: 120
    label: "Default BPM"
    description: "Default tempo for play_pattern and drum_pattern"
  virtual_port_name:
    type: str
    default: "MIDI Bridge"
    label: "Virtual port name"
    description: "Name of the virtual MIDI port created by the plugin"
```

## Dependencies

| Package | Purpose | Pin |
|---|---|---|
| `mido` | Cross-platform MIDI message sending (CoreMIDI/ALSa) | `>=1.3,<2.0` |
| `numpy` | Used by mido for message construction | `>=1.24,<3.0` |

No heavy dependencies. No ONNX, no transformers, no huggingface — just MIDI.

## Bundled Recipe Skills

The plugin ships genre/style "recipe" skills that teach the agent how to construct specific patterns. When the user says "play a trap beat", the agent loads the `midi-bridge:trap-beat` skill which knows the BPM, drum placement, and characteristics of that style — no note-by-note describing needed.

### Core skill (`skills/SKILL.md`)
- DAW setup instructions (open, arm track, set MIDI input, hit play)
- Music theory basics (note names → MIDI numbers, scales, intervals)
- Drum pattern construction (steps, bar, 16th notes)
- Troubleshooting ("I don't hear anything" checklist)
- Pattern/drum JSON formats

### Recipe: `trap-beat.md`
- **BPM:** 140-150
- **Drums (channel 10):** Kick on 1+3 (steps 0, 8), snare on 2+4 (steps 4, 12), hats on every 16th (all even steps), 808 sub-bass on 1
- **Vibe:** dark, heavy, sub-bass-driven
- **Example `drum_pattern` call included**

### Recipe: `rap-boom-bap.md`
- **BPM:** 88-95
- **Drums:** Kick on 1+3, snare on 2+4, no hats or sparse, swing on the snare
- **Vibe:** 90s golden age, punchy, dry
- **Example call included**

### Recipe: `house-beat.md`
- **BPM:** 124-130
- **Drums:** Kick on every beat (four-on-the-floor), hats on off-beats, clap on 2+4
- **Vibe:** groovy, steady, dancefloor
- **Example call included**

### Recipe: `kanye-style.md`
- **BPM:** 138-142
- **Drums:** Kick on 1 with long 808 tail, snare on 3 with reverb, hats fast (32nd notes), pitched 808 slides
- **Vibe:** heavy, emotional, 808-forward
- **Example call included**

### Recipe: `bach-melody.md`
- **BPM:** 60-80 (classical tempo)
- **Notes:** Diatonic arpeggios over I-IV-V-vi, baroque counterpoint style, passing tones, sequences
- **Scales:** Major/minor, church modes
- **Example `play_pattern` call with a 4-bar Bachian progression

### Recipe: `mozart-mode.md`
- **BPM:** 100-120 (allegro)
- **Notes:** Elegant melodies, alberti bass accompaniment, balanced phrases, grace notes
- **Scales:** Major, focused on elegance and simplicity
- **Example call with a Mozart-style melody + alberti bass line

## Build Phases

### Phase 1: Core Plugin (Day 1-2)
- [ ] Create plugin directory structure
- [ ] Write `plugin.yaml` manifest
- [ ] Implement `midi_utils.py` — note name↔MIDI conversion, port management, virtual port creation
- [ ] Implement `tools.py` — all 10 tool handlers
- [ ] Implement `pattern_player.py` — timing engine for sequences and drum patterns
- [ ] Write `schemas.py` — tool schemas
- [ ] Write `__init__.py` — registration
- [ ] Test with `hermes plugins validate`
- [ ] Test with `hermes plugins doctor`

### Phase 2: Skills + Polish (Day 3)
- [ ] Write core skill (music theory, DAW setup, troubleshooting)
- [ ] Write 6 recipe skills (trap, boom-bap, house, kanye, bach, mozart)
- [ ] Write README.md
- [ ] Test `send_note` → does a MIDI note reach the DAW?
- [ ] Test `drum_pattern` → does a beat play?
- [ ] Test `play_pattern` → does a sequence play?
- [ ] Test recipe skills → does "play a trap beat" produce the right pattern?
- [ ] Edge cases (no DAW running, no track armed, bad port name)

### Phase 3: Demo + Submit (Day 4)
- [ ] Record <90s demo video (agent generates a beat, Logic Pro plays it)
- [ ] Create GitHub repo
- [ ] Open PR to NousResearch/hermes-agent
- [ ] Post demo on X tagging @NousResearch
- [ ] Submit entry form

## Demo Video Script (<90 seconds)

### Setup before recording
- Logic Pro (or GarageBand) open with a drum instrument on track 1
- Track 1 armed, MIDI input set to "MIDI Bridge" virtual port
- Transport playing (record or just play)

### [0:00-0:10] Intro
> "MIDI Bridge is a Hermes Agent plugin that sends live MIDI to your DAW — notes, drums, patterns, control changes — from natural language."

### [0:10-0:30] DAW setup
Show Logic Pro with armed drum track. Point at the MIDI input set to "MIDI Bridge".

> "The plugin creates a virtual MIDI port. Arm a track in your DAW, set its input to that port, hit play."

### [0:30-0:60] The beat
Type in Hermes chat: "Play a 4-bar trap beat at 140 BPM — kick on 1 and 3, snare on 2 and 4, hats on every 16th, add an 808 kick on the 3 of beat 3."

Show Logic Pro playing the drum pattern in real time.

> "The agent constructed the MIDI pattern and sent it to Logic Pro. I didn't program a single note."

### [0:60-0:80] A melody
Type: "Now play a C minor melody over it — C, Eb, G, C one note per beat at 140 BPM."

Show the melody playing alongside the drums.

> "Notes, drums, patterns — all from conversation. No piano roll, no MIDI programming."

### [0:80-0:90] Close
> "MIDI Bridge — because a prompt can't play piano."

## What Makes This a Winner

1. **Zero competition** — no music production plugins in the catalog or any hackathon PRs
2. **Killer demo** — audio + visual, the judges hear it work
3. **Genuinely impossible via prompt** — you can't send MIDI from text
4. **Low dependencies** — just `mido` + `numpy`, no heavy ML
5. **Broad appeal** — every music producer, songwriter, sound designer who uses AI tools
6. **Your edge** — you built beatstoch, you use Logic Pro, you have a working MIDI setup
