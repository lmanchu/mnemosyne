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

import capture
import storage
import provider_gemini as gemini

# ── Config ────────────────────────────────────────

CAPTURE_INTERVAL = int(os.environ.get("MNEMOSYNE_CAPTURE_INTERVAL", "10"))
BATCH_INTERVAL = int(os.environ.get("MNEMOSYNE_BATCH_INTERVAL", str(15 * 60)))
API_PORT = int(os.environ.get("MNEMOSYNE_PORT", "5700"))
MIN_SCREENSHOTS_PER_BATCH = 3

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
    analyze_enabled = bool(os.environ.get("GEMINI_API_KEY"))

    while running:
        # Capture
        try:
            path = capture.capture_screenshot()
            ts = int(datetime.now().timestamp())
            storage.save_screenshot(
                captured_at=ts,
                file_path=str(path),
                file_size=path.stat().st_size
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


# ── API server thread ─────────────────────────────

def api_loop(port):
    from http.server import HTTPServer
    # Import the handler from api.py
    import api
    server = HTTPServer(("127.0.0.1", port), api.Handler)
    print(f"[{now()}] API: http://127.0.0.1:{port}")
    print(f"[{now()}] Dashboard: http://127.0.0.1:{port}/")
    print(f"[{now()}] Onboarding: http://127.0.0.1:{port}/onboarding")
    print(f"[{now()}] Persona: http://127.0.0.1:{port}/persona")
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
