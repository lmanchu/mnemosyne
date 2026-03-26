"""Build Mnemosyne into a distributable package.

Usage:
  python build.py          # build exe
  python build.py --clean  # clean build artifacts first
"""

import os
import sys
import subprocess
import shutil
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).parent
DIST = ROOT / "dist"
BUILD = ROOT / "build"

VERSION = os.environ.get("MNEMOSYNE_BUILD_VERSION", "0.6.0")
DATE_CODE = datetime.now().strftime("%Y%m%d")

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

    # Write version file
    (dist_dir / "VERSION").write_text(f"{VERSION}\n{DATE_CODE}\n")

    print(f"\nBuild complete: {dist_dir}")
    print(f"Version: v{VERSION} ({DATE_CODE})")
    print(f"Run: {dist_dir / 'mnemosyne.exe'}")

    # Show size
    total = sum(f.stat().st_size for f in dist_dir.rglob("*") if f.is_file())
    print(f"Total size: {total / 1024 / 1024:.1f} MB")

    # Create zip with version + date code
    zip_name = f"mnemosyne-v{VERSION}-{DATE_CODE}-windows-x64.zip"
    zip_path = DIST / zip_name
    if zip_path.exists():
        zip_path.unlink()
    import zipfile
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for f in dist_dir.rglob("*"):
            if f.is_file():
                zf.write(f, f"mnemosyne/{f.relative_to(dist_dir)}")
    print(f"Zip: {zip_path} ({zip_path.stat().st_size / 1024 / 1024:.1f} MB)")


if __name__ == "__main__":
    if "--clean" in sys.argv:
        clean()
    build()
