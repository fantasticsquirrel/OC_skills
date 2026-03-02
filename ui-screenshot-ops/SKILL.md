---
name: ui-screenshot-ops
description: Deterministic visual QA and screenshot workflow for any web UI. Use when implementing or validating frontend/UI changes, reviewing before/after states, generating screenshots for user updates, or troubleshooting browser automation reliability.
---

# UI Screenshot Ops

## Default Workflow

1. Preflight
   - Confirm target URL and auth state.
   - Run a quick health check (page opens + key element visible).

2. Baseline capture
   - Capture full-page screenshot.
   - Capture focused component screenshot.

3. Apply changes

4. Post-change capture
   - Capture same full-page and same focused component.
   - Keep viewport and zoom identical.

5. Report
   - Summarize visible changes.
   - Provide screenshot paths and (if requested) send images.

## Capture Conventions

- Root folder: `/tmp/ui-captures/<project>/<YYYY-MM-DD>/`
- Filenames:
  - `before-full.png`
  - `before-component-<name>.png`
  - `after-full.png`
  - `after-component-<name>.png`

## Reliability Rules

If browser control is unstable:
1. Retry one clean browser start.
2. Fall back to repo-local Playwright capture script.
3. If still blocked, return exact blocker + next action needed.

## Minimum Evidence Standard

For any meaningful UI change, always produce at least:
- 1 full-page before/after pair
- 1 component before/after pair
