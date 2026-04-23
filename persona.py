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


def to_markdown(persona_row: dict = None) -> str:
    """Convert persona data to editable markdown."""
    if not persona_row:
        persona_row = storage.get_latest_persona()
    if not persona_row:
        return "# My Persona\n\n_No persona generated yet. Run the onboarding or daemon first._\n"

    data = persona_row.get("data", {})
    if isinstance(data, str):
        try:
            data = json.loads(data)
        except:
            data = {}

    version = persona_row.get("version", "?")
    confidence = persona_row.get("confidence", 0)
    created = persona_row.get("created_at", "?")

    lines = [
        f"# My Persona",
        f"",
        f"> Version {version} | Confidence {confidence:.0%} | Last updated: {created}",
        f"> Edit freely — your changes override AI-generated content.",
        f"",
    ]

    # Summary
    if data.get("summary"):
        lines += [f"## Summary", f"", data["summary"], f""]

    # Identity — handle both synthesized (likely_role) and onboarding (role) formats
    ident = data.get("identity", {})
    role = ident.get("likely_role", "") or ident.get("role", "") or "_not yet determined_"
    seniority = ident.get("seniority", "_unknown_")
    lines += [
        f"## Identity",
        f"",
        f"- **Role**: {role}",
        f"- **Seniority**: {seniority}",
        f"",
    ]

    # Work Style — handle both formats
    ws = data.get("work_style", {})
    lines += [f"## Work Style", f""]
    if ws.get("type"):
        lines.append(f"- **Type**: {ws['type']}")
    if ws.get("peak_hours"):
        lines.append(f"- **Peak hours**: {ws['peak_hours']}")
    if ws.get("communication"):
        lines.append(f"- **Communication**: {ws['communication']}")
    if ws.get("context_switches"):
        lines.append(f"- **Context switches**: {ws['context_switches']}")
    # From onboarding format
    top_cats = ws.get("top_categories", [])
    if top_cats:
        lines.append(f"")
        lines.append(f"**Activity breakdown**:")
        for tc in top_cats:
            lines.append(f"- {tc.get('name', '?')}: {tc.get('pct', '?')}%")
    lines.append("")

    # Tools — handle both formats
    tools = data.get("tools", {})
    primary = tools.get("primary", []) or ws.get("apps_primary", [])
    secondary = tools.get("secondary", [])
    lines += [f"## Tools", f""]
    if primary:
        lines.append(f"**Primary**: {', '.join(primary)}")
    if secondary:
        lines.append(f"**Secondary**: {', '.join(secondary)}")
    if not primary and not secondary:
        lines.append("_No tools detected yet_")
    lines.append("")

    # Interests — handle both formats
    interests = data.get("interests", {})
    current = interests.get("current", [])
    inferred = interests.get("inferred", []) or interests.get("from_context", [])
    lines += [f"## Interests", f""]
    if current:
        lines.append(f"**Current**: {', '.join(current)}")
    if inferred:
        lines.append(f"**Inferred**: {', '.join(inferred)}")
    lines.append("")

    # Social profiles (placeholder for user to fill)
    social = data.get("social_profiles", {})
    lines += [
        f"## Social Profiles",
        f"",
        f"- **LinkedIn**: {social.get('linkedin', '_paste URL_')}",
        f"- **Twitter/X**: {social.get('twitter', '_paste @handle_')}",
        f"- **Instagram**: {social.get('instagram', '_paste @handle_')}",
        f"- **Facebook**: {social.get('facebook', '_paste URL_')}",
        f"- **Medium/Blog**: {social.get('blog', '_paste URL_')}",
        f"- **GitHub**: {social.get('github', '_paste username_')}",
        f"",
    ]

    # Entertainment & culture
    entertainment = data.get("entertainment", {})
    lines += [
        f"## Entertainment & Culture",
        f"",
        f"_Add your favorites — this helps the AI use references and analogies you'll appreciate._",
        f"",
    ]
    for cat in ["anime", "movies", "tv_shows", "books", "games", "music", "hobbies"]:
        items = entertainment.get(cat, [])
        label = cat.replace("_", " ").title()
        if items:
            lines.append(f"**{label}**: {', '.join(items)}")
        else:
            lines.append(f"**{label}**: _none yet_")
    lines.append("")

    # Personality
    personality = data.get("personality", {})
    patterns = data.get("patterns", {})
    lines += [
        f"## Personality",
        f"",
        f"- **MBTI**: {personality.get('mbti', '_unknown_')}",
        f"- **Focus level**: {patterns.get('focus_level', '_unknown_')}",
        f"- **Distractions**: {patterns.get('distractions', '_unknown_')}",
        f"- **Work/life**: {patterns.get('work_life', '_unknown_')}",
        f"",
    ]

    # Categories
    cats = data.get("categories", {})
    dist = cats.get("distribution", {})
    if dist:
        lines += [f"## Activity Distribution", f""]
        for k, v in sorted(dist.items(), key=lambda x: -float(str(x[1]).rstrip('%'))):
            pct = f"{float(str(v).rstrip('%')) * 100:.1f}%" if isinstance(v, float) and v <= 1 else str(v)
            lines.append(f"- {k}: {pct}")
        lines.append("")

    # Custom notes
    custom = data.get("custom_notes", "")
    lines += [
        f"## My Notes",
        f"",
        f"_Add anything the AI should know about you that isn't captured above._",
        f"",
        custom if custom else "",
        f"",
    ]

    return "\n".join(lines)


