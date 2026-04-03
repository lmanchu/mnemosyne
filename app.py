"""Mnemosyne — unified entry point for packaged distribution.

Runs daemon (capture + analysis) and API server in one process.
Usage:
  python app.py                    # start everything
  python app.py --no-capture       # API only, no capture
  python app.py --port 5700        # custom port

For packaged exe:
  mnemosyne.exe
  mnemosyne.exe --no-capture
"""

import argparse
import os
import sys
import threading
import time
import signal
from datetime import datetime
from pathlib import Path

# Ensure we can find our modules when packaged
if getattr(sys, 'frozen', False):
    os.chdir(os.path.dirname(sys.executable))
    sys.path.insert(0, os.path.dirname(sys.executable))

import json
import capture
import storage
import provider_gemini as gemini
import aw_bridge
import persona as persona_mod

# ── Config ────────────────────────────────────────

CAPTURE_INTERVAL = int(os.environ.get("MNEMOSYNE_CAPTURE_INTERVAL", "10"))
BATCH_INTERVAL = int(os.environ.get("MNEMOSYNE_BATCH_INTERVAL", str(15 * 60)))
API_PORT = int(os.environ.get("MNEMOSYNE_PORT", "5700"))
MIN_SCREENSHOTS_PER_BATCH = 3
PERSONA_EVOLVE_DAYS = int(os.environ.get("MNEMOSYNE_PERSONA_EVOLVE_DAYS", "3"))
PERSONA_CHECK_INTERVAL = 60 * 60  # check every hour if evolve is due
CLEANUP_INTERVAL = 60 * 60  # check every hour for stale batches + old screenshots
BATCH_TIMEOUT_MINUTES = 30  # pending batches older than this get marked failed
SCREENSHOT_KEEP_DAYS = 3  # delete processed screenshot files after this many days
MAX_BATCH_SIZE = 50  # cap screenshots per batch to avoid API overload

# Markdown export path (Obsidian PKM-Vault)
PKM_VAULT = Path(os.environ.get("MNEMOSYNE_PKM_VAULT", Path.home() / "Dropbox" / "PKM-Vault"))
DAILY_REPORTS_DIR = PKM_VAULT / "2-Areas" / "Context-Engine" / "Daily-Reports"
WEEKLY_REPORTS_DIR = PKM_VAULT / "2-Areas" / "Context-Engine" / "Weekly-Reports"

running = True


def handle_signal(sig, frame):
    global running
    print(f"\n[{now()}] Shutting down...")
    running = False


def now():
    return datetime.now().strftime("%H:%M:%S")


# ── Daemon thread ─────────────────────────────────

def daemon_loop():
    capture_count = 0
    last_batch_time = time.time()
    last_persona_check = time.time()
    last_cleanup_time = time.time()
    analyze_enabled = bool(os.environ.get("GEMINI_API_KEY"))

    # Run cleanup once at startup
    _do_maintenance()

    while running:
        # Check AFK before capturing — skip entirely if user is idle/locked
        try:
            ctx = aw_bridge.get_current_context()
            if ctx.get("afk") and ctx.get("afk_duration", 0) > 60:
                # User has been AFK for >60s, skip capture entirely
                pass
            else:
                # Capture + AW metadata (with smart dedup)
                path = capture.capture_screenshot()
                if path is None:
                    # Smart dedup: screen unchanged, skip
                    pass
                else:
                    ts = int(datetime.now().timestamp())
                    storage.save_screenshot(
                        captured_at=ts,
                        file_path=str(path),
                        file_size=path.stat().st_size,
                        active_app=ctx.get("app", ""),
                        window_title=ctx.get("title", ""),
                        url=ctx.get("url", ""),
                        idle_seconds=ctx.get("afk_duration", 0) if ctx.get("afk") else 0
                    )
                    capture_count += 1
                    if capture_count % 6 == 0:
                        print(f"[{now()}] {capture_count} captures")
        except Exception as e:
            print(f"[{now()}] Capture error: {e}")

        # Analyze on interval
        if analyze_enabled and (time.time() - last_batch_time) >= BATCH_INTERVAL:
            _do_analyze()
            last_batch_time = time.time()

        # Persona auto-evolve + daily/weekly summary check (every hour)
        if analyze_enabled and (time.time() - last_persona_check) >= PERSONA_CHECK_INTERVAL:
            _maybe_generate_daily_summary()
            _maybe_generate_weekly_summary()
            _maybe_evolve_persona()
            last_persona_check = time.time()

        # Maintenance: stale batch recovery + screenshot cleanup (every hour)
        if (time.time() - last_cleanup_time) >= CLEANUP_INTERVAL:
            _do_maintenance()
            last_cleanup_time = time.time()

        # Sleep in small increments
        for _ in range(CAPTURE_INTERVAL * 10):
            if not running:
                break
            time.sleep(0.1)

    # Final analysis
    if analyze_enabled:
        print(f"[{now()}] Final analysis...")
        _do_analyze()


