"""Tool schemas — what the LLM sees."""

SEND_NOTE = {
    "name": "send_note",
    "description": (
        "Play a single MIDI note on a DAW instrument track. "
        "The note plays through whatever instrument is armed in the user's DAW. "
        "Use note names like 'C4' (middle C) or MIDI numbers (60=middle C). "
        "Velocity controls how hard the note hits (0-127)."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "note": {
                "type": "string",
                "description": "Note name (e.g. 'C4', 'F#5') or MIDI number as string (e.g. '60')",
            },
            "velocity": {
                "type": "integer",
                "description": "Note velocity 0-127 (default 100)",
            },
            "duration": {
                "type": "number",
                "description": "Duration in seconds (default 0.5)",
            },
            "channel": {
                "type": "integer",
                "description": "MIDI channel 1-16 (default 1)",
            },
        },
        "required": ["note"],
    },
}

SEND_NOTES = {
    "name": "send_notes",
    "description": (
        "Play multiple MIDI notes simultaneously — a chord. "
        "All notes start and stop at the same time. "
        "Use for chords, harmony, or layered sounds."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "notes": {
                "type": "array",
                "items": {"type": "string"},
                "description": "List of note names or MIDI numbers (e.g. ['C4', 'E4', 'G4'] for C major)",
            },
            "velocity": {
                "type": "integer",
                "description": "Note velocity 0-127 (default 100)",
            },
            "duration": {
                "type": "number",
                "description": "Duration in seconds (default 0.5)",
            },
            "channel": {
                "type": "integer",
                "description": "MIDI channel 1-16 (default 1)",
            },
        },
        "required": ["notes"],
    },
}

SEND_CC = {
    "name": "send_cc",
    "description": (
        "Send a MIDI control change message — knods, sliders, mod wheel, "
        "filter sweeps, pan, etc. Controller 1=mod wheel, 74=cutoff filter."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "controller": {
                "type": "integer",
                "description": "MIDI controller number 0-127 (e.g. 1=mod wheel, 74=filter cutoff)",
            },
            "value": {
                "type": "integer",
                "description": "Controller value 0-127",
            },
            "channel": {
                "type": "integer",
                "description": "MIDI channel 1-16 (default 1)",
            },
        },
        "required": ["controller", "value"],
    },
}

SEND_PROGRAM_CHANGE = {
    "name": "send_program_change",
    "description": (
        "Switch the instrument preset on a MIDI channel. "
        "Changes which sound plays on that channel (e.g. piano→strings). "
        "Program 0=acoustic grand piano, 40=violin, 73=flute."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "program": {
                "type": "integer",
                "description": "Program number 0-127 (0=piano, 40=violin, 73=flute)",
            },
            "channel": {
                "type": "integer",
                "description": "MIDI channel 1-16 (default 1)",
            },
        },
        "required": ["program"],
    },
}

SEND_PITCH_BEND = {
    "name": "send_pitch_bend",
    "description": (
        "Send a MIDI pitch bend message — slide pitch up or down. "
        "Value ranges from -8192 to 8191 (0=center/no bend)."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "value": {
                "type": "integer",
                "description": "Pitch bend value -8192 to 8191 (0=no bend)",
            },
            "channel": {
                "type": "integer",
                "description": "MIDI channel 1-16 (default 1)",
            },
        },
        "required": ["value"],
    },
}

PLAY_PATTERN = {
    "name": "play_pattern",
    "description": (
        "Play a timed sequence of MIDI notes — a melody, bassline, or arpeggio. "
        "Each note has a start time, duration, and velocity. "
        "The sequence plays in real time through the armed DAW track. "
        "Load a recipe skill (midi-bridge:trap-beat, midi-bridge:bach-melody, etc.) "
        "for genre-specific patterns."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "pattern": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "note": {"type": "string", "description": "Note name or MIDI number"},
                        "time": {"type": "number", "description": "When to play (seconds from start)"},
                        "duration": {"type": "number", "description": "How long to hold (seconds)"},
                        "velocity": {"type": "integer", "description": "0-127"},
                    },
                },
                "description": "List of timed notes",
            },
            "bpm": {
                "type": "integer",
                "description": "Tempo in BPM (default 120)",
            },
            "channel": {
                "type": "integer",
                "description": "MIDI channel 1-16 (default 1)",
            },
        },
        "required": ["pattern"],
    },
}

DRUM_PATTERN = {
    "name": "drum_pattern",
    "description": (
        "Play a drum pattern from a 16-step grid — a beat. "
        "Steps 0-15 = 16th notes in a 4/4 bar (0=beat 1, 4=beat 2, etc.). "
        "Use drum names: 'kick', 'snare', 'hihat', 'crash', 'ride', etc. "
        "Load the midi-bridge:trap-beat or midi-bridge:rap-boom-bap skill for genre recipes. "
        "Drums play on channel 10 (GM standard)."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "steps": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "step": {"type": "integer", "description": "0-15 (16th note position)"},
                        "drums": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Drum names (e.g. ['kick', 'snare'])",
                        },
                    },
                },
                "description": "Step grid",
            },
            "bpm": {
                "type": "integer",
                "description": "Tempo in BPM (default 120)",
            },
            "bars": {
                "type": "integer",
                "description": "Number of bars to play (default 1)",
            },
            "channel": {
                "type": "integer",
                "description": "MIDI channel (default 10 for drums)",
            },
        },
        "required": ["steps"],
    },
}

LIST_MIDI_PORTS = {
    "name": "list_midi_ports",
    "description": (
        "List available MIDI output ports. "
        "Use this to find the right port name before set_output, "
        "or to troubleshooth if the user doesn't hear anything."
    ),
    "parameters": {
        "type": "object",
        "properties": {},
    },
}

SET_OUTPUT = {
    "name": "set_output",
    "description": (
        "Route MIDI output to a specific port. "
        "Use list_midi_ports to see available ports. "
        "The default virtual port 'MIDI Bridge' works if a DAW is listening."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "port_name": {
                "type": "string",
                "description": "MIDI port name (e.g. 'MIDI Bridge')",
            },
        },
        "required": ["port_name"],
    },
}
