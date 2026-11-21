"""Builds the images the profile README uses.

    python design/build.py

Writes assets/*.svg (banner, stack panel, buttons) and assets/*.png (project
cards, drawn as HTML and captured with headless Chrome at 2x). Every image has a
light and a dark version; the README picks one with <picture>.
"""
from __future__ import annotations

import base64
import re
import subprocess
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
DESIGN = ROOT / "design"
SHOTS = DESIGN / "shots"
ICONS = DESIGN / "icons"
ASSETS = ROOT / "assets"
TMP = DESIGN / ".tmp"
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

MONO = "ui-monospace, SFMono-Regular, 'SF Mono', 'Cascadia Mono', Menlo, Consolas, 'Liberation Mono', monospace"
SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif"

THEMES = {
    "dark": dict(
        bg="#0b1a30", bg2="#0f2342", grid="#7eaaff", grid_o="0.07", grid2_o="0.13",
        line="#2c4f82", ink="#8fbaff", text="#eaf2ff", muted="#9fb6d8",
        accent="#ffb454", chip="#112a4d", on_ink="#0b1a30",
    ),
    "light": dict(
        bg="#f6f9fd", bg2="#eaf1fb", grid="#1f4e9c", grid_o="0.06", grid2_o="0.11",
        line="#b5c8e6", ink="#1f4e9c", text="#0c2340", muted="#4c6183",
        accent="#b8430b", chip="#e6eefa", on_ink="#f6f9fd",
    ),
}


# --------------------------------------------------------------------------
# Banner
# --------------------------------------------------------------------------
def banner(t: dict) -> str:
    w, h = 880, 320
    cells = [
        ("BASED IN", "Israel"),
        ("LANGUAGES", "Hebrew, English"),
        ("BUILDS", "Desktop and web apps"),
        ("WITH", "TypeScript, React, Rust"),
    ]
    cell_w = (w - 28) / 4
    block = ""
    for i, (label, value) in enumerate(cells):
        x = 14 + i * cell_w
        if i:
            block += f'<line x1="{x:.1f}" y1="240" x2="{x:.1f}" y2="306" class="frame"/>'
        block += (
            f'<text x="{x + 16:.1f}" y="264" class="label">{label}</text>'
            f'<text x="{x + 16:.1f}" y="288" class="value">{value}</text>'
        )

    boxes = [
        (462, 112, "INTERFACE", ["React", "TypeScript", "Kotlin"]),
        (598, 126, "SERVICES", ["TypeScript APIs", "Rust services"]),
        (748, 96, "DATA", ["PostgreSQL", "SQLite"]),
    ]
    diagram = ""
    for x, bw, label, lines in boxes:
        diagram += f'<rect x="{x}" y="84" width="{bw}" height="86" rx="4" class="box"/>'
        diagram += f'<text x="{x + 12}" y="104" class="label">{label}</text>'
        diagram += f'<line x1="{x}" y1="113" x2="{x + bw}" y2="113" class="frame"/>'
        for j, line in enumerate(lines):
            diagram += f'<text x="{x + 12}" y="{132 + j * 16}" class="node">{line}</text>'
    for x1, x2 in ((574, 598), (724, 748)):
        diagram += f'<line x1="{x1}" y1="127" x2="{x2}" y2="127" class="flow"/>'
        diagram += f'<path d="M{x2 - 5} 123 L{x2} 127 L{x2 - 5} 131" class="arrow"/>'
    # dimension line under the diagram
    diagram += (
        '<line x1="462" y1="196" x2="844" y2="196" class="dim"/>'
        '<line x1="462" y1="190" x2="462" y2="202" class="dim"/>'
        '<line x1="844" y1="190" x2="844" y2="202" class="dim"/>'
        f'<rect x="563" y="187" width="180" height="18" fill="{t["bg"]}"/>'
        '<text x="653" y="200" text-anchor="middle" class="label">FIG. 1  WHAT I BUILD</text>'
    )

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-labelledby="t d">
<title id="t">Rotem Grinhut: full-stack developer and system designer, currently looking for opportunities</title>
<desc id="d">A drawing sheet with a title block. Based in Israel. Languages: Hebrew, English. Builds desktop and web apps with TypeScript, React and Rust. Figure 1 shows the three layers he builds: interface, services and data.</desc>
<style>
  .frame {{ stroke: {t["line"]}; stroke-width: 1; fill: none; }}
  .box {{ stroke: {t["ink"]}; stroke-width: 1.2; fill: {t["bg2"]}; }}
  .label {{ font: 600 10.5px {MONO}; letter-spacing: 1.4px; fill: {t["muted"]}; }}
  .value {{ font: 600 15px {SANS}; fill: {t["text"]}; }}
  .node {{ font: 12px {MONO}; fill: {t["text"]}; }}
  .name {{ font: 700 48px {SANS}; letter-spacing: -0.5px; fill: {t["text"]}; }}
  .role {{ font: 600 14.5px {MONO}; letter-spacing: 1.2px; fill: {t["ink"]}; }}
  .status {{ font: 700 12.5px {MONO}; letter-spacing: 1.1px; fill: {t["accent"]}; }}
  .dim {{ stroke: {t["muted"]}; stroke-width: 1; }}
  .arrow {{ stroke: {t["ink"]}; stroke-width: 1.4; fill: none; }}
  .flow {{ stroke: {t["ink"]}; stroke-width: 1.4; stroke-dasharray: 4 4; animation: flow 1s linear infinite; }}
  .pulse {{ fill: none; stroke: {t["accent"]}; stroke-width: 1.5; transform-origin: 62px 204px; animation: pulse 2.4s ease-out infinite; }}
  @keyframes flow {{ to {{ stroke-dashoffset: -8; }} }}
  @keyframes pulse {{ 0% {{ transform: scale(1); opacity: .9; }} 70%, 100% {{ transform: scale(2.6); opacity: 0; }} }}
  @media (prefers-reduced-motion: reduce) {{ .flow, .pulse {{ animation: none; }} .pulse {{ opacity: 0; }} }}
