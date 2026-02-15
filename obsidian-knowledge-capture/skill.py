"""
Obsidian knowledge capture skill - structured note-taking with PARA+MOC schema.
"""

import json
from datetime import datetime
from pathlib import Path


def run(input):
    """
    Capture and structure notes in Obsidian using PARA+MOC methodology.
    
    Input:
    - action: "capture" (create note), "guide" (get methodology), "template" (get note template)
    - note_type: "project|research|meeting|person|idea|task|reference"
    - title: Note title
    - content: Note body
    - tags: List of tags
    - vault_path: Path to Obsidian vault (optional)
    
    Output:
    - file_path: Created note path
    - frontmatter: Generated YAML frontmatter
    - guide: Methodology guide (if action=guide)
    """
    
    action = input.get("action", "guide")
    
    if action == "guide":
        return {
            "guide": get_methodology_guide(),
            "folder_structure": get_folder_structure(),
            "tag_vocabulary": get_tag_vocabulary()
        }
    
    elif action == "template":
        note_type = input.get("note_type", "idea")
        return {
            "template": get_note_template(note_type),
            "frontmatter_fields": [
                "title", "type", "status", "created", "updated", 
                "owner", "source", "tags", "related"
            ]
        }
    
    elif action == "capture":
        note_type = input.get("note_type", "idea")
        title = input.get("title", "Untitled")
        content = input.get("content", "")
        tags = input.get("tags", [])
        vault_path = input.get("vault_path", "/root/obsidian-vault")
        
        # Determine folder
        folder = get_folder_for_type(note_type)
        
        # Generate frontmatter
        frontmatter = generate_frontmatter(title, note_type, tags)
        
        # Construct full note
        note_content = f"{frontmatter}\n\n{content}"
        
        # Generate filename
        filename = sanitize_filename(title) + ".md"
        file_path = f"{vault_path}/{folder}/{filename}"
        
        return {
            "file_path": file_path,
            "folder": folder,
            "frontmatter": frontmatter,
            "content_preview": note_content[:200],
            "next_steps": [
                "Review and edit the note in Obsidian",
                "Add internal links to related notes",
                "Update relevant MOC in 90 MOCs/"
            ]
        }
    
    else:
        return {
            "error": f"Unknown action: {action}",
            "valid_actions": ["guide", "template", "capture"]
        }


def get_methodology_guide():
    """Return PARA+MOC methodology guide."""
    return """
# Obsidian Knowledge Capture Methodology

## PARA Framework

- **Projects** (10 Projects/) - Active work with defined outcomes
- **Areas** (20 Areas/) - Ongoing responsibilities
- **Resources** (30 Resources/) - Reference materials
- **Archive** (40 Archive/) - Completed or inactive items

## MOC (Map of Content) Strategy

Create index notes in `90 MOCs/` to connect related notes.
Prefer shallow folder hierarchies + MOCs over deep nesting.

## Capture Workflow

1. Decide note type (project, research, meeting, person, idea, task, reference)
2. Save to Inbox (00 Inbox/) if uncertain, or direct to PARA folder
3. Add standard frontmatter
4. Write summary-first content (actionable bullets at top)
5. Add 1-3 internal links
6. Update relevant MOC

## Quality Standards

- Atomic notes (one concept per note)
- Shallow folder depth
- Tight tag vocabulary
- Machine-readable metadata
- Summary-first formatting
"""


def get_folder_structure():
    """Return standard folder structure."""
    return {
        "00 Inbox": "Unsorted new captures",
        "10 Projects": "Active projects with deliverables",
        "20 Areas": "Ongoing responsibilities",
        "30 Resources": "Reference materials",
        "40 Archive": "Completed/inactive items",
        "90 MOCs": "Maps of Content (index notes)",
        "99 Templates": "Note templates"
    }


def get_tag_vocabulary():
    """Return standard tag sets."""
    return {
        "status": ["active", "blocked", "done", "archived"],
        "kind": ["research", "project", "meeting", "idea", "task"],
        "domain": ["openclaw", "eoh", "family", "tech", "health"]
    }


def get_folder_for_type(note_type):
    """Map note type to PARA folder."""
    mapping = {
        "project": "10 Projects",
        "area": "20 Areas",
        "research": "30 Resources",
        "reference": "30 Resources",
        "meeting": "10 Projects",
        "person": "30 Resources",
        "idea": "00 Inbox",
        "task": "10 Projects"
    }
    return mapping.get(note_type, "00 Inbox")


def generate_frontmatter(title, note_type, tags):
    """Generate YAML frontmatter."""
    now = datetime.now().isoformat()
    
    frontmatter_data = {
        "title": title,
        "type": note_type,
        "status": "active",
        "created": now,
        "updated": now,
        "owner": "Jon",
        "tags": tags if tags else [f"kind/{note_type}"]
    }
    
    lines = ["---"]
    for key, value in frontmatter_data.items():
        if isinstance(value, list):
            lines.append(f"{key}:")
            for item in value:
                lines.append(f"  - {item}")
        else:
            lines.append(f"{key}: {value}")
    lines.append("---")
    
    return "\\n".join(lines)


def get_note_template(note_type):
    """Return note template for given type."""
    templates = {
        "project": """
## Summary
[One-line project goal]

## Status
- Current phase:
- Next milestone:
- Blockers:

## Tasks
- [ ] Task 1
- [ ] Task 2

## Notes
[Detailed notes]

## Links
- [[Related Note 1]]
- [[Related Note 2]]
""",
        "research": """
## Key Takeaways
- Point 1
- Point 2
- Point 3

## Context
[Background and source]

## Details
[Full research notes]

## Related
- [[Related Topic 1]]
- [[Related Topic 2]]
""",
        "idea": """
## The Idea
[Quick summary]

## Why This Matters
[Value proposition]

## Next Steps
- [ ] Action 1
- [ ] Action 2

## References
- [[Related Idea]]
"""
    }
    
    return templates.get(note_type, templates["idea"])


def sanitize_filename(title):
    """Convert title to safe filename."""
    # Remove/replace unsafe characters
    safe = title.replace("/", "-").replace("\\\\", "-").replace(":", "-")
    # Remove leading/trailing spaces and dots
    safe = safe.strip(". ")
    # Limit length
    if len(safe) > 100:
        safe = safe[:100]
    return safe if safe else "untitled"
