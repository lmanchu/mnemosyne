"""Phase 0: Screen capture validation on Windows AIPC.

Takes a single screenshot, scales to ~1080p, saves as JPEG.
Run: python capture.py
Output: ~/.mnemosyne/captures/{date}/{HHMMSS}.jpg
"""

import time
from datetime import datetime
from pathlib import Path

import mss
from PIL import Image

# Config
TARGET_HEIGHT = 1080
JPEG_QUALITY = 85
DATA_DIR = Path.home() / ".mnemosyne"


def capture_screenshot() -> Path:
    """Capture primary monitor, scale to 1080p, save as JPEG."""
    today = datetime.now().strftime("%Y-%m-%d")
    timestamp = datetime.now().strftime("%H%M%S")
    out_dir = DATA_DIR / "captures" / today
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{timestamp}.jpg"

    with mss.mss() as sct:
        # Monitor 0 = all monitors combined, 1 = primary
        monitor = sct.monitors[1]
        raw = sct.grab(monitor)

        img = Image.frombytes("RGB", raw.size, raw.bgra, "raw", "BGRX")

        # Scale to target height
        if img.height > TARGET_HEIGHT:
            ratio = TARGET_HEIGHT / img.height
            new_size = (int(img.width * ratio), TARGET_HEIGHT)
            img = img.resize(new_size, Image.LANCZOS)

        img.save(out_path, "JPEG", quality=JPEG_QUALITY)

    return out_path


if __name__ == "__main__":
    t0 = time.perf_counter()
    path = capture_screenshot()
    elapsed = (time.perf_counter() - t0) * 1000

    size_kb = path.stat().st_size / 1024
    img = Image.open(path)

    print(f"Saved: {path}")
    print(f"Size:  {size_kb:.1f} KB")
    print(f"Res:   {img.width}x{img.height}")
    print(f"Time:  {elapsed:.0f} ms")
