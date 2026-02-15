"""Ralph Loop skill - dashboard-compatible runtime contract + runbook."""


def run(input: dict):
    action = input.get("action", "guide")

    if action == "guide":
        return {
            "summary": "Ralph loop file contract + control semantics for Ralph Dashboard compatibility.",
            "key_files": [
                ".ralph/ralph.log",
                ".ralph/iterations.jsonl",
                ".ralph/ralph.pid",
                ".ralph/pause",
                ".ralph/inject.md",
                ".ralph/pending-notification.txt",
                ".ralph/config.json",
            ],
            "next_steps": [
                "Ensure project contains .ralph/ directory",
                "Emit iteration headers in .ralph/ralph.log",
                "Append one JSON object per line to .ralph/iterations.jsonl",
                "Implement pause/inject checks between iterations",
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
            "checklist": [
                "Project is under a scanned RALPH_PROJECT_DIRS root",
                "Project contains .ralph/ directory",
                ".ralph/ralph.pid exists and PID is live (or clear it)",
                ".ralph/ralph.log is being appended",
                ".ralph/iterations.jsonl is valid JSONL (one JSON per line)",
            ]
        }

    return {"error": f"Unknown action: {action}", "valid_actions": ["guide", "schema", "debug"]}
