"""Builds the portfolio page: docs/index.html and docs/img/.

    python design/site.py

GitHub Pages serves docs/ at https://doofess.github.io/Doofess/.
"""
from __future__ import annotations

import html
import re
import shutil
from pathlib import Path

from PIL import Image

from build import CHROME, DESIGN, ICONS, ROOT, SHOTS, STACK, THEMES, TMP, banner, capture, icon_path

DOCS = ROOT / "docs"
IMG = DOCS / "img"

PROJECTS = [
    dict(
        id="inwire", sheet="02", name="Inwire", logo="inwire-logo.svg",
        tagline="Desktop packet analyzer for Windows",
        status="Version 0.5.0 / Windows",
        points=[
            "The app runs without administrator rights: a separate Rust service holds the Npcap capture handle and streams frames to it over a named pipe.",
            "Packet list virtualised by hand, reading older rows back from disk. In replays of a recorded burst on my PC the live view kept up with about 85,000 frames a second.",
            "Display filters run over the whole capture on disk, including frames that have left memory.",
            "Decodes about 100 protocols in its own TypeScript dissectors, from Ethernet and TCP to QUIC, HTTP/3, SMB2 and Kerberos, and decrypts TLS 1.2, TLS 1.3 and QUIC from a browser's SSLKEYLOGFILE.",
            "74 decision records explain the design, each with what it cost.",
        ],
        metrics=[("≈ 100", "protocols decoded"), ("≈ 85,000", "frames a second in replay"),
                 ("74", "decision records"), ("365", "assertion scripts")],
        stack=["Electron", "React", "TypeScript", "Rust", "Npcap"],
        note=None,
        links=[("Repository", "https://github.com/Doofess/inwire", True),
               ("How it works (PDF)", "https://github.com/Doofess/inwire/blob/main/docs/how-inwire-works.pdf", False)],
        shots=[("inwire-capture.png", "Inwire during a live capture: packet list, decoded layers and raw bytes"),
               ("inwire-monitoring.png", "Inwire's monitoring view")],
        phones=[],
        caption="Live capture and monitoring",
    ),
    dict(
        id="gymbro", sheet="03", name="GymBro", logo=None,
        tagline="Appointment booking system for gyms, Hebrew first and right to left",
        status="Staging / Source private",
        points=[
            "Members book sessions with their trainer on Android; staff run calendars, packages and the branch from Android or a Windows desktop app. Both clients call one TypeScript API, hosted on Vercel.",
            "Postgres refuses a double booking with an exclusion constraint, and a concurrency test proves it.",
            "Permissions are checked in the API and again in Postgres: nine roles and 38 permission grants, enforced by middleware and by row-level security.",
            "One contract for both clients: Zod schemas validate requests, type the desktop client and produce OpenAPI, which generates the Kotlin models.",
            "Every screen works in Hebrew and English, right to left, light and dark.",
        ],
        metrics=[("9", "roles"), ("38", "permission grants"),
                 ("≈ 4,740", "Vitest cases in CI"), ("12", "TypeScript projects")],
        stack=["TypeScript", "Kotlin", "Jetpack Compose", "PostgreSQL", "Electron", "React", "Hono"],
        note="Runs in staging only: nothing is in production and no real member uses it. The source is private; the repository documents the system. The screenshots use made-up data.",
        links=[("Architecture and screenshots", "https://github.com/Doofess/gymbro", True)],
        shots=[("gymbro-windows-calendar.png", "GymBro's staff calendar in the Windows app, in Hebrew")],
        phones=[("gymbro-android-calendar.png", "The trainer calendar on Android, dark theme"),
                ("gymbro-android-booking.png", "Booking a session on Android, in English"),
                ("gymbro-android-booking-he.png", "Booking a session on Android, in Hebrew")],
        caption="Staff calendar on Windows, member app on Android",
    ),
    dict(
        id="marshell", sheet="04", name="Marshell", logo="marshell-icon.svg",
        tagline="Windows app for AI coding-agent CLIs from any vendor",
        status="Alpha / Windows 11",
        points=[
            "Gives Claude Code, Codex CLI and other vendors' agents a session list with live status, approval cards and searchable history, while each agent stays a plain terminal.",
            "A Rust core runs an HTTP and WebSocket server on localhost inside the app and owns the terminals, sessions and history; the React UI talks to it through that API.",
            "Holds an agent's permission request through its hook and shows it as a card to allow or deny.",
            "Every write to an agent's config is a diff preview with a snapshot and an undo.",
            "The localhost API follows a written threat model: random port, a 32-byte token per launch, Host and Origin checks.",
        ],
        metrics=[("13.8 MB", "installer"), ("2,955", "Rust tests"),
                 ("≈ 4,500", "Vitest cases"), ("188", "generated protocol types")],
        stack=["Tauri 2", "Rust", "React", "TypeScript", "xterm.js", "SQLite"],
        note=None,
        links=[("Repository", "https://github.com/Doofess/marshell", True),
               ("Alpha release", "https://github.com/Doofess/marshell/releases/tag/v0.1.0-alpha.1", False)],
        shots=[("marshell-approval.png", "Marshell showing an agent's permission request as a card with Deny and Allow once"),
               ("marshell-sessions.jpg", "Marshell with sessions from three different agent CLIs in one list")],
        phones=[],
        caption="An approval card, and three vendors in one list",
    ),
    dict(
        id="claude-setup", sheet="05", name="claude-setup", logo=None,
        tagline="My Claude Code setup, kept as code",
        status="Windows",
        points=[
            "Work runs from .md plan files: a main Opus session plans, Sonnet workers write code, Haiku searches.",
            "Plugins, MCP servers and skills are switched on per project, since each one costs tokens on every turn.",
            "A status bar shows how full the context is and how much of the 5-hour and 7-day usage is left.",
            "A hook written in Python refuses to merge a pull request until its latest commit has been reviewed.",
            "One installer makes every Windows PC the same: settings, hooks, skills, plugins and terminal colours.",
        ],
        metrics=[("374", "Python tests"), ("91", "test cases for the view mod"),
                 ("553", "lines in the merge gate"), ("14", "unittest files")],
        stack=["Python", "PowerShell", "TypeScript"],
        note=None,
        links=[("Repository", "https://github.com/Doofess/claude-setup", True)],
        shots=[("claude-setup-session-cards.png", "The modified Claude Code session view, with prompts and agent runs as cards"),
               ("claude-setup-statusbar-crop.png", "The left part of the status bar: repository, branch, pull request, model and effort",
                "claude-setup-statusbar.png")],
        phones=[],
        caption="Session view and status bar",
    ),
]

