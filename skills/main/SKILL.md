---
name: midi-bridge
description: "Send live MIDI to a DAW — notes, drums, patterns, CC, program changes. Includes setup, music theory, and genre recipes."
version: 1.0.0
---

# MIDI Bridge — Playing MIDI from Hermes Agent

MIDI Bridge creates a virtual MIDI port and sends events to your DAW in real time. The agent can play notes, chords, drum patterns, control changes, and program changes through whatever instrument track you have armed.

## DAW setup (do this first!)

1. **Open your DAW** — Logic Pro, Bitwig, Ableton, GarageBand, or any app that receives MIDI
2. **Arm a track** with an instrument (Drum Machine Designer, EXS24, a synth, a piano — anything)
3. **Set the track's MIDI input** to the "MIDI Bridge" virtual port (use `list_midi_ports` to find it if the name differs)
4. **Hit play** so the DAW is listening
5. Then ask the agent to play something

## If the user says "I don't hear anything"

- Run `list_midi_ports` to check available outputs
- Run `set_output` with the correct port name
- Ask: is a track armed? Is the DAW playing (not stopped)?
- Try `send_note` with note="C4", velocity=100, duration=1 to test

## Note names → MIDI numbers

Middle C = C4 = 60. Each octave spans 12 semitones.

Common notes: C4=60, D4=62, E4=64, F4=65, G4=67, A4=69, B4=71, C5=72.

Sharps: C#4=61, F#4=66, etc. Flats: Db4=61, Eb4=63, etc. (use either form).

## Drum names (channel 10, GM standard)

kick=36, snare=38, hihat=42, hihat_open=46, low_tom=41, mid_tom=47, high_tom=48, crash=49, ride=51, cowbell=56, clap=39.

## Pattern format for play_pattern

```json
{
  "pattern": [
    {"note": "C4", "time": 0.0, "duration": 0.5, "velocity": 100},
    {"note": "E4", "time": 0.5, "duration": 0.5, "velocity": 90},
    {"note": "G4", "time": 1.0, "duration": 0.5, "velocity": 80}
  ],
  "bpm": 120,
  "channel": 1
}
```

## Drum format for drum_pattern

```json
{
  "steps": [
    {"step": 0, "drums": ["kick"]},
    {"step": 4, "drums": ["snare"]},
    {"step": 8, "drums": ["kick"]},
    {"step": 12, "drums": ["snare"]},
    {"step": 0, "drums": ["hihat"]}, {"step": 2, "drums": ["hihat"]},
    {"step": 4, "drums": ["hihat"]}, {"step": 6, "drums": ["hihat"]}
  ],
  "bpm": 120,
  "bars": 1,
  "channel": 10
}
```

## Slash commands

- `/midi` — show usage
- `/midi ports` — list available MIDI ports
- `/midi test` — play a test note (C4)
- `/midi port <name>` — set output port

## Genre recipe skills

Load these with `skill_view(name="midi-bridge:<recipe>")`:

- **trap-beat** — trap beat (140+ BPM, 808s, fast hats)
- **rap-boom-bap** — 90s boom-bap rap (90 BPM, punchy)
- **house-beat** — 4-on-the-floor house (128 BPM)
- **kanye-style** — Kanye-style heavy beat (808 tail, reverb snare)
- **bach-melody** — Bachian counterpoint + arpeggios
- **mozart-mode** — Mozart elegant melodies + alberti bass
