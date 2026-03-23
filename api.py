"""Mnemosyne REST API + Dashboard server.

Serves:
  - GET /api/v1/context/now
  - GET /api/v1/cards?date=&category=&limit=
  - GET /api/v1/profile?date=
  - GET /api/v1/summary?date=
  - GET /api/v1/health
  - GET / → dashboard HTML

Run: python api.py
Opens: http://localhost:5700
"""

import json
import os
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse, parse_qs

import storage

HOST = "127.0.0.1"
PORT = int(os.environ.get("MNEMOSYNE_PORT", "5700"))
DASHBOARD_PATH = Path(__file__).parent / "dashboard.html"


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

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        params = {k: v[0] for k, v in parse_qs(parsed.query).items()}

        if path == "/" or path == "/dashboard":
            self._serve_dashboard()
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
        else:
            self.send_error(404)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.end_headers()

    def _serve_dashboard(self):
        if not DASHBOARD_PATH.exists():
            self.send_error(404, "dashboard.html not found")
            return
        body = DASHBOARD_PATH.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", len(body))
        self.end_headers()
        self.wfile.write(body)

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
