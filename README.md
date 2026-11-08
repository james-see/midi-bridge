# MIDI Bridge

> Send live MIDI to your DAW from Hermes Agent. Notes, drums, patterns, CC, program changes — from natural language. No cloud, no API keys, everything is local.

## What it does

MIDI Bridge is a [Hermes Agent](https://hermes-agent.nousresearch.com) plugin that creates a virtual MIDI port and sends events to your DAW in real time. The agent can play notes, chords, drum patterns, control changes, and program changes through whatever instrument track you have armed.

**The agent plays MIDI. Your DAW makes the sound.**

## Tools

| Tool | Description |
|---|---|
| `send_note` | Play a single note (pitch, velocity, duration) |
| `send_notes` | Play a chord (multiple notes at once) |
| `send_cc` | Control change (knobs, sliders, mod wheel) |
| `send_program_change` | Switch instrument preset |
| `send_pitch_bend` | Pitch bend |
| `play_pattern` | Timed note sequence (melody, bassline, arpeggio) |
| `drum_pattern` | Drum pattern from a 16-step grid |
| `list_midi_ports` | Show available MIDI ports |
| `set_output` | Route MIDI to a specific port |

## Genre recipe skills

The plugin ships with genre-specific "recipe" skills so you can say "play a trap beat" and get the right pattern:

| Skill | BPM | Vibe |
|---|---|---|
| `trap-beat` | 140-150 | Dark, 808 sub-bass, fast hats |
| `rap-boom-bap` | 88-95 | 90s golden age, punchy, dry |
| `house-beat` | 124-130 | Four-on-the-floor, dancefloor |
| `kanye-style` | 138-142 | Heavy, 808 tail, reverb snare |
| `bach-melody` | 60-80 | Baroque counterpoint, arpeggios |
| `mozart-mode` | 100-120 | Elegant melodies, alberti bass |

## DAW setup

1. **Open your DAW** — Logic Pro, Bitwig, Ableton, GarageBand, or any app that receives MIDI
2. **Arm a track** with an instrument (any instrument — the plugin doesn't care what sound plays)
3. **Set the track's MIDI input** to "MIDI Bridge" (use `list_midi_ports` to find it)
4. **Hit play** so the DAW is listening
5. Then ask the agent to play something

## How it works

```
You: "Play a trap beat at 140 BPM"
        │
        ▼
┌──────────────────────────────┐
│  Agent loads trap-beat skill     │
│  Calls drum_pattern with the     │
│  right kick/snare/hat pattern    │
└──────────┬───────────────────┘
           │ MIDI events (mido)
           ▼
┌──────────────────────────────┐
│  CoreMIDI (macOS) / ALSA      │
│  via virtual port                 │
└──────────┬───────────────────┘
           │
           ▼
┌──────────────────────────────┐
│  Logic Pro / Bitwig /           │  ← plays through armed track
│  Ableton / GarageBand /         │
│  any DAW with an instrument      │
└──────────────────────────────┘
```

## Installation

```bash
hermes plugins install james-see/midi-bridge
hermes plugins enable midi-bridge
```

## Configuration

```yaml
plugins:
  entries:
    midi-bridge:
      settings:
        default_channel: 1        # MIDI channel (1-16)
        default_velocity: 100     # Note velocity (0-127)
        default_bpm: 120           # Tempo
        virtual_port_name: "MIDI Bridge"  # Virtual port name
```

## Privacy

- **No network calls.** Everything is local via CoreMIDI/ALSA.
- **No data collection.** No telemetry, no cloud, no API keys.
- **Dependencies:** just `mido` + `numpy`.

## License

MIT
