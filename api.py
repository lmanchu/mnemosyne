"""Mnemosyne REST API + Dashboard server.

Serves:
  - GET /api/v1/context/now
  - GET /api/v1/cards?date=&category=&limit=
  - GET /api/v1/profile?date=
  - GET /api/v1/summary?date=
  - GET /api/v1/health
  - POST /api/v1/onboarding/seed   (60s behavioral seed capture)
  - POST /api/v1/onboarding/persona (generate ground zero persona)
  - GET / → dashboard HTML
  - GET /onboarding → onboarding HTML

Run: python api.py
Opens: http://localhost:5700
"""

import json
import os
import threading
import time
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse, parse_qs

import storage

HOST = "127.0.0.1"
PORT = int(os.environ.get("MNEMOSYNE_PORT", "5700"))
DASHBOARD_PATH = Path(__file__).parent / "dashboard.html"
ONBOARDING_PATH = Path(__file__).parent / "onboarding.html"
PERSONA_EDITOR_PATH = Path(__file__).parent / "persona-editor.html"


def _json_response(handler, data, status=200):
    body = json.dumps(data, indent=2, default=str).encode()
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json")
    handler.send_header("Access-Control-Allow-Origin", "*")
    handler.send_header("Content-Length", len(body))
    handler.end_headers()
    handler.wfile.write(body)


def _build_system_prompt_fragment(cards):
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
        try: apps = json.loads(apps)
        except: apps = []
    if apps:
        lines.append(f"- Apps: {', '.join(apps)}")
    lines.append("\nAdapt your responses to their current context.")
    return "\n".join(lines)


def _build_profile(cards, date):
    if not cards:
        return {"date": date, "status": "no_data"}
    cat_minutes = {}
    for c in cards:
        cat = c.get("category", "Other")
        try:
            s = datetime.fromisoformat(c["start_time"])
            e = datetime.fromisoformat(c["end_time"])
            m = (e - s).total_seconds() / 60
        except: m = 15
        cat_minutes[cat] = cat_minutes.get(cat, 0) + m
    total = sum(cat_minutes.values()) or 1
    all_apps = set()
    for c in cards:
        apps = c.get("apps_used", [])
        if isinstance(apps, str):
            try: apps = json.loads(apps)
            except: apps = []
        all_apps.update(apps)
    return {
        "date": date,
        "card_count": len(cards),
        "total_minutes": round(total),
        "categories": [
            {"name": k, "minutes": round(v), "pct": round(v / total * 100)}
            for k, v in sorted(cat_minutes.items(), key=lambda x: -x[1])
        ],
        "apps_used": sorted(all_apps),
    }


