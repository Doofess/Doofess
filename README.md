<p>
<a href="https://doofess.github.io/Doofess/">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/banner-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="assets/banner-light.svg">
    <img src="assets/banner-light.svg" width="100%" alt="Rotem Grinhut. Full-stack developer and system designer, currently looking for opportunities. Based in Israel. Languages: Hebrew, English. Builds desktop and web apps with TypeScript, React and Rust.">
  </picture>
</a>
</p>

Full-stack developer and system designer in Israel, currently looking for opportunities. I build desktop and web apps with TypeScript, React and Rust.

<p>
  <a href="https://doofess.github.io/Doofess/"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/button-portfolio-dark.svg"><source media="(prefers-color-scheme: light)" srcset="assets/button-portfolio-light.svg"><img src="assets/button-portfolio-light.svg" height="38" alt="Portfolio page"></picture></a>
  <a href="https://www.linkedin.com/in/rotem-grinhut-979547262/"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/button-linkedin-dark.svg"><source media="(prefers-color-scheme: light)" srcset="assets/button-linkedin-light.svg"><img src="assets/button-linkedin-light.svg" height="38" alt="LinkedIn"></picture></a>
  <a href="https://x.com/Rotemgr"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/button-x-dark.svg"><source media="(prefers-color-scheme: light)" srcset="assets/button-x-light.svg"><img src="assets/button-x-light.svg" height="38" alt="X"></picture></a>
</p>

These projects are built with AI coding agents (Claude Code). I make the design and UX/UI decisions, review the code and test by hand. Each README has the architecture, the decisions behind it and how it is tested.

## Projects

<p>
<a href="https://github.com/Doofess/inwire">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/card-inwire-dark.png">
    <source media="(prefers-color-scheme: light)" srcset="assets/card-inwire-light.png">
    <img src="assets/card-inwire-light.png" width="100%" alt="Inwire, a desktop packet analyzer for Windows. The screenshot shows a live capture. About 100 protocols decoded, about 85,000 frames a second in replay, 74 decision records, 365 assertion scripts.">
  </picture>
</a>
</p>

