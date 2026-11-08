"""Tool handlers — the code that runs when the LLM calls each tool."""

from __future__ import annotations

import json
import logging
from typing import Any

from . import midi_utils
from . import pattern_player

logger = logging.getLogger(__name__)

_config: dict[str, Any] = {}


def set_config(config: dict) -> None:
    global _config
    _config = config


# ---------------------------------------------------------------------------
# Tool handlers
# ---------------------------------------------------------------------------


def send_note(args: dict, **kwargs) -> str:
    """Play a single MIDI note."""
    note = args.get("note", "C4")
    try:
        note_num = int(note) if str(note).lstrip("-").isdigit() else midi_utils.note_to_number(str(note))
    except (ValueError, TypeError):
        try:
            note_num = midi_utils.note_to_number(str(note))
        except Exception as e:
            return json.dumps({"error": f"Invalid note: {note} — {e}"})

    velocity = int(args.get("velocity", _config.get("default_velocity", 100)))
    duration = float(args.get("duration", 0.5))
    channel = int(args.get("channel", _config.get("default_channel", 1)))

    try:
        import mido
        msg_on = mido.Message("note_on", note=note_num, velocity=velocity, channel=channel)
        msg_off = mido.Message("note_off", note=note_num, velocity=0, channel=channel)
        midi_utils.send_midi(msg_on)
        import time
        time.sleep(duration)
        midi_utils.send_midi(msg_off)
        midi_utils.record_activity(midi_utils.number_to_note(note_num), velocity, channel, "note")
        return json.dumps({"note": midi_utils.number_to_note(note_num), "velocity": velocity, "duration": duration})
    except ImportError:
        return json.dumps({"error": "mido not installed"})
    except Exception as e:
        return json.dumps({"error": str(e)})


def send_notes(args: dict, **kwargs) -> str:
    """Play multiple notes simultaneously — a chord."""
    notes = args.get("notes", [])
    if not notes:
        return json.dumps({"error": "No notes provided"})

    note_nums = []
    for n in notes:
        try:
            note_nums.append(int(n) if str(n).lstrip("-").isdigit() else midi_utils.note_to_number(str(n)))
        except Exception as e:
            return json.dumps({"error": f"Invalid note {n}: {e}"})

    velocity = int(args.get("velocity", _config.get("default_velocity", 100)))
    duration = float(args.get("duration", 0.5))
    channel = int(args.get("channel", _config.get("default_channel",1)))

    try:
        import mido
        import time
        for num in note_nums:
            msg_on = mido.Message("note_on", note=num, velocity=velocity, channel=channel)
            midi_utils.send_midi(msg_on)
        time.sleep(duration)
        for num in note_nums:
            msg_off = mido.Message("note_off", note=num, velocity=0, channel=channel)
            midi_utils.send_midi(msg_off)
        return json.dumps({"notes": [midi_utils.number_to_note(n) for n in note_nums], "velocity": velocity, "duration": duration})
    except ImportError:
        return json.dumps({"error": "mido not installed"})
    except Exception as e:
        return json.dumps({"error": str(e)})


def send_cc(args: dict, **kwargs) -> str:
    """Send a control change message."""
    controller = int(args.get("controller", 1))
    value = int(args.get("value", 0))
    channel = int(args.get("channel", _config.get("default_channel",1)))

    try:
        import mido
        msg = mido.Message("control_change", control=controller, value=value, channel=channel)
        midi_utils.send_midi(msg)
        return json.dumps({"controller": controller, "value": value, "channel": channel})
    except ImportError:
        return json.dumps({"error": "mido not installed"})
    except Exception as e:
        return json.dumps({"error": str(e)})


def send_program_change(args: dict, **kwargs) -> str:
    """Send a program change message."""
    program = int(args.get("program", 0))
    channel = int(args.get("channel", _config.get("default_channel",1)))

    try:
        import mido
        msg = mido.Message("program_change", program=program, channel=channel)
        midi_utils.send_midi(msg)
        return json.dumps({"program": program, "channel": channel})
    except ImportError:
        return json.dumps({"error": "mido not installed"})
    except Exception as e:
        return json.dumps({"error": str(e)})


def send_pitch_bend(args: dict, **kwargs) -> str:
    """Send a pitch bend message."""
    value = int(args.get("value", 0))
    channel = int(args.get("channel", _config.get("default_channel",1)))

    # Clamp to valid range
    value = max(-8192, min(8191, value))

    try:
        import mido
        msg = mido.Message("pitchwheel", pitch=value, channel=channel)
        midi_utils.send_midi(msg)
        return json.dumps({"value": value, "channel": channel})
    except ImportError:
        return json.dumps({"error": "mido not installed"})
    except Exception as e:
        return json.dumps({"error": str(e)})


def play_pattern(args: dict, **kwargs) -> str:
    """Play a timed note sequence."""
    pattern = args.get("pattern", [])
    if not pattern:
        return json.dumps({"error": "No pattern provided"})

    bpm = int(args.get("bpm", _config.get("default_bpm", 120)))
    channel = int(args.get("channel", _config.get("default_channel",1)))
    velocity = int(args.get("velocity", _config.get("default_velocity",100)))

    # Run in a thread so we don't block the agent
    import threading
    result = pattern_player.play_note_sequence(pattern, bpm, channel, velocity)
    return json.dumps(result)


def drum_pattern(args: dict, **kwargs) -> str:
    """Play a drum pattern from a step grid."""
    steps = args.get("steps", [])
    if not steps:
        return json.dumps({"error": "No steps provided"})

    bpm = int(args.get("bpm", _config.get("default_bpm", 120)))
    bars = int(args.get("bars", 1))
    channel = int(args.get("channel", 10))

    # Run in a thread so we don't block the agent
    import threading
    result = pattern_player.play_drum_pattern(steps, bpm, bars, channel)
    # Record activity for the monitor
    for item in steps:
        for drum_name in item.get("drums", []):
            midi_utils.record_activity(drum_name, 100, channel, "drum")
    return json.dumps(result)


def list_midi_ports(args: dict, **kwargs) -> str:
    """List available MIDI output ports."""
    ports = midi_utils.list_ports()
    if not ports:
        return json.dumps({"ports": [], "warning": "No MIDI ports found. Open a DAW with a MIDI track armed."})
    return json.dumps({"ports": ports})


def set_output(args: dict, **kwargs) -> str:
    """Set the MIDI output port."""
    port_name = args.get("port_name", "")
    if not port_name:
        return json.dumps({"error": "No port_name provided"})

    success = midi_utils.set_output_port(port_name)
    if success:
        return json.dumps({"output": port_name, "success": True})
    return json.dumps({"error": f"Failed to set output port: {port_name}"})
