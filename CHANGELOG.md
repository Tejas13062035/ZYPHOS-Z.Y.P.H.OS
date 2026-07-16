# Changelog

All notable changes to Z.Y.P.H.O.S are documented in this file.

---

## Phase 3 — Intelligence Layer

### Voice & Biometrics
- Added voice biometric authentication (`core/voice_auth.py`) using Resemblyzer
- `--enroll` flag records 3 voice samples and builds a voiceprint
- Sensitive tools (gmail, drive, calendar, notes, whatsapp, delete_file) gated behind voice verification
- Cosine similarity threshold tuned to 0.70 after testing genuine vs. altered voice samples
- Switched TTS engine from `pyttsx3` to Microsoft Edge TTS (`en-GB-RyanNeural`) — major quality upgrade
- Fixed TTS file permission conflicts by using timestamped filenames per utterance
- Auto-speak added for conversational goals ("tell me...", "what is...", "who is...") — result text is spoken automatically without an explicit `speak` flag

### LLM Backend
- Migrated default LLM from Phi-3.5 (LM Studio) → Gemma 3 4B (Ollama) → Hermes 3 3B → **Cerebras `gpt-oss-120b`** (current default)
- Added multi-backend support: Cerebras (default), Gemini 3.5 Flash, Groq Llama 3.3 70B, Ollama (fully offline fallback)
- Removed dead code from early backend-switching experiments (`PHI_URL`, `BACKEND` env var)
- Fixed JSON extraction from LLM responses using brace-depth parsing (handles models that add explanatory text after JSON)

### Planning & Execution
- Built smart planner — LLM converts natural language goals into structured task lists
- Built smart executor — LLM routes each task to the correct tool via JSON tool-calling
- Added self-critique loop (`core/critic.py`) — evaluates task results, retries on failure (max 2 retries)
- Added goal chaining (`core/chainer.py`) — autonomously continues a goal based on prior results
- Added FAISS-based semantic memory (`memory/store.py`) — replaces linear search, indexes every goal + result
- Added plugin system (`core/plugin_loader.py`) — drop any `.py` file into `plugins/` to add a new tool automatically, no core changes needed

### Plugins Added (25+)
calendar, gmail, drive, whatsapp, whatsapp_bulk, music, youtube, weather, notes, timer, system_stats, clipboard, file_organizer, network_scan, security, port_scanner, joke, nasa, news, countries, github_stats, spotify, hello

Notable plugin fixes:
- `joke` — routes through JokeAPI (not LLM-generated), supports category + count, safe-mode disabled, speaks each joke sequentially
- `nasa` — 6 actions (apod, asteroids, earth, donki, image, eonet) after Mars Photos API was found deprecated/archived
- `countries` — REST Countries v3.1/v3.2 found deprecated mid-session; added Wikipedia REST API as reliable fallback
- `github_stats` — fixed private repo access issue by making the repo public and using `public_repo`-scoped token

### Vision & Perception
- Screen vision via Groq `llama-4-scout-17b-16e-instruct` (free tier)
- Webcam support scaffolded for future ambient awareness

### Daemon & Reliability
- Always-on daemon (`core/daemon.py`) with PID tracking, `--stop`/`--restart`
- Auto-start on WSL boot via `~/.bashrc`
- Watchdog script (`scripts/watchdog.py`) — auto-restarts daemon if it crashes
- Daemon smart-mode toggle (`--smart-daemon`)

### Monitoring
- TUI monitor (`scripts/monitor.py`) using `rich` — daemon status, pending queue, live logs, goal history
- Web UI dashboard (`scripts/webui.py`) — Flask app on `localhost:6789`, send goals from browser, view logs and history in real time

### Self-Awareness
- `--explain` flag — Zyphos reads its own source code and describes its own capabilities

---

## Phase 2 — Perception & Control

- Windows sidecar (Flask + pyautogui) for OS-level control: click, type, screenshot, scroll, drag, hotkey
- Screenshot auto-save with timestamps
- Multi-goal queue — run several goals sequentially in one command
- `--status` and `--memory` flags
- Scheduled tasks — `--schedule` with `--every` (interval) and `--at` (specific time), foreground or background

---

## Phase 1 — Skeleton

- Core CLI entry point (`zyphos.py`)
- Keyword-based planner and executor
- Persistent JSON state and task queue
- Basic filesystem and shell tools
- Git repository initialized, iterative commit history established

---

## Infrastructure

- Repository migrated to GitHub, made public for portfolio visibility
- `requirements.txt` generated for one-command portable setup on new hardware
- `.env` properly gitignored throughout; `.env.example` added as a template
- MIT License added
