"""Shared system-prompt fragment builder.

Both api.py (REST /api/v1/context/now) and mcp_server.py (MCP tool
`mnemosyne_context_now`) need to emit the same persona + activity context.
Previously each file had its own copy, which silently drifted — api.py
gained persona injection while the MCP path did not, so IrisGo's UI chat
saw richer context than Telegram/Discord replies routed through MCP.

Single source of truth: use `build_fragment(cards)` from both paths.
"""

import json


def _persona_lines(persona_row: dict | None) -> list[str]:
    """Build the persona block. Empty list if no useful data."""
    if not persona_row:
        return []
    pdata = persona_row.get("data", {})
    if isinstance(pdata, str):
        try: pdata = json.loads(pdata)
        except (json.JSONDecodeError, TypeError): pdata = {}

    lines: list[str] = []

    summary = (pdata.get("summary") or "").strip()
    if summary:
        lines += ["About this user:", summary]

    ident = pdata.get("identity") or {}
    role = ident.get("likely_role") or ident.get("role")
    if role:
        lines.append(f"- Role: {role}")
    seniority = ident.get("seniority")
    if seniority and seniority not in ("_unknown_", "_not yet determined_"):
        lines.append(f"- Seniority: {seniority}")

    ws = pdata.get("work_style") or {}
    if ws.get("communication"):
        lines.append(f"- Communication style: {ws['communication']}")
    if ws.get("peak_hours"):
        lines.append(f"- Peak hours: {ws['peak_hours']}")

    interests = pdata.get("interests") or {}
    current_interests = interests.get("current") or []
    if isinstance(current_interests, str):
        current_interests = [current_interests]
    if current_interests:
        lines.append(f"- Interests: {', '.join(current_interests)}")

    if not lines:
        return []
    if not summary:
        lines.insert(0, "About this user:")
    return lines


def _activity_lines(cards: list[dict]) -> list[str]:
    """Build the 'what the user is doing now' block."""
    if not cards:
        return ["No recent activity data available."]
    latest = cards[0]
    lines = [
        "You are assisting a user who is currently:",
        f"- Activity: {latest.get('title', 'Unknown')}",
        f"- Category: {latest.get('category', 'Unknown')}",
    ]
    summary = (latest.get("summary") or "").strip()
    if summary:
        lines.append(f"- Summary: {summary}")
    apps = latest.get("apps_used", [])
    if isinstance(apps, str):
        try: apps = json.loads(apps)
        except (json.JSONDecodeError, TypeError): apps = []
    if apps:
        lines.append(f"- Apps: {', '.join(apps)}")
    source = latest.get("source")
    if source:
        lines.append(f"- Context source: {source}")
    return lines


def build_fragment(cards: list[dict], persona_row: dict | None = None) -> str:
    """Compose the system prompt fragment: persona → activity → guidance.

    Caller supplies persona_row (usually `storage.get_latest_persona()`).
    Pass `None` to skip persona injection entirely.
    """
    sections: list[list[str]] = []

    plines = _persona_lines(persona_row)
    if plines:
        sections.append(plines)

    sections.append(_activity_lines(cards))
    sections.append(["Adapt your responses to their persona and current context."])

    return "\n\n".join("\n".join(section) for section in sections)