ARROW = '<svg viewBox="0 0 16 16" aria-hidden="true" style="fill:none;stroke:currentColor;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round"><path d="M4 12 L12 4 M6 4 H12 V10"/></svg>'


def icon(slug: str) -> str:
    return f'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="{icon_path(slug)}"/></svg>'


def shot(name: str, alt: str, full: str | None = None) -> str:
    w, h = Image.open(IMG / name).size
    return (f'<a class="shot" href="img/{full or name}"><img src="img/{name}" width="{w}" height="{h}" '
            f'loading="lazy" alt="{html.escape(alt)}"></a>')


def project(p: dict) -> str:
    logo = f'<img src="img/{p["logo"]}" alt="" width="40" height="40">' if p["logo"] else ""
    points = "".join(f"<li>{html.escape(x)}</li>" for x in p["points"])
    metrics = "".join(f"<div><strong>{v}</strong><span>{label}</span></div>" for v, label in p["metrics"])
    chips = "".join(f"<li>{s}</li>" for s in p["stack"])
    note = f'<p class="note">{html.escape(p["note"])}</p>' if p["note"] else ""
    links = "".join(
        f'<a class="btn{" primary" if primary else ""}" href="{url}" rel="noopener">{label}{ARROW}</a>'
        for label, url, primary in p["links"]
    )
    shots = "".join(shot(*x) for x in p["shots"])
    if p["phones"]:
        shots += '<div class="phones">' + "".join(shot(n, a) for n, a in p["phones"]) + "</div>"
    return f'''
  <section class="sheet project" id="{p["id"]}" aria-labelledby="{p["id"]}-h">
    <div class="sheet-head label"><span>Sheet <b>{p["sheet"]}</b> / Project</span><span>{p["status"]}</span></div>
    <div class="project-body">
      <div class="shots">
        {shots}
        <p class="caption label"><span>Fig. {int(p["sheet"])}</span><i></i><span>{p["caption"]}</span></p>
      </div>
      <div>
        <div class="title-row">{logo}<h3 id="{p["id"]}-h">{p["name"]}</h3></div>
        <p class="tagline">{p["tagline"]}</p>
        <ul class="points">{points}</ul>
        <div class="metrics">{metrics}</div>
        <ul class="chips" aria-label="Built with">{chips}</ul>
        {note}
        <div class="btns">{links}</div>
      </div>
    </div>
  </section>'''


def stack_html() -> str:
    names = {"Compose": "Jetpack Compose", "Actions": "GitHub Actions"}
    out = ""
    for title, items in STACK:
        cells = "".join(f"<li>{icon(slug)}{names.get(name, name)}</li>" for slug, name in items)
        out += f'      <div><p class="label" style="margin:0">{title.title().replace(" And ", " and ")}</p><ul>{cells}</ul></div>\n'
    return out


def images() -> None:
    IMG.mkdir(parents=True, exist_ok=True)
    for p in PROJECTS:
        for names in p["shots"]:
            for name in (names[0], *names[2:]):
                shutil.copyfile(SHOTS / name, IMG / name)
        for name, _ in p["phones"]:
            Image.open(SHOTS / name).resize((540, 1200), Image.LANCZOS).save(IMG / name, optimize=True)
        if p["logo"]:
            shutil.copyfile(SHOTS / p["logo"], IMG / p["logo"])
    # link preview image: the dark banner on the page colour, 1200 x 630
    TMP.mkdir(exist_ok=True)
    page = TMP / "og.html"
    page.write_text(
        '<!doctype html><meta charset="utf-8"><style>html,body{margin:0;width:1200px;height:630px;background:#071223;'
        'display:grid;place-items:center}svg{width:1120px;height:auto}</style>' + banner(THEMES["dark"]),
        encoding="utf-8",
    )
    capture(page, IMG / "og.png", 1200, 630, scale=1)
    Image.open(IMG / "og.png").convert("RGB").save(IMG / "og.png", optimize=True)


def main() -> None:
    images()
    page = (DESIGN / "site.template.html").read_text(encoding="utf-8")
    page = page.replace("<!--PROJECTS-->", "".join(project(p) for p in PROJECTS))
    page = page.replace("<!--STACK-->", stack_html())
    page = re.sub(r"<!--ICON:(\w+)-->", lambda m: icon(m.group(1)), page)
    (DOCS / "index.html").write_text(page, encoding="utf-8", newline="\n")
    (DOCS / ".nojekyll").write_text("", encoding="utf-8")
    total = sum(f.stat().st_size for f in DOCS.rglob("*") if f.is_file())
    print("docs/index.html", (DOCS / "index.html").stat().st_size // 1024, "KB; docs total", total // 1024, "KB")


if __name__ == "__main__":
    main()
