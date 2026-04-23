#!/usr/bin/env python3
"""One-shot Dayflow → IrisGo CAE importer.

Reads Dayflow's `timeline_cards` from
~/Library/Application Support/Dayflow/chunks.sqlite (read-only) and
copies pre-CAE history into ~/.irisgo/cae.db's `timeline_cards` so the
Hermes agent can answer "what was I doing last week?" via cae.* MCP
tools alone — without the Mnemosyne sidecar's dayflow_bridge fallback.

Cutoff
------
By default, only Dayflow rows whose start_ts is strictly before the
oldest cae.db row land in cae.db. This avoids double-counting the
overlap window (cae's daemon and Dayflow may have both summarised the
same minutes once you ran the daemon for the first time).

Override with `--cutoff-ts <unix>` if you want a different boundary,
or `--cutoff-day YYYY-MM-DD`.

Idempotency
-----------
Imported rows are tagged `provider='dayflow'`. Re-running with
`--replace` clears every `provider='dayflow'` row from cae.db before
re-importing, so the script is safe to repeat after Dayflow gains new
old-history rows. Without `--replace`, a re-run is a no-op for any
(start_ts, title) pair already present from a previous import.

Usage
-----
    python3 scripts/import_dayflow_to_cae.py --dry-run
    python3 scripts/import_dayflow_to_cae.py
    python3 scripts/import_dayflow_to_cae.py --replace
    python3 scripts/import_dayflow_to_cae.py --cutoff-day 2026-04-21
"""

from __future__ import annotations

import argparse
import os
import sqlite3
import sys
from pathlib import Path

DAYFLOW_DB = Path.home() / "Library/Application Support/Dayflow/chunks.sqlite"
CAE_DB = Path.home() / ".irisgo/cae.db"

# We pin a single string for traceability so future maintainers can
# `SELECT COUNT(*) FROM timeline_cards WHERE provider='dayflow'`.
PROVIDER_TAG = "dayflow"


def open_dayflow() -> sqlite3.Connection:
    if not DAYFLOW_DB.exists():
        sys.exit(f"Dayflow DB not found at {DAYFLOW_DB} — is Dayflow installed?")
    # Read-only + WAL-aware so the live Dayflow process can keep writing.
    conn = sqlite3.connect(f"file:{DAYFLOW_DB}?mode=ro", uri=True, timeout=5)
    conn.row_factory = sqlite3.Row
    return conn


def open_cae() -> sqlite3.Connection:
    if not CAE_DB.exists():
        sys.exit(
            f"cae.db not found at {CAE_DB} — open IrisGo at least once "
            "to let the Tauri app create + migrate the schema."
        )
    conn = sqlite3.connect(str(CAE_DB), timeout=5)
    conn.row_factory = sqlite3.Row
    return conn


def resolve_cutoff_ts(args, cae: sqlite3.Connection) -> int | None:
    if args.cutoff_ts is not None:
        return args.cutoff_ts
    if args.cutoff_day:
        # Convert day → unix ts (00:00 local of that day)
        import datetime as dt
        d = dt.datetime.strptime(args.cutoff_day, "%Y-%m-%d")
        return int(d.timestamp())
    # Auto-cutoff = oldest cae row's start_ts. Anything older we trust
    # Dayflow for; anything newer we trust the daemon for. Excluding
    # rows where provider='dayflow' so we don't shrink the window after
    # a previous import.
    row = cae.execute(
        "SELECT MIN(start_ts) FROM timeline_cards "
        "WHERE is_deleted=0 AND (provider IS NULL OR provider != ?)",
        (PROVIDER_TAG,),
    ).fetchone()
    return row[0] if row and row[0] is not None else None


def fetch_dayflow_rows(dayflow: sqlite3.Connection, cutoff_ts: int | None) -> list[sqlite3.Row]:
    sql = (
        "SELECT id, start_ts, end_ts, day, title, summary, detailed_summary, "
        "category, subcategory, metadata, created_at "
        "FROM timeline_cards "
        "WHERE is_deleted=0 AND start_ts IS NOT NULL"
    )
    params: list = []
    if cutoff_ts is not None:
        sql += " AND start_ts < ?"
        params.append(cutoff_ts)
    sql += " ORDER BY start_ts ASC"
    return dayflow.execute(sql, params).fetchall()