class Handler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # silence request logs

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length) if content_length else b'{}'
        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            data = {}

        if path == "/api/v1/onboarding/seed":
            self._api_onboarding_seed(data)
        elif path == "/api/v1/onboarding/persona":
            self._api_onboarding_persona(data)
        elif path == "/api/v1/onboarding/interview":
            self._api_onboarding_interview(data)
        elif path == "/api/v1/onboarding/preferences":
            self._api_onboarding_preferences(data)
        elif path == "/api/v1/persona":
            self._api_save_persona(data)
        else:
            self.send_error(404)

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        params = {k: v[0] for k, v in parse_qs(parsed.query).items()}

        if path == "/" or path == "/dashboard":
            self._serve_dashboard()
        elif path == "/onboarding":
            self._serve_file(ONBOARDING_PATH, "text/html")
        elif path == "/api/v1/context/now":
            self._api_context_now()
        elif path == "/api/v1/cards":
            self._api_cards(params)
        elif path == "/api/v1/profile":
            self._api_profile(params)
        elif path == "/api/v1/summary":
            self._api_summary(params)
        elif path == "/api/v1/health":
            self._api_health()
        elif path == "/api/v1/onboarding/seed/status":
            self._api_seed_status()
        elif path == "/api/v1/engine/stats":
            self._api_engine_stats()
        elif path == "/api/v1/persona":
            self._api_get_persona(params)
        elif path == "/persona":
            self._serve_file(PERSONA_EDITOR_PATH, "text/html")
        else:
            self.send_error(404)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def _serve_file(self, filepath, content_type):
        if not filepath.exists():
            self.send_error(404, f"{filepath.name} not found")
            return
        body = filepath.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", f"{content_type}; charset=utf-8")
        self.send_header("Content-Length", len(body))
        self.end_headers()
        self.wfile.write(body)

    def _serve_dashboard(self):
        self._serve_file(DASHBOARD_PATH, "text/html")

    def _api_context_now(self):
        cards = storage.get_cards(limit=5)
        _json_response(self, {
            "current": cards[0] if cards else None,
            "recent_cards_count": len(cards),
            "system_prompt_fragment": _build_system_prompt_fragment(cards),
        })

    def _api_cards(self, params):
        date = params.get("date")
        category = params.get("category")
        limit = int(params.get("limit", "50"))
        cards = storage.get_cards(date=date, limit=limit)
        if category:
            cards = [c for c in cards if c.get("category", "").lower() == category.lower()]
        _json_response(self, cards)

    def _api_profile(self, params):
        date = params.get("date", datetime.now().strftime("%Y-%m-%d"))
        cards = storage.get_cards(date=date, limit=200)
        _json_response(self, _build_profile(cards, date))

    def _api_summary(self, params):
        date = params.get("date", datetime.now().strftime("%Y-%m-%d"))
        cards = storage.get_cards(date=date, limit=200)
        if not cards:
            _json_response(self, {"date": date, "summary": "No data."})
            return
        cats = {}
        for c in cards:
            cat = c.get("category", "Other")
            cats[cat] = cats.get(cat, 0) + 1
        cat_str = ", ".join(f"{v} blocks of {k}" for k, v in sorted(cats.items(), key=lambda x: -x[1]))
        _json_response(self, {
            "date": date,
            "card_count": len(cards),
            "summary": f"Tracked {len(cards)} activity blocks: {cat_str}.",
            "highlights": [c.get("title", "") for c in cards[:5]],
            "categories": cats,
        })

    def _api_onboarding_seed(self, data):
        """Capture N screenshots as behavioral seed for onboarding."""
        count = data.get("count", 6)
        interval = data.get("interval", 10)

        def _capture_in_bg():
            import capture
            results = []
            for i in range(count):
                if i > 0:
                    time.sleep(interval)
                try:
                    path = capture.capture_screenshot()
                    ts = int(datetime.now().timestamp())
                    sid = storage.save_screenshot(
                        captured_at=ts,
                        file_path=str(path),
                        file_size=path.stat().st_size
                    )
                    results.append({"id": sid, "file": path.name})
                except Exception as e:
                    results.append({"error": str(e)})

        # Run capture in background thread
        thread = threading.Thread(target=_capture_in_bg, daemon=True)
        thread.start()

        _json_response(self, {
            "status": "capturing",
            "count": count,
            "interval": interval,
            "message": f"Capturing {count} screenshots over {count * interval}s"
        })

    def _api_onboarding_persona(self, data):
        """Generate ground zero persona from available data."""
        # Gather all cards
        cards = storage.get_cards(limit=200)

        # User-provided data from onboarding form
        interview = data.get("interview", {})
        mbti = data.get("mbti", "")
        interests = data.get("interests", [])
        sources = data.get("sources", [])

        # Build persona from cards + user input
        profile = _build_profile(cards, datetime.now().strftime("%Y-%m-%d"))

        persona = {
            "version": "0.1.0",
            "created_at": datetime.now().isoformat(),
            "confidence": min(0.3 + len(cards) * 0.05 + (0.1 if interview else 0) + (0.05 if mbti else 0) + len(interests) * 0.02, 0.95),
            "days_observed": len(set(c.get("start_time", "")[:10] for c in cards)),
            "identity": {
                "role": interview.get("role", ""),
                "source": "interview"
            },
            "work_style": {
                "top_categories": profile.get("categories", []),
                "apps_primary": profile.get("apps_used", [])[:5],
                "source": "context_engine + interview"
            },
            "personality": {
                "mbti": mbti,
                "source": "user_input"
            },
            "interests": {
                "current": interests,
                "from_context": [c.get("subcategory", "") for c in cards[:5] if c.get("subcategory")],
                "source": "user_input + context_engine"
            },
            "corrections": [],
            "context_cards_count": len(cards),
            "sources_connected": sources
        }

        # Persist persona
        storage.save_persona(persona.get("version", "0.1.0"), persona, persona.get("confidence", 0))
        _json_response(self, persona)

    def _api_onboarding_interview(self, data):
        answers = data.get("answers", {})
        storage.save_onboarding_step("interview", answers)
        _json_response(self, {"status": "saved", "step": "interview"})

    def _api_onboarding_preferences(self, data):
        storage.save_onboarding_step("preferences", data)
        _json_response(self, {"status": "saved", "step": "preferences"})

    def _api_seed_status(self):
        conn = storage.get_db()
        now_ts = int(datetime.now().timestamp())
        recent = conn.execute(
            "SELECT COUNT(*) FROM screenshots WHERE captured_at > ?", (now_ts - 70,)
        ).fetchone()[0]
        total = conn.execute("SELECT COUNT(*) FROM screenshots").fetchone()[0]
        conn.close()
        target = 6
        _json_response(self, {
            "total_screenshots": total,
            "recent_70s": recent,
            "seed_target": target,
            "complete": recent >= target,
            "progress_pct": min(100, int(recent / target * 100))
        })

    def _api_engine_stats(self):
        conn = storage.get_db()
        s_total = conn.execute("SELECT COUNT(*) FROM screenshots").fetchone()[0]
        s_unbatched = conn.execute("SELECT COUNT(*) FROM screenshots WHERE batch_id IS NULL").fetchone()[0]
        latest_capture = conn.execute("SELECT captured_at FROM screenshots ORDER BY captured_at DESC LIMIT 1").fetchone()
        b_total = conn.execute("SELECT COUNT(*) FROM batches").fetchone()[0]
        b_completed = conn.execute("SELECT COUNT(*) FROM batches WHERE status='completed'").fetchone()[0]
        b_failed = conn.execute("SELECT COUNT(*) FROM batches WHERE status='failed'").fetchone()[0]
        avg_lat = conn.execute("SELECT AVG(llm_call_duration_ms) FROM batches WHERE status='completed'").fetchone()[0]
        total_in_tok = conn.execute("SELECT SUM(llm_input_tokens) FROM batches WHERE status='completed'").fetchone()[0]
        total_out_tok = conn.execute("SELECT SUM(llm_output_tokens) FROM batches WHERE status='completed'").fetchone()[0]
        last_batch = conn.execute("SELECT * FROM batches ORDER BY id DESC LIMIT 1").fetchone()
        c_total = conn.execute("SELECT COUNT(*) FROM cards").fetchone()[0]
        conn.close()

        captures_dir = Path.home() / ".mnemosyne" / "captures"
        cap_size = sum(f.stat().st_size for f in captures_dir.rglob("*.jpg")) if captures_dir.exists() else 0
        cap_interval = int(os.environ.get("MNEMOSYNE_CAPTURE_INTERVAL", "10"))
        batch_interval = int(os.environ.get("MNEMOSYNE_BATCH_INTERVAL", "900"))

        last_cap_ts = latest_capture[0] if latest_capture else 0
        daemon_active = (int(datetime.now().timestamp()) - last_cap_ts) < cap_interval * 3

        _json_response(self, {
            "screenshots": {"total": s_total, "unbatched": s_unbatched},
            "batches": {
                "total": b_total, "completed": b_completed, "failed": b_failed,
                "avg_latency_ms": round(avg_lat) if avg_lat else 0,
                "total_input_tokens": total_in_tok or 0,
                "total_output_tokens": total_out_tok or 0,
                "last": {
                    "id": dict(last_batch)["id"] if last_batch else None,
                    "status": dict(last_batch)["status"] if last_batch else None,
                    "time": dict(last_batch)["created_at"] if last_batch else None,
                } if last_batch else None
            },
            "cards": {"total": c_total},
            "storage": {"captures_size_mb": round(cap_size / 1024 / 1024, 1)},
            "daemon": {
                "active": daemon_active,
                "capture_interval": cap_interval,
                "batch_interval": batch_interval,
                "last_capture": datetime.fromtimestamp(last_cap_ts).isoformat() if last_cap_ts else None,
            }
        })

    def _api_get_persona(self, params):
        fmt = params.get("format", "json")
        import persona as persona_mod
        p = storage.get_latest_persona()
        if fmt == "markdown":
            md = persona_mod.to_markdown(p)
            _json_response(self, {"markdown": md, "version": p.get("version") if p else None})
        else:
            _json_response(self, p.get("data", {}) if p else {"status": "no_persona"})

    def _api_save_persona(self, data):
        import persona as persona_mod
        md = data.get("markdown", "")
        existing = storage.get_latest_persona()
        existing_data = existing.get("data", {}) if existing else {}
        if isinstance(existing_data, str):
            try: existing_data = json.loads(existing_data)
            except: existing_data = {}

        updated = persona_mod.from_markdown(md, existing_data)

        conn = storage.get_db()
        count = conn.execute("SELECT COUNT(*) FROM persona").fetchone()[0]
        conn.close()
        version = f"0.{count + 1}.0"

        confidence = min((existing.get("confidence", 0.5) if existing else 0.5) + 0.1, 0.99)
        pid = storage.save_persona(version, updated, confidence)
        _json_response(self, {"status": "saved", "version": version, "id": pid})

    def _api_health(self):
        conn = storage.get_db()
        stats = {t: conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
                 for t in ("screenshots", "batches", "cards")}
        latest = conn.execute(
            "SELECT captured_at FROM screenshots ORDER BY captured_at DESC LIMIT 1"
        ).fetchone()
        conn.close()
        captures_dir = Path.home() / ".mnemosyne" / "captures"
        cap_size = sum(f.stat().st_size for f in captures_dir.rglob("*.jpg")) if captures_dir.exists() else 0
        _json_response(self, {
            "status": "running",
            "db_rows": stats,
            "captures_size_mb": round(cap_size / 1024 / 1024, 1),
            "last_capture": datetime.fromtimestamp(latest[0]).isoformat() if latest else None,
        })


if __name__ == "__main__":
    server = HTTPServer((HOST, PORT), Handler)
    print(f"Mnemosyne dashboard: http://{HOST}:{PORT}")
    print(f"API: http://{HOST}:{PORT}/api/v1/")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down.")
        server.server_close()
