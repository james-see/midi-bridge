"""MIDI utility functions — note name conversion, port management."""

from __future__ import annotations

import logging
import threading
from typing import Optional

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Note name ↔ MIDI number conversion
# ---------------------------------------------------------------------------

_NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B", "B"]


def note_to_number(note_spec: str) -> int:
    """Convert a note name like 'C4' or 'F#5' to a MIDI note number.

    Format: <name><octave>  e.g. C4=60, A5=81, F#3=54
    """
    note_spec = note_spec.strip()
    # Handle both 'F#4' and 'F#4'
    if "#" in note_spec:
        name = note_spec[:-1].capitalize() + "#"
        octave = int(note_spec[-1])
    elif "b" in note_spec:
        # Convert flat to sharp
        flat_map = {"Db": "C#", "Eb": "D#", "Gb": "F#",
                    "Ab": "G#", "Bb": "A#"}
        name = note_spec[:-1].capitalize()
        name = flat_map.get(name, name)
        octave = int(note_spec[-1])
    else:
        name = note_spec[:-1].capitalize()
        octave = int(note_spec[-1])

    try:
        semitone = _NOTE_NAMES.index(name)
    except ValueError:
        raise ValueError(f"Unknown note name: {note_spec}")

    return (octave + 1) * 12 + semitone


def number_to_note(number: int) -> str:
    """Convert a MIDI note number to a name like 'C4'."""
    octave = (number // 12) - 1
    semitone = number % 12
    return f"{_NOTE_NAMES[semitone]}{octave}"


# ---------------------------------------------------------------------------
# Drum name ↔ MIDI number (GM standard, channel 10)
# ---------------------------------------------------------------------------

_DRUM_MAP = {
    "kick": 36, "bass": 36,
    "snare": 38,
    "side_stick": 37, "rimshot": 37,
    "hihat": 42, "hihat_closed": 42, "hihat_closed": 42,
    "hihat_open": 46, "open_hihat": 46,
    "low_tom": 41, "tom_low": 41,
    "mid_tom": 47, "tom_mid": 47, "midtom": 47,
    "high_tom": 48, "tom_high": 48, "hitom": 48,
    "crash": 49, "crash_cymbal": 49,
    "ride": 51, "ride_cymbal": 51,
    "cowbell": 56,
    "clap": 39,
    "tambourine": 54,
}


def drum_to_number(name: str) -> int:
    """Convert a drum name like 'kick' to GM MIDI note number."""
    key = name.strip().lower().replace(" ", "_")
    if key not in _DRUM_MAP:
        raise ValueError(f"Unknown drum: {name}. Known: {list(_DRUM_MAP.keys())}")
    return _DRUM_MAP[key]


def number_to_drum(number: int) -> str:
    """Convert a GM MIDI note number back to drum name."""
    for name, num in _DRUM_MAP.items():
        if num == number:
            return name
    return f"drum_{number}"


# ---------------------------------------------------------------------------
# Port management
# ---------------------------------------------------------------------------

_port_lock = threading.Lock()
_output_port: Optional[str] = None
_virtual_port_name = "MIDI Bridge"
_virtual_port = None  # mido port object


def set_virtual_port_name(name: str) -> None:
    global _virtual_port_name
    with _port_lock:
        _virtual_port_name = name
        _virtual_port = None  # force re-init


def get_output_port() -> Optional[str]:
    """Return the active output port name, initializing if needed."""
    global _output_port, _virtual_port
    with _port_lock:
        if _output_port is not None:
            return _output_port
        try:
            import mido
        except ImportError:
            logger.warning("mido not installed — MIDI tools will fail")
            return None

        # Try to open a virtual port first (creates one if none exists)
        try:
            _virtual_port = mido.open_output(_virtual_port_name, virtual=True)
            _output_port = _virtual_port_name
            logger.info("MIDI Bridge virtual port created: %s", _virtual_port_name)
        except Exception as exc:
            # Fallback: try to find an existing output port
            try:
                names = mido.get_output_names()
                if names:
                    _output_port = names[0]
                    logger.info("MIDI Bridge using existing port: %s", _output_port)
                else:
                    logger.warning("No MIDI output ports available")
            except Exception:
                logger.warning("Failed to find MIDI ports: %s", exc)
        return _output_port


def set_output_port(port_name: str) -> bool:
    """Set the output port by name."""
    global _output_port, _virtual_port
    with _port_lock:
        try:
            import mido
            # Close existing virtual port
            if _virtual_port is not None:
                try:
                    _virtual_port.close()
                except Exception:
                    pass
                _virtual_port = None
            _output_port = port_name
            return True
        except Exception as exc:
            logger.warning("Failed to set output port: %s", exc)
            return False


def list_ports() -> list[str]:
    """List available MIDI output ports."""
    try:
        import mido
        return mido.get_output_names() or []
    except ImportError:
        return []


def send_midi(msg) -> bool:
    """Send a mido Message to the active output port."""
    port = get_output_port()
    if port is None:
        return False
    try:
        import mido
        out = mido.open_output(port)
        out.send(msg)
        # Don't close — keep the port open for subsequent notes
        # mido caches open ports by name
        return True
    except Exception as exc:
        logger.warning("MIDI send failed: %s", exc)
        return False
