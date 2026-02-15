# obsidian_knowledge_capture

## Description

Capture, structure, and store notes in Obsidian using a consistent PARA+MOC schema with normalized frontmatter, clean tags, and summary-first note formatting.

Use when saving, organizing, or archiving ideas, research, or tasks into Obsidian.

## Input

```json
{
  "action": "capture|guide|template",
  "note_type": "project|research|meeting|person|idea|task|reference",
  "title": "Note Title",
  "content": "Note content...",
  "tags": ["tag1", "tag2"],
  "vault_path": "/path/to/vault"
}
```

**Fields:**
- `action` (string, required): Action to perform
  - `guide` - Get PARA+MOC methodology guide
  - `template` - Get note template for a type
  - `capture` - Create a new note
- `note_type` (string): Type of note (default: "idea")
- `title` (string): Note title (required for capture)
- `content` (string): Note body content
- `tags` (array): List of tags to add
- `vault_path` (string): Path to Obsidian vault (optional)

## Output

```json
{
  "file_path": "/vault/00 Inbox/Note Title.md",
  "folder": "00 Inbox",
  "frontmatter": "---\\ntitle: ...\\n---",
  "guide": "...",
  "template": "...",
  "next_steps": ["..."]
}
```

## Examples

### Get methodology guide
```json
{
  "action": "guide"
}
```

### Get note template
```json
{
  "action": "template",
  "note_type": "project"
}
```

### Capture a new idea
```json
{
  "action": "capture",
  "note_type": "idea",
  "title": "New Feature Idea",
  "content": "## Summary\\n\\nBuild a...\\n\\n## Next Steps\\n- [ ] Research\\n",
  "tags": ["kind/idea", "domain/openclaw"]
}
```

## PARA Folder Structure

- `00 Inbox/` - Unsorted new captures
- `10 Projects/` - Active projects with deliverables
- `20 Areas/` - Ongoing responsibilities
- `30 Resources/` - Reference materials
- `40 Archive/` - Completed/inactive items
- `90 MOCs/` - Maps of Content (index notes)
- `99 Templates/` - Note templates

## Standard Tags

- `#status/active|blocked|done|archived`
- `#kind/research|project|meeting|idea|task`
- `#domain/openclaw|eoh|family|tech|health`

## Quality Standards

- Atomic notes (one concept per note)
- Shallow folder depth
- Tight tag vocabulary
- Machine-readable metadata
- Summary-first formatting

## Permissions

- `filesystem` - Create and organize notes in vault

## Version History

- 1.0.0 - Initial release
