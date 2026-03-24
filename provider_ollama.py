"""Ollama local provider — fully private, no cloud, uses NPU/GPU.

Requires Ollama running locally with a vision model (llava, minicpm-v, etc.).
Install: https://ollama.com/download
Pull model: ollama pull llava:13b

Two LLM calls per batch (same interface as Gemini provider):
1. transcribe(): images → text description (per-frame, then merge)
2. generate_card(): text → structured ActivityCard JSON
"""

import base64
import json
import os
import urllib.request
from pathlib import Path

OLLAMA_BASE = os.environ.get("OLLAMA_BASE", "http://localhost:11434")
VISION_MODEL = os.environ.get("OLLAMA_VISION_MODEL", "llava:13b")
TEXT_MODEL = os.environ.get("OLLAMA_TEXT_MODEL", "llama3.2:3b")
MODEL = f"ollama/{VISION_MODEL}"

TRANSCRIBE_PROMPT = """Describe what the user is doing on their computer screen.
Be specific: mention apps, documents, websites, code files, and tasks.
Additional context: {metadata}
Output 2-3 sentences."""

GENERATE_CARD_PROMPT = """Based on this activity description, generate a structured ActivityCard as JSON.

Activity description:
{transcription}

Time window: {start_time} to {end_time}

Return ONLY valid JSON:
{{
  "start_time": "{start_time}",
  "end_time": "{end_time}",
  "category": "one of: Development, Communication, Research, Writing, Meeting, Entertainment, Idle, Other",
  "subcategory": "more specific label",
  "title": "5-10 word description",
  "summary": "1-2 sentence summary",
  "detailed_summary": "full paragraph description",
  "apps_used": ["list of app names"],
  "urls_visited": [],
  "distractions": [],
  "confidence": 0.0-1.0
}}"""


def _call_ollama(model: str, prompt: str, images: list[str] = None) -> str:
    """Call Ollama API. images = list of base64-encoded image strings."""
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
    }
    if images:
        payload["images"] = images

    req = urllib.request.Request(
        f"{OLLAMA_BASE}/api/generate",
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    with urllib.request.urlopen(req, timeout=120) as resp:
        result = json.loads(resp.read())

    return result.get("response", "")


def is_available() -> bool:
    """Check if Ollama is running and has a vision model."""
    try:
        req = urllib.request.Request(f"{OLLAMA_BASE}/api/tags")
        with urllib.request.urlopen(req, timeout=3) as resp:
            data = json.loads(resp.read())
            models = [m.get("name", "") for m in data.get("models", [])]
            return any(VISION_MODEL.split(":")[0] in m for m in models)
    except Exception:
        return False


def transcribe(screenshots: list[dict], start_time: str, end_time: str) -> tuple[str, dict]:
    """Send screenshots to Ollama vision model, get text description.

    Ollama processes images one at a time (no batch), so we sample fewer frames.
    Returns: (transcription_text, usage_dict)
    """
    # Sample up to 5 images
    max_images = 5
    if len(screenshots) <= max_images:
        sampled = screenshots
    else:
        step = len(screenshots) / max_images
        sampled = [screenshots[int(i * step)] for i in range(max_images)]

    # Build metadata
    apps_seen = set()
    for s in screenshots:
        if s.get("active_app"):
            apps_seen.add(s["active_app"])
    metadata = f"Apps: {', '.join(sorted(apps_seen))}" if apps_seen else "No metadata"

    # Transcribe each frame, then merge
    descriptions = []
    for s in sampled:
        p = Path(s["file_path"])
        if not p.exists():
            continue
        b64 = base64.b64encode(p.read_bytes()).decode()
        prompt = TRANSCRIBE_PROMPT.format(metadata=metadata)
        desc = _call_ollama(VISION_MODEL, prompt, images=[b64])
        descriptions.append(desc.strip())

    # Merge descriptions
    if len(descriptions) > 1:
        merge_prompt = f"Merge these {len(descriptions)} screen descriptions into one coherent 2-4 paragraph summary:\n\n" + "\n---\n".join(descriptions)
        merged = _call_ollama(TEXT_MODEL, merge_prompt)
        return merged.strip(), {"frames": len(descriptions)}
    elif descriptions:
        return descriptions[0], {"frames": 1}
    else:
        return "No screenshots available for analysis.", {"frames": 0}


def generate_card(transcription: str, start_time: str, end_time: str) -> tuple[dict, dict]:
    """Generate structured ActivityCard from transcription.
    Returns: (card_dict, usage_dict)
    """
    prompt = GENERATE_CARD_PROMPT.format(
        transcription=transcription,
        start_time=start_time,
        end_time=end_time
    )

    text = _call_ollama(TEXT_MODEL, prompt)

    # Parse JSON
    clean = text.strip()
    brace_start = clean.find("{")
    brace_end = clean.rfind("}")
    if brace_start == -1 or brace_end == -1:
        raise ValueError(f"No JSON in Ollama response: {clean[:200]}")
    clean = clean[brace_start:brace_end + 1]

    card = json.loads(clean)
    card["provider"] = "ollama"
    card["model"] = VISION_MODEL
    return card, {}


if __name__ == "__main__":
    print(f"Ollama base: {OLLAMA_BASE}")
    print(f"Vision model: {VISION_MODEL}")
    print(f"Text model: {TEXT_MODEL}")
    print(f"Available: {is_available()}")
