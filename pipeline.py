"""Phase 2: End-to-end pipeline — capture N screenshots, batch, analyze, produce ActivityCard.

Usage:
  GEMINI_API_KEY=xxx python pipeline.py              # capture 6 screenshots (1 min), then analyze
  GEMINI_API_KEY=xxx python pipeline.py --skip-capture  # analyze existing unbatched screenshots
  GEMINI_API_KEY=xxx python pipeline.py --count 3    # capture 3 screenshots (30s)

This is the full proof: screenshots → DB → batch → VLM transcribe → LLM card → DB → print.
"""

import argparse
import time
from datetime import datetime, timezone

import capture
import provider_gemini as gemini
import storage


def capture_screenshots(count: int, interval: int = 10):
    """Take N screenshots, save to disk + DB."""
    print(f"Capturing {count} screenshots ({count * interval}s)...")
    for i in range(count):
        if i > 0:
            time.sleep(interval)

        path = capture.capture_screenshot()
        ts = int(datetime.now().timestamp())
        size = path.stat().st_size

        sid = storage.save_screenshot(
            captured_at=ts,
            file_path=str(path),
            file_size=size
        )
        print(f"  [{i+1}/{count}] id={sid} {path.name} ({size/1024:.0f}KB)")


def run_pipeline():
    """Batch unbatched screenshots, transcribe, generate card."""
    screenshots = storage.get_unbatched_screenshots()
    if not screenshots:
        print("No unbatched screenshots. Run with --capture or capture.py first.")
        return

    print(f"\nBatching {len(screenshots)} screenshots...")
    ids = [s["id"] for s in screenshots]
    start_ts = min(s["captured_at"] for s in screenshots)
    end_ts = max(s["captured_at"] for s in screenshots)
    start_time = datetime.fromtimestamp(start_ts).isoformat()
    end_time = datetime.fromtimestamp(end_ts).isoformat()

    batch_id = storage.create_batch(ids, start_time, end_time)
    print(f"Batch {batch_id}: {start_time} → {end_time}")

    # Stage 1: Transcribe
    print("\nStage 1: Transcribing screenshots with Gemini...")
    t0 = time.perf_counter()
    try:
        transcription, usage1 = gemini.transcribe(screenshots, start_time, end_time)
    except Exception as e:
        storage.update_batch(batch_id, status="failed", error_message=str(e))
        print(f"FAILED: {e}")
        return

    t1 = time.perf_counter()
    print(f"  Transcription ({(t1-t0)*1000:.0f}ms):")
    print(f"  {transcription[:300]}...")

    # Stage 2: Generate ActivityCard
    print("\nStage 2: Generating ActivityCard...")
    t2 = time.perf_counter()
    try:
        card, usage2 = gemini.generate_card(transcription, start_time, end_time)
    except Exception as e:
        storage.update_batch(batch_id, status="failed", error_message=str(e),
                            transcription=transcription)
        print(f"FAILED: {e}")
        return

    t3 = time.perf_counter()
    total_ms = int((t3 - t0) * 1000)

    # Save to DB
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

    # Print result
    print(f"\n{'='*60}")
    print(f"ActivityCard #{card_id}")
    print(f"{'='*60}")
    print(f"Category:  {card.get('category')}")
    print(f"Title:     {card.get('title')}")
    print(f"Summary:   {card.get('summary')}")
    print(f"Apps:      {card.get('apps_used')}")
    print(f"Confidence:{card.get('confidence')}")
    print(f"Time:      {start_time} → {end_time}")
    print(f"Provider:  {card.get('provider')} / {card.get('model')}")
    print(f"Latency:   {total_ms}ms (transcribe {(t1-t0)*1000:.0f}ms + card {(t3-t2)*1000:.0f}ms)")
    print(f"{'='*60}")
    print(f"\nDetailed summary:")
    print(f"  {card.get('detailed_summary')}")

    # Show DB stats
    print()
    storage.get_db()  # trigger schema
    import sqlite3
    conn = storage.get_db()
    for table in ("screenshots", "batches", "cards"):
        count = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        print(f"  DB {table}: {count} rows")
    conn.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Mnemosyne pipeline: capture → analyze → card")
    parser.add_argument("--skip-capture", action="store_true", help="Skip capture, use existing screenshots")
    parser.add_argument("--count", type=int, default=6, help="Number of screenshots to capture (default: 6)")
    parser.add_argument("--interval", type=int, default=10, help="Seconds between captures (default: 10)")
    args = parser.parse_args()

    if not args.skip_capture:
        capture_screenshots(args.count, args.interval)

    run_pipeline()
