"""Builds the portfolio page: docs/index.html and docs/img/.

    python design/site.py

GitHub Pages serves docs/ at https://doofess.github.io/Doofess/.

Run it on Windows 11: the link preview image is drawn by a headless browser with Segoe UI, and comes out
different with another font.

docs/img belongs to this script. Every file the page uses is written there on each run, and a file the run
did not write is removed at the end, so keep nothing else in that folder.
"""
from __future__ import annotations

import html
import re
import shutil

from PIL import Image

from build import DESIGN, ROOT, SANS, SHOTS, THEMES, TMP, capture, icon_path, optimise

DOCS = ROOT / "docs"
IMG = DOCS / "img"

# A screenshot runs across the page. In a window at least 1060 px wide that is 1012 px, and three phone
# screenshots in a row are 324 px each. The page offers a copy of exactly that width, which a 1x screen
# shows one to one, and a larger one for high-density screens.
FULL = 1012
FULL_SIZES = "(min-width: 1060px) 1012px, calc(100vw - 48px)"
PHONE = 324
PHONE_SIZES = "(min-width: 1060px) 324px, calc(33vw - 30px)"

WRITTEN: set[str] = set()  # the files this run put in docs/img; main() removes the others at the end

PROJECTS = [
    dict(
        id="inwire", name="Inwire", logo="inwire-logo.svg",
        tagline="Desktop packet analyzer for Windows",
        status="Version 0.5.0, Windows",
        points=[
            "The app runs without administrator rights: a separate Rust service holds the Npcap capture handle and streams frames to it over a named pipe.",
            "Packet list virtualised by hand, reading older rows back from disk. In replays of a recorded burst on my PC the live view kept up with about 85,000 frames a second.",
            "Display filters run over the whole capture on disk, including frames that have left memory.",
            "Decodes about 100 protocols in its own TypeScript dissectors, from Ethernet and TCP to QUIC, HTTP/3, SMB2 and Kerberos, and decrypts TLS 1.2, TLS 1.3 and QUIC from a browser's SSLKEYLOGFILE.",
            "74 decision records explain the design, each with what it cost.",
        ],
        stack=["Electron", "React", "TypeScript", "Rust", "Npcap"],
        note=None,
        links=[("Repository", "https://github.com/Doofess/inwire", True),
               ("How it works (PDF)", "https://github.com/Doofess/inwire/blob/main/docs/how-inwire-works.pdf", False)],
        main=("inwire-capture.png", "Inwire during a live capture: packet list, decoded layers and raw bytes", "Live capture"),
        more=[("inwire-monitoring.png", "Inwire's monitoring view", "Monitoring")],
        phones=[],
    ),
    dict(
        id="gymbro", name="GymBro", logo=None,
        tagline="Appointment booking system for gyms, Hebrew first and right to left",
        status="Staging, source private",
        points=[
            "Members book sessions with their trainer on Android; staff run calendars, packages and the branch from Android or a Windows desktop app. Both clients call one TypeScript API, hosted on Vercel.",
            "Postgres refuses a double booking with an exclusion constraint, and a concurrency test proves it.",
            "Permissions are checked in the API and again in Postgres: nine roles and 38 permission grants, enforced by middleware and by row-level security.",
            "One contract for both clients: Zod schemas validate requests, type the desktop client and produce OpenAPI, which generates the Kotlin models.",
            "Every screen works in Hebrew and English, right to left, light and dark.",
        ],
        stack=["TypeScript", "Kotlin", "Jetpack Compose", "PostgreSQL", "Electron", "React", "Hono"],
        note="Runs in staging only: nothing is in production and no real member uses it. The source is private; the repository documents the system. The screenshots use made-up data.",
        links=[("Architecture and screenshots", "https://github.com/Doofess/gymbro", True)],
        main=("gymbro-windows-calendar.png", "GymBro's staff calendar in the Windows app, in Hebrew", "Staff calendar on Windows"),
        more=[],
        phones=[("gymbro-android-calendar.png", "The trainer calendar on Android, dark theme"),
                ("gymbro-android-booking.png", "Booking a session on Android, in English"),
                ("gymbro-android-booking-he.png", "Booking a session on Android, in Hebrew")],
        phones_caption="The app on Android: trainer calendar, and booking in English and Hebrew",
    ),
    dict(
        id="marshell", name="Marshell", logo="marshell-icon.svg",
        tagline="Windows app for AI coding-agent CLIs from any vendor",
        status="Alpha, Windows 11",
        points=[
            "Gives Claude Code, Codex CLI and other vendors' agents a session list with live status, approval cards and searchable history, while each agent stays a plain terminal.",
            "A Rust core runs an HTTP and WebSocket server on localhost inside the app and owns the terminals, sessions and history; the React UI talks to it through that API.",
            "Holds an agent's permission request through its hook and shows it as a card to allow or deny.",
            "Every write to an agent's config is a diff preview with a snapshot and an undo.",
            "The localhost API follows a written threat model: random port, a 32-byte token per launch, Host and Origin checks.",
        ],
        stack=["Tauri 2", "Rust", "React", "TypeScript", "xterm.js", "SQLite"],
        note=None,
        links=[("Repository", "https://github.com/Doofess/marshell", True),
               ("Alpha release", "https://github.com/Doofess/marshell/releases/tag/v0.1.0-alpha.1", False)],
        main=("marshell-approval.png", "Marshell showing an agent's permission request as a card with Deny and Allow once",
              "An agent's permission request, shown as a card"),
        more=[("marshell-sessions.jpg", "Marshell with sessions from three different agent CLIs in one list",
               "Three vendors' agents in one list")],
        phones=[],
    ),
    dict(
        id="claude-setup", name="claude-setup", logo=None,
        tagline="My coding-agent setup, kept as code",
        status="Windows",
        points=[
            "Work runs from .md plan files, with a large model planning, mid-size workers writing the code and a small model handling searches.",
            "Plugins, MCP servers and skills are switched on per project, since each one costs tokens on every turn.",
            "A status bar shows how full the context is and how much of the 5-hour and 7-day usage is left.",
            "A hook written in Python refuses to merge a pull request until its latest commit has been reviewed.",
            "One installer makes every Windows PC the same: settings, hooks, skills, plugins and terminal colours.",
        ],
        stack=["Python", "PowerShell", "TypeScript"],
        note=None,
        links=[("Repository", "https://github.com/Doofess/claude-setup", True)],
        main=("claude-setup-session-cards.png", "The coding agent's session view, modified to show prompts and agent runs as cards",
              "Session view"),
        more=[],
        phones=[],
        # the bar is 2880 px wide and was captured at 2x: it is cut in two at 1506, a gap between two of its
        # elements, and each half is shown at its real size
        strips=("claude-setup-statusbar.png", 2, [
            ((0, 1506), "The status bar, left half: repository, branch, pull request, model, effort and the context meter"),
            ((1506, 2880), "The status bar, right half: the 5-hour and 7-day usage left, the cost and the time"),
        ], "Status bar, in two halves"),
    ),
]