_PLACEHOLDERS = {
    "_unknown_", "_not yet determined_", "_none yet_",
    "_paste url_", "_paste @handle_", "_paste username_",
}


def _parse_value(line: str, prefix: str) -> str | None:
    """Strip a `prefix` off `line` and return the trimmed value, or None
    if it's missing / a placeholder. Centralises the placeholder check
    so each scalar field doesn't repeat the same guard."""
    if not line.startswith(prefix):
        return None
    val = line.split(":", 1)[1].strip()
    if not val or val.lower() in _PLACEHOLDERS:
        return None
    return val


def _parse_list(val: str) -> list[str]:
    """Parse 'a, b, c' from `to_markdown`'s list serialisation. Empty
    items are dropped so 'a, , b' doesn't smuggle in blanks."""
    return [x.strip() for x in val.split(",") if x.strip()]


def from_markdown(md: str, existing_data: dict = None) -> dict:
    """Parse user-edited markdown back into persona data. Preserves fields user didn't edit.

    Scope: every field `to_markdown()` writes as user-editable should
    round-trip here. Synthesizer-generated fields (summary, activity
    distribution) are intentionally left to the daemon — the editor
    surfaces them as context but they aren't intended for hand-editing.
    """
    data = existing_data.copy() if existing_data else {}
    lines = [l.strip() for l in md.split("\n")]

    # Identity ---------------------------------------------------------
    for line in lines:
        val = _parse_value(line, "- **Role**:")
        if val:
            data.setdefault("identity", {})["likely_role"] = val
            data.setdefault("identity", {})["role"] = val
        val = _parse_value(line, "- **Seniority**:")
        if val:
            data.setdefault("identity", {})["seniority"] = val

    # Work Style -------------------------------------------------------
    # All four come from `to_markdown` as `- **<Field>**: value` bullets
    # under the `## Work Style` header. We don't bother scoping by
    # header — each prefix is unique enough across the document that
    # collisions are unlikely; if a user re-uses the wording in My Notes
    # we still write the right field.
    for line in lines:
        if val := _parse_value(line, "- **Type**:"):
            data.setdefault("work_style", {})["type"] = val
        if val := _parse_value(line, "- **Peak hours**:"):
            data.setdefault("work_style", {})["peak_hours"] = val
        if val := _parse_value(line, "- **Communication**:"):
            data.setdefault("work_style", {})["communication"] = val
        if val := _parse_value(line, "- **Context switches**:"):
            data.setdefault("work_style", {})["context_switches"] = val

    # Tools ------------------------------------------------------------
    # `**Primary**: app1, app2` — note no leading "- " (matches to_markdown).
    for line in lines:
        if val := _parse_value(line, "**Primary**:"):
            data.setdefault("tools", {})["primary"] = _parse_list(val)
        if val := _parse_value(line, "**Secondary**:"):
            data.setdefault("tools", {})["secondary"] = _parse_list(val)

    # Interests --------------------------------------------------------
    for line in lines:
        if val := _parse_value(line, "**Current**:"):
            data.setdefault("interests", {})["current"] = _parse_list(val)
        if val := _parse_value(line, "**Inferred**:"):
            data.setdefault("interests", {})["inferred"] = _parse_list(val)

    # Social profiles -------------------------------------------------
    social_map = {
        "- **LinkedIn**:": "linkedin",
        "- **Twitter/X**:": "twitter",
        "- **Instagram**:": "instagram",
        "- **Facebook**:": "facebook",
        "- **Medium/Blog**:": "blog",
        "- **GitHub**:": "github",
    }
    social: dict[str, str] = {}
    for line in lines:
        for prefix, key in social_map.items():
            if val := _parse_value(line, prefix):
                social[key] = val
    if social:
        data["social_profiles"] = social

    # Entertainment ----------------------------------------------------
    entertainment: dict[str, list[str]] = {}
    for cat in ["Anime", "Movies", "Tv Shows", "Books", "Games", "Music", "Hobbies"]:
        for line in lines:
            if val := _parse_value(line, f"**{cat}**:"):
                key = cat.lower().replace(" ", "_")
                entertainment[key] = _parse_list(val)
    if entertainment:
        data["entertainment"] = entertainment

    # Personality + Patterns ------------------------------------------
    # MBTI lives under personality; focus_level / distractions / work_life
    # render alongside it but belong to patterns (they're synthesised
    # signals the user can override).
    for line in lines:
        if val := _parse_value(line, "- **MBTI**:"):
            data.setdefault("personality", {})["mbti"] = val
        if val := _parse_value(line, "- **Focus level**:"):
            data.setdefault("patterns", {})["focus_level"] = val
        if val := _parse_value(line, "- **Distractions**:"):
            data.setdefault("patterns", {})["distractions"] = val
        if val := _parse_value(line, "- **Work/life**:"):
            data.setdefault("patterns", {})["work_life"] = val

    # Custom notes -----------------------------------------------------
    if "## My Notes" in md:
        notes_section = md.split("## My Notes")[1].strip()
        notes_lines = [
            l for l in notes_section.split("\n")
            if not l.strip().startswith("_Add anything")
        ]
        custom = "\n".join(notes_lines).strip()
        if custom:
            data["custom_notes"] = custom

    data["user_edited"] = True
    data["last_edited"] = datetime.now().isoformat()
    return data


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
