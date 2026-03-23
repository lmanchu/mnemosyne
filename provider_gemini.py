"""Gemini Vision provider — transcribe screenshots + generate ActivityCard.

Two LLM calls per batch (same as Dayflow's Gemini flow):
1. transcribe(): images + metadata → text description
2. generate_card(): text → structured ActivityCard JSON
"""

import base64
import json
import os
import urllib.request
from pathlib import Path

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
MODEL = "gemini-2.5-flash"
ENDPOINT = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"

TRANSCRIBE_PROMPT = """You are analyzing {count} screenshots of a computer screen, taken every ~10 seconds.
Time window: {start_time} to {end_time}

Additional context from system monitoring:
{metadata}

Describe what the user was doing during this period in 2-4 paragraphs.
Be specific: mention apps, documents, websites, code files, and tasks.
Note any context switches or distractions.
Describe the flow of work, not just a list of apps."""

GENERATE_CARD_PROMPT = """Based on this activity description, generate a structured ActivityCard as JSON.

Activity description:
{transcription}

Time window: {start_time} to {end_time}

Return ONLY valid JSON matching this schema (no markdown, no fences):
{{
  "start_time": "{start_time}",
  "end_time": "{end_time}",
  "category": "one of: Development, Communication, Research, Writing, Meeting, Entertainment, Idle, Other",
  "subcategory": "more specific label",
  "title": "5-10 word description",
  "summary": "1-2 sentence summary",
  "detailed_summary": "full paragraph description",
  "apps_used": ["list of app names"],
  "urls_visited": ["list of URLs if visible"],
  "distractions": [],
  "confidence": 0.0-1.0
}}"""


def _call_gemini(parts: list, temperature: float = 0.2, max_tokens: int = 2048) -> tuple[str, dict]:
    """Make a Gemini API call. Returns (text, usage_metadata)."""
    payload = {
        "contents": [{"parts": parts}],
        "generationConfig": {
            "temperature": temperature,
            "maxOutputTokens": max_tokens
        }
    }

    url = f"{ENDPOINT}?key={GEMINI_API_KEY}"
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    with urllib.request.urlopen(req, timeout=60) as resp:
        result = json.loads(resp.read())

    text = result["candidates"][0]["content"]["parts"][0]["text"]
    usage = result.get("usageMetadata", {})
    return text, usage


def _encode_image(path: Path) -> dict:
    b64 = base64.b64encode(path.read_bytes()).decode()
    return {"inline_data": {"mime_type": "image/jpeg", "data": b64}}


def transcribe(screenshots: list[dict], start_time: str, end_time: str) -> tuple[str, dict]:
    """Send screenshots to Gemini, get text description.

    screenshots: list of dicts with 'file_path', 'active_app', 'window_title', etc.
    Returns: (transcription_text, usage_metadata)
    """
    # Build metadata summary from screenshot records
    apps_seen = set()
    titles_seen = set()
    for s in screenshots:
        if s.get("active_app"):
            apps_seen.add(s["active_app"])
        if s.get("window_title"):
            titles_seen.add(s["window_title"])

    metadata_lines = []
    if apps_seen:
        metadata_lines.append(f"Apps used: {', '.join(sorted(apps_seen))}")
    if titles_seen:
        # Only show unique titles, truncated
        unique_titles = list(titles_seen)[:10]
        metadata_lines.append(f"Window titles: {'; '.join(unique_titles)}")
    metadata = "\n".join(metadata_lines) if metadata_lines else "No additional metadata available."

    prompt_text = TRANSCRIBE_PROMPT.format(
        count=len(screenshots),
        start_time=start_time,
        end_time=end_time,
        metadata=metadata
    )

    # Build parts: prompt text + sampled images
    # For cost/speed, sample up to 10 images evenly from the batch
    max_images = 10
    if len(screenshots) <= max_images:
        sampled = screenshots
    else:
        step = len(screenshots) / max_images
        sampled = [screenshots[int(i * step)] for i in range(max_images)]

    parts = [{"text": prompt_text}]
    for s in sampled:
        p = Path(s["file_path"])
        if p.exists():
            parts.append(_encode_image(p))

    return _call_gemini(parts, temperature=0.2, max_tokens=2048)


def generate_card(transcription: str, start_time: str, end_time: str) -> tuple[dict, dict]:
    """Generate structured ActivityCard from transcription text.

    Returns: (card_dict, usage_metadata)
    """
    prompt_text = GENERATE_CARD_PROMPT.format(
        transcription=transcription,
        start_time=start_time,
        end_time=end_time
    )

    text, usage = _call_gemini([{"text": prompt_text}], temperature=0.1, max_tokens=4096)

    # Extract JSON from response — handle markdown fences, mixed text, thinking blocks
    clean = text.strip()
    # Find the first { and last } to extract JSON object
    brace_start = clean.find("{")
    brace_end = clean.rfind("}")
    if brace_start == -1 or brace_end == -1:
        raise ValueError(f"No JSON object found in response: {clean[:200]}")
    clean = clean[brace_start:brace_end + 1]

    card = json.loads(clean)
    card["provider"] = "gemini"
    card["model"] = MODEL
    return card, usage
