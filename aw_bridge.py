"""ActivityWatch bridge — enrich screenshots with app/window metadata.

Queries ActivityWatch REST API for active window and AFK status.
Falls back gracefully if AW is not running.

AW API: http://localhost:5600/api/0/
"""

import json
import socket
import urllib.request
from datetime import datetime, timezone

AW_BASE = "http://localhost:5600/api/0"
AW_TIMEOUT = 2  # seconds


def _get(path: str) -> dict | list | None:
    try:
        req = urllib.request.Request(f"{AW_BASE}{path}")
        with urllib.request.urlopen(req, timeout=AW_TIMEOUT) as resp:
            return json.loads(resp.read())
    except Exception:
        return None


def is_running() -> bool:
    """Check if ActivityWatch server is running."""
    try:
        s = socket.create_connection(("localhost", 5600), timeout=1)
        s.close()
        return True
    except (ConnectionRefusedError, OSError):
        return False


def get_hostname() -> str:
    """Get hostname for bucket names."""
    return socket.gethostname()


def get_window_buckets() -> list[str]:
    """Find all aw-watcher-window buckets."""
    buckets = _get("/buckets")
    if not buckets:
        return []
    return [b for b in buckets if b.startswith("aw-watcher-window")]


def get_afk_buckets() -> list[str]:
    """Find all aw-watcher-afk buckets."""
    buckets = _get("/buckets")
    if not buckets:
        return []
    return [b for b in buckets if b.startswith("aw-watcher-afk")]


def get_current_window() -> dict | None:
    """Get the currently active window.
    Returns: {app, title, url} or None.
    """
    buckets = get_window_buckets()
    if not buckets:
        return None

    # Get the most recent event from the first window bucket
    events = _get(f"/buckets/{buckets[0]}/events?limit=1")
    if not events or len(events) == 0:
        return None

    data = events[0].get("data", {})
    return {
        "app": data.get("app", ""),
        "title": data.get("title", ""),
        "url": data.get("url", ""),
    }


def get_afk_status() -> dict | None:
    """Get current AFK status.
    Returns: {status: 'not-afk'|'afk', duration: seconds} or None.
    """
    buckets = get_afk_buckets()
    if not buckets:
        return None

    events = _get(f"/buckets/{buckets[0]}/events?limit=1")
    if not events or len(events) == 0:
        return None

    data = events[0].get("data", {})
    duration = events[0].get("duration", 0)
    return {
        "status": data.get("status", "unknown"),
        "duration": round(duration),
    }


def get_current_context() -> dict:
    """Get combined current context from AW.
    Always returns a dict, empty fields if AW not running.
    """
    if not is_running():
        return {"aw_running": False, "app": "", "title": "", "url": "", "afk": False}

    window = get_current_window() or {}
    afk = get_afk_status() or {}

    return {
        "aw_running": True,
        "app": window.get("app", ""),
        "title": window.get("title", ""),
        "url": window.get("url", ""),
        "afk": afk.get("status") == "afk",
        "afk_duration": afk.get("duration", 0),
    }


if __name__ == "__main__":
    print(f"ActivityWatch running: {is_running()}")
    if is_running():
        print(f"Hostname: {get_hostname()}")
        print(f"Window buckets: {get_window_buckets()}")
        print(f"AFK buckets: {get_afk_buckets()}")
        print(f"Current window: {get_current_window()}")
        print(f"AFK status: {get_afk_status()}")
        print(f"Full context: {json.dumps(get_current_context(), indent=2)}")
    else:
        print("AW not running. Install from https://activitywatch.net/")
