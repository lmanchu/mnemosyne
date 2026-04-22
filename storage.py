"""SQLite storage for screenshots, batches, and activity cards.

Schema follows INTERFACE.md spec. Single file, no ORM.
"""

import json
import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path.home() / ".mnemosyne" / "context.db"

# Phase 2 CAE migration: persona writes also land in irisgo-hermes' cae.db
# so the Rust chat path can read persona without a sidecar round-trip.
# Schema (id/version/data/confidence/created_at) matches mnemosyne's persona
# table exactly — see cae-core/src/storage.rs migrate(). Read-only consumers
# (synthesizer, editor) keep using mnemosyne.db; only writes are mirrored.
CAE_DB_PATH = Path.home() / ".irisgo" / "cae.db"


def get_db() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    _ensure_schema(conn)
    return conn


def _ensure_schema(conn: sqlite3.Connection):
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS screenshots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            captured_at INTEGER NOT NULL,
            file_path TEXT NOT NULL,
            file_size INTEGER,
            idle_seconds INTEGER DEFAULT 0,
            active_app TEXT,
            window_title TEXT,
            url TEXT,
            batch_id INTEGER,
            is_deleted INTEGER DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS batches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            start_time TEXT NOT NULL,
            end_time TEXT NOT NULL,
            screenshot_count INTEGER DEFAULT 0,
            status TEXT DEFAULT 'pending',
            provider TEXT,
            model TEXT,
            llm_call_duration_ms INTEGER,
            llm_input_tokens INTEGER,
            llm_output_tokens INTEGER,
            transcription TEXT,
            error_message TEXT,
            created_at TEXT DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS cards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            batch_id INTEGER NOT NULL,
            start_time TEXT NOT NULL,
            end_time TEXT NOT NULL,
            category TEXT,
            subcategory TEXT,
            title TEXT,
            summary TEXT,
            detailed_summary TEXT,
            apps_used TEXT,
            urls_visited TEXT,
            distractions TEXT,
            confidence REAL,
            provider TEXT,
            model TEXT,
            created_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (batch_id) REFERENCES batches(id)
        );

        CREATE TABLE IF NOT EXISTS onboarding (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            step TEXT NOT NULL,
            data TEXT NOT NULL,
            completed_at TEXT DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS persona (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            version TEXT NOT NULL,
            data TEXT NOT NULL,
            confidence REAL DEFAULT 0.0,
            created_at TEXT DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS daily_summaries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL UNIQUE,
            summary TEXT NOT NULL,
            card_count INTEGER DEFAULT 0,
            categories TEXT,
            top_apps TEXT,
            active_hours REAL DEFAULT 0.0,
            provider TEXT,
            model TEXT,
            created_at TEXT DEFAULT (datetime('now'))
        );

        CREATE INDEX IF NOT EXISTS idx_screenshots_batch ON screenshots(batch_id);
        CREATE INDEX IF NOT EXISTS idx_screenshots_captured ON screenshots(captured_at);
        CREATE INDEX IF NOT EXISTS idx_cards_time ON cards(start_time, end_time);
        CREATE INDEX IF NOT EXISTS idx_batches_status ON batches(status);
    """)


def save_screenshot(captured_at: int, file_path: str, file_size: int,
                    idle_seconds: int = 0, active_app: str = "",
                    window_title: str = "", url: str = "") -> int:
    conn = get_db()
    cur = conn.execute(
        "INSERT INTO screenshots (captured_at, file_path, file_size, idle_seconds, active_app, window_title, url) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)",
        (captured_at, file_path, file_size, idle_seconds, active_app, window_title, url)
    )
    conn.commit()
    conn.close()
    return cur.lastrowid


def get_unbatched_screenshots() -> list[dict]:
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM screenshots WHERE batch_id IS NULL AND is_deleted = 0 ORDER BY captured_at"
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def create_batch(screenshot_ids: list[int], start_time: str, end_time: str) -> int:
    conn = get_db()
    cur = conn.execute(
        "INSERT INTO batches (start_time, end_time, screenshot_count, status) VALUES (?, ?, ?, 'pending')",
        (start_time, end_time, len(screenshot_ids))
    )
    batch_id = cur.lastrowid
    placeholders = ",".join("?" * len(screenshot_ids))
    conn.execute(
        f"UPDATE screenshots SET batch_id = ? WHERE id IN ({placeholders})",
        [batch_id] + screenshot_ids
    )
    conn.commit()
    conn.close()
    return batch_id


def update_batch(batch_id: int, **kwargs):
    conn = get_db()
    sets = ", ".join(f"{k} = ?" for k in kwargs)
    vals = list(kwargs.values()) + [batch_id]
    conn.execute(f"UPDATE batches SET {sets} WHERE id = ?", vals)
    conn.commit()
    conn.close()


def save_card(batch_id: int, card: dict) -> int:
    conn = get_db()
    cur = conn.execute(
        "INSERT INTO cards (batch_id, start_time, end_time, category, subcategory, "
        "title, summary, detailed_summary, apps_used, urls_visited, distractions, "
        "confidence, provider, model) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (
            batch_id, card["start_time"], card["end_time"],
            card.get("category", ""), card.get("subcategory", ""),
            card.get("title", ""), card.get("summary", ""),
            card.get("detailed_summary", ""),
            json.dumps(card.get("apps_used", [])),
            json.dumps(card.get("urls_visited", [])),
            json.dumps(card.get("distractions", [])),
            card.get("confidence", 0.0),
            card.get("provider", ""), card.get("model", "")
        )
    )
    conn.commit()
    conn.close()
    return cur.lastrowid


def get_cards(date: str = None, limit: int = 50) -> list[dict]:
    conn = get_db()
    if date:
        rows = conn.execute(
            "SELECT * FROM cards WHERE start_time LIKE ? ORDER BY start_time DESC LIMIT ?",
            (f"{date}%", limit)
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM cards ORDER BY start_time DESC LIMIT ?", (limit,)
        ).fetchall()
    conn.close()
    results = []
    for r in rows:
        d = dict(r)
        for field in ("apps_used", "urls_visited", "distractions"):
            if d.get(field):
                try:
                    d[field] = json.loads(d[field])
                except (json.JSONDecodeError, TypeError):
                    pass
        results.append(d)
    return results


def get_cards_since(days: int = 3, limit: int = 500) -> list[dict]:
    """Get all cards from the last N days."""
    conn = get_db()
    cutoff = (datetime.now().timestamp() - days * 86400)
    cutoff_iso = datetime.fromtimestamp(cutoff).isoformat()
    rows = conn.execute(
        "SELECT * FROM cards WHERE start_time >= ? ORDER BY start_time DESC LIMIT ?",
        (cutoff_iso, limit)
    ).fetchall()
    conn.close()
    results = []
    for r in rows:
        d = dict(r)
        for field in ("apps_used", "urls_visited", "distractions"):
            if d.get(field):
                try:
                    d[field] = json.loads(d[field])
                except (json.JSONDecodeError, TypeError):
                    pass
        results.append(d)
    return results


def save_onboarding_step(step: str, data: dict) -> int:
    conn = get_db()
    cur = conn.execute(
        "INSERT INTO onboarding (step, data) VALUES (?, ?)",
        (step, json.dumps(data))
    )
    conn.commit()
    conn.close()
    return cur.lastrowid


def get_onboarding_step(step: str) -> dict | None:
    conn = get_db()
    row = conn.execute(
        "SELECT * FROM onboarding WHERE step = ? ORDER BY id DESC LIMIT 1", (step,)
    ).fetchone()
    conn.close()
    if not row:
        return None
    d = dict(row)
    try:
        d["data"] = json.loads(d["data"])
    except (json.JSONDecodeError, TypeError):
        pass
    return d


def save_persona(version: str, data: dict, confidence: float) -> int:
    conn = get_db()
    cur = conn.execute(
        "INSERT INTO persona (version, data, confidence) VALUES (?, ?, ?)",
        (version, json.dumps(data), confidence)
    )
    conn.commit()
    conn.close()
    rowid = cur.lastrowid
    _mirror_persona_to_cae(version, data, confidence)
    return rowid


def _mirror_persona_to_cae(version: str, data: dict, confidence: float) -> None:
    """Best-effort dual-write into irisgo-hermes' cae.db.

    Skips silently if the file doesn't exist (IrisGo not installed) or
    the write fails (table missing, locked, schema drift). Mnemosyne's
    own write must never fail because of this — it's a cache for the
    Rust chat path, not the source of truth.
    """
    if not CAE_DB_PATH.exists():
        return
    try:
        conn = sqlite3.connect(str(CAE_DB_PATH), timeout=2.0)
        try:
            conn.execute(
                "INSERT INTO persona (version, data, confidence) VALUES (?, ?, ?)",
                (version, json.dumps(data), confidence),
            )
            conn.commit()
        finally:
            conn.close()
    except sqlite3.Error as e:
        # Don't propagate — this is a mirror, not the primary path.
        print(f"[storage] cae.db persona mirror skipped: {e}")


def get_latest_persona() -> dict | None:
    conn = get_db()
    row = conn.execute(
        "SELECT * FROM persona ORDER BY id DESC LIMIT 1"
    ).fetchone()
    conn.close()
    if not row:
        return None
    d = dict(row)
    try:
        d["data"] = json.loads(d["data"])
    except (json.JSONDecodeError, TypeError):
        pass
    return d


def save_daily_summary(date: str, summary: str, card_count: int,
                      categories: list[str], top_apps: list[str],
                      active_hours: float, provider: str = "", model: str = "") -> int:
    conn = get_db()
    conn.execute(
        """INSERT OR REPLACE INTO daily_summaries
           (date, summary, card_count, categories, top_apps, active_hours, provider, model)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (date, summary, card_count, json.dumps(categories), json.dumps(top_apps),
         active_hours, provider, model)
    )
    conn.commit()
    rid = conn.execute("SELECT id FROM daily_summaries WHERE date = ?", (date,)).fetchone()[0]
    conn.close()
    return rid