def _do_maintenance():
    """Recover stale batches and clean up old screenshot files."""
    recovered = storage.recover_stale_batches(timeout_minutes=BATCH_TIMEOUT_MINUTES)
    if recovered:
        print(f"[{now()}] Maintenance: recovered {recovered} stale batches")

    deleted, mb_freed = storage.cleanup_processed_screenshots(keep_days=SCREENSHOT_KEEP_DAYS)
    if deleted:
        print(f"[{now()}] Maintenance: deleted {deleted} old screenshots, freed {mb_freed:.1f} MB")


def _do_analyze():
    screenshots = storage.get_unbatched_screenshots()
    if len(screenshots) < MIN_SCREENSHOTS_PER_BATCH:
        return

    # Cap batch size to avoid API overload — process oldest first
    if len(screenshots) > MAX_BATCH_SIZE:
        screenshots = screenshots[:MAX_BATCH_SIZE]

    try:
        ids = [s["id"] for s in screenshots]
        start_ts = min(s["captured_at"] for s in screenshots)
        end_ts = max(s["captured_at"] for s in screenshots)
        start_time = datetime.fromtimestamp(start_ts).isoformat()
        end_time = datetime.fromtimestamp(end_ts).isoformat()

        batch_id = storage.create_batch(ids, start_time, end_time)
        t0 = time.perf_counter()
        transcription, usage1 = gemini.transcribe(screenshots, start_time, end_time)
        card, usage2 = gemini.generate_card(transcription, start_time, end_time)
        total_ms = int((time.perf_counter() - t0) * 1000)

        card_id = storage.save_card(batch_id, card)
        storage.update_batch(
            batch_id, status="completed", provider="gemini", model=gemini.MODEL,
            llm_call_duration_ms=total_ms, transcription=transcription,
            llm_input_tokens=usage1.get("promptTokenCount", 0) + usage2.get("promptTokenCount", 0),
            llm_output_tokens=usage1.get("candidatesTokenCount", 0) + usage2.get("candidatesTokenCount", 0)
        )
        print(f"[{now()}] Card #{card_id}: {card.get('category')} — {card.get('title')} ({total_ms}ms)")
    except Exception as e:
        print(f"[{now()}] Analysis failed: {e}")
        # Mark batch as failed so screenshots get released by maintenance
        try:
            storage.update_batch(batch_id, status="failed", error_message=str(e)[:500])
        except Exception:
            pass


# ── Daily summary generation ─────────────────────

DAILY_SUMMARY_PROMPT = """You are summarizing a person's computer activity for {date}.
They had {card_count} activity sessions. Here are the ActivityCards:

{cards_text}

Write a concise daily summary (3-5 paragraphs) that:
1. Describes the overall narrative of their day (what they accomplished, what they focused on)
2. Notes any context switches or productivity patterns
3. Highlights the most significant work done

Write in second person ("You spent the morning..."). Be specific about apps, projects, and tasks.
Keep it under 300 words. Do NOT use bullet points — write flowing prose."""


def _maybe_generate_daily_summary():
    """Generate summary for yesterday if not already done."""
    from datetime import timedelta
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    # Skip if already generated
    existing = storage.get_daily_summary(yesterday)
    if existing:
        return

    # Get yesterday's cards
    timeline = storage.get_timeline(yesterday)
    cards = timeline["cards"]
    if len(cards) < 2:
        return  # Not enough data

    cards_text = "\n\n".join(
        f"[{c['start_time']} - {c['end_time']}] {c.get('category','?')}: {c.get('title','?')}\n{c.get('summary','')}"
        for c in cards
    )

    prompt = DAILY_SUMMARY_PROMPT.format(
        date=yesterday,
        card_count=len(cards),
        cards_text=cards_text
    )

    try:
        t0 = time.perf_counter()
        text, usage = gemini._call_gemini([{"text": prompt}], temperature=0.3, max_tokens=1024)
        elapsed = (time.perf_counter() - t0) * 1000

        stats = timeline["stats"]
        storage.save_daily_summary(
            date=yesterday,
            summary=text.strip(),
            card_count=len(cards),
            categories=list(stats["categories"].keys()),
            top_apps=stats["top_apps"],
            active_hours=stats["active_hours"],
            provider="gemini",
            model=gemini.MODEL
        )
        print(f"[{now()}] Daily summary for {yesterday}: {len(cards)} cards, {elapsed:.0f}ms")

        # Export to PKM-Vault as markdown
        _export_daily_markdown(yesterday, text.strip(), stats, cards)

    except Exception as e:
        print(f"[{now()}] Daily summary failed: {e}")


