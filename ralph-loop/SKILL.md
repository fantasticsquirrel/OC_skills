---
name: ralph-loop
description: Standardize and operate Ralph Loop projects so they work with the Ralph Dashboard (file-based runtime + control interface). Use when creating or fixing a Ralph loop project, wiring in pause/resume/inject behavior, emitting .ralph/iterations.jsonl + ralph.log + ralph.pid, or debugging why the dashboard can’t detect status/iterations.
---

# Ralph Loop (Dashboard-Compatible)

This skill is a **runbook + scaffolding kit** for generating Ralph loops that are **fully compatible** with the Ralph Dashboard.

Bundled resources:
- `scripts/ralph.sh` (copy to your project root as `ralph.sh`)
- `templates/AGENTS.md`, `templates/PROMPT.md`, `templates/IMPLEMENTATION_PLAN.md`

## Required on-disk contract (what the dashboard reads)

Project root should contain:
- `AGENTS.md`
- `PROMPT.md`
- `IMPLEMENTATION_PLAN.md`
- `specs/*.md` (optional)

Project runtime directory:
- `.ralph/ralph.log` — append-only human log (iteration headers recommended)
- `.ralph/iterations.jsonl` — **one JSON object per line**, keyed by `iteration`
- `.ralph/ralph.pid` — PID of the loop process
- `.ralph/pause` — if present, loop is paused
- `.ralph/inject.md` — user injection message consumed between iterations
- `.ralph/pending-notification.txt` — short user-facing status updates
- `.ralph/config.json` — loop config (CLI, flags, max iterations, test command, pricing)

## Status rules (match dashboard behavior)
- `running` if PID in `.ralph/ralph.pid` is live and `.ralph/pause` absent
- `paused` if PID live and `.ralph/pause` present
- `complete` if plan includes `STATUS: COMPLETE` (and not running)
- otherwise `stopped`

## Iteration log format (recommended)
In `.ralph/ralph.log`, emit headers like:
- `[HH:MM:SS] === Iteration N/M ===`

The dashboard parses this pattern to find iteration boundaries.

## iterations.jsonl schema (minimum viable)
Each line is JSON. Minimum fields:
```json
{"iteration": 1, "phase": "PLANNING", "started_at": "2026-02-15T20:00:00Z", "ended_at": "2026-02-15T20:05:00Z", "status": "success"}
```
Recommended fields (when available):
- `iteration` (int)
- `phase` ("PLANNING" | "BUILDING" | etc)
- `status` ("success" | "error" | "partial")
- `duration_seconds`
- `tokens_in`, `tokens_out`, `tokens_total`
- `cost_usd`
- `tasks_done`, `tasks_total`
- `commit` (git hash)
- `tests` ("pass"|"fail"|"skip")
- `errors` (array of strings)

## Control semantics (pause / inject)
Between iterations:
1) If `.ralph/pause` exists → wait/sleep until removed
2) If `.ralph/inject.md` exists → append contents to next prompt context, then delete it

## Quickstart (recommended)
1) Copy `scripts/ralph.sh` → `<project>/ralph.sh` and `chmod +x ralph.sh`.
2) Copy templates into project root:
   - `templates/AGENTS.md` → `AGENTS.md`
   - `templates/PROMPT.md` → `PROMPT.md`
   - `templates/IMPLEMENTATION_PLAN.md` → `IMPLEMENTATION_PLAN.md`
3) Optional: create `.ralph/config.json` to configure the loop (CLI, flags, max iterations, tests).
4) Start the loop:
   - Preferred: Start from **Ralph Dashboard** (so PID/pause/stop controls are consistent).
   - Or: run `./ralph.sh 20` from the project root.

## Implementation guidance (if you roll your own runner)
Your runner must:
- create `.ralph/` on startup
- write its PID to `.ralph/ralph.pid`
- append to `.ralph/ralph.log`
- append JSON objects to `.ralph/iterations.jsonl`
- clear stale PID if it’s zombie/dead
- handle SIGTERM/SIGINT gracefully

## Debug checklist (dashboard not showing your project)
- Does the project live under one of `RALPH_PROJECT_DIRS`?
- Does it contain a `.ralph/` directory?
- Is `.ralph/ralph.pid` present and valid?
- Is `.ralph/ralph.log` being appended?
- Is `.ralph/iterations.jsonl` valid JSONL (one JSON per line, no trailing commas)?

## Reference
Ralph Dashboard docs: see the upstream repo `Endogen/ralph-dashboard`.
