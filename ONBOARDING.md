# Mnemosyne Onboarding — Building Ground Zero Persona

> From stranger to "I know you" in 5 minutes.
> Then let the context engine evolve it forever.

## The Problem

Lman's Deep Persona Profile took 4 months and 8 data sources to reach v1.717 (confidence 0.95). A new user can't wait 4 months. They need value on day one.

## The Insight

A persona has two parts:
- **Who you are** (stable, changes slowly) → get this during onboarding
- **What you're doing** (dynamic, changes hourly) → get this from context engine

Onboarding builds the first part. Context engine handles the second.

## Onboarding Flow: 4 Stages, 5 Minutes Total

```
Stage 1: Quick Signal (30 sec)
  "Connect one account, we'll figure you out"
         │
Stage 2: AI Interview (2 min)
  "Tell me about yourself in your own words"
         │
Stage 3: Behavioral Seed (1 min)
  "Let me watch you work for 60 seconds"
         │
Stage 4: Persona Draft (1 min)
  "Here's what I think I know. Correct me."
         │
  Ground Zero Persona (confidence ~0.5)
         │
  Context engine takes over → confidence grows daily
```

### Stage 1: Quick Signal — Import Existing Digital Footprint

**Pick one** (or more). Each gives different persona dimensions:

| Source | What it reveals | How | Time |
|--------|----------------|-----|------|
| LinkedIn profile | Role, skills, career arc, industry | OAuth or paste URL | 10s |
| Twitter/X feed | Interests, voice, community, opinions | OAuth or paste @handle | 10s |
| Medium/blog | Thinking patterns, writing style, expertise depth | Paste URL | 10s |
| GitHub profile | Tech stack, collaboration style, project types | OAuth or username | 10s |
| MBTI result | Personality framework (optional) | Select from dropdown | 5s |

**Why this works**: OpenClaw proved that a single social profile gives enough signal to generate a useful initial persona. The key insight from Iris building Lman's profile: 209 Medium articles revealed thinking patterns, values, and writing style that no questionnaire could capture.

**Implementation**: Use VLM to analyze social profile screenshots (same pipeline as context engine), or call public APIs where available.

### Stage 2: AI Interview — 3 Questions, Free-Form

Not a form. A conversation.

```
Q1: "What do you do for work, and what's the hardest part?"
    → Reveals: role, domain, pain points, communication style

Q2: "Describe a typical productive day for you."
    → Reveals: work patterns, tools, peak hours, priorities

Q3: "What topics are you currently obsessed with?"
    → Reveals: interests, learning mode, curiosity direction
```

**Why 3 questions, not 30**: Each answer is analyzed by LLM for multiple persona dimensions simultaneously. One rich paragraph > 20 checkbox answers.

**Why free-form, not multiple choice**: The WAY someone answers reveals as much as WHAT they answer (concise vs verbose, structured vs stream-of-consciousness, technical vs casual).

### Stage 3: Behavioral Seed — 60 Seconds of Screen Capture

```
"I'm going to watch your screen for 60 seconds. Just do what you normally do."
```

Captures 6 screenshots → runs through the standard pipeline → produces:
- Apps used (tools preference)
- Window titles (current projects)
- Desktop layout (organization style)
- Browser tabs (current interests)

**Why this matters**: Self-reported data has bias. People say they use VS Code 8 hours a day but screen capture shows 3 hours of Slack. Behavioral data is ground truth.

### Stage 4: Persona Draft — Show & Correct

Present the generated persona and let the user correct it:

```
"Based on what I've learned, here's my understanding of you:

  Role: Startup COO, technical background
  Work style: Deep focus mornings, async communication
  Tools: VS Code, Slack, Chrome, Terminal
  Interests: AI agents, system architecture, AIPC
  Personality: Strategic, data-driven, concise communicator

  Confidence: 0.52 (I'm just getting started)

  What did I get wrong? What's missing?"
```

