#!/usr/bin/env python3
"""Regenerate the whole site in the correct order. Run after editing any source
(spreadsheets, literature.md, or the Claywork photos):

    python3 build.py

Steps:
  1. build_data.py       — Science & Visual Art cards + JSON-LD (from spreadsheets)
  2. build_literature.py — story/poem pages + indexes (from literature.md)
  3. build_claywork.py   — Claywork gallery + home teaser (from Images/Claywork)
  4. build_sitemap.py    — sitemap.xml (run last, after all pages exist)
"""
import subprocess, sys, pathlib

ROOT = pathlib.Path(__file__).parent
STEPS = ["build_data.py", "build_literature.py", "build_claywork.py", "build_sitemap.py"]

def main():
    for step in STEPS:
        print(f"\n=== {step} ===")
        r = subprocess.run([sys.executable, str(ROOT / step)])
        if r.returncode != 0:
            sys.exit(f"Failed at {step}")
    print("\nAll generators finished.")

if __name__ == "__main__":
    main()
