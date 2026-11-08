"""Desktop plugin backend API for MIDI Bridge.

Exposes /activity endpoint returning recent MIDI events
so the desktop monitor pane can display them.
"""

from __future__ import annotations

from .. import midi_utils


def register(ctx):
    """Register the plugin API routes."""

    @ctx.route("/activity")
    def _get_activity(request):
        count = int(request.args.get("count", 20))
        activity = midi_utils.get_activity(count)
        return {"activity": activity}