</style>
<defs>
  <pattern id="g1" width="20" height="20" patternUnits="userSpaceOnUse">
    <path d="M20 0H0V20" fill="none" stroke="{t["grid"]}" stroke-opacity="{t["grid_o"]}" stroke-width="1"/>
  </pattern>
  <pattern id="g2" width="100" height="100" patternUnits="userSpaceOnUse">
    <path d="M100 0H0V100" fill="none" stroke="{t["grid"]}" stroke-opacity="{t["grid2_o"]}" stroke-width="1"/>
  </pattern>
  <clipPath id="clip"><rect width="{w}" height="{h}" rx="12"/></clipPath>
</defs>
<g clip-path="url(#clip)">
  <rect width="{w}" height="{h}" fill="{t["bg"]}"/>
  <rect width="{w}" height="{h}" fill="url(#g1)"/>
  <rect width="{w}" height="{h}" fill="url(#g2)"/>
</g>
<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="12" class="frame"/>
<rect x="14" y="14" width="{w - 28}" height="{h - 28}" rx="3" class="frame"/>
<line x1="14" y1="240" x2="{w - 14}" y2="240" class="frame"/>
<text x="38" y="52" class="label">SHEET 01  /  PROFILE</text>
<text x="842" y="52" text-anchor="end" class="label">GITHUB.COM/DOOFESS</text>
<text x="36" y="122" class="name">Rotem Grinhut</text>
<text x="38" y="156" class="role">FULL-STACK DEVELOPER  /  SYSTEM DESIGNER</text>
<rect x="38" y="186" width="366" height="36" rx="18" fill="{t["bg2"]}" stroke="{t["accent"]}" stroke-width="1.2"/>
<circle cx="62" cy="204" r="5" class="pulse"/>
<circle cx="62" cy="204" r="5" fill="{t["accent"]}"/>
<text x="80" y="208.5" class="status">CURRENTLY LOOKING FOR OPPORTUNITIES</text>
{diagram}
{block}
</svg>
'''


# --------------------------------------------------------------------------
# Stack panel
# --------------------------------------------------------------------------
STACK = [
    ("INTERFACE", [("react", "React"), ("typescript", "TypeScript"), ("vite", "Vite"), ("tailwindcss", "Tailwind CSS")]),
    ("DESKTOP AND MOBILE", [("electron", "Electron"), ("tauri", "Tauri 2"), ("kotlin", "Kotlin"), ("jetpackcompose", "Compose")]),
    ("SERVICES AND DATA", [("rust", "Rust"), ("nodedotjs", "Node.js"), ("postgresql", "PostgreSQL"), ("supabase", "Supabase"), ("sqlite", "SQLite")]),
    ("TOOLING", [("githubactions", "Actions"), ("vitest", "Vitest"), ("playwright", "Playwright"), ("python", "Python"), ("powershell", "PowerShell")]),
]


def icon_path(slug: str) -> str:
    svg = (ICONS / f"{slug}.svg").read_text(encoding="utf-8")
    return re.search(r'<path d="([^"]+)"', svg).group(1)


def stack(t: dict) -> str:
    w, h = 880, 252
    col_w, row_h = 440, 126
    out = ""
    for i, (title, items) in enumerate(STACK):
        gx, gy = (i % 2) * col_w, (i // 2) * row_h
        out += f'<text x="{gx + 28}" y="{gy + 34}" class="label">{title}</text>'
        cell = 80
        for j, (slug, name) in enumerate(items):
            cx = gx + 28 + j * cell + 28
            out += (
                f'<g transform="translate({cx - 14} {gy + 50}) scale({28 / 24:.4f})">'
                f'<path d="{icon_path(slug)}" fill="{t["ink"]}"/></g>'
                f'<text x="{cx}" y="{gy + 100}" text-anchor="middle" class="name">{name}</text>'
            )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-labelledby="t">
<title id="t">What I build with. Interface: React, TypeScript, Vite, Tailwind CSS. Desktop and mobile: Electron, Tauri 2, Kotlin, Jetpack Compose. Services and data: Rust, Node.js, PostgreSQL, Supabase, SQLite. Tooling: GitHub Actions, Vitest, Playwright, Python, PowerShell.</title>
<style>
  .frame {{ stroke: {t["line"]}; stroke-width: 1; fill: none; }}
  .label {{ font: 600 10.5px {MONO}; letter-spacing: 1.4px; fill: {t["muted"]}; }}
  .name {{ font: 11.5px {MONO}; fill: {t["text"]}; }}
</style>
<defs>
  <pattern id="g1" width="20" height="20" patternUnits="userSpaceOnUse">
    <path d="M20 0H0V20" fill="none" stroke="{t["grid"]}" stroke-opacity="{t["grid_o"]}" stroke-width="1"/>
  </pattern>
  <clipPath id="clip"><rect width="{w}" height="{h}" rx="12"/></clipPath>
</defs>
<g clip-path="url(#clip)">
  <rect width="{w}" height="{h}" fill="{t["bg"]}"/>
  <rect width="{w}" height="{h}" fill="url(#g1)"/>
</g>
<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="12" class="frame"/>
<line x1="{col_w}" y1="0" x2="{col_w}" y2="{h}" class="frame"/>
<line x1="0" y1="{row_h}" x2="{w}" y2="{row_h}" class="frame"/>
{out}
</svg>
'''


