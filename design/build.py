"""Builds the images the profile README uses.

    python design/build.py

Writes to assets/:

- header-*.svg and button-*.svg, a light and a dark version of each; the README picks one with <picture>.
  They are SVG with live text on a clear background, so they stay sharp at any size and sit on whichever
  theme GitHub shows.
- shot-*.png, close-ups cut from the screenshots in design/shots.

The colours are GitHub's own greys and its blue, so the images read as part of the page.

capture() and find_chrome() are for site.py, which draws the link preview image with a headless browser.
"""
from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
DESIGN = ROOT / "design"
SHOTS = DESIGN / "shots"
ICONS = DESIGN / "icons"
ASSETS = ROOT / "assets"
TMP = DESIGN / ".tmp"


def find_chrome() -> str:
    """A Chromium browser for the capture: CHROME_PATH, then PATH, then the usual install folders."""
    candidates = [os.environ.get("CHROME_PATH")]
    candidates += [shutil.which(n) for n in ("chrome", "msedge", "google-chrome", "chromium", "chromium-browser")]
    for base in (os.environ.get("PROGRAMFILES"), os.environ.get("PROGRAMFILES(X86)"), os.environ.get("LOCALAPPDATA")):
        if base:
            candidates += [str(Path(base) / "Google/Chrome/Application/chrome.exe"),
                           str(Path(base) / "Microsoft/Edge/Application/msedge.exe")]
    for c in candidates:
        if c and Path(c).is_file():
            return c
    raise SystemExit("No Chrome or Edge found. Set CHROME_PATH to a Chromium browser.")


SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif"

# GitHub's light and dark colours: text, secondary text, borders, links, the blue button.
THEMES = {
    "dark": dict(fg="#f0f6fc", muted="#9198a1", line="#3d444d", accent="#4493f8", button="#1f6feb", page="#0d1117"),
    "light": dict(fg="#1f2328", muted="#59636e", line="#d1d9e0", accent="#0969da", button="#0969da", page="#ffffff"),
}

# The width GitHub gives an image in a profile README on a desktop screen. Images made this wide are drawn
# one to one there.
WIDTH = 846


# --------------------------------------------------------------------------
# Header
# --------------------------------------------------------------------------
def header(t: dict) -> str:
    w, h = WIDTH, 112
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="Rotem Grinhut. Full-stack developer and system designer. Currently looking for opportunities. Israel. Hebrew and English.">
<style>
  text {{ font-family: {SANS}; }}
  .name {{ font-size: 40px; font-weight: 600; letter-spacing: -0.8px; fill: {t["fg"]}; }}
  .role {{ font-size: 18px; fill: {t["muted"]}; }}
  .meta {{ font-size: 14px; fill: {t["muted"]}; }}
  .open {{ font-weight: 600; fill: {t["fg"]}; }}
</style>
<text x="0" y="42" class="name">Rotem Grinhut</text>
<text x="1" y="72" class="role">Full-stack developer and system designer</text>
<circle cx="6" cy="97" r="4" fill="{t["accent"]}"/>
<text x="18" y="102" class="meta"><tspan class="open">Currently looking for opportunities</tspan><tspan dx="12">Israel</tspan><tspan dx="12">Hebrew and English</tspan></text>
</svg>
'''


# --------------------------------------------------------------------------
# Buttons
# --------------------------------------------------------------------------
# The label width is the label in Segoe UI Semibold at 14 px plus 6%. It is written down here, not measured,
# so the files come out the same on every PC. It only sizes the box: the label is drawn in the viewer's own
# font, unstretched, and the 14 px of padding on each side takes up a wider or narrower one.
BUTTONS = [
    # file name, label, label width, icon, filled
    ("portfolio", "Portfolio", 59, None, True),
    ("linkedin", "LinkedIn", 57, "linkedin", False),
    ("x", "X", 9, "x", False),
]


def icon_path(slug: str) -> str:
    """The path data of a Simple Icons file in design/icons."""
    svg = (ICONS / f"{slug}.svg").read_text(encoding="utf-8")
    return svg.split(' d="', 1)[1].split('"', 1)[0]


def button(t: dict, label: str, tw: int, icon: str | None, filled: bool) -> str:
    h, pad = 32, 14
    w = pad + (16 + 8 if icon else 0) + tw + pad
    ink = "#ffffff" if filled else t["fg"]
    box = (f'<rect width="{w}" height="{h}" rx="6" fill="{t["button"]}"/>' if filled else
           f'<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="6" fill="none" stroke="{t["line"]}"/>')
    mark = ""
    if icon:
        mark = f'<path transform="translate({pad} 8) scale({16 / 24:.4f})" fill="{t["muted"]}" d="{icon_path(icon)}"/>'
    # without an icon the label is centred; with one it starts after the icon
    at = f'x="{pad + 24}"' if icon else f'x="{w / 2}" text-anchor="middle"'
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{label}">
{box}{mark}
<text {at} y="21" font-family="{SANS}" font-size="14" font-weight="600" fill="{ink}">{label}</text>
</svg>
'''


