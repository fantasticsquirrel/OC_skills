---
name: chore-shortcode
description: Add or update chores in the hosted Chore Tracker from Jon-style shortcode lines like "task" .25 ew1 sh sa av t3. Use when receiving compact chore entries with reward/schedule/completion/assignment/kid/timeout/expiry tokens and you need to create chores quickly and consistently.
---

# Chore Shortcode

Use deterministic parsing for chore lines and write directly to the hosted tracker DB.

## Canonical format

`"<task name>" .<dollars> <schedule> <completion> <assignment> <kids> [tN] [xYYYY-MM-DD]`

Examples:
- `"gather eggs" .15 ed1 sh sa av t1`
- `"clean upstairs bathroom toilet and sink" .4 ew1 pc ro av t3`

## Token mapping

- Reward: `.15` => 15 cents, `.4` => 40 cents, `.25` => 25 cents
- Schedule:
  - `sn` => `NONE`
  - `so` => `ONCE`
  - `edN` => `EVERY` + `N DAY`
  - `ewN` => `EVERY` + `N WEEK`
  - `emN` => `EVERY` + `N MONTH`
  - `adN` => `AFTER_COMPLETION` + `N DAY`
  - `awN` => `AFTER_COMPLETION` + `N WEEK`
- Completion:
  - `pc` => `PER_CHILD`
  - `sh` => `SHARED`
- Assignment:
  - `sa` => `STATIC`
  - `ro` => `ROTATING`
- Kids token: letters `a/v/w` in any combo (`av`, `avw`, `vw`)
- Optional timeout: `tN` => `timeout_days=N`
- Optional expiry: `xYYYY-MM-DD` => `expires_at`

## Execution

Run:

`python3 scripts/add_chore_shortcode.py --household 1 --line '"task" .25 ew1 sh sa av t3'`

Batch input:

`python3 scripts/add_chore_shortcode.py --household 1 --line '"task1" ...' --line '"task2" ...'`

Or:

`python3 scripts/add_chore_shortcode.py --household 1 --file /tmp/chores.txt`

Default DB path is `/var/ralph-projects/chore_tracking/data/chore_tracking.db`.

## Behavior rules

- Create missing children `A`, `V`, `W` in target household when referenced.
- Insert chore into `chores` and attach targeted kids in `chore_allowed_children`.
- For `RO`, also populate `chore_rotation_members` and `chore_rotation_state`.
- Do not archive/modify existing chores unless user explicitly asks to update/replace.
- After writes, report created chore IDs and parsed fields.
