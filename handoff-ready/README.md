# Handoff Ready Skill

Standardized handoff format for long or tool-heavy sessions to avoid context overflow and make `/new` transitions fast.

## What it does

- Uses a fixed `TL;DR_HANDOFF` line
- Uses a fixed `# 🧭 HANDOFF_READY` block
- Ensures every handoff includes:
  - goal
  - completed work
  - decisions
  - current state
  - next steps
  - first command/action
  - paste-ready continuation text

## Files

- `SKILL.md` — trigger + formatting contract
- `skill.yaml` — metadata
- `skill.py` — optional CLI helper to scaffold handoff text

## CLI helper

```bash
python3 skill.py \
  --session "EoH UI pass" \
  --goal "Finalize map alignment and log UX" \
  --branch main \
  --deploy "eoh active" \
  --next "Run screenshot capture" "Send results to Jon" "Prepare /new handoff"
```