User corrections are weighted heavily (confidence 1.0) because they're explicit first-person statements — like Lman's "Inner World" self-narrative that reached confidence 1.0 in the Deep Persona Profile.

## Ground Zero Persona Schema

```json
{
  "version": "0.1.0",
  "created_at": "2026-03-24T08:00:00",
  "confidence": 0.52,
  "days_observed": 0,

  "identity": {
    "role": "Startup COO",
    "industry": "AI / Technology",
    "experience_years": 10,
    "source": "linkedin + interview"
  },

  "work_style": {
    "type": "deep_focus_blocks",
    "peak_hours": "morning",
    "communication": "async_first",
    "tools_primary": ["VS Code", "Slack", "Chrome"],
    "source": "interview + behavioral_seed"
  },

  "personality": {
    "mbti": "INTJ",
    "communication_style": "concise",
    "decision_style": "data_driven",
    "source": "mbti + interview_analysis"
  },

  "interests": {
    "current": ["AI agents", "system architecture"],
    "source": "twitter + interview"
  },

  "writing_style": {
    "tone": "pragmatic",
    "structure": "outline_first",
    "length_preference": "concise",
    "source": "medium_analysis"
  },

  "corrections": [
    {"field": "peak_hours", "from": "afternoon", "to": "morning", "confidence": 1.0}
  ]
}
```

## Evolution: How Persona Grows After Onboarding

```
Day 0:  Ground Zero (onboarding)     confidence 0.5
Day 1:  + 8h of context data          confidence 0.55
Day 3:  + daily synthesis x3          confidence 0.65
Day 7:  + weekly pattern merge        confidence 0.75
Day 30: + monthly deep analysis       confidence 0.85
Day 90: + stable persona reached      confidence 0.90+
```

The context engine (ActivityCards) feeds into persona evolution:
- Daily: aggregate today's cards → update work_style, tools, interests
- Weekly: pattern detection → update personality traits, routines
- Monthly: deep LLM analysis → update identity, expertise

**Key principle**: Onboarding gets you to 0.5 in 5 minutes. The context engine gets you from 0.5 to 0.9 over 90 days. Neither alone is sufficient.

## Data Sources Mapping (from Lman's Deep Persona Profile)

What Lman built manually over 4 months, Mnemosyne automates:

| Lman's source | Persona dimension | Onboarding stage | Ongoing source |
|--------------|-------------------|-----------------|----------------|
| 209 Medium articles | Thinking patterns, values, writing style | Stage 1 (blog URL) | — (stable) |
| LinkedIn | Career, skills, industry | Stage 1 (OAuth) | — (stable) |
| DayFlow captures | Tools, focus, patterns | Stage 3 (behavioral seed) | Context engine (daily) |
| MBTI analysis | Personality framework | Stage 1 (dropdown) | Validated by behavior |
| Self-narrative | Inner world, motivations | Stage 2 (interview) | User corrections |
| Twitter/X | Interests, voice, community | Stage 1 (handle) | Context engine (if browsing) |
| Otaku attributes | Cultural interests | Stage 2 Q3 | Context engine |
| DayFlow daily stats | Focus score, efficiency | — | Context engine (daily) |

## For IrisGo App Integration

```
First launch
  → Show onboarding flow (4 stages)
  → Generate ground zero persona
  → Store in Mnemosyne DB
  → Start context engine daemon
  → Every AI interaction uses: persona + live context

Subsequent launches
  → Load persona from DB
  → Check for daily/weekly updates
  → Context engine continues enriching
```

## Non-Goals for Onboarding

- No mandatory social login (paste URL works too)
- No lengthy questionnaire (3 questions max)
- No personality quiz (MBTI is optional, not required)
- No data upload (we capture, not import)
- No "complete your profile" nagging

---

*The best onboarding feels like a conversation, not a form.*
*The best persona is one that gets better every day without you noticing.*
