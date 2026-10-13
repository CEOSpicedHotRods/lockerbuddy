#!/usr/bin/env python3
"""
build_release.py

Create a release ZIP for LockerBuddy in one step.

Behavior:
- If a `release/` directory exists in the repo root, the script zips everything inside that directory (preserving relative paths).
- Otherwise the script collects a sensible default set of files (see DEFAULT_FILES) and zips the ones that exist.

Usage:
  python3 scripts/build_release.py            -> creates LockerBuddy-Standalone-v1.zip
  python3 scripts/build_release.py 1.2       -> creates LockerBuddy-Standalone-v1.2.zip
  python3 scripts/build_release.py 1.2 out.zip -> creates out.zip

Run this from the repo root. The resulting ZIP will be created in the current working directory.

This is intentionally simple so you (or your build automation) can produce the exact ZIP that you'll upload to Gumroad.
"""

import sys
import os
import zipfile
from pathlib import Path

DEFAULT_FILES = [
    "lockerbuddy-standalone.html",
    "LockerBuddy-Standalone.html",
    "README.md",
    "GUMROAD-README.md",
    "README.txt",
    "LICENSE",
    "LICENSE.txt",
    "icon-192.png",
    "icon-512.png",
    "apple-touch-icon.png",
]


def collect_files_from_release_dir(release_dir: Path):
    files = []
    for p in sorted(release_dir.rglob("*")):
        if p.is_file():
            # store relative path inside the zip
            rel = p.relative_to(release_dir)
            files.append((p, str(rel)))
    return files


def collect_default_files(repo_root: Path):
    files = []
    for name in DEFAULT_FILES:
        p = repo_root / name
        if p.exists() and p.is_file():
            # use the base filename in the zip root
            files.append((p, p.name))
    return files


def make_zip(out_path: Path, files):
    with zipfile.ZipFile(out_path, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for src_path, arcname in files:
            print(f"Adding {src_path} as {arcname}")
            z.write(src_path, arcname)
    print(f"Created {out_path} ({out_path.stat().st_size} bytes)")


def main(argv):
    repo_root = Path.cwd()
    version = argv[1] if len(argv) > 1 else "1"
    out_name = argv[2] if len(argv) > 2 else f"LockerBuddy-Standalone-v{version}.zip"
    out_path = repo_root / out_name

    release_dir = repo_root / "release"
    if release_dir.exists() and release_dir.is_dir():
        print("Found release/ directory — packaging its contents.")
        files = collect_files_from_release_dir(release_dir)
        if not files:
            print("release/ is empty — aborting.")
            sys.exit(1)
    else:
        print("No release/ directory — using default file list.")
        files = collect_default_files(repo_root)
        if not files:
            print("No files found to include in the release. Please put files in a release/ folder or update DEFAULT_FILES in this script.")
            sys.exit(1)

    make_zip(out_path, files)


if __name__ == "__main__":
    main(sys.argv)