def _export_daily_markdown(date: str, summary: str, stats: dict, cards: list):
    """Write daily summary as Obsidian-compatible markdown."""
    DAILY_REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    md_path = DAILY_REPORTS_DIR / f"{date}.md"

    categories = stats.get("categories", {})
    top_apps = stats.get("top_apps", [])[:8]
    active_hours = stats.get("active_hours", 0)

    cat_lines = "\n".join(f"  - {k}: {v}" for k, v in categories.items())
    app_tags = " ".join(f"#{a.replace(' ', '-')}" for a in top_apps[:5])

    # Timeline section
    tl_lines = []
    for c in cards:
        t = (c.get("start_time") or "")[:16].replace("T", " ")
        dur = c.get("duration_minutes", 0)
        tl_lines.append(f"| {t} | {c.get('category', '?')} | {c.get('title', '?')} | {dur}m |")
    tl_table = "\n".join(tl_lines)

    md = f"""---
date: {date}
type: daily-report
source: mnemosyne
cards: {len(cards)}
active_hours: {active_hours}
tags: [mnemosyne, daily-report]
---

# Daily Report — {date}

**{len(cards)} activity sessions** | **{active_hours}h** active

## Summary

{summary}

## Categories
{cat_lines}

## Timeline

| Time | Category | Activity | Duration |
|------|----------|----------|----------|
{tl_table}

## Top Apps
{app_tags}

---
*Generated by Mnemosyne Engine*
"""
    md_path.write_text(md, encoding="utf-8")
    print(f"[{now()}] Exported: {md_path.name}")


# ── Weekly summary generation ────────────────────

WEEKLY_SUMMARY_PROMPT = """You are summarizing a person's computer activity for the week of {week_start} to {week_end}.

Here are their daily summaries:

{dailies_text}

Weekly stats:
- Total cards: {total_cards}
- Total active hours: {total_hours}
- Category breakdown: {categories}

Write a concise weekly review (3-5 paragraphs) that:
1. Describes the overall arc of the week (major projects, shifts in focus)
2. Identifies productivity patterns (which days were most productive, any recurring distractions)
3. Notes what was accomplished vs what seems unfinished

Write in second person. Be specific. Keep it under 400 words. No bullet points."""


def _maybe_generate_weekly_summary():
    """Generate weekly summary on Mondays for the previous week."""
    from datetime import timedelta
    today = datetime.now()
    if today.weekday() != 0:  # Monday = 0
        return

    # Previous week: Monday to Sunday
    week_end = (today - timedelta(days=1)).strftime("%Y-%m-%d")  # yesterday = Sunday
    week_start = (today - timedelta(days=7)).strftime("%Y-%m-%d")  # last Monday

    # Check if already generated
    week_key = f"{week_start}__{week_end}"
    existing = storage.get_daily_summary(week_key)  # reuse daily_summaries table with week key
    if existing:
        return

    # Collect daily summaries for the week
    dailies = []
    total_cards = 0
    total_hours = 0
    all_categories = {}

    for i in range(7):
        d = (today - timedelta(days=7-i)).strftime("%Y-%m-%d")
        ds = storage.get_daily_summary(d)
        if ds and ds.get("summary"):
            dailies.append((d, ds))
            total_cards += ds.get("card_count", 0)
            total_hours += ds.get("active_hours", 0)
            for cat in (ds.get("categories") or []):
                all_categories[cat] = all_categories.get(cat, 0) + 1

    if len(dailies) < 2:
        return  # Not enough data

    dailies_text = "\n\n".join(
        f"### {d}\n{ds['summary']}" for d, ds in dailies
    )
    cat_str = ", ".join(f"{k}({v}d)" for k, v in sorted(all_categories.items(), key=lambda x: -x[1]))

    prompt = WEEKLY_SUMMARY_PROMPT.format(
        week_start=week_start,
        week_end=week_end,
        dailies_text=dailies_text,
        total_cards=total_cards,
        total_hours=round(total_hours, 1),
        categories=cat_str
    )

    try:
        t0 = time.perf_counter()
        text, usage = gemini._call_gemini([{"text": prompt}], temperature=0.3, max_tokens=1500)
        elapsed = (time.perf_counter() - t0) * 1000

        storage.save_daily_summary(
            date=week_key,
            summary=text.strip(),
            card_count=total_cards,
            categories=list(all_categories.keys()),
            top_apps=[],
            active_hours=total_hours,
            provider="gemini",
            model=gemini.MODEL
        )
        print(f"[{now()}] Weekly summary for {week_start}~{week_end}: {len(dailies)} days, {elapsed:.0f}ms")

        # Export to PKM-Vault
        _export_weekly_markdown(week_start, week_end, text.strip(), dailies, total_cards, total_hours, all_categories)

    except Exception as e:
        print(f"[{now()}] Weekly summary failed: {e}")