def existing_keys(cae: sqlite3.Connection) -> set[tuple[int, str]]:
    """(start_ts, title) tuples already in cae.db, used for dedup when not in --replace mode."""
    rows = cae.execute(
        "SELECT start_ts, title FROM timeline_cards WHERE is_deleted=0"
    ).fetchall()
    return {(r["start_ts"], r["title"]) for r in rows}


def insert_rows(
    cae: sqlite3.Connection,
    rows: list[sqlite3.Row],
    *,
    skip_keys: set[tuple[int, str]],
    dry_run: bool,
) -> tuple[int, int]:
    """Insert Dayflow rows into cae.db. Returns (inserted, skipped)."""
    inserted = 0
    skipped = 0
    for r in rows:
        key = (r["start_ts"], r["title"] or "")
        if key in skip_keys:
            skipped += 1
            continue
        if dry_run:
            inserted += 1
            continue
        cae.execute(
            """
            INSERT INTO timeline_cards
              (start_ts, end_ts, day, title, summary, detailed_summary,
               category, subcategory, metadata, confidence, provider, model)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                r["start_ts"],
                r["end_ts"] if r["end_ts"] is not None else r["start_ts"],
                r["day"],
                r["title"] or "(untitled)",
                r["summary"],
                r["detailed_summary"],
                r["category"] or "Unknown",
                r["subcategory"],
                r["metadata"],
                None,  # confidence — Dayflow doesn't expose this
                PROVIDER_TAG,
                None,  # model — Dayflow doesn't tag the LLM in the row
            ),
        )
        inserted += 1
    return inserted, skipped


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true", help="Print what would be imported, write nothing.")
    ap.add_argument("--replace", action="store_true", help="DELETE provider='dayflow' rows from cae.db before importing.")
    ap.add_argument("--cutoff-ts", type=int, help="Override auto-cutoff. Only Dayflow rows with start_ts < this land in cae.db.")
    ap.add_argument("--cutoff-day", type=str, help="Same as --cutoff-ts but YYYY-MM-DD shorthand (uses 00:00 local).")
    args = ap.parse_args()

    dayflow = open_dayflow()
    cae = open_cae()

    cutoff_ts = resolve_cutoff_ts(args, cae)
    if cutoff_ts is None:
        print("[dayflow→cae] cae.db is empty — importing every Dayflow row.")
    else:
        import datetime as dt
        cutoff_iso = dt.datetime.fromtimestamp(cutoff_ts).isoformat()
        print(f"[dayflow→cae] cutoff: start_ts < {cutoff_ts} ({cutoff_iso})")

    rows = fetch_dayflow_rows(dayflow, cutoff_ts)
    print(f"[dayflow→cae] dayflow has {len(rows)} candidate rows")
    if not rows:
        print("[dayflow→cae] nothing to import.")
        return 0

    if args.replace and not args.dry_run:
        deleted = cae.execute(
            "DELETE FROM timeline_cards WHERE provider = ?", (PROVIDER_TAG,)
        ).rowcount
        cae.commit()
        print(f"[dayflow→cae] --replace: deleted {deleted} prior dayflow rows from cae.db")
        skip_keys: set[tuple[int, str]] = set()
    else:
        skip_keys = existing_keys(cae)
        print(f"[dayflow→cae] cae.db already has {len(skip_keys)} (start_ts,title) keys — will skip duplicates")

    try:
        inserted, skipped = insert_rows(cae, rows, skip_keys=skip_keys, dry_run=args.dry_run)
        if not args.dry_run:
            cae.commit()
    except sqlite3.Error as e:
        cae.rollback()
        print(f"[dayflow→cae] FAILED: {e}", file=sys.stderr)
        return 1

    verb = "would insert" if args.dry_run else "inserted"
    print(f"[dayflow→cae] {verb} {inserted}, skipped {skipped} duplicate(s).")

    if not args.dry_run:
        post = cae.execute(
            "SELECT COUNT(*), MIN(day), MAX(day) FROM timeline_cards WHERE provider = ?",
            (PROVIDER_TAG,),
        ).fetchone()
        print(f"[dayflow→cae] cae.db now holds {post[0]} provider='dayflow' rows ({post[1]} → {post[2]})")

    return 0


if __name__ == "__main__":
    sys.exit(main())
