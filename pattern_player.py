"""Timing engine for play_pattern and drum_pattern tools."""

from __future__ import annotations

import logging
import threading
import time
from typing import Any

from . import midi_utils

logger = logging.getLogger(__name__)


def play_note_sequence(
    pattern: list[dict],
    bpm: int = 120,
    channel: int = 1,
    velocity: int = 100,
) -> dict:
    """Play a timed sequence of MIDI notes.

    Each item in pattern: {"note": 60, "time": 0.0, "duration": 0.5, "velocity": 100}
    - note: MIDI note number (0-127) or note name like "C4"
    - time: when to play (seconds from start)
    - duration: how long to hold (seconds)
    - velocity: how hard (0-127, default from param)

    Returns a summary dict.
    """
    try:
        import mido
    except ImportError:
        return {"error": "mido not installed"}

    # Sort by time
    sorted_pattern = sorted(pattern, key=lambda p: p.get("time", 0))

    # Open port once
    port = midi_utils.get_output_port()
    if port is None:
        return {"error": "No MIDI output port available. Use list_midi_ports to check."}

    spb = 60.0 / bpm  # seconds per beat

    for item in sorted_pattern:
        note = item.get("note")
        if isinstance(note, str):
            note = midi_utils.note_to_number(note)
        t = item.get("time", 0)
        dur = item.get("duration", spb * 0.5)
        vel = item.get("velocity", velocity)
        ch = item.get("channel", channel)

        # Wait until it's time
        time.sleep(max(0, t))

        # Send note on
        note_on = mido.Message("note_on", note=int(note), velocity=int(vel), channel=int(ch))
        midi_utils.send_midi(note_on)

        # Hold for duration
        time.sleep(dur)

        # Send note off
        note_off = mido.Message("note_off", note=int(note), velocity=0, channel=int(ch))
        midi_utils.send_midi(note_off)

    return {"played": len(sorted_pattern), "bpm": bpm}


def play_drum_pattern(
    steps: list[dict],
    bpm: int = 120,
    bars: int = 1,
    channel: int = 10,
) -> dict:
    """Play a drum pattern from a step grid.

    Each item in steps: {"step": 0, "drums": ["kick", "snare"]}
    - step: 0-15 (16th note position in a 4/4 bar)
    - drums: list of drum names ("kick", "snare", "hihat", etc.)

    Returns a summary dict.
    """
    try:
        import mido
    except ImportError:
        return {"error": "mido not installed"}

    port = midi_utils.get_output_port()
    if port is None:
        return {"error": "No MIDI output port available. Use list_midi_ports to check."}

    spb = 60.0 / bpm  # seconds per beat
    step_duration = spb / 4  # 16th note duration

    total_steps = bars * 16
    current_step = 0

    for bar in range(bars):
        for step_num in range(16):
            # Find drums for this step
            for item in steps:
                if item.get("step") == step_num:
                    for drum_name in item.get("drums", []):
                        try:
                            note = midi_utils.drum_to_number(drum_name)
                            note_on = mido.Message(
                                "note_on", note=note, velocity=100, channel=int(channel)
                            )
                            midi_utils.send_midi(note_on)
                        except ValueError as exc:
                            logger.warning("Unknown drum %s: %s", drum_name, exc)

            time.sleep(step_duration)

    return {"played": total_steps, "bpm": bpm, "bars": bars}
