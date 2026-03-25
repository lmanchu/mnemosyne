"""Mnemosyne daemon — continuous capture + periodic analysis.

Run: GEMINI_API_KEY=xxx python daemon.py
Ctrl+C to stop.

Captures a screenshot every CAPTURE_INTERVAL seconds.
Every BATCH_INTERVAL seconds, batches unbatched screenshots and runs the AI pipeline.
"""

import os
import signal
import sys
import time
from datetime import datetime
from pathlib import Path

import capture
import provider_gemini as gemini
import storage
import aw_bridge

CAPTURE_INTERVAL = int(os.environ.get("MNEMOSYNE_CAPTURE_INTERVAL", "10"))
BATCH_INTERVAL = int(os.environ.get("MNEMOSYNE_BATCH_INTERVAL", str(15 * 60)))  # 15 min
MIN_SCREENSHOTS_PER_BATCH = 3
STORAGE_QUOTA_GB = float(os.environ.get("MNEMOSYNE_STORAGE_QUOTA_GB", "10"))
CLEANUP_INTERVAL = 60 * 60  # check every hour

running = True


def handle_signal(sig, frame):
    global running
    print(f"\n[{now()}] Shutting down...")
    running = False


def now():
    return datetime.now().strftime("%H:%M:%S")


def do_capture():
    try:
        path = capture.capture_screenshot()
        ts = int(datetime.now().timestamp())
        ctx = aw_bridge.get_current_context()
        storage.save_screenshot(
            captured_at=ts,
            file_path=str(path),
            file_size=path.stat().st_size,
            active_app=ctx.get("app", ""),
            window_title=ctx.get("title", ""),
            url=ctx.get("url", ""),
            idle_seconds=ctx.get("afk_duration", 0) if ctx.get("afk") else 0
        )
        return True
    except Exception as e:
        print(f"[{now()}] Capture error: {e}")
        return False


def do_analyze():
    screenshots = storage.get_unbatched_screenshots()
    if len(screenshots) < MIN_SCREENSHOTS_PER_BATCH:
        return

    print(f"[{now()}] Analyzing batch of {len(screenshots)} screenshots...")

    ids = [s["id"] for s in screenshots]
    start_ts = min(s["captured_at"] for s in screenshots)
    end_ts = max(s["captured_at"] for s in screenshots)
    start_time = datetime.fromtimestamp(start_ts).isoformat()
    end_time = datetime.fromtimestamp(end_ts).isoformat()

    batch_id = storage.create_batch(ids, start_time, end_time)

    try:
        t0 = time.perf_counter()
        transcription, usage1 = gemini.transcribe(screenshots, start_time, end_time)
        card, usage2 = gemini.generate_card(transcription, start_time, end_time)
        total_ms = int((time.perf_counter() - t0) * 1000)

        card_id = storage.save_card(batch_id, card)
        storage.update_batch(
            batch_id,
            status="completed",
            provider="gemini",
            model=gemini.MODEL,
            llm_call_duration_ms=total_ms,
            transcription=transcription,
            llm_input_tokens=usage1.get("promptTokenCount", 0) + usage2.get("promptTokenCount", 0),
            llm_output_tokens=usage1.get("candidatesTokenCount", 0) + usage2.get("candidatesTokenCount", 0)
        )

        print(f"[{now()}] Card #{card_id}: {card.get('category')} — {card.get('title')} ({total_ms}ms)")

    except Exception as e:
        storage.update_batch(batch_id, status="failed", error_message=str(e))
        print(f"[{now()}] Analysis failed: {e}")


