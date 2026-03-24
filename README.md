# Mnemosyne

> Context-Aware Engine for AIPC — understands what you're doing, not just which app is open.

Mnemosyne watches your screen, analyzes it with AI, and produces structured context that IrisGo uses to personalize everything. Local-first. Multi-provider. ~1500 lines of Python.

## How It Works

```
Every 10 seconds          Every 15 minutes              Always available
┌──────────────┐          ┌────────────────────┐        ┌──────────────┐
│  Screenshot  │──batch──▶│  VLM: what is the  │──────▶│  REST API    │
│  + metadata  │          │  user doing?       │        │  localhost:   │
│  (mss + AW)  │          │  → ActivityCard    │        │  5700        │
└──────────────┘          └────────────────────┘        └──────────────┘
```

**Input**: Screenshots (JPEG, 1080p) + ActivityWatch metadata (app, window title, URL, AFK)

**Output**: ActivityCards — structured JSON with category, title, summary, apps used, confidence score

**Consumers**: IrisGo desktop app, mnemosyne.irisgo.xyz dashboard

## Quick Start

```bash
# Clone
git clone https://github.com/lmanchu/mnemosyne.git
cd mnemosyne

# Setup
python -m venv .venv
source .venv/Scripts/activate   # Windows
# source .venv/bin/activate     # macOS/Linux
pip install mss Pillow mcp

# Phase 0: Take a screenshot
python capture.py

# Phase 1: Test VLM understanding
GEMINI_API_KEY=your_key python test_vlm.py

# Phase 2: Full pipeline (capture 3 screenshots → analyze → produce ActivityCard)
GEMINI_API_KEY=your_key python pipeline.py --count 3

# Dashboard (open http://localhost:5700)
python api.py
```

## What's Built (as of 2026-03-24)

| File | Lines | What it does | Status |
|------|------:|-------------|--------|
| `capture.py` | 50 | Screenshot → 1080p JPEG (250ms, ~350KB) | Validated on Windows 11 AIPC |
| `test_vlm.py` | 80 | Single screenshot → Gemini Flash → activity description | Confidence 1.0 |
| `storage.py` | 210 | SQLite: 5 tables (screenshots, batches, cards, onboarding, persona) | Working |
| `provider_gemini.py` | 150 | Gemini 2.5 Flash: transcribe + generate card (2 API calls) | Working |
| `pipeline.py` | 100 | End-to-end: capture → batch → analyze → store | Produces real ActivityCards |
| `daemon.py` | 150 | Background daemon: continuous capture + periodic analysis | Running (1800+ screenshots) |
| `mcp_server.py` | 200 | MCP server: 5 tools + 1 resource + background capture | Working |
| `persona.py` | 400 | Persona evolution: daily synthesis + markdown export/import | Working |
| `api.py` | 430 | REST API + onboarding + persona + engine stats (localhost:5700) | Working |
| `dashboard.html` | 220 | Engine Console: pipeline status, metrics, batch history (cyan) | Working |
| `onboarding.html` | 380 | 4-step onboarding: interview + social profiles + interests | Working |
| `persona-editor.html` | 180 | Markdown persona editor with Edit/Preview + Ctrl+S | Working |
| `INTERFACE.md` | 400 | Interface spec + Philosophy (Memory vs Context Engine) | Spec complete |
| `ONBOARDING.md` | 220 | Persona building spec: ground zero in 5 minutes | Spec complete |

### Example ActivityCard (real output)

```json
{
  "category": "Development",
  "title": "Monitoring AI Python Script in WSL PowerShell",
  "summary": "The user monitored an AI-driven Python script in a WSL environment via PowerShell, which was actively capturing and processing screenshots using the Gemini API.",
  "apps_used": ["Windows PowerShell", "WSL", "Python", "bash"],
  "confidence": 1.0,
  "provider": "gemini",
  "model": "gemini-2.5-flash"
}
```

## Architecture

