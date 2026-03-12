---
name: handoff-ready
description: Generate standardized handoff summaries when a thread gets long, tool-heavy, or reaches a milestone. Use for context-overflow prevention and smooth /new thread transitions with a fixed, easy-to-scan format.
---

# Handoff Ready

Generate a consistent handoff block when context risk or workflow boundaries appear.

## Trigger Conditions

Emit a handoff when any of these are true:

1. Major milestone completes (build/deploy/migration/feature)
2. Topic changes materially (e.g., UI → contracts)
3. Tool-heavy run produces large logs/artifacts
4. Response latency/timeouts increase
5. User asks for a handoff directly

## Output Contract (always exact order)

Use this exact structure every time:

```text
TL;DR_HANDOFF: <single-line status + immediate next action>

# 🧭 HANDOFF_READY
SESSION: <short session name>
DATE: <yyyy-mm-dd hh:mm tz>
GOAL: <current objective>

DONE:
- ...
- ...

DECISIONS:
- ...
- ...

CURRENT STATE:
- branch: <branch>
- deploy status: <status>
- blockers: <none|details>

NEXT STEPS:
1) ...
2) ...
3) ...

RUN THIS FIRST:
<single best first command or action>

PASTE INTO /new:
<compact paragraph containing only what is needed to continue>
```

## Formatting Rules

- Keep concise and operational; avoid narrative fluff.
- Include concrete identifiers when relevant: commit SHA, branch, service name, contract ID, migration report path.
- If unknown, write `unknown` explicitly.
- Keep `PASTE INTO /new` under ~1200 characters.
- Never omit `RUN THIS FIRST`.

## Quality Bar

Before sending, verify:

- A fresh operator can continue work from only this handoff.
- The first step is actionable without extra clarification.
- Blockers are explicit and non-ambiguous.
