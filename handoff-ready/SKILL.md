---
name: handoff-ready
description: Generate standardized handoff summaries that preserve full working context (not just the last ask) when a thread gets long, tool-heavy, or reaches a milestone. Use for context-overflow prevention and smooth /new thread transitions.
user-invocable: true
---

# Handoff Ready

Generate a consistent handoff block that captures the **entire practical state of work** so a fresh thread can continue immediately.

## Trigger Conditions

Emit a handoff when any of these are true:

1. Major milestone completes (build/deploy/migration/feature)
2. Topic changes materially (UI → contracts, contracts → infra, etc.)
3. Tool-heavy run produces large logs/artifacts
4. Response latency/timeouts increase
5. User asks for a handoff directly (`handoff now`)

## Core Rule

Do **not** summarize only the latest request.
Always include:
- active objective,
- what changed recently,
- current system state,
- open risks,
- exact next action.

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

## Expanded Context Requirements (mandatory)

When the session involves engineering/project work, ensure the handoff captures all applicable categories:

1. **Code & Git State**
   - repo path, branch, latest commit(s), pushed/not pushed
2. **Deployment State**
   - services restarted? active? env vars switched?
3. **Data/Contract State**
   - active contract IDs, migration status, counts, verification results
4. **User-Visible Changes**
   - what changed in UI/behavior and what still looks wrong
5. **Validation Evidence**
   - tests run, build status, screenshot paths/artifacts
6. **Known Risks / Partials**
   - flaky checks, race conditions, pending manual confirmations
7. **Immediate Operator Action**
   - one exact command/action to start with

If any category is unknown, write `unknown` explicitly.

## Formatting Rules

- Keep concise and operational; avoid narrative fluff.
- Include concrete identifiers when relevant: commit SHA, branch, service name, contract ID, migration report path.
- Keep `PASTE INTO /new` under ~1200 characters.
- Never omit `RUN THIS FIRST`.

## Quality Bar

Before sending, verify:

- A fresh operator can continue work from only this handoff.
- The first step is actionable without extra clarification.
- Blockers are explicit and non-ambiguous.
- The handoff reflects **full current context**, not a narrow recap.
