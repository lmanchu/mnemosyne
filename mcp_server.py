"""Mnemosyne MCP Server — context-aware engine for IrisGo.

Exposes Mnemosyne's context data as MCP tools and resources.
Run: python mcp_server.py (stdio transport for MCP clients)

Tools:
  - mnemosyne_context_now: Current activity + system prompt fragment
  - mnemosyne_get_cards: Query ActivityCards by date/time
  - mnemosyne_get_profile: Aggregated user context profile
  - mnemosyne_get_summary: AI-generated day summary
  - mnemosyne_health: System status
  - mnemosyne_timeline: Chronological activity timeline for a day
  - mnemosyne_daily_summary: AI-generated narrative daily summary

Resources:
  - mnemosyne://context/now: Auto-injectable current context
"""

import json
import os
import threading
import time
from datetime import datetime, timedelta
from pathlib import Path

from mcp.server.fastmcp import FastMCP

import storage

# ── Server setup ──────────────────────────────────────────

mcp = FastMCP("mnemosyne")

# ── Background capture (optional, if GEMINI_API_KEY set) ──

CAPTURE_ACTIVE = False
CAPTURE_THREAD = None


def _background_capture_loop():
    """Capture screenshots in background every INTERVAL seconds."""
    import capture
    interval = int(os.environ.get("MNEMOSYNE_CAPTURE_INTERVAL", "10"))
    global CAPTURE_ACTIVE
    CAPTURE_ACTIVE = True
    while CAPTURE_ACTIVE:
        try:
            path = capture.capture_screenshot()
            ts = int(datetime.now().timestamp())
            storage.save_screenshot(
                captured_at=ts,
                file_path=str(path),
                file_size=path.stat().st_size
            )
        except Exception as e:
            print(f"[mnemosyne] capture error: {e}")
        time.sleep(interval)


def start_capture():
    global CAPTURE_THREAD
    if CAPTURE_THREAD and CAPTURE_THREAD.is_alive():
        return
    CAPTURE_THREAD = threading.Thread(target=_background_capture_loop, daemon=True)
    CAPTURE_THREAD.start()


# ── Helper: build system prompt fragment ──────────────────

def _build_system_prompt_fragment(cards: list[dict]) -> str:
    if not cards:
        return "No recent activity data available."

    latest = cards[0]
    lines = [
        "You are assisting a user who is currently:",
        f"- Activity: {latest.get('title', 'Unknown')}",
        f"- Category: {latest.get('category', 'Unknown')}",
    ]

    apps = latest.get("apps_used", [])
    if isinstance(apps, str):
        try:
            apps = json.loads(apps)
        except (json.JSONDecodeError, TypeError):
            apps = []
    if apps:
        lines.append(f"- Apps: {', '.join(apps)}")

    if len(cards) > 1:
        categories = [c.get("category", "") for c in cards[:5] if c.get("category")]
        if categories:
            lines.append(f"- Recent focus: {', '.join(dict.fromkeys(categories))}")

    lines.append("")
    lines.append("Adapt your responses to their current context.")
    return "\n".join(lines)


def _build_profile(cards: list[dict]) -> dict:
    """Aggregate cards into a context profile."""
    if not cards:
        return {"status": "no_data", "message": "No activity cards yet. Run the pipeline first."}

    # Category breakdown
    cat_minutes = {}
    for c in cards:
        cat = c.get("category", "Other")
        try:
            start = datetime.fromisoformat(c["start_time"])
            end = datetime.fromisoformat(c["end_time"])
            minutes = (end - start).total_seconds() / 60
        except (ValueError, KeyError):
            minutes = 15  # default batch duration
        cat_minutes[cat] = cat_minutes.get(cat, 0) + minutes

    total = sum(cat_minutes.values()) or 1
    top_categories = [
        {"name": k, "minutes": round(v), "pct": round(v / total * 100)}
        for k, v in sorted(cat_minutes.items(), key=lambda x: -x[1])
    ]

    # Apps used
    all_apps = set()
    for c in cards:
        apps = c.get("apps_used", [])
        if isinstance(apps, str):
            try:
                apps = json.loads(apps)
            except (json.JSONDecodeError, TypeError):
                apps = []
        all_apps.update(apps)

    return {
        "generated_at": datetime.now().isoformat(),
        "card_count": len(cards),
        "total_tracked_minutes": round(total),
        "top_categories": top_categories,
        "apps_used": sorted(all_apps),
        "current_activity": cards[0].get("title", "") if cards else None,
    }


# ── MCP Tools ─────────────────────────────────────────────

@mcp.tool()
def mnemosyne_context_now() -> str:
    """Get the user's current activity context and a system prompt fragment.
    Call this before each AI interaction to personalize responses.
    Returns current activity, recent cards, and a ready-to-use system prompt fragment."""
    cards = storage.get_cards(limit=5)
    fragment = _build_system_prompt_fragment(cards)

    result = {
        "current": cards[0] if cards else None,
        "recent_cards_count": len(cards),
        "system_prompt_fragment": fragment
    }
    return json.dumps(result, indent=2, default=str)


