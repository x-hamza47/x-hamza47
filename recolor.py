"""
Recolors your purple SVGs to dark blackish maroon.

Usage: put this file in your profile repo (next to the assets/ folder), then run:
    python recolor.py
Original files are backed up as <name>.svg.bak before changes.
"""
import re, shutil
from pathlib import Path

MAP = {
    "#0a0014": "#0a0508",  # near-black background
    "#150029": "#1a0710",  # dark gradient end
    "#1a0533": "#240a13",  # dark panel
    "#3b0764": "#3d0b18",  # dark border
    "#4c1d95": "#4a0e1e",
    "#5b21b6": "#5a0c1f",
    "#6d28d9": "#6b0f25",  # deep maroon
    "#7c3aed": "#7d1230",  # maroon
    "#8b5cf6": "#8f1a3a",
    "#a855f7": "#a3203f",  # main accent (royal maroon)
    "#c084fc": "#d4506e",  # light accent / glow
    "#d8b4fe": "#e58aa0",
    "#e9d5ff": "#f2c4d0",
}

found_other = set()
for svg in Path("assets").glob("*.svg"):
    text = svg.read_text(encoding="utf-8")
    new = text
    for old, repl in MAP.items():
        new = re.sub(re.escape(old), repl, new, flags=re.I)
    for h in re.findall(r"#[0-9a-fA-F]{6}\b", new):
        if h.lower() not in {v for v in MAP.values()}:
            found_other.add((svg.name, h.lower()))
    if new != text:
        shutil.copy(svg, str(svg) + ".bak")
        svg.write_text(new, encoding="utf-8")
        print("recolored", svg.name)
    else:
        print("no changes", svg.name)

keep = {"#c9d1d9", "#4ade80", "#ffffff", "#fff"}
leftover = sorted(x for x in found_other if x[1] not in keep)
if leftover:
    print("\nOther colors still in your SVGs (check if any look purple/blue):")
    for name, h in leftover:
        print(" ", name, h)
