"""Phase 0: Screen capture validation on Windows AIPC.

Takes a single screenshot, scales to ~1080p, saves as JPEG.
Smart dedup: skips saving if the screen hasn't changed significantly.

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

# Smart dedup: downscale to tiny thumbnail and compare pixel difference
_THUMB_SIZE = (32, 18)  # 32x18 = 576 pixels, very fast to compare
_last_thumb = None
_same_count = 0
_FORCE_SAVE_EVERY = 30  # force save every 30 captures (~5 min) even if unchanged
_DIFF_THRESHOLD = 5  # avg pixel difference below this = "same screen" (0-255 scale)


def _get_thumb(img: Image.Image) -> bytes:
    """Downscale to tiny grayscale thumbnail for comparison."""
    return img.resize(_THUMB_SIZE, Image.NEAREST).convert("L").tobytes()


def _pixel_diff(a: bytes, b: bytes) -> float:
    """Average absolute pixel difference between two grayscale thumbnails."""
    return sum(abs(x - y) for x, y in zip(a, b)) / len(a)


def capture_screenshot(force: bool = False) -> Path | None:
    """Capture primary monitor, scale to 1080p, save as JPEG.

    Args:
        force: Skip the dedup check and always save. Use for onboarding
            seeding where the UI blocks on a static page that would
            otherwise make every capture look identical.

    Returns None if the screen hasn't changed (smart dedup).
    Returns the file path if saved.
    """
    global _last_thumb, _same_count

    with mss.mss() as sct:
        monitor = sct.monitors[1]
        raw = sct.grab(monitor)
        img = Image.frombytes("RGB", raw.size, raw.bgra, "raw", "BGRX")

    # Scale to target height
    if img.height > TARGET_HEIGHT:
        ratio = TARGET_HEIGHT / img.height
        new_size = (int(img.width * ratio), TARGET_HEIGHT)
        img = img.resize(new_size, Image.LANCZOS)

    # Smart dedup check (skipped when force=True)
    current_thumb = _get_thumb(img)
    if not force and _last_thumb is not None:
        diff = _pixel_diff(current_thumb, _last_thumb)
        if diff < _DIFF_THRESHOLD:
            _same_count += 1
            if _same_count < _FORCE_SAVE_EVERY:
                return None  # screen unchanged, skip

    _last_thumb = current_thumb
    _same_count = 0

    # Save
    today = datetime.now().strftime("%Y-%m-%d")
    timestamp = datetime.now().strftime("%H%M%S")
    out_dir = DATA_DIR / "captures" / today
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{timestamp}.jpg"
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
