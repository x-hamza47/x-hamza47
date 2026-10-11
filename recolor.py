"""
Recolors purple SVGs to dark blackish maroon.

Usage: put this file in your profile repo (next to the assets/ folder), then run:
    python recolor.py
Backups are saved as <name>.svg.bak. Running it twice is safe.
Any purple/blue/violet color not in the table below is converted automatically.
"""
import re, shutil, colorsys
from pathlib import Path

MAP = {
    "#08000f": "#080206",  # darkest background
    "#0a0014": "#0a0508",
    "#150029": "#1a0710",
    "#170430": "#1a0710",
    "#1a0533": "#240a13",
    "#3b0764": "#3d0b18",
    "#4c1d95": "#4a0e1e",
    "#5b21b6": "#5a0c1f",
    "#6d28d9": "#6b0f25",
    "#7c3aed": "#7d1230",
    "#8b5cf6": "#8f1a3a",
    "#a855f7": "#a3203f",  # main accent
    "#c084fc": "#d4506e",  # light accent
    "#d8b4fe": "#e58aa0",
    "#e9d5ff": "#f2c4d0",
    "#f3e8ff": "#f8dbe3",
    "#7c7c94": "#8a7a80",  # muted grey text
}
KEEP = {"#c9d1d9", "#4ade80", "#ffffff", "#000000"}

def auto_shift(hexcolor):
    r, g, b = (int(hexcolor[i:i+2], 16) / 255 for i in (1, 3, 5))
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    deg = h * 360
    if s < 0.12 or not (200 <= deg <= 330):
        return hexcolor
    h = 345 / 360
    if l > 0.4:
        l *= 0.72
    s *= 0.85
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return "#%02x%02x%02x" % (round(r*255), round(g*255), round(b*255))

def convert(m):
    c = m.group(0).lower()
    if c in MAP: return MAP[c]
    if c in KEEP: return c
    return auto_shift(c)

for svg in sorted(Path("assets").glob("*.svg")):
    text = svg.read_text(encoding="utf-8")
    new = re.sub(r"#[0-9a-fA-F]{6}\b", convert, text)
    if new != text:
        bak = Path(str(svg) + ".bak")
        if not bak.exists():
            shutil.copy(svg, bak)
        svg.write_text(new, encoding="utf-8")
        print("recolored", svg.name)
    else:
        print("no changes", svg.name)