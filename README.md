# Rotem Grinhut

Frontend and full-stack developer in Israel. I build desktop and web apps with TypeScript, React and Rust.

These projects are built with AI coding agents (Claude Code). Each README has the architecture, the decisions behind it and how it is tested.

## Projects

| Project | What it is | Built with |
|---|---|---|
| [Inwire](https://github.com/Doofess/inwire) | Desktop packet analyzer for Windows. The app runs without administrator rights; a separate service holds the capture handle and streams frames over a named pipe. The packet list is virtualised by hand and stays smooth during heavy live capture. | Electron, React, TypeScript, Rust |
| GymBro | Appointment booking system for gyms, Hebrew first and right to left: an Android app for members and staff, a Windows app for staff, one API. Postgres refuses a double booking with an exclusion constraint, and a concurrency test proves it. The source is private. | TypeScript, Kotlin, PostgreSQL, Electron, React |
| [Marshell](https://github.com/Doofess/marshell) | Windows app for AI coding-agent CLIs from any vendor. It gives Claude Code, Codex and others a session list with live status, approval cards and searchable history, while each agent stays a plain terminal. A Rust core serves the React UI over a local HTTP and WebSocket API. | Tauri 2, Rust, React, TypeScript |
| [Bookandry](https://github.com/Doofess/bookandry) | Money manager for households in Israel, in English and Hebrew. Every device keeps a full copy of the data and works offline; changes sync through Postgres, and a property test checks that devices converge. | React, TypeScript, IndexedDB, Supabase |
| [claude-setup](https://github.com/Doofess/claude-setup) | My Claude Code configuration as code, with a hook that refuses to merge a pull request until its latest commit has been reviewed. | Python, PowerShell, TypeScript |

## Contact

[LinkedIn](https://www.linkedin.com/in/rotem-grinhut-979547262/). Hebrew and English.
