---
name: obsidian-knowledge-capture
description: Capture, structure, and store notes in Obsidian using a consistent PARA+MOC schema with normalized frontmatter, clean tags, and summary-first note formatting. Use when Jon asks to save, organize, or archive ideas/research/tasks into Obsidian.
---

# Obsidian Knowledge Capture

Use `OBSIDIAN_DATA_STRUCTURE_PLAYBOOK.md` as canonical guidance.

## Default Storage Workflow

1. Decide note type (`project`, `research`, `meeting`, `person`, `idea`, `task`, `reference`).
2. If uncertain, save to `00 Inbox/`; otherwise save directly in PARA folder.
3. Add standard frontmatter fields:
   - `title`, `type`, `status`, `created`, `updated`, `owner`, `source`, `tags`, `related`
4. Write summary-first content (short actionable bullets at top).
5. Add 1-3 internal links to related notes.
6. Update relevant MOC note in `90 MOCs/`.

## Folder Defaults

- `00 Inbox/`
- `10 Projects/`
- `20 Areas/`
- `30 Resources/`
- `40 Archive/`
- `90 MOCs/`
- `99 Templates/`

## Tag Defaults

- `#status/active|blocked|done`
- `#kind/research|project|meeting`
- `#domain/openclaw|eoh|family`

## Quality Bar

- Keep notes atomic.
- Keep folder depth shallow.
- Prefer links and MOCs over deeply nested folders.
- Keep tag vocabulary tight.
- Keep metadata machine-readable and consistent.