def get_daily_summary(date: str) -> dict | None:
    conn = get_db()
    row = conn.execute(
        "SELECT * FROM daily_summaries WHERE date = ?", (date,)
    ).fetchone()
    conn.close()
    if not row:
        return None
    d = dict(row)
    for field in ("categories", "top_apps"):
        if d.get(field):
            try:
                d[field] = json.loads(d[field])
            except (json.JSONDecodeError, TypeError):
                pass
    return d


def get_timeline(date: str) -> dict:
    """Get chronological activity timeline for a date.

    Returns: {date, cards: [...], stats: {card_count, categories, top_apps, active_hours}}
    """
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM cards WHERE start_time LIKE ? ORDER BY start_time ASC",
        (f"{date}%",)
    ).fetchall()
    conn.close()

    cards = []
    all_apps = {}
    categories = {}
    total_seconds = 0

    for r in rows:
        d = dict(r)
        for field in ("apps_used", "urls_visited", "distractions"):
            if d.get(field):
                try:
                    d[field] = json.loads(d[field])
                except (json.JSONDecodeError, TypeError):
                    pass

        # Calculate duration from start_time to end_time
        try:
            st = datetime.fromisoformat(d["start_time"])
            et = datetime.fromisoformat(d["end_time"])
            d["duration_minutes"] = round((et - st).total_seconds() / 60, 1)
            total_seconds += (et - st).total_seconds()
        except (ValueError, TypeError):
            d["duration_minutes"] = 0

        # Aggregate stats
        cat = d.get("category", "Other")
        categories[cat] = categories.get(cat, 0) + 1
        for app in (d.get("apps_used") or []):
            all_apps[app] = all_apps.get(app, 0) + 1

        cards.append(d)

    # Sort apps by frequency
    top_apps = sorted(all_apps.keys(), key=lambda a: all_apps[a], reverse=True)[:10]

    return {
        "date": date,
        "cards": cards,
        "stats": {
            "card_count": len(cards),
            "categories": dict(categories),
            "top_apps": top_apps,
            "active_hours": round(total_seconds / 3600, 1),
        }
    }


