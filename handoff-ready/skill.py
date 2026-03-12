#!/usr/bin/env python3
"""Generate a standardized HANDOFF_READY block."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Generate HANDOFF_READY handoff text")
    p.add_argument("--session", default="unknown")
    p.add_argument("--goal", default="unknown")
    p.add_argument("--branch", default="unknown")
    p.add_argument("--deploy", default="unknown")
    p.add_argument("--blockers", default="none")
    p.add_argument("--tldr", default="Status unknown; continue with listed next steps.")
    p.add_argument("--done", action="append", default=[])
    p.add_argument("--decisions", action="append", default=[])
    p.add_argument("--next", action="append", default=[])
    p.add_argument("--run-first", default="Review CURRENT STATE and execute NEXT STEPS[1].")
    p.add_argument("--paste", default="Continue from this handoff block and execute NEXT STEPS in order.")
    return p.parse_args()


def bullets(items: list[str], fallback: str = "- none") -> str:
    if not items:
        return fallback
    return "\n".join(f"- {x}" for x in items)


def numbered(items: list[str]) -> str:
    if not items:
        return "1) Validate current state\n2) Resolve blockers\n3) Continue implementation"
    return "\n".join(f"{i+1}) {x}" for i, x in enumerate(items))


def main() -> None:
    a = parse_args()
    now = datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M %Z")

    out = f"""TL;DR_HANDOFF: {a.tldr}

# 🧭 HANDOFF_READY
SESSION: {a.session}
DATE: {now}
GOAL: {a.goal}

DONE:
{bullets(a.done)}

DECISIONS:
{bullets(a.decisions)}

CURRENT STATE:
- branch: {a.branch}
- deploy status: {a.deploy}
- blockers: {a.blockers}

NEXT STEPS:
{numbered(a.next)}

RUN THIS FIRST:
{a.run_first}

PASTE INTO /new:
{a.paste}
"""
    print(out.strip())


if __name__ == "__main__":
    main()