**[Inwire](https://github.com/Doofess/inwire).** Desktop packet analyzer for Windows. The app runs without administrator rights; a separate service holds the capture handle and streams frames over a named pipe. The packet list is virtualised by hand and stays smooth during heavy live capture.

Built with Electron, React, TypeScript and Rust. [Repository](https://github.com/Doofess/inwire) · [How it works (PDF)](https://github.com/Doofess/inwire/blob/main/docs/how-inwire-works.pdf)

<p>
<a href="https://github.com/Doofess/gymbro">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/card-gymbro-dark.png">
    <source media="(prefers-color-scheme: light)" srcset="assets/card-gymbro-light.png">
    <img src="assets/card-gymbro-light.png" width="100%" alt="GymBro, an appointment booking system for gyms, Hebrew first. The screenshots show the staff calendar on Windows and the member app on Android. 9 roles, 38 permission grants, about 4,740 Vitest cases in CI, 12 TypeScript projects.">
  </picture>
</a>
</p>

**[GymBro](https://github.com/Doofess/gymbro).** Appointment booking system for gyms, Hebrew first and right to left: an Android app for members and staff, a Windows app for staff, one API. Postgres refuses a double booking with an exclusion constraint, and a concurrency test proves it. The source is private; the repository documents the system.

Built with TypeScript, Kotlin, PostgreSQL, Electron and React. [Architecture and screenshots](https://github.com/Doofess/gymbro)

<p>
<a href="https://github.com/Doofess/marshell">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/card-marshell-dark.png">
    <source media="(prefers-color-scheme: light)" srcset="assets/card-marshell-light.png">
    <img src="assets/card-marshell-light.png" width="100%" alt="Marshell, a Windows app for AI coding-agent CLIs from any vendor. The screenshot shows an agent's permission request as a card with Deny and Allow once. 13.8 MB installer, 2,955 Rust tests, about 4,500 Vitest cases, 188 generated protocol types.">
  </picture>
</a>
</p>

**[Marshell](https://github.com/Doofess/marshell).** Windows app for AI coding-agent CLIs from any vendor. It gives Claude Code, Codex and others a session list with live status, approval cards and searchable history, while each agent stays a plain terminal. A Rust core serves the React UI over a local HTTP and WebSocket API.

Built with Tauri 2, Rust, React and TypeScript. [Repository](https://github.com/Doofess/marshell) · [Alpha release](https://github.com/Doofess/marshell/releases/tag/v0.1.0-alpha.1)

<p>
<a href="https://github.com/Doofess/claude-setup">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/card-claude-setup-dark.png">
    <source media="(prefers-color-scheme: light)" srcset="assets/card-claude-setup-light.png">
    <img src="assets/card-claude-setup-light.png" width="100%" alt="claude-setup, my Claude Code setup kept as code. The screenshots show the session view and the status bar. 374 Python tests, 91 test cases for the session view, 553 lines in the merge gate, 14 unittest files.">
  </picture>
</a>
</p>

**[claude-setup](https://github.com/Doofess/claude-setup).** My Claude Code configuration as code, with a hook that refuses to merge a pull request until its latest commit has been reviewed.

Built with Python, PowerShell and TypeScript. [Repository](https://github.com/Doofess/claude-setup)

## What I build with

<p>
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/stack-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/stack-light.svg">
  <img src="assets/stack-light.svg" width="100%" alt="Interface: React, TypeScript, Vite, Tailwind CSS. Desktop and mobile: Electron, Tauri 2, Kotlin, Jetpack Compose. Services and data: Rust, Node.js, PostgreSQL, Supabase, SQLite. Tooling: GitHub Actions, Vitest, Playwright, Python, PowerShell.">
</picture>
</p>

## Activity

<p>
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://streak-stats.demolab.com?user=Doofess&background=0B1A30&border=2C4F82&stroke=2C4F82&ring=8FBAFF&fire=FFB454&currStreakNum=EAF2FF&sideNums=EAF2FF&currStreakLabel=8FBAFF&sideLabels=8FBAFF&dates=9FB6D8&border_radius=12">
    <source media="(prefers-color-scheme: light)" srcset="https://streak-stats.demolab.com?user=Doofess&background=F6F9FD&border=B5C8E6&stroke=B5C8E6&ring=1F4E9C&fire=B8430B&currStreakNum=0C2340&sideNums=0C2340&currStreakLabel=1F4E9C&sideLabels=1F4E9C&dates=4C6183&border_radius=12">
    <img src="https://streak-stats.demolab.com?user=Doofess&background=F6F9FD&border=B5C8E6&stroke=B5C8E6&ring=1F4E9C&fire=B8430B&currStreakNum=0C2340&sideNums=0C2340&currStreakLabel=1F4E9C&sideLabels=1F4E9C&dates=4C6183&border_radius=12" width="53.5%" alt="Total contributions, current streak and longest streak">
  </picture>
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://github-readme-stats.vercel.app/api/top-langs/?username=Doofess&layout=compact&langs_count=6&card_width=350&bg_color=0B1A30&title_color=EAF2FF&text_color=9FB6D8&border_color=2C4F82&border_radius=12&custom_title=Languages%20in%20public%20repos">
    <source media="(prefers-color-scheme: light)" srcset="https://github-readme-stats.vercel.app/api/top-langs/?username=Doofess&layout=compact&langs_count=6&card_width=350&bg_color=F6F9FD&title_color=0C2340&text_color=4C6183&border_color=B5C8E6&border_radius=12&custom_title=Languages%20in%20public%20repos">
    <img src="https://github-readme-stats.vercel.app/api/top-langs/?username=Doofess&layout=compact&langs_count=6&card_width=350&bg_color=F6F9FD&title_color=0C2340&text_color=4C6183&border_color=B5C8E6&border_radius=12&custom_title=Languages%20in%20public%20repos" width="44.5%" alt="Languages in my public repositories">
  </picture>
</p>

<p>
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://github-readme-activity-graph.vercel.app/graph?username=Doofess&bg_color=0B1A30&color=9FB6D8&line=8FBAFF&point=FFB454&area=true&area_color=8FBAFF&title_color=EAF2FF&radius=12&hide_border=true&custom_title=Contributions%2C%20last%2031%20days">
  <source media="(prefers-color-scheme: light)" srcset="https://github-readme-activity-graph.vercel.app/graph?username=Doofess&bg_color=F6F9FD&color=4C6183&line=1F4E9C&point=B8430B&area=true&area_color=1F4E9C&title_color=0C2340&radius=12&hide_border=true&custom_title=Contributions%2C%20last%2031%20days">
  <img src="https://github-readme-activity-graph.vercel.app/graph?username=Doofess&bg_color=F6F9FD&color=4C6183&line=1F4E9C&point=B8430B&area=true&area_color=1F4E9C&title_color=0C2340&radius=12&hide_border=true&custom_title=Contributions%2C%20last%2031%20days" width="100%" alt="Contributions over the last 31 days">
</picture>
</p>

## Contact

[LinkedIn](https://www.linkedin.com/in/rotem-grinhut-979547262/). Hebrew and English. The [portfolio page](https://doofess.github.io/Doofess/) has more on each project.
