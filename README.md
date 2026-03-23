# Mnemosyne

> Context-Aware Engine for AIPC — understands what you're doing, not just which app is open.

Mnemosyne watches your screen, analyzes it with AI, and produces structured context that IrisGo uses to personalize everything. Local-first. Multi-provider. ~900 lines of Python.

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
pip install mss Pillow

# Phase 0: Take a screenshot
python capture.py

# Phase 1: Test VLM understanding
GEMINI_API_KEY=your_key python test_vlm.py

# Phase 2: Full pipeline (capture 3 screenshots → analyze → produce ActivityCard)
GEMINI_API_KEY=your_key python pipeline.py --count 3
```

## What's Built (as of 2026-03-24)

| File | Lines | What it does | Status |
|------|------:|-------------|--------|
| `capture.py` | 50 | Screenshot → 1080p JPEG (250ms, ~350KB) | Validated on Windows 11 AIPC |
| `test_vlm.py` | 80 | Single screenshot → Gemini Flash → activity description | Confidence 1.0 |
| `storage.py` | 160 | SQLite: screenshots, batches, cards tables | Working |
| `provider_gemini.py` | 150 | Gemini 2.5 Flash: transcribe + generate card (2 API calls) | Working |
| `pipeline.py` | 100 | End-to-end: capture → batch → analyze → store | Produces real ActivityCards |
| `INTERFACE.md` | 380 | Full interface spec: inputs, outputs, API, dashboard | Spec complete |

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
├── capture.py           # Screen capture daemon (mss library)
├── storage.py           # SQLite: screenshots, batches, cards
├── provider_gemini.py   # Gemini Vision: transcribe + generate card
├── pipeline.py          # Orchestrator: capture → batch → analyze → store
├── test_vlm.py          # VLM validation script
├── INTERFACE.md         # Interface specification (inputs/outputs/API)
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
- [ ] Phase 4: Daemon mode + REST API (`localhost:5700`)
- [ ] Phase 5: Dashboard (mnemosyne.irisgo.xyz)
- [ ] Phase 6: IrisGo app integration
- [ ] Phase 7: ActivityWatch bridge for metadata enrichment

## API (Planned)

```
GET /api/v1/context/now    # Current activity + system prompt fragment
GET /api/v1/cards          # ActivityCards by date/category
GET /api/v1/profile        # Aggregated context profile
GET /api/v1/summary        # AI-generated day summary
GET /api/v1/health         # System status
POST /api/v1/settings      # Configuration
```

See [INTERFACE.md](./INTERFACE.md) for full specification.

## Requirements

- Python 3.11+
- `mss` (screen capture)
- `Pillow` (image processing)
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