STACK = [
    ("Interface", "React, TypeScript, Vite, Tailwind CSS"),
    ("Desktop and mobile", "Electron, Tauri 2, Kotlin, Jetpack Compose"),
    ("Services and data", "Rust, Node.js, PostgreSQL, Supabase, SQLite"),
    ("Tooling", "GitHub Actions, Vitest, Playwright, Python, PowerShell"),
]


def icon(slug: str) -> str:
    return f'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="{icon_path(slug)}"/></svg>'


def resized(name: str, width: int) -> tuple[str, int]:
    """Puts a screenshot in docs/img, made `width` px wide when it is wider. Returns the file's name and width."""
    src = SHOTS / name
    with Image.open(src) as im:
        if im.width <= width:
            shutil.copyfile(src, IMG / name)
            WRITTEN.add(name)
            return name, im.width
        if im.mode == "P":  # a palette image would be resampled without a filter
            im = im.convert("RGBA")
        small = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    out = f"{src.stem}-{width}{src.suffix}"
    small.save(IMG / out, optimize=True, **({"quality": 90} if src.suffix == ".jpg" else {}))
    WRITTEN.add(out)
    return out, width


def shot(name: str, alt: str, caption: str | None = None, width: int = FULL, sizes: str = FULL_SIZES,
         largest: int | None = None) -> str:
    """A screenshot that links to its largest copy. A 1x screen gets the copy that is `width` px wide.
    The largest copy is the screenshot itself, or `largest` px wide when that is given."""
    e = html.escape
    one, w = resized(name, width)
    big, bw = resized(name, largest or 10 ** 6)
    with Image.open(IMG / one) as im:
        h = im.height
    srcset = f' srcset="img/{e(one)} {w}w, img/{e(big)} {bw}w" sizes="{sizes}"' if big != one else ""
    out = (f'<a class="shot" href="img/{e(big)}"><img src="img/{e(one)}"{srcset} width="{w}" height="{h}" '
           f'loading="lazy" alt="{e(alt)}"></a>')
    if caption:
        out += f'<p class="caption muted small">{e(caption)}</p>'
    return out


def strips(name: str, density: int, parts: list, caption: str) -> str:
    """A wide, low screenshot cut into parts, one under the other. Each part is shown at the size it has on
    screen (its pixels divided by the capture's density), so its text is not shrunk. All link to the whole."""
    e = html.escape
    src = SHOTS / name
    shutil.copyfile(src, IMG / name)
    WRITTEN.add(name)
    out = ""
    with Image.open(src) as im:
        for i, ((left, right), alt) in enumerate(parts, 1):
            part = f"{src.stem}-part{i}{src.suffix}"
            im.crop((left, 0, right, im.height)).save(IMG / part, optimize=True)
            WRITTEN.add(part)
            out += (f'<a class="shot strip" href="img/{e(name)}"><img src="img/{e(part)}" width="{(right - left) // density}" '
                    f'height="{im.height // density}" loading="lazy" alt="{e(alt)}"></a>')
    return f'\n      <div class="more">{out}<p class="caption muted small">{e(caption)}</p></div>'