def _export_weekly_markdown(week_start, week_end, summary, dailies, total_cards, total_hours, categories):
    """Write weekly summary as Obsidian-compatible markdown."""
    WEEKLY_REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    md_path = WEEKLY_REPORTS_DIR / f"{week_start}.md"

    cat_lines = "\n".join(f"  - {k}: {v} days" for k, v in categories.items())
    daily_links = "\n".join(f"- [[{d}]] — {ds.get('card_count', 0)} cards" for d, ds in dailies)

    md = f"""---
week_start: {week_start}
week_end: {week_end}
type: weekly-report
source: mnemosyne
total_cards: {total_cards}
active_hours: {round(total_hours, 1)}
tags: [mnemosyne, weekly-report]
---

# Weekly Report — {week_start} to {week_end}

**{total_cards} activity sessions** | **{round(total_hours, 1)}h** active | **{len(dailies)} days** tracked

## Summary

{summary}

## Daily Breakdown
{daily_links}

## Categories
{cat_lines}

---
*Generated by Mnemosyne Engine*
"""
    md_path.write_text(md, encoding="utf-8")
    print(f"[{now()}] Exported: {md_path.name}")


# ── Persona auto-evolve ──────────────────────────

def _maybe_evolve_persona():
    """Check if persona evolve is due (every PERSONA_EVOLVE_DAYS days)."""
    existing = storage.get_latest_persona()

    if existing and existing.get("created_at"):
        # Parse the created_at timestamp
        try:
            last_ts = datetime.fromisoformat(existing["created_at"])
        except (ValueError, TypeError):
            last_ts = datetime.min
        elapsed_days = (datetime.now() - last_ts).total_seconds() / 86400
        if elapsed_days < PERSONA_EVOLVE_DAYS:
            return  # Not due yet

    # Get cards from the last N days
    cards = storage.get_cards_since(days=PERSONA_EVOLVE_DAYS)
    if len(cards) < 3:
        print(f"[{now()}] Persona evolve: not enough cards ({len(cards)}), skipping")
        return

    print(f"[{now()}] Persona auto-evolve: {len(cards)} cards from last {PERSONA_EVOLVE_DAYS} days")

    try:
        # Build the synthesis prompt using persona module's format
        cards_text = persona_mod.format_cards_for_prompt(cards)

        # Preserve user-edited fields from existing persona
        existing_data = {}
        user_sticky_fields = {}
        if existing:
            existing_data = existing.get("data", {})
            if isinstance(existing_data, str):
                try:
                    existing_data = json.loads(existing_data)
                except (json.JSONDecodeError, TypeError):
                    existing_data = {}
            # Collect user-edited values to restore after synthesis
            if existing_data.get("user_edited"):
                user_sticky_fields = _extract_user_edits(existing_data)

        prev_text = ""
        if existing_data:
            prev_text = f"\nPrevious persona (for continuity — update, don't replace):\n{json.dumps(existing_data, indent=2)}"
        else:
            prev_text = "\nNo previous persona exists. This is the first synthesis."

        today = datetime.now().strftime("%Y-%m-%d")
        prompt = persona_mod.SYNTHESIZE_PROMPT.format(
            card_count=len(cards),
            date=today,
            cards_text=cards_text,
            previous_persona=prev_text
        )

        t0 = time.perf_counter()
        text, usage = gemini._call_gemini([{"text": prompt}], temperature=0.2, max_tokens=4096)
        elapsed = (time.perf_counter() - t0) * 1000

        # Parse JSON response
        clean = text.strip()
        brace_start = clean.find("{")
        brace_end = clean.rfind("}")
        if brace_start == -1 or brace_end == -1:
            print(f"[{now()}] Persona evolve: failed to parse JSON")
            return
        new_persona = json.loads(clean[brace_start:brace_end + 1])

        # Restore user-edited sticky fields (they take priority)
        _apply_user_edits(new_persona, user_sticky_fields)

        new_persona["synthesized_at"] = datetime.now().isoformat()
        new_persona["card_count"] = len(cards)
        new_persona["llm_latency_ms"] = round(elapsed)
        new_persona["auto_evolved"] = True

        # Version
        conn = storage.get_db()
        count = conn.execute("SELECT COUNT(*) FROM persona").fetchone()[0]
        conn.close()
        version = f"0.{count + 1}.0"

        confidence = min(new_persona.get("confidence", 0.5), 0.95)
        pid = storage.save_persona(version, new_persona, confidence)
        print(f"[{now()}] Persona v{version} auto-evolved (confidence={confidence:.0%}, {elapsed:.0f}ms)")

    except Exception as e:
        print(f"[{now()}] Persona evolve failed: {e}")


