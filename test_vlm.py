"""Phase 1: Single VLM call — can Gemini understand what the user is doing?

Takes the latest screenshot and sends it to Gemini Flash with a transcription prompt.
Run: GEMINI_API_KEY=xxx python test_vlm.py

This is the most important test. If the VLM can't describe the screenshot
accurately, nothing else matters.
"""

import base64
import json
import os
import sys
import time
from pathlib import Path

import urllib.request

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
MODEL = "gemini-2.5-flash"
ENDPOINT = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"

PROMPT = """You are analyzing a screenshot of a computer screen.

Describe what the user is doing in 2-3 sentences. Be specific:
- What application(s) are visible?
- What task are they working on?
- What content is on screen?

Then output a JSON object:
{
  "category": "one of: Development, Communication, Research, Writing, Meeting, Entertainment, Idle, Other",
  "title": "5-10 word description of the activity",
  "summary": "1-2 sentence summary",
  "apps_visible": ["list of app names"],
  "confidence": 0.0-1.0
}

Return ONLY the description paragraphs followed by the JSON. No markdown fences."""


def encode_image(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode()


def call_gemini(image_path: Path) -> str:
    b64 = encode_image(image_path)

    payload = {
        "contents": [{
            "parts": [
                {"text": PROMPT},
                {"inline_data": {"mime_type": "image/jpeg", "data": b64}}
            ]
        }],
        "generationConfig": {
            "temperature": 0.2,
            "maxOutputTokens": 1024
        }
    }

    url = f"{ENDPOINT}?key={GEMINI_API_KEY}"
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    with urllib.request.urlopen(req, timeout=30) as resp:
        result = json.loads(resp.read())

    return result["candidates"][0]["content"]["parts"][0]["text"]


def find_latest_screenshot() -> Path:
    captures_dir = Path.home() / ".mnemosyne" / "captures"
    all_files = sorted(captures_dir.rglob("*.jpg"))
    if not all_files:
        print("No screenshots found. Run capture.py first.")
        sys.exit(1)
    return all_files[-1]


if __name__ == "__main__":
    if not GEMINI_API_KEY:
        print("Set GEMINI_API_KEY environment variable.")
        print("Usage: GEMINI_API_KEY=xxx python test_vlm.py")
        sys.exit(1)

    img_path = find_latest_screenshot()
    print(f"Image: {img_path}")
    print(f"Size:  {img_path.stat().st_size / 1024:.1f} KB")
    print(f"Model: {MODEL}")
    print("---")

    t0 = time.perf_counter()
    response = call_gemini(img_path)
    elapsed = (time.perf_counter() - t0) * 1000

    print(response)
    print("---")
    print(f"Latency: {elapsed:.0f} ms")