def project(p: dict) -> str:
    e = html.escape  # every string from PROJECTS is plain text and is escaped here
    logo = ""
    if p["logo"]:
        shutil.copyfile(SHOTS / p["logo"], IMG / p["logo"])
        WRITTEN.add(p["logo"])
        logo = f'<img src="img/{e(p["logo"])}" alt="" width="30" height="30">'
    points = "".join(f"<li>{e(x)}</li>" for x in p["points"])
    note = f'<p class="muted small">{e(p["note"])}</p>' if p["note"] else ""
    links = "".join(
        f'<a class="btn{" primary" if primary else ""}" href="{e(url)}" rel="noopener">{e(label)}</a>'
        for label, url, primary in p["links"]
    )
    more = "".join(f'\n      <div class="more">{shot(*x)}</div>' for x in p["more"])
    if p["phones"]:
        phones = "".join(shot(name, alt, None, PHONE, PHONE_SIZES, 2 * PHONE) for name, alt in p["phones"])
        more += (f'\n      <div class="more"><div class="phones">{phones}</div>'
                 f'<p class="caption muted small">{e(p["phones_caption"])}</p></div>')
    if p.get("strips"):
        more += strips(*p["strips"])
    return f'''
    <article class="project" id="{p["id"]}" aria-labelledby="{p["id"]}-h">
      <div class="title-row">{logo}<h3 id="{p["id"]}-h">{e(p["name"])}</h3><span class="status muted small">{e(p["status"])}</span></div>
      <p class="tagline">{e(p["tagline"])}</p>
      {shot(*p["main"])}
      <div class="project-text">
        <ul class="points">{points}</ul>
        <div class="facts">
          <h4>Built with</h4>
          <p>{e(", ".join(p["stack"]))}</p>
          {note}
          <div class="btns">{links}</div>
        </div>
      </div>{more}
    </article>'''


def stack_html() -> str:
    return "".join(f"      <dt>{html.escape(k)}</dt><dd>{html.escape(v)}</dd>\n" for k, v in STACK)


def preview_image() -> None:
    """The link preview image, 1200 x 630, in the page's light colours."""
    t = THEMES["light"]
    TMP.mkdir(exist_ok=True)
    page = TMP / "og.html"
    page.write_text(
        f'''<!doctype html><meta charset="utf-8"><style>
html, body {{ margin: 0; width: 1200px; height: 630px; background: {t["page"]}; color: {t["fg"]}; font-family: {SANS}; }}
body {{ display: flex; flex-direction: column; justify-content: center; padding: 0 96px; box-sizing: border-box; }}
h1 {{ font-size: 104px; line-height: 1.05; letter-spacing: -3px; font-weight: 600; margin: 0; }}
p {{ font-size: 40px; color: {t["muted"]}; margin: 22px 0 0; }}
.open {{ font-size: 30px; font-weight: 600; color: {t["fg"]}; margin-top: 56px; display: flex; align-items: center; gap: 18px; }}
.open::before {{ content: ""; width: 16px; height: 16px; border-radius: 50%; background: {t["accent"]}; }}
</style><h1>Rotem Grinhut</h1><p>Full-stack developer and system designer</p>
<p class="open">Currently looking for opportunities</p>''',
        encoding="utf-8",
    )
    capture(page, IMG / "og.png", 1200, 630, scale=1)
    optimise(IMG / "og.png", rgb=True)
    WRITTEN.add("og.png")


def main() -> None:
    IMG.mkdir(parents=True, exist_ok=True)
    preview_image()
    page = (DESIGN / "site.template.html").read_text(encoding="utf-8")
    page = page.replace("<!--PROJECTS-->", "".join(project(p) for p in PROJECTS))
    page = page.replace("<!--STACK-->", stack_html())
    page = re.sub(r"<!--ICON:(\w+)-->", lambda m: icon(m.group(1)), page)
    (DOCS / "index.html").write_text(page, encoding="utf-8", newline="\n")
    (DOCS / ".nojekyll").write_text("", encoding="utf-8")
    # only now, with the page and every image written, remove what an older page left behind
    for old in IMG.iterdir():
        if old.is_file() and old.name not in WRITTEN:
            old.unlink()
    total = sum(f.stat().st_size for f in DOCS.rglob("*") if f.is_file())
    print("docs/index.html", (DOCS / "index.html").stat().st_size // 1024, "KB; docs total", total // 1024, "KB")


if __name__ == "__main__":
    main()