def _extract_user_edits(data):
    """Extract fields that were manually edited by the user."""
    sticky = {}
    # Identity
    ident = data.get("identity", {})
    if ident.get("role") or ident.get("likely_role"):
        sticky["identity"] = ident
    # Personality (MBTI etc)
    if data.get("personality"):
        sticky["personality"] = data["personality"]
    # User-added interests
    interests = data.get("interests", {})
    if interests.get("current"):
        sticky["interests_current"] = interests["current"]
    # Summary if user wrote one
    if data.get("summary") and data.get("user_edited"):
        sticky["summary"] = data["summary"]
    # Custom notes
    if data.get("custom_notes"):
        sticky["custom_notes"] = data["custom_notes"]
    # Social profiles
    if data.get("social_profiles"):
        sticky["social_profiles"] = data["social_profiles"]
    # Entertainment
    if data.get("entertainment"):
        sticky["entertainment"] = data["entertainment"]
    return sticky


def _apply_user_edits(persona, sticky):
    """Merge user-edited sticky fields back into the new persona."""
    if not sticky:
        return
    if "identity" in sticky:
        persona["identity"] = {**persona.get("identity", {}), **sticky["identity"]}
    if "personality" in sticky:
        persona["personality"] = {**persona.get("personality", {}), **sticky["personality"]}
    if "interests_current" in sticky:
        if "interests" not in persona:
            persona["interests"] = {}
        # Merge: keep AI inferred + user's manual additions
        ai_current = set(persona.get("interests", {}).get("current", []))
        user_current = set(sticky["interests_current"])
        persona["interests"]["current"] = list(ai_current | user_current)
    if "summary" in sticky:
        persona["summary"] = sticky["summary"]
    if "custom_notes" in sticky:
        persona["custom_notes"] = sticky["custom_notes"]
    if "social_profiles" in sticky:
        persona["social_profiles"] = sticky["social_profiles"]
    if "entertainment" in sticky:
        persona["entertainment"] = sticky["entertainment"]
    persona["user_edited"] = True


# ── API server thread ─────────────────────────────

def api_loop(port):
    from http.server import HTTPServer
    # Import the handler from api.py
    import api
    server = HTTPServer(("127.0.0.1", port), api.Handler)
    print(f"[{now()}] API: http://127.0.0.1:{port}")
    print(f"[{now()}] Dashboard: http://127.0.0.1:{port}/")
    print(f"[{now()}] Onboarding: http://127.0.0.1:{port}/onboarding")
    while running:
        server.handle_request()
    server.server_close()


# ── Main ──────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Mnemosyne Context-Aware Engine")
    parser.add_argument("--no-capture", action="store_true", help="API only, no screen capture")
    parser.add_argument("--port", type=int, default=API_PORT, help=f"API port (default: {API_PORT})")
    args = parser.parse_args()

    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)

    conn = storage.get_db()
    total_screenshots = conn.execute("SELECT COUNT(*) FROM screenshots").fetchone()[0]
    total_cards = conn.execute("SELECT COUNT(*) FROM cards").fetchone()[0]
    conn.close()

    print(f"[{now()}] Mnemosyne started")
    print(f"  Capture: {'disabled' if args.no_capture else f'every {CAPTURE_INTERVAL}s'}")
    print(f"  Analyze: {'disabled' if not os.environ.get('GEMINI_API_KEY') else f'every {BATCH_INTERVAL // 60} min'}")
    print(f"  Persona: auto-evolve every {PERSONA_EVOLVE_DAYS} days")
    print(f"  DB: {total_screenshots} screenshots, {total_cards} cards")
    print()

    # Start API thread
    api_thread = threading.Thread(target=api_loop, args=(args.port,), daemon=True)
    api_thread.start()

    if args.no_capture:
        # Just keep alive for API
        while running:
            time.sleep(1)
    else:
        daemon_loop()

    print(f"[{now()}] Stopped.")


if __name__ == "__main__":
    main()