# --------------------------------------------------------------------------
# Buttons
# --------------------------------------------------------------------------
BUTTONS = [
    ("portfolio", "PORTFOLIO PAGE", None, True),
    ("linkedin", "LINKEDIN", "linkedin", False),
    ("x", "X", "x", False),
]


def button(t: dict, label: str, icon: str | None, primary: bool) -> str:
    text_w = len(label) * 8.6
    icon_w = 24 if icon else 0
    w = round(18 + icon_w + text_w + 34)
    h = 38
    fg = t["on_ink"] if primary else t["ink"]
    fill = t["ink"] if primary else t["bg"]
    x = 18
    body = ""
    if icon:
        body += f'<g transform="translate({x} 11.5) scale({15 / 24:.4f})"><path d="{icon_path(icon)}" fill="{fg}"/></g>'
        x += icon_w
    body += f'<text x="{x}" y="23.5" style="font: 700 12.5px {MONO}; letter-spacing: 1.1px; fill: {fg}">{label}</text>'
    ax = w - 24
    body += f'<path d="M{ax} 23 L{ax + 8} 15 M{ax + 2} 15 H{ax + 8} V21" fill="none" stroke="{fg}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>'
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{label.title()}">
<rect x="0.75" y="0.75" width="{w - 1.5}" height="{h - 1.5}" rx="6" fill="{fill}" stroke="{t["ink"]}" stroke-width="1.5"/>
{body}
</svg>
'''


# --------------------------------------------------------------------------
# Project cards (HTML, captured by Chrome)
# --------------------------------------------------------------------------
PROJECTS = [
    dict(
        id="inwire", no="01", name="Inwire", logo="inwire-logo.svg",
        tagline="Desktop packet analyzer for Windows",
        status="V0.5.0 / WINDOWS",
        fig="LIVE CAPTURE",
        shots=[("inwire-capture.png", "main")],
        metrics=[("≈ 100", "protocols decoded"), ("≈ 85,000", "frames a second in replay"),
                 ("74", "decision records"), ("365", "assertion scripts")],
        stack=["Electron", "React", "TypeScript", "Rust"],
    ),
    dict(
        id="gymbro", no="02", name="GymBro", logo=None,
        tagline="Appointment booking system for gyms, Hebrew first",
        status="STAGING / SOURCE PRIVATE",
        fig="STAFF CALENDAR AND MEMBER APP",
        shots=[("gymbro-windows-calendar.png", "main"), ("gymbro-android-calendar.png", "phone")],
        metrics=[("9", "roles"), ("38", "permission grants"),
                 ("≈ 4,740", "Vitest cases in CI"), ("12", "TypeScript projects")],
        stack=["TypeScript", "Kotlin", "PostgreSQL", "Electron", "React"],
    ),
    dict(
        id="marshell", no="03", name="Marshell", logo="marshell-icon.svg",
        tagline="Windows app for AI coding-agent CLIs from any vendor",
        status="ALPHA / WINDOWS 11",
        fig="AN AGENT ASKS, A CARD ANSWERS",
        shots=[("marshell-approval.png", "main")],
        metrics=[("13.8 MB", "installer"), ("2,955", "Rust tests"),
                 ("≈ 4,500", "Vitest cases"), ("188", "generated protocol types")],
        stack=["Tauri 2", "Rust", "React", "TypeScript"],
    ),
    dict(
        id="claude-setup", no="04", name="claude-setup", logo=None,
        tagline="My Claude Code setup, kept as code",
        status="WINDOWS",
        fig="SESSION VIEW AND STATUS BAR",
        shots=[("claude-setup-session-cards.png", "top"), ("claude-setup-statusbar-crop.png", "strip")],
        metrics=[("374", "Python tests"), ("91", "test cases for the view mod"),
                 ("553", "lines in the merge gate"), ("14", "unittest files")],
        stack=["Python", "PowerShell", "TypeScript"],
    ),
]

CARD_W, CARD_H = 880, 344

CARD_CSS = """
* { box-sizing: border-box; margin: 0; }
html, body { width: %(w)dpx; height: %(h)dpx; background: transparent; overflow: hidden; }
.card {
  width: %(w)dpx; height: %(h)dpx; border-radius: 12px; border: 1px solid %(line)s;
  background-color: %(bg)s;
  background-image:
    linear-gradient(%(gridc)s 1px, transparent 1px), linear-gradient(90deg, %(gridc)s 1px, transparent 1px);
  background-size: 20px 20px; background-position: -1px -1px;
  display: grid; grid-template-columns: 516px 1fr; overflow: hidden;
  font-family: 'Segoe UI', sans-serif; color: %(text)s;
}
.mono { font-family: 'Cascadia Mono', Consolas, monospace; }
.left { padding: 22px 0 0 22px; position: relative; }
.stage { position: relative; width: 476px; height: 278px; }
.win { position: absolute; border: 1px solid %(ink)s; border-radius: 6px; overflow: hidden; background: #000;
       box-shadow: 0 10px 30px %(shadow)s; }
.win img { display: block; width: 100%%; height: 100%%; object-fit: cover; object-position: left top; }
.main { inset: 0; }
.top { left: 0; top: 0; width: 476px; height: 226px; }
.strip { left: 0; bottom: 0; width: 476px; height: 39px; border-radius: 4px; }
.gym .main { left: 0; top: 0; width: 418px; height: 262px; inset: auto; }
.phone { right: 0; bottom: 0; width: 112px; height: 249px; border-radius: 12px; border-width: 2px; }
.fig { margin-top: 14px; display: flex; align-items: center; gap: 8px; font-size: 10px; letter-spacing: 1.4px;
       font-weight: 600; color: %(muted)s; width: 476px; }
.fig i { flex: 1; height: 1px; background: %(muted)s; opacity: .55; position: relative; }
.fig i::before, .fig i::after { content: ''; position: absolute; top: -4px; width: 1px; height: 9px; background: %(muted)s; }
.fig i::before { left: 0; } .fig i::after { right: 0; }
.right { padding: 24px 26px 22px 26px; display: flex; flex-direction: column; border-left: 1px solid %(line)s;
         margin-left: 18px; background: %(bg)s; }
.head { display: flex; justify-content: space-between; font-size: 10px; letter-spacing: 1.4px; font-weight: 600; color: %(muted)s; }
.head b { color: %(accent)s; font-weight: 700; }
.title { display: flex; align-items: center; gap: 12px; margin-top: 18px; }
.title img { width: 34px; height: 34px; }
.title h1 { font-size: 30px; line-height: 34px; font-weight: 700; letter-spacing: -0.4px; }
.tag { margin-top: 8px; font-size: 14.5px; line-height: 20px; color: %(muted)s; min-height: 40px; }
.metrics { margin-top: 14px; display: grid; grid-template-columns: 1fr 1fr; gap: 12px 14px; }
.metrics div { border-left: 2px solid %(ink)s; padding-left: 10px; }
.metrics strong { display: block; font-size: 20px; line-height: 24px; font-weight: 600; color: %(text)s; }
.metrics span { display: block; font-size: 11.5px; line-height: 15px; color: %(muted)s; }
.chips { margin-top: auto; display: flex; flex-wrap: wrap; gap: 6px; }
.chips span { font-size: 10.5px; line-height: 14px; padding: 3px 8px; border: 1px solid %(line)s; border-radius: 4px;
              background: %(chip)s; color: %(ink)s; font-weight: 600; }
"""


def data_uri(path: Path) -> str:
    mime = {"png": "image/png", "jpg": "image/jpeg", "svg": "image/svg+xml"}[path.suffix[1:]]
    return f"data:{mime};base64,{base64.b64encode(path.read_bytes()).decode()}"


def card_html(p: dict, theme: str) -> str:
    t = THEMES[theme]
    css = CARD_CSS % dict(
        w=CARD_W, h=CARD_H, line=t["line"], bg=t["bg"], text=t["text"], ink=t["ink"], muted=t["muted"],
        accent=t["accent"], chip=t["chip"],
        gridc="rgba(126,170,255,.07)" if theme == "dark" else "rgba(31,78,156,.06)",
        shadow="rgba(0,0,0,.45)" if theme == "dark" else "rgba(12,35,64,.18)",
    )
    shots = "".join(
        f'<div class="win {cls}"><img src="{data_uri(SHOTS / name)}"></div>' for name, cls in p["shots"]
    )
    logo = f'<img src="{data_uri(SHOTS / p["logo"])}">' if p["logo"] else ""
    metrics = "".join(f'<div><strong class="mono">{v}</strong><span>{label}</span></div>' for v, label in p["metrics"])
    chips = "".join(f'<span class="mono">{s}</span>' for s in p["stack"])
    return f"""<!doctype html><meta charset="utf-8"><style>{css}</style>
<div class="card">
  <div class="left">
    <div class="stage {'gym' if p['id'] == 'gymbro' else ''}">{shots}</div>
    <div class="fig mono"><span>FIG. {int(p['no']) + 1}</span><i></i><span>{p['fig']}</span></div>
  </div>
  <div class="right">
    <div class="head mono"><span><b>{p['no']}</b> / 04</span><span>{p['status']}</span></div>
    <div class="title">{logo}<h1>{p['name']}</h1></div>
    <p class="tag">{p['tagline']}</p>
    <div class="metrics">{metrics}</div>
    <div class="chips">{chips}</div>
  </div>
</div>"""


def capture(html: Path, png: Path, w: int, h: int, scale: int = 2) -> None:
    subprocess.run(
        [CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--default-background-color=00000000",
         f"--force-device-scale-factor={scale}", f"--window-size={w},{h}", f"--screenshot={png}", html.as_uri()],
        check=True, capture_output=True,
    )


def prepare_shots() -> None:
    # The status bar is 2880 px wide and 94 px tall: keep its left part so the text stays readable.
    bar = Image.open(SHOTS / "claude-setup-statusbar.png")
    bar.crop((0, 0, 1147, 94)).save(SHOTS / "claude-setup-statusbar-crop.png")


def main() -> None:
    ASSETS.mkdir(exist_ok=True)
    TMP.mkdir(exist_ok=True)
    prepare_shots()
    for theme, t in THEMES.items():
        (ASSETS / f"banner-{theme}.svg").write_text(banner(t), encoding="utf-8", newline="\n")
        (ASSETS / f"stack-{theme}.svg").write_text(stack(t), encoding="utf-8", newline="\n")
        for slug, label, icon, primary in BUTTONS:
            (ASSETS / f"button-{slug}-{theme}.svg").write_text(button(t, label, icon, primary), encoding="utf-8", newline="\n")
        for p in PROJECTS:
            if len(sys.argv) > 1 and p["id"] not in sys.argv[1:]:
                continue
            html = TMP / f"{p['id']}-{theme}.html"
            html.write_text(card_html(p, theme), encoding="utf-8")
            png = ASSETS / f"card-{p['id']}-{theme}.png"
            capture(html, png, CARD_W, CARD_H)
            Image.open(png).save(png, optimize=True)
            print(png.name, png.stat().st_size // 1024, "KB")


if __name__ == "__main__":
    main()
