"""MIDI Bridge — send live MIDI to a DAW from Hermes Agent.

Registers 10 tools for sending MIDI events (notes, chords, drum patterns,
control changes, program changes, pitch bend, port management) plus
a slash command and 7 bundled skills (core + 6 genre recipes).
"""

from __future__ import annotations

import logging
import time
from pathlib import Path

from . import schemas, tools, midi_utils

logger = logging.getLogger(__name__)


def _handle_midi_command(raw_args: str) -> str:
    """Handle /midi slash command."""
    parts = raw_args.strip().split()
    if not parts or parts[0] in ("ports", "list"):
        return tools.list_midi_ports({})
    elif parts[0] == "test":
        # Send a test note
        return tools.send_note({"note": "C4", "velocity": 100, "duration": 0.5})
    elif parts[0] == "port":
        if len(parts) > 1:
            return tools.set_output({"port_name": parts[1]})
        return "Usage: /midi port <name>  (use /midi ports to list available)"
    elif parts[0] == "activity":
        count = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 20
        activity = midi_utils.get_activity(count)
        if not activity:
            return "No MIDI activity yet. Play some notes first."
        lines = [f"Last {len(activity)} MIDI events:"]
        for evt in activity:
            t = time.strftime("%H:%M:%S", time.localtime(evt["time"]))
            lines.append(f"  {t} [{evt['kind']}] {evt['note']} vel={evt['velocity']} ch={evt['channel']}")
        return "\n".join(lines)
    return (
        "Usage: /midi [ports|test|port <name>|activity]\n"
        "  ports    — list available MIDI ports\n"
        "  test     — play a test note (C4)\n"
        "  port <name> — set output port\n"
        "  activity — show recent MIDI events"
    )


def register(ctx):
    """Register MIDI Bridge tools, slash command, and skills."""
    config = {
        "default_channel": ctx.get_config("default_channel", default=1),
        "default_velocity": ctx.get_config("default_velocity", default=100),
        "default_bpm": ctx.get_config("default_bpm", default=120),
        "virtual_port_name": ctx.get_config("virtual_port_name", default="MIDI Bridge"),
    }
    tools.set_config(config)
    midi_utils.set_virtual_port_name(config["virtual_port_name"])

    # Register tools
    toolset = "midi-bridge"
    tool_map = {
        "send_note": tools.send_note,
        "send_notes": tools.send_notes,
        "send_cc": tools.send_cc,
        "send_program_change": tools.send_program_change,
        "send_pitch_bend": tools.send_pitch_bend,
        "play_pattern": tools.play_pattern,
        "drum_pattern": tools.drum_pattern,
        "list_midi_ports": tools.list_midi_ports,
        "set_output": tools.set_output,
    }

    for name, handler in tool_map.items():
        schema = getattr(schemas, name.upper(), None)
        if schema:
            ctx.register_tool(name=name, toolset=toolset, schema=schema, handler=handler)

    # Register slash command
    ctx.register_command(
        "midi",
        _handle_midi_command,
        description="List MIDI ports, test, or set output port",
    )

    # Register all bundled skills
    skills_dir = Path(__file__).parent / "skills"
    skill_count = 0
    if skills_dir.is_dir():
        for child in sorted(skills_dir.iterdir()):
            skill_md = child / "SKILL.md"
            if child.is_dir() and skill_md.exists():
                ctx.register_skill(child.name, str(skill_md))
                logger.info("MIDI Bridge skill registered: %s", child.name)
                skill_count += 1

    logger.info(
        "MIDI Bridge active (port=%s, tools=%d, skills=%d)",
        config["virtual_port_name"],
        len(tool_map),
        skill_count,
    )
