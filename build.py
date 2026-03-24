"""Build Mnemosyne into a distributable package.

Usage:
  python build.py          # build exe
  python build.py --clean  # clean build artifacts first
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

ROOT = Path(__file__).parent
DIST = ROOT / "dist"
BUILD = ROOT / "build"

DATA_FILES = [
    "dashboard.html",
    "onboarding.html",
    "persona-editor.html",
]

HIDDEN_IMPORTS = [
    "mss",
    "mss.windows",
    "PIL",
    "PIL.Image",
    "mcp",
    "mcp.server",
    "mcp.server.fastmcp",
]


def clean():
    for d in [DIST, BUILD]:
        if d.exists():
            shutil.rmtree(d)
            print(f"Cleaned {d}")
    spec = ROOT / "app.spec"
    if spec.exists():
        spec.unlink()


def build():
    # Build PyInstaller command
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name", "mnemosyne",
        "--noconfirm",
        "--console",  # show console for daemon output
    ]

    # Add data files (HTML pages)
    for f in DATA_FILES:
        src = str(ROOT / f)
        cmd += ["--add-data", f"{src};."]

    # Hidden imports
    for h in HIDDEN_IMPORTS:
        cmd += ["--hidden-import", h]

    # Add all Python modules
    for py in ROOT.glob("*.py"):
        if py.name not in ("build.py", "test_vlm.py", "app.py"):
            cmd += ["--hidden-import", py.stem]

    # Entry point
    cmd.append(str(ROOT / "app.py"))

    print("Building...")
    print(f"  Command: {' '.join(cmd[:6])}...")
    subprocess.run(cmd, check=True)

    # Copy HTML files to dist (PyInstaller sometimes misses them)
    dist_dir = DIST / "mnemosyne"
    for f in DATA_FILES:
        src = ROOT / f
        dst = dist_dir / f
        if src.exists() and not dst.exists():
            shutil.copy2(src, dst)

    print(f"\nBuild complete: {dist_dir}")
    print(f"Run: {dist_dir / 'mnemosyne.exe'}")

    # Show size
    total = sum(f.stat().st_size for f in dist_dir.rglob("*") if f.is_file())
    print(f"Total size: {total / 1024 / 1024:.1f} MB")


if __name__ == "__main__":
    if "--clean" in sys.argv:
        clean()
    build()
