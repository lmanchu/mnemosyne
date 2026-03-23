# Mnemosyne Interface Specification

> What goes in. What comes out. How IrisGo app talks to it.
> Everything else is implementation detail.

**Version**: 2.0 (2026-03-24)
**Status**: Draft — replaces scattered docs from v1.x
**Author**: AK mode

---

## Philosophy

> The memory system can be seen as the most direct and intimate connection between the user and the agent. By contrast, the context-aware engine acts more like a bridge between the agent and the real world, giving the agent a better chance to fully understand and assist the user.
>
> — Lman Chu, 2026-03-24

```
User ←── Memory ──→ Agent ←── Context Engine ──→ Real World
        (intimate)            (bridge)
```

**Memory** is what the agent remembers about you — your preferences, past conversations, accumulated knowledge. It's the relationship.

**Context Engine** (Mnemosyne) is what the agent perceives about your world right now — what you're working on, which apps are open, how your day is going. It's the awareness.

An agent with memory but no context is like a friend who knows you well but can't see what you're doing. An agent with context but no memory is like a stranger watching over your shoulder. You need both.

## One Sentence

Mnemosyne watches your screen, understands what you're doing (not just which app is open), and serves structured context to IrisGo so it can personalize everything.

## System Boundary

```
┌──────────────────────────────────────────────────────────────┐
│                    User's AIPC (local)                        │
│                                                              │
│  ┌──────────┐   ┌──────────────────────┐   ┌─────────────┐  │
│  │ Screen    │──▶│    Mnemosyne Engine   │──▶│ REST API    │  │
│  │ Capture   │   │  (batch AI analysis)  │   │ :5700       │  │
│  └──────────┘   └──────────────────────┘   └──────┬──────┘  │
│                                                     │        │
│  ┌──────────┐                                       │        │
│  │Activity  │──▶ metadata enrichment                │        │
│  │Watch     │                                       │        │
│  └──────────┘                                       │        │
│                                                     │        │
│  ┌──────────────────────────────────────────────────┘        │
│  │                                                           │
│  ▼                                                           │
│  ┌──────────────────────┐    ┌────────────────────────────┐  │
│  │  IrisGo Desktop App  │    │  mnemosyne.irisgo.xyz      │  │
│  │  (primary consumer)  │    │  (dashboard + settings UI) │  │
│  └──────────────────────┘    └────────────────────────────┘  │
│                                                              │
└──────────────────────────────────────────────────────────────┘
        Nothing leaves the machine unless user opts in.
```

---

## INPUT: What Mnemosyne Collects

### Source 1: Screenshots (primary signal)

| Field | Type | Example |
|-------|------|---------|
| `captured_at` | unix timestamp | `1711267200` |
| `file_path` | string | `captures/2026-03-24/143022.jpg` |
| `file_size` | int64 bytes | `87432` |
| `display_index` | int | `0` |
| `idle_seconds` | int | `0` |

**Capture config:**
- Interval: 10 seconds (configurable: 5-30s)
- Resolution: scaled to ~1080p height
- Format: JPEG quality 85
- Storage: `~/.mnemosyne/captures/{YYYY-MM-DD}/{HHMMSS}.jpg`

### Source 2: ActivityWatch metadata (enrichment)

| Field | Type | Source |
|-------|------|--------|
| `active_app` | string | `aw-watcher-window` |
| `window_title` | string | `aw-watcher-window` |
| `url` | string | `aw-watcher-window` (browser extension) |
| `afk_status` | bool | `aw-watcher-afk` |
| `afk_since` | unix timestamp | `aw-watcher-afk` |

**Query endpoint:** `http://localhost:5600/api/0/`

### Source 3: Calendar (optional, via IrisGo)

| Field | Type | Source |
|-------|------|--------|
| `events` | array | Google Calendar API (via IrisGo MCP) |
| `current_meeting` | object | Real-time meeting context |

---

## OUTPUT: What Mnemosyne Produces

### Core Output: ActivityCard

This is the atomic unit of context. One card = one coherent activity block.