@mcp.tool()
def mnemosyne_get_cards(date: str = "", category: str = "", limit: int = 20) -> str:
    """Query ActivityCards. Each card represents a 15-minute block of user activity.

    Args:
        date: Filter by date (YYYY-MM-DD format). Empty = all dates.
        category: Filter by category (Development, Communication, Research, etc). Empty = all.
        limit: Max cards to return (default 20).
    """
    cards = storage.get_cards(date=date if date else None, limit=limit)
    if category:
        cards = [c for c in cards if c.get("category", "").lower() == category.lower()]
    return json.dumps(cards, indent=2, default=str)


@mcp.tool()
def mnemosyne_get_profile(date: str = "") -> str:
    """Get aggregated user context profile — category breakdown, apps used, patterns.

    Args:
        date: Date to profile (YYYY-MM-DD). Empty = today.
    """
    if not date:
        date = datetime.now().strftime("%Y-%m-%d")
    cards = storage.get_cards(date=date, limit=200)
    profile = _build_profile(cards)
    profile["date"] = date
    return json.dumps(profile, indent=2, default=str)


@mcp.tool()
def mnemosyne_get_summary(date: str = "") -> str:
    """Get a natural language summary of the user's day.

    Args:
        date: Date to summarize (YYYY-MM-DD). Empty = today.
    """
    if not date:
        date = datetime.now().strftime("%Y-%m-%d")
    cards = storage.get_cards(date=date, limit=200)

    if not cards:
        return json.dumps({"date": date, "summary": "No activity data for this date."})

    # Build summary from cards (no extra LLM call for now — just aggregate)
    categories = {}
    for c in cards:
        cat = c.get("category", "Other")
        categories[cat] = categories.get(cat, 0) + 1

    titles = [c.get("title", "") for c in cards[:10]]
    cat_str = ", ".join(f"{v} blocks of {k}" for k, v in sorted(categories.items(), key=lambda x: -x[1]))

    summary = {
        "date": date,
        "card_count": len(cards),
        "summary": f"Tracked {len(cards)} activity blocks: {cat_str}.",
        "highlights": titles[:5],
        "categories": categories
    }
    return json.dumps(summary, indent=2, default=str)


@mcp.tool()
def mnemosyne_health() -> str:
    """Check Mnemosyne system status — capture state, DB stats, provider info."""
    db_path = storage.DB_PATH
    captures_dir = Path.home() / ".mnemosyne" / "captures"

    # DB stats
    conn = storage.get_db()
    stats = {}
    for table in ("screenshots", "batches", "cards"):
        stats[table] = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]

    # Latest capture
    latest = conn.execute(
        "SELECT captured_at FROM screenshots ORDER BY captured_at DESC LIMIT 1"
    ).fetchone()
    conn.close()

    # Captures dir size
    captures_size = sum(f.stat().st_size for f in captures_dir.rglob("*.jpg")) if captures_dir.exists() else 0

    result = {
        "status": "running" if CAPTURE_ACTIVE else "idle",
        "capture_active": CAPTURE_ACTIVE,
        "capture_interval": int(os.environ.get("MNEMOSYNE_CAPTURE_INTERVAL", "10")),
        "db_path": str(db_path),
        "db_rows": stats,
        "captures_size_mb": round(captures_size / 1024 / 1024, 1),
        "last_capture": datetime.fromtimestamp(latest[0]).isoformat() if latest else None,
        "gemini_configured": bool(os.environ.get("GEMINI_API_KEY")),
    }
    return json.dumps(result, indent=2, default=str)


@mcp.tool()
def mnemosyne_timeline(date: str = "") -> str:
    """Get chronological activity timeline for a given day.
    Returns cards in time order with duration, categories, and summary stats.

    Args:
        date: Date to query (YYYY-MM-DD). Empty = today.
    """
    if not date:
        date = datetime.now().strftime("%Y-%m-%d")
    timeline = storage.get_timeline(date)
    return json.dumps(timeline, indent=2, default=str)


@mcp.tool()
def mnemosyne_daily_summary(date: str = "") -> str:
    """Get AI-generated daily narrative summary.
    Returns a prose summary of the user's day based on their ActivityCards.

    Args:
        date: Date to query (YYYY-MM-DD). Empty = yesterday.
    """
    if not date:
        date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    summary = storage.get_daily_summary(date)
    if summary:
        return json.dumps(summary, indent=2, default=str)

    # Fallback: return stats without narrative
    timeline = storage.get_timeline(date)
    return json.dumps({
        "date": date,
        "summary": None,
        "message": "No AI summary generated yet. Will auto-generate overnight.",
        "stats": timeline["stats"]
    }, indent=2, default=str)


# ── MCP Resource ──────────────────────────────────────────

@mcp.resource("mnemosyne://context/now")
def context_resource() -> str:
    """Current user context — auto-injectable into conversations."""
    return mnemosyne_context_now()


# ── Entry point ───────────────────────────────────────────

if __name__ == "__main__":
    # Start background capture if GEMINI_API_KEY is set
    if os.environ.get("MNEMOSYNE_CAPTURE_ENABLED", "").lower() in ("1", "true", "yes"):
        start_capture()
        print("[mnemosyne] Background capture started")

    # Run MCP server on stdio
    mcp.run()