# --------------------------------------------------------------------------
# Screenshots
# --------------------------------------------------------------------------
# Each image is a close-up, so the text in it is the size it has in the app. An image is (file, scale, width,
# height, panels) and a panel is (screenshot, box, x, y, w, h, radius): the part `box` of the screenshot, drawn
# w x h at (x, y). Sizes are in README pixels and the PNG has `scale` times as many.
#
# At scale 1 a box is the size of its panel, so the screenshot's own pixels reach a 1x screen untouched. The
# GymBro and status bar captures were taken at a higher density, so those images are scale 2: one to one on a
# 2x screen and an even halving on a 1x screen.
README_SHOTS = [
    ("shot-inwire.png", 1, WIDTH, 420, [
        ("inwire-capture.png", (341, 559, 1187, 979), 0, 0, 846, 420, 8)]),
    ("shot-gymbro.png", 2, WIDTH, 556, [
        ("gymbro-windows-calendar.png", (683, 203, 1843, 1315), 0, 0, 580, 556, 8),
        ("gymbro-android-booking.png", (0, 0, 1080, 2400), 596, 0, 250, 556, 16)]),
    ("shot-marshell.png", 1, WIDTH, 440, [
        ("marshell-approval.png", (0, 0, 846, 440), 0, 0, 846, 440, 8)]),
    ("shot-claude-setup.png", 1, WIDTH, 390, [
        ("claude-setup-session-cards.png", (0, 0, 846, 390), 0, 0, 846, 390, 8)]),
    # 1506 is in the gap after the context meter, so the bar ends between two elements
    ("shot-claude-setup-bar.png", 2, 753, 47, [
        ("claude-setup-statusbar.png", (0, 0, 1506, 94), 0, 0, 753, 47, 6)]),
]

EDGE = (128, 136, 148, 115)  # a hairline that shows on a light page and on a dark one


def framed(im: Image.Image, radius: int, line: int) -> Image.Image:
    """Rounds the corners of a screenshot and draws a hairline around it. Both are drawn at four times the
    size and scaled down, which smooths the curves."""
    w, h = im.size
    big = (w * 4, h * 4)
    box = (0, 0, big[0] - 1, big[1] - 1)
    mask = Image.new("L", big, 0)
    ImageDraw.Draw(mask).rounded_rectangle(box, radius * 4, fill=255)
    edge = Image.new("RGBA", big, (0, 0, 0, 0))
    ImageDraw.Draw(edge).rounded_rectangle(box, radius * 4, outline=EDGE, width=line * 4)
    out = Image.alpha_composite(im.convert("RGBA"), edge.resize((w, h), Image.LANCZOS))
    out.putalpha(ImageChops.multiply(out.getchannel("A"), mask.resize((w, h), Image.LANCZOS)))
    return out


def readme_shot(scale: int, width: int, height: int, panels: list) -> Image.Image:
    sheet = Image.new("RGBA", (width * scale, height * scale), (0, 0, 0, 0))
    for name, box, x, y, w, h, radius in panels:
        with Image.open(SHOTS / name) as im:
            if box[2] > im.width or box[3] > im.height:
                raise SystemExit(f"{name}: the box {box} is outside the {im.width} x {im.height} screenshot")
            part = im.convert("RGB").crop(box)
        size = (w * scale, h * scale)
        if part.size != size:
            part = part.resize(size, Image.LANCZOS)
        sheet.alpha_composite(framed(part, radius * scale, scale), (x * scale, y * scale))
    return sheet


# --------------------------------------------------------------------------
# Used by site.py
# --------------------------------------------------------------------------
def capture(html: Path, png: Path, w: int, h: int, scale: int = 2) -> None:
    png.unlink(missing_ok=True)  # an older capture must not pass for this one
    result = subprocess.run(
        [find_chrome(), "--headless=new", "--disable-gpu", "--hide-scrollbars", "--default-background-color=00000000",
         f"--force-device-scale-factor={scale}", f"--window-size={w},{h}", f"--screenshot={png}", html.as_uri()],
        capture_output=True, text=True,
    )
    if result.returncode or not png.is_file():
        raise SystemExit(f"The browser could not capture {html.name}: {result.stderr.strip()}")
    with Image.open(png) as im:
        if im.size != (w * scale, h * scale):
            raise SystemExit(f"{png.name} came out {im.size[0]} x {im.size[1]}, expected {w * scale} x {h * scale}")


def optimise(png: Path, rgb: bool = False) -> None:
    """Rewrites a PNG smaller. The image is read fully and closed before the same path is written."""
    with Image.open(png) as im:
        im.load()
        copy = im.convert("RGB") if rgb else im.copy()
    copy.save(png, optimize=True)


def main() -> None:
    ASSETS.mkdir(exist_ok=True)
    for theme, t in THEMES.items():
        (ASSETS / f"header-{theme}.svg").write_text(header(t), encoding="utf-8", newline="\n")
        for slug, label, tw, icon, filled in BUTTONS:
            (ASSETS / f"button-{slug}-{theme}.svg").write_text(button(t, label, tw, icon, filled), encoding="utf-8", newline="\n")
    for name, scale, width, height, panels in README_SHOTS:
        readme_shot(scale, width, height, panels).save(ASSETS / name, optimize=True)
        print(name, (ASSETS / name).stat().st_size // 1024, "KB")


if __name__ == "__main__":
    main()