```json
{
  "id": 42,
  "batch_id": 7,
  "start_time": "2026-03-24T14:30:00+08:00",
  "end_time": "2026-03-24T14:47:00+08:00",
  "category": "Development",
  "subcategory": "Frontend",
  "title": "Implementing login form validation in React",
  "summary": "Working on the IrisGo web app login page, adding email format validation and error message display using React Hook Form.",
  "detailed_summary": "The user spent 17 minutes in VS Code editing LoginForm.tsx. They were implementing form validation using React Hook Form library, specifically adding email regex validation and displaying inline error messages. They referenced the react-hook-form docs in Chrome and tested the form in localhost:3000. No distractions detected during this focused block.",
  "apps_used": ["VS Code", "Chrome"],
  "urls_visited": ["localhost:3000", "react-hook-form.com/api"],
  "distractions": [],
  "confidence": 0.92,
  "provider": "gemini",
  "model": "gemini-2.5-flash",
  "processing_ms": 3200,
  "created_at": "2026-03-24T14:48:12+08:00"
}
```

### Derived Output: Context Profile

Aggregated from ActivityCards. Updated after each batch. This is what IrisGo app consumes for personalization.

```json
{
  "user_id": "local",
  "generated_at": "2026-03-24T23:00:00+08:00",
  "period": "2026-03-24",

  "current_context": {
    "activity": "Reading Hacker News in Chrome",
    "category": "Research",
    "since": "2026-03-24T22:45:00+08:00",
    "focus_level": "low"
  },

  "day_summary": {
    "total_active_hours": 8.5,
    "focus_score": 76,
    "top_categories": [
      {"name": "Development", "hours": 3.2, "pct": 38},
      {"name": "Communication", "hours": 2.1, "pct": 25},
      {"name": "Research", "hours": 1.8, "pct": 21},
      {"name": "Writing", "hours": 0.9, "pct": 11},
      {"name": "Idle", "hours": 0.5, "pct": 6}
    ],
    "apps_used": ["VS Code", "Chrome", "Slack", "Notion"],
    "peak_focus_hours": ["09:00-11:30", "14:00-16:00"],
    "distractions_count": 7,
    "context_switches": 23
  },

  "patterns": {
    "work_style": "deep_focus_blocks",
    "communication_style": "async_first",
    "learning_mode": "docs_then_implement",
    "peak_productivity": "morning",
    "tools_expertise": {
      "primary": ["VS Code", "Chrome", "Slack"],
      "secondary": ["Notion", "Figma", "Terminal"]
    }
  },

  "interests": {
    "current": ["React", "AI agents", "system design"],
    "trending_up": ["Rust", "WebAssembly"],
    "trending_down": ["Python scripting"]
  }
}
```

### Derived Output: System Prompt Fragment

Generated from Context Profile. Injected into IrisGo AI conversations.

```
You are assisting a user who is currently:
- Working on: IrisGo web app frontend (React + TypeScript)
- Focus level: High (in a 45-min coding block)
- Communication style: Async-first, concise, prefers code examples over explanations
- Current tools: VS Code, Chrome (localhost:3000)
- Today's pattern: 3.2h coding, 2.1h in Slack/email, research in mornings

Adapt your responses accordingly:
- Keep answers concise and code-focused
- Reference React/TypeScript conventions they're using
- Don't suggest context switches during focus blocks
```

---

## API: How IrisGo App Talks to Mnemosyne

Base URL: `http://localhost:5700/api/v1`

### Endpoints

#### GET /context/now
**The most important endpoint.** Returns current activity + recent context.

```json
{
  "current": {
    "activity": "Coding in VS Code",
    "category": "Development",
    "since": "2026-03-24T14:30:00+08:00",
    "app": "VS Code",
    "title": "LoginForm.tsx — irisgo-web"
  },
  "recent_cards": [ /* last 3 ActivityCards */ ],
  "focus_level": "high",
  "system_prompt_fragment": "You are assisting a user who is currently..."
}
```

#### GET /cards
Query ActivityCards by time range.

```
GET /cards?date=2026-03-24
GET /cards?start=2026-03-24T09:00&end=2026-03-24T12:00
GET /cards?category=Development&limit=10
```

#### GET /profile
Full Context Profile for the day or period.

```
GET /profile?date=2026-03-24
GET /profile?period=week
```

#### GET /summary
AI-generated natural language summary.

```
GET /summary?date=2026-03-24
```