def recover_stale_batches(timeout_minutes: int = 30) -> int:
    """Mark pending batches older than timeout as failed, release their screenshots.

    Returns number of batches recovered.
    """
    conn = get_db()
    cutoff = datetime.now().timestamp() - timeout_minutes * 60
    cutoff_iso = datetime.fromtimestamp(cutoff).isoformat()

    # Find stale pending batches
    stale = conn.execute(
        "SELECT id FROM batches WHERE status = 'pending' AND created_at < ?",
        (cutoff_iso,)
    ).fetchall()

    if not stale:
        conn.close()
        return 0

    stale_ids = [r["id"] for r in stale]
    placeholders = ",".join("?" * len(stale_ids))

    # Release screenshots back to unbatched pool
    conn.execute(
        f"UPDATE screenshots SET batch_id = NULL WHERE batch_id IN ({placeholders})",
        stale_ids
    )

    # Mark batches as failed
    conn.execute(
        f"UPDATE batches SET status = 'failed', error_message = 'timeout: stale pending batch recovered' "
        f"WHERE id IN ({placeholders})",
        stale_ids
    )

    conn.commit()
    conn.close()
    return len(stale_ids)


def cleanup_processed_screenshots(keep_days: int = 3) -> tuple[int, float]:
    """Delete screenshot files for completed batches older than keep_days.

    Marks DB records as is_deleted=1 but keeps the rows.
    Returns (files_deleted, mb_freed).
    """
    conn = get_db()
    cutoff = datetime.now().timestamp() - keep_days * 86400
    cutoff_iso = datetime.fromtimestamp(cutoff).isoformat()

    # Find screenshots in completed batches that are old enough and not yet deleted
    rows = conn.execute(
        """SELECT s.id, s.file_path, s.file_size FROM screenshots s
           JOIN batches b ON s.batch_id = b.id
           WHERE b.status = 'completed'
             AND s.is_deleted = 0
             AND b.created_at < ?""",
        (cutoff_iso,)
    ).fetchall()

    deleted = 0
    freed_bytes = 0
    for r in rows:
        p = Path(r["file_path"])
        if p.exists():
            try:
                freed_bytes += r["file_size"] or 0
                p.unlink()
                deleted += 1
            except OSError:
                continue

    if deleted > 0:
        ids = [r["id"] for r in rows]
        # Mark in chunks to avoid SQL variable limit
        for i in range(0, len(ids), 500):
            chunk = ids[i:i + 500]
            placeholders = ",".join("?" * len(chunk))
            conn.execute(
                f"UPDATE screenshots SET is_deleted = 1 WHERE id IN ({placeholders})",
                chunk
            )
        conn.commit()

    conn.close()
    return deleted, freed_bytes / (1024 * 1024)


if __name__ == "__main__":
    conn = get_db()
    print(f"DB: {DB_PATH}")
    for table in ("screenshots", "batches", "cards", "onboarding", "persona"):
        count = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        print(f"  {table}: {count} rows")
    conn.close()
