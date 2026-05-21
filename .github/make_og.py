#!/usr/bin/env python3
"""Regenerate the Council social-preview cards.

Background + wordmark are rendered via SVG (rsvg-convert); the Clawd mascot
(clawd.png, already transparent with its own cream outline) is composited on the
right with a soft drop shadow. Outputs clawd-crimson.png and clawd-purple.png.

Requirements: rsvg-convert (librsvg) and Pillow.
    python3 .github/make_og.py
"""
import subprocess
import tempfile
from pathlib import Path
from PIL import Image, ImageFilter

HERE = Path(__file__).resolve().parent
MASCOT = HERE / "clawd.png"

CREAM = "#f4f1e8"
TARGET_W = 480              # mascot width on the card
RIGHT_EDGE = 1205           # mascot right edge x
CENTER_Y = 322              # mascot vertical center

VARIANTS = {
    "clawd-crimson": "#9b1c31",
    "clawd-purple":  "#5b2a86",
}


def build_svg(bg):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="640" viewBox="0 0 1280 640">
  <rect width="1280" height="640" fill="{bg}"/>
  <rect x="40" y="40" width="1200" height="560" fill="none" stroke="#ffffff" stroke-opacity="0.10" stroke-width="1"/>
  <text x="88" y="150" font-family="Menlo, monospace" font-size="20" letter-spacing="5" fill="#ffffff" fill-opacity="0.62" xml:space="preserve">CLAUDE  CODE  ·  AGENT  SKILL</text>
  <text x="84" y="300" font-family="Helvetica Neue, Helvetica, Arial, sans-serif" font-weight="700" font-size="150" letter-spacing="-3" fill="{CREAM}">Council</text>
  <rect x="92" y="336" width="190" height="4" fill="{CREAM}"/>
  <text x="90" y="404" font-family="Helvetica Neue, Helvetica, Arial, sans-serif" font-size="32" fill="#ffffff" fill-opacity="0.82">Pressure-test any decision —</text>
  <text x="90" y="446" font-family="Helvetica Neue, Helvetica, Arial, sans-serif" font-size="32" fill="#ffffff" fill-opacity="0.82">five advisors, one verdict.</text>
  <text x="90" y="560" font-family="Menlo, monospace" font-size="20" letter-spacing="1" fill="#ffffff" fill-opacity="0.45">github.com/unhingged/council</text>
</svg>'''


# prepare the mascot once: trim transparent margins, scale to TARGET_W
m = Image.open(MASCOT).convert("RGBA")
m = m.crop(m.getbbox())
m = m.resize((TARGET_W, round(m.height * TARGET_W / m.width)), Image.LANCZOS)
mx = RIGHT_EDGE - m.width
my = CENTER_Y - m.height // 2

# soft drop shadow from the alpha channel
shadow = Image.new("RGBA", m.size, (0, 0, 0, 0))
shadow.putalpha(m.split()[3].point(lambda a: 110 if a > 40 else 0))
shadow = shadow.filter(ImageFilter.GaussianBlur(7))

for name, bg in VARIANTS.items():
    with tempfile.TemporaryDirectory() as tmp:
        svg_path = Path(tmp) / "card.svg"
        base_png = Path(tmp) / "base.png"
        svg_path.write_text(build_svg(bg))
        subprocess.run(["rsvg-convert", "-w", "1280", "-h", "640", str(svg_path), "-o", str(base_png)], check=True)
        card = Image.open(base_png).convert("RGBA")
    card.alpha_composite(shadow, (mx + 8, my + 12))
    card.alpha_composite(m, (mx, my))
    out = HERE / f"{name}.png"
    card.convert("RGB").save(out)
    print(f"wrote {out}")
