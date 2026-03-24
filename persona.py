"""Persona evolution — synthesize ActivityCards into an evolving user persona.

Three layers:
  - Session: last 2 hours of cards → what they're doing now
  - Daily: all cards today → what kind of day
  - Stable: accumulated across days → who they are

Usage:
  GEMINI_API_KEY=xxx python persona.py                # synthesize today
  GEMINI_API_KEY=xxx python persona.py --date 2026-03-24
  GEMINI_API_KEY=xxx python persona.py --show         # show current persona
"""

import argparse
import json
import os
import time
from datetime import datetime

import provider_gemini as gemini
import storage

SYNTHESIZE_PROMPT = """You are building a user persona from their computer activity data.

Here are {card_count} activity cards from {date}, each representing a ~15-minute block:

{cards_text}

{previous_persona}

Based on this activity data, synthesize a user persona. Output ONLY valid JSON (no markdown):
{{
  "date": "{date}",
  "confidence": 0.0-1.0,
  "identity": {{
    "likely_role": "best guess of their job/role based on activity",
    "seniority": "junior/mid/senior/lead/executive"
  }},
  "work_style": {{
    "type": "deep_focus_blocks / multitasker / meeting_heavy / mixed",
    "peak_hours": "when they seem most productive",
    "communication": "async_first / sync_heavy / balanced",
    "context_switches": "low / medium / high"
  }},
  "tools": {{
    "primary": ["top 3-5 most used apps"],
    "secondary": ["other apps seen"]
  }},
  "categories": {{
    "top": "most time spent category",
    "distribution": {{"category": "percentage"}}
  }},
  "interests": {{
    "current": ["topics they're actively working on"],
    "inferred": ["broader interests based on tools and content"]
  }},
  "patterns": {{
    "focus_level": "low / medium / high",
    "distractions": "none / few / frequent",
    "work_life": "all_work / mostly_work / balanced / mostly_personal"
  }},
  "summary": "2-3 sentence natural language description of this person"
}}"""


def format_cards_for_prompt(cards: list[dict]) -> str:
    lines = []
    for c in cards:
        apps = c.get("apps_used", [])
        if isinstance(apps, str):
            try:
                apps = json.loads(apps)
            except:
                apps = []
        lines.append(
            f"[{c.get('start_time', '?')} → {c.get('end_time', '?')}] "
            f"Category: {c.get('category', '?')} | "
            f"Title: {c.get('title', '?')} | "
            f"Apps: {', '.join(apps) if apps else 'unknown'} | "
            f"Summary: {c.get('summary', '')}"
        )
    return "\n".join(lines)


def synthesize_daily(date: str = None) -> dict | None:
    """Synthesize a daily persona from all cards on the given date."""
    if not date:
        date = datetime.now().strftime("%Y-%m-%d")

    cards = storage.get_cards(date=date, limit=200)
    if not cards:
        print(f"No cards for {date}. Run the pipeline first.")
        return None

    print(f"Synthesizing persona from {len(cards)} cards on {date}...")

    # Check for existing persona to provide continuity
    existing = storage.get_latest_persona()
    if existing and existing.get("data"):
        prev_data = existing["data"] if isinstance(existing["data"], dict) else {}
        prev_text = f"\nPrevious persona (for continuity — update, don't replace):\n{json.dumps(prev_data, indent=2)}"
    else:
        prev_text = "\nNo previous persona exists. This is the first synthesis."

    cards_text = format_cards_for_prompt(cards)

    prompt = SYNTHESIZE_PROMPT.format(
        card_count=len(cards),
        date=date,
        cards_text=cards_text,
        previous_persona=prev_text
    )

    t0 = time.perf_counter()
    text, usage = gemini._call_gemini([{"text": prompt}], temperature=0.2, max_tokens=4096)
    elapsed = (time.perf_counter() - t0) * 1000

    # Parse JSON
    clean = text.strip()
    brace_start = clean.find("{")
    brace_end = clean.rfind("}")
    if brace_start == -1 or brace_end == -1:
        print(f"Failed to parse persona JSON: {clean[:200]}")
        return None
    clean = clean[brace_start:brace_end + 1]

    try:
        persona = json.loads(clean)
    except json.JSONDecodeError as e:
        print(f"JSON parse error: {e}")
        print(f"Raw: {clean[:300]}")
        return None

    # Enrich with metadata
    persona["synthesized_at"] = datetime.now().isoformat()
    persona["card_count"] = len(cards)
    persona["llm_latency_ms"] = round(elapsed)

    # Calculate version
    existing_count = 0
    conn = storage.get_db()
    existing_count = conn.execute("SELECT COUNT(*) FROM persona").fetchone()[0]
    conn.close()
    version = f"0.{existing_count + 1}.0"

    # Save
    confidence = persona.get("confidence", 0.5)
    pid = storage.save_persona(version, persona, confidence)
    print(f"Persona v{version} saved (id={pid}, confidence={confidence}, {elapsed:.0f}ms)")

    return persona


def show_persona():
    """Display the latest persona."""
    p = storage.get_latest_persona()
    if not p:
        print("No persona yet. Run: GEMINI_API_KEY=xxx python persona.py")
        return

    data = p.get("data", {})
    if isinstance(data, str):
        try:
            data = json.loads(data)
        except:
            data = {}

    print(f"\n{'='*60}")
    print(f"Persona v{p.get('version', '?')} (confidence: {p.get('confidence', 0):.0%})")
    print(f"{'='*60}")

    if data.get("summary"):
        print(f"\n{data['summary']}")

    if data.get("identity"):
        ident = data["identity"]
        print(f"\nRole: {ident.get('likely_role', '—')} ({ident.get('seniority', '—')})")

    if data.get("work_style"):
        ws = data["work_style"]
        print(f"Work style: {ws.get('type', '—')}")
        print(f"Peak hours: {ws.get('peak_hours', '—')}")
        print(f"Communication: {ws.get('communication', '—')}")

    if data.get("tools"):
        tools = data["tools"]
        print(f"Primary tools: {', '.join(tools.get('primary', []))}")

    if data.get("categories"):
        cats = data["categories"]
        print(f"Top category: {cats.get('top', '—')}")
        dist = cats.get("distribution", {})
        if dist:
            print(f"Distribution: {', '.join(f'{k} {v}' for k, v in dist.items())}")

    if data.get("interests"):
        interests = data["interests"]
        current = interests.get("current", [])
        if current:
            print(f"Current interests: {', '.join(current)}")

    if data.get("patterns"):
        pat = data["patterns"]
        print(f"Focus: {pat.get('focus_level', '—')} | Distractions: {pat.get('distractions', '—')}")

    print(f"\nCards analyzed: {data.get('card_count', '?')}")
    print(f"Synthesized: {data.get('synthesized_at', p.get('created_at', '?'))}")
    print(f"{'='*60}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Mnemosyne persona evolution")
    parser.add_argument("--date", help="Date to synthesize (YYYY-MM-DD, default: today)")
    parser.add_argument("--show", action="store_true", help="Show current persona")
    args = parser.parse_args()

    if args.show:
        show_persona()
    else:
        if not os.environ.get("GEMINI_API_KEY"):
            print("Set GEMINI_API_KEY. Usage: GEMINI_API_KEY=xxx python persona.py")
            exit(1)
        persona = synthesize_daily(args.date)
        if persona:
            print(f"\nSummary: {persona.get('summary', '—')}")