Response:
```json
{
  "date": "2026-03-24",
  "summary": "Productive coding day focused on IrisGo frontend. Spent morning on login form validation (3.2h deep focus). Afternoon split between Slack discussions about the Acer PRD and research on React Hook Form patterns. 7 distraction events, mostly from Slack notifications. Recommend blocking notifications during morning focus blocks.",
  "highlights": [
    "Completed login form validation feature",
    "Reviewed Acer PRD feedback with team",
    "Discovered react-hook-form resolver pattern"
  ]
}
```

#### GET /health
System status.

```json
{
  "status": "running",
  "capture": {"active": true, "interval_seconds": 10, "last_capture": "2026-03-24T14:47:52"},
  "activitywatch": {"connected": true, "version": "0.12.3"},
  "provider": {"name": "gemini", "model": "gemini-2.5-flash", "last_call": "2026-03-24T14:48:12"},
  "storage": {"db_size_mb": 12.4, "captures_size_mb": 847.2, "captures_count": 31204},
  "uptime_hours": 72.3
}
```

#### POST /settings
Update configuration.

```json
{
  "provider": "gemini",
  "gemini_api_key": "...",
  "capture_interval": 10,
  "categories": ["Development", "Communication", "Research", "Writing", "Meeting", "Idle"],
  "storage_limit_gb": 5,
  "batch_duration_minutes": 15
}
```

---

## mnemosyne.irisgo.xyz — Dashboard

A local-first web UI served by the Mnemosyne engine on `localhost:5700`.
The `mnemosyne.irisgo.xyz` domain redirects to docs + download.

### Pages

#### 1. Timeline (/)
- Visual timeline of the day (like Dayflow)
- ActivityCards as colored blocks on a time axis
- Click card → expand to see screenshots + summary
- Filter by category

#### 2. Profile (/profile)
- Context Profile visualization
- Work patterns radar chart
- Category distribution donut
- Focus score trend (7-day)
- App usage breakdown

#### 3. Settings (/settings)
- Provider selection (Gemini / Claude / OpenAI / Ollama)
- API key management
- Capture interval slider
- Category editor
- Storage management (current usage + cleanup)
- Privacy controls: what data to collect, retention period

#### 4. Live (/live)
- Current activity card (real-time)
- Last 3 completed cards
- System status indicators
- Useful for demo / Computex booth

### Tech Stack (dashboard)

Minimal. No build step.

```
Single HTML file + Tailwind CDN + Alpine.js
Fetches from localhost:5700/api/v1/*
Served by the same Python process
```

Why: One file. No npm. No build. Ship it in the repo. Open in browser. Done.

---

## For IrisGo App Integration

The IrisGo Electron app integrates via:

1. **Startup**: Check if Mnemosyne is running (`GET /health`)
2. **Context injection**: Before each AI call, fetch `GET /context/now` and prepend `system_prompt_fragment` to the conversation
3. **Dashboard embed**: Load `http://localhost:5700/` in an iframe or webview for the Activity tab
4. **Settings sync**: IrisGo app settings page calls `POST /settings` to configure Mnemosyne

```
IrisGo App                          Mnemosyne Engine
─────────                          ──────────────────
User opens app
  → GET /health                    → 200 OK (or start engine)

User asks AI question
  → GET /context/now               → {current, system_prompt_fragment}
  → Prepend fragment to system prompt
  → Send to LLM
  → Response is personalized ✓

User opens Activity tab
  → iframe localhost:5700           → Timeline dashboard

User changes settings
  → POST /settings                  → Update config
```

---

## What We Don't Build (Non-Goals)

- No cloud sync (local only, unless user opts in)
- No mobile app (AIPC desktop only)
- No real-time streaming to LLM (batch is enough)
- No OCR preprocessing (VLM handles it)
- No browser extension (ActivityWatch has one)
- No social features (single user)

---

## Eval: How We Know It Works

**Primary metric**: Card Accuracy
- Show user 10 random cards from their day
- Ask: "Is this what you were doing?" (yes/no)
- Target: >80% yes

**Secondary metric**: Personalization Delta
- Same question to IrisGo with Mnemosyne context vs without
- Blind evaluation: which response is more helpful?
- Target: >70% prefer Mnemosyne-enhanced

---

*This spec defines the contract. Implementation follows.*
