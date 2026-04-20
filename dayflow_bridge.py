"""Dayflow bridge — read Dayflow's timeline_cards as a context source.

Dayflow (teleportlabs.com) already captures screen + runs an LLM pipeline and
stores structured cards in ~/Library/Application Support/Dayflow/chunks.sqlite.
Reusing its cards avoids a duplicate capture loop and exposes months of history
without running Mnemosyne's own daemon.

Returns card dicts in the same shape that storage.get_cards() emits, so
api.py consumers (notably _build_system_prompt_fragment) need no changes.

Opens the DB read-only (uri=True, mode=ro) so we can't interfere with Dayflow.
"""

import json
import os
import sqlite3
from datetime import datetime

DB_PATH = os.path.expanduser(
    "~/Library/Application Support/Dayflow/chunks.sqlite"
)


def is_available() -> bool:
    return os.path.exists(DB_PATH)


def _open() -> sqlite3.Connection:
    # mode=ro + immutable=0 so we still see WAL updates from the live Dayflow.
    uri = f"file:{DB_PATH}?mode=ro"
    conn = sqlite3.connect(uri, uri=True, timeout=2)
    conn.row_factory = sqlite3.Row
    return conn


def _iso(ts: int | None) -> str:
    if ts is None:
        return ""
    return datetime.fromtimestamp(ts).isoformat()


def _row_to_card(r: sqlite3.Row) -> dict:
    meta = {}
    if r["metadata"]:
        try:
            meta = json.loads(r["metadata"]) or {}
        except (json.JSONDecodeError, TypeError):
            meta = {}
    distractions = meta.get("distractions", []) if isinstance(meta, dict) else []
    return {
        "id": r["id"],
        "start_time": _iso(r["start_ts"]),
        "end_time": _iso(r["end_ts"]),
        "category": r["category"] or "",
        "subcategory": r["subcategory"] or "",
        "title": r["title"] or "",
        "summary": r["summary"] or "",
        "detailed_summary": r["detailed_summary"] or "",
        "apps_used": [],
        "urls_visited": [],
        "distractions": distractions,
        "source": "dayflow",
    }


def get_cards(
    limit: int = 5,
    date: str | None = None,
    category: str | None = None,
) -> list[dict]:
    """Return non-deleted Dayflow timeline cards, most-recent first.

    Args:
        limit: Max cards to return.
        date: Filter to a specific day in YYYY-MM-DD format (matches `day` column).
        category: Case-insensitive category filter (Work/Personal/…).
    """
    if not is_available():
        return []
    try:
        conn = _open()
    except sqlite3.OperationalError:
        return []
    sql = (
        "SELECT id, start_ts, end_ts, title, summary, detailed_summary, "
        "category, subcategory, metadata "
        "FROM timeline_cards WHERE is_deleted = 0"
    )
    params: list = []
    if date:
        sql += " AND day = ?"
        params.append(date)
    if category:
        sql += " AND LOWER(category) = LOWER(?)"
        params.append(category)
    sql += " ORDER BY start_ts DESC LIMIT ?"
    params.append(limit)
    try:
        rows = conn.execute(sql, params).fetchall()
    except sqlite3.OperationalError:
        return []
    finally:
        conn.close()
    return [_row_to_card(r) for r in rows]


def get_timeline(date: str) -> dict:
    """Return all cards for a given day in chronological order, with stats."""
    cards = get_cards(limit=500, date=date)
    cards.sort(key=lambda c: c.get("start_time", ""))
    categories: dict[str, int] = {}
    for c in cards:
        cat = c.get("category") or "Other"
        categories[cat] = categories.get(cat, 0) + 1
    return {
        "date": date,
        "source": "dayflow",
        "card_count": len(cards),
        "categories": categories,
        "cards": cards,
    }


if __name__ == "__main__":
    import sys
    print(f"Dayflow DB available: {is_available()}")
    date_arg = sys.argv[1] if len(sys.argv) > 1 else None
    for card in get_cards(limit=5, date=date_arg):
        print(f"[{card['start_time']}] {card['category']}: {card['title']}")
        print(f"  {card['summary'][:120]}")
