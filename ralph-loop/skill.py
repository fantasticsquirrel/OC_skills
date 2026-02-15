"""Ralph Loop skill - dashboard-compatible runtime contract + scaffolding helpers."""

from __future__ import annotations

from pathlib import Path


def run(input: dict):
    """Return guidance/templates for producing Ralph Dashboard-compatible loops.

    Note: OpenClaw skills are advisory; file writes are performed by the agent using exec/write tools.
    """

    action = input.get("action", "guide")

    if action == "guide":
        return {
            "summary": "Generate/run a Ralph loop that produces real dashboard stats via .ralph/* artifacts.",
            "runner_script": "scripts/ralph.sh (copy to your project root as ralph.sh)",
            "templates": {
                "AGENTS.md": "templates/AGENTS.md",
                "PROMPT.md": "templates/PROMPT.md",
                "IMPLEMENTATION_PLAN.md": "templates/IMPLEMENTATION_PLAN.md",
            },
            "key_files": [
                ".ralph/ralph.log",
                ".ralph/iterations.jsonl",
                ".ralph/ralph.pid",
                ".ralph/pause",
                ".ralph/inject.md",
                ".ralph/pending-notification.txt",
                ".ralph/config.json",
            ],
            "quickstart": [
                "1) Copy scripts/ralph.sh -> <project>/ralph.sh (chmod +x)",
                "2) Copy templates/* into project root (AGENTS.md, PROMPT.md, IMPLEMENTATION_PLAN.md)",
                "3) Create <project>/.ralph/config.json (optional) to set cli/flags/max_iterations/test_command",
                "4) Start from Ralph Dashboard (writes/uses .ralph/ralph.pid) or run ./ralph.sh",
            ],
        }

    if action == "schema":
        return {
            "iterations_jsonl_minimum": {
                "iteration": 1,
                "phase": "PLANNING",
                "started_at": "2026-02-15T20:00:00Z",
                "ended_at": "2026-02-15T20:05:00Z",
                "status": "success",
            },
            "recommended_fields": [
                "duration_seconds",
                "tokens_in",
                "tokens_out",
                "tokens_total",
                "cost_usd",
                "tasks_done",
                "tasks_total",
                "commit",
                "tests",
                "errors",
            ],
        }

    if action == "debug":
        return {
            "why_stats_blank": [
                "iterations.jsonl not valid JSONL (must be 1 JSON object per line)",
                "missing required fields (iteration/status/timestamps)",
                "stale .ralph/pause or bogus .ralph/ralph.pid (e.g., '0')",
                "loop not started via ralph.sh/dashboard so no PID/log writes",
            ],
            "checklist": [
                "Project is under a scanned RALPH_PROJECT_DIRS root",
                "Project contains .ralph/ directory",
                ".ralph/ralph.pid contains a live PID when running (otherwise remove it)",
                ".ralph/pause exists only when intentionally paused",
                ".ralph/ralph.log includes iteration headers",
                ".ralph/iterations.jsonl is valid JSONL with increasing iteration numbers",
            ],
        }

    if action == "paths":
        base = Path("ralph-loop")
        return {
            "runner": str(base / "scripts" / "ralph.sh"),
            "templates": {
                "AGENTS.md": str(base / "templates" / "AGENTS.md"),
                "PROMPT.md": str(base / "templates" / "PROMPT.md"),
                "IMPLEMENTATION_PLAN.md": str(base / "templates" / "IMPLEMENTATION_PLAN.md"),
            },
        }

    return {"error": f"Unknown action: {action}", "valid_actions": ["guide", "schema", "debug", "paths"]}