def main():
    if not os.environ.get("GEMINI_API_KEY"):
        print("Set GEMINI_API_KEY to enable analysis.")
        print("Without it, daemon will only capture screenshots.")
        analyze_enabled = False
    else:
        analyze_enabled = True

    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)

    # Stats
    capture_count = 0
    last_batch_time = time.time()
    last_persona_time = time.time()
    last_cleanup_time = time.time()
    PERSONA_INTERVAL = 2 * 60 * 60  # every 2 hours

    conn = storage.get_db()
    total_cards = conn.execute("SELECT COUNT(*) FROM cards").fetchone()[0]
    total_screenshots = conn.execute("SELECT COUNT(*) FROM screenshots").fetchone()[0]
    conn.close()

    print(f"[{now()}] Mnemosyne daemon started")
    print(f"  Capture: every {CAPTURE_INTERVAL}s")
    print(f"  Analyze: every {BATCH_INTERVAL}s ({BATCH_INTERVAL // 60} min)")
    print(f"  DB: {total_screenshots} screenshots, {total_cards} cards")
    print(f"  Provider: {'gemini' if analyze_enabled else 'none (capture only)'}")
    print(f"  Dashboard: python api.py → http://localhost:5700")
    print()

    while running:
        # Capture
        if do_capture():
            capture_count += 1
            if capture_count % 6 == 0:  # Log every minute
                print(f"[{now()}] {capture_count} captures this session")

        # Analyze on interval
        if analyze_enabled and (time.time() - last_batch_time) >= BATCH_INTERVAL:
            do_analyze()
            last_batch_time = time.time()

        # Persona synthesis on interval
        if analyze_enabled and (time.time() - last_persona_time) >= PERSONA_INTERVAL:
            do_persona_synthesis()
            last_persona_time = time.time()

        # Storage cleanup on interval
        if (time.time() - last_cleanup_time) >= CLEANUP_INTERVAL:
            do_storage_cleanup()
            last_cleanup_time = time.time()

        # Sleep (in small increments so Ctrl+C is responsive)
        for _ in range(CAPTURE_INTERVAL * 10):
            if not running:
                break
            time.sleep(0.1)

    # Final analysis of remaining screenshots
    if analyze_enabled:
        print(f"[{now()}] Running final analysis...")
        do_analyze()
        # Synthesize daily persona
        do_persona_synthesis()

    print(f"[{now()}] Done. {capture_count} captures this session.")


def do_storage_cleanup():
    """Delete oldest screenshots when storage exceeds quota. Keeps DB records (marks as deleted)."""
    captures_dir = Path.home() / ".mnemosyne" / "captures"
    if not captures_dir.exists():
        return

    # Calculate current size
    total_bytes = sum(f.stat().st_size for f in captures_dir.rglob("*.jpg") if f.is_file())
    total_gb = total_bytes / (1024 ** 3)
    quota = STORAGE_QUOTA_GB

    if total_gb <= quota:
        return

    excess_gb = total_gb - quota
    print(f"[{now()}] Storage cleanup: {total_gb:.1f} GB > {quota:.0f} GB quota, removing {excess_gb:.1f} GB")

    # Get all jpg files sorted by age (oldest first)
    files = sorted(captures_dir.rglob("*.jpg"), key=lambda f: f.stat().st_mtime)

    freed = 0
    deleted_count = 0
    target_bytes = excess_gb * (1024 ** 3)

    conn = storage.get_db()
    for f in files:
        if freed >= target_bytes:
            break
        size = f.stat().st_size
        path_str = str(f)

        # Mark as deleted in DB
        conn.execute("UPDATE screenshots SET is_deleted = 1 WHERE file_path = ?", (path_str,))

        # Delete file
        try:
            f.unlink()
            freed += size
            deleted_count += 1
        except OSError:
            pass

    conn.commit()
    conn.close()

    # Remove empty date directories
    for d in captures_dir.iterdir():
        if d.is_dir() and not any(d.iterdir()):
            d.rmdir()

    print(f"[{now()}] Cleaned {deleted_count} files, freed {freed / (1024**3):.1f} GB")


def do_persona_synthesis():
    """Synthesize daily persona from today's cards."""
    try:
        import persona as persona_mod
        today = datetime.now().strftime("%Y-%m-%d")
        cards = storage.get_cards(date=today, limit=200)
        if len(cards) >= 2:
            print(f"[{now()}] Synthesizing persona from {len(cards)} cards...")
            result = persona_mod.synthesize_daily(today)
            if result:
                print(f"[{now()}] Persona updated: {result.get('summary', '')[:80]}")
        else:
            print(f"[{now()}] Not enough cards for persona synthesis ({len(cards)})")
    except Exception as e:
        print(f"[{now()}] Persona synthesis failed: {e}")


if __name__ == "__main__":
    main()
