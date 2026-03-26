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
    analyze_enabled = bool(os.environ.get("GEMINI_API_KEY"))

    while running:
        # Capture + AW metadata
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
            capture_count += 1
            if capture_count % 6 == 0:
                print(f"[{now()}] {capture_count} captures")
        except Exception as e:
            print(f"[{now()}] Capture error: {e}")

        # Analyze on interval
        if analyze_enabled and (time.time() - last_batch_time) >= BATCH_INTERVAL:
            _do_analyze()
            last_batch_time = time.time()

        # Persona auto-evolve check (every hour)
        if analyze_enabled and (time.time() - last_persona_check) >= PERSONA_CHECK_INTERVAL:
            _maybe_evolve_persona()
            last_persona_check = time.time()

        # Sleep in small increments
        for _ in range(CAPTURE_INTERVAL * 10):
            if not running:
                break
            time.sleep(0.1)

    # Final analysis
    if analyze_enabled:
        print(f"[{now()}] Final analysis...")
        _do_analyze()


def _do_analyze():
    screenshots = storage.get_unbatched_screenshots()
    if len(screenshots) < MIN_SCREENSHOTS_PER_BATCH:
        return
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