```
mnemosyne/
├── capture.py           # Screen capture (mss library, 250ms/shot)
├── storage.py           # SQLite: 5 tables + CRUD
├── provider_gemini.py   # Gemini Vision: transcribe + generate card
├── pipeline.py          # Orchestrator: capture → batch → analyze → store
├── daemon.py            # Background daemon: continuous capture + analysis
├── mcp_server.py        # MCP server: 5 tools for IrisGo integration
├── persona.py           # Persona evolution: synthesize + markdown I/O
├── api.py               # REST API + onboarding + persona (localhost:5700)
├── dashboard.html       # Engine Console (cyan accent, system diagnostics)
├── onboarding.html      # 4-step onboarding (interview + social + interests)
├── persona-editor.html  # Markdown persona editor (Edit/Preview)
├── test_vlm.py          # VLM validation script
├── start.bat / stop.bat # Windows auto-start on login
├── INTERFACE.md         # Interface spec + Philosophy (Memory vs Context)
├── ONBOARDING.md        # Persona building spec
└── docs/                # Design documents (v1.x, historical)
```

## Providers

| Provider | Status | Vision | Cost/batch | Privacy |
|----------|--------|--------|-----------|---------|
| Gemini 2.5 Flash | Working | Native | ~$0.002 | Cloud (Google) |
| Claude Sonnet | Planned | Image batches | ~$0.01 | Cloud (Anthropic) |
| OpenAI GPT-4o | Planned | Image batches | ~$0.01 | Cloud (OpenAI) |
| Ollama (local) | Planned | Per-frame | $0 | Fully local |

## Roadmap

- [x] Phase 0: Screen capture on Windows AIPC
- [x] Phase 1: VLM validation (Gemini understands screenshots)
- [x] Phase 2: Full pipeline (capture → batch → ActivityCard → SQLite)
- [ ] Phase 3: Multi-provider (Claude, OpenAI, Ollama)
- [x] Phase 4: MCP server (5 tools + IrisGo skill)
- [x] Phase 5: Engine Console + REST API (`localhost:5700`)
- [x] Phase 5b: Onboarding flow (4-step, wired to real API)
- [x] Phase 5c: 3-Part UI overhaul (onboarding real data, engine console, new endpoints)
- [x] Phase 8: Persona evolution (daily synthesis from ActivityCards)
- [x] Persona editor: Editable markdown at `/persona` (user edits override AI)
- [x] Social profiles + interests in onboarding (LinkedIn, Twitter, IG, GitHub, books, anime, etc.)
- [x] Daemon: Background capture + periodic analysis (2000+ screenshots accumulated)
- [x] Windows auto-start: `start.bat` in Startup folder
- [ ] Phase 3: Multi-provider (Claude, OpenAI, Ollama)
- [ ] Phase 6: IrisGo app integration
- [ ] Phase 7: ActivityWatch bridge for metadata enrichment

## API

Running on `http://localhost:5700`:

```
GET /                       # Dashboard UI
GET /api/v1/context/now      # Current activity + system prompt fragment
GET /api/v1/cards            # ActivityCards by date/category
GET /api/v1/profile          # Aggregated context profile
GET /api/v1/summary          # Day summary
GET /api/v1/health           # System status
GET /api/v1/engine/stats     # Comprehensive engine metrics
GET /api/v1/persona?format=  # Current persona (json or markdown)
POST /api/v1/persona         # Save edited persona markdown
POST /api/v1/onboarding/*    # Interview, preferences, seed, persona generation
```

## MCP Integration

Mnemosyne runs as an MCP server for direct integration with IrisGo and Claude Code:

```json
{
  "mcpServers": {
    "mnemosyne": {
      "command": "python",
      "args": ["mcp_server.py"],
      "env": { "GEMINI_API_KEY": "your-key" }
    }
  }
}
```

Tools: `mnemosyne_context_now`, `mnemosyne_get_cards`, `mnemosyne_get_profile`, `mnemosyne_get_summary`, `mnemosyne_health`

See [INTERFACE.md](./INTERFACE.md) for full specification.

## Requirements

- Python 3.11+
- `mss` (screen capture)
- `Pillow` (image processing)
- `mcp` (MCP server SDK)
- Gemini API key (or other provider)
- Optional: [ActivityWatch](https://activitywatch.net/) for metadata enrichment

## Privacy

- All data stays local by default
- Screenshots stored in `~/.mnemosyne/captures/`
- SQLite DB at `~/.mnemosyne/context.db`
- API binds to `127.0.0.1` only
- User controls which provider processes their data

## Reference

Inspired by [Dayflow](https://github.com/JerryZLiu/Dayflow)'s screen recording + AI analysis architecture, adapted for Windows AIPC with multi-provider support.

## License

MIT

---

*Part of the [IrisGo.AI](https://irisgo.ai) ecosystem — The AI That Knows You*
