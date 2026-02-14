OpenClaw Skills Repository

This repository contains OpenClaw Skills.

Skills are modular, reusable capability units that extend OpenClaw's functionality. They enable OpenClaw to perform tasks such as interacting with APIs, automating workflows, querying services, and controlling systems.

This repository defines only skills and follows the standard OpenClaw skill format.

---

What is OpenClaw

OpenClaw is an open-source personal AI assistant platform that runs locally or on your infrastructure and can execute skills, workflows, and automations.
https://github.com/openclaw/openclaw

Skills extend OpenClaw by providing executable capabilities.

Examples of skill categories:

- API integrations
- Blockchain interaction
- File system automation
- Web interaction
- System control
- DevOps automation

---

What is a Skill

A Skill is a self-contained capability module that OpenClaw can execute.

A skill typically includes:

- Metadata
- Execution logic
- Input schema
- Output schema
- Documentation

Skills can be composed into workflows using OpenClaw workflow engines.

---

Skill Repository Scope

This repository contains ONLY:

- Skill definitions
- Skill logic
- Skill metadata
- Skill documentation

This repository does NOT contain:

- OpenClaw core engine
- Workflow engine
- OpenClaw server
- OpenClaw UI

---

Skill Directory Structure

Standard skill layout:

skills/
  skill_name/
    skill.yaml
    skill.py
    README.md
    schemas/
      input.json
      output.json
    examples/
      example.json

Each folder represents one skill.

---

Required Skill Files

Minimum required files:

skill.yaml
skill.py
README.md

Optional files:

schemas/input.json
schemas/output.json
examples/example.json

---

skill.yaml Format

Defines metadata and execution properties.

Example:

name: get_token_balance
version: 1.0.0
description: Get token balance from blockchain

author: your_name

entrypoint: skill.py

input_schema: schemas/input.json
output_schema: schemas/output.json

permissions:
  - network

Required fields:

name
version
description
entrypoint

---

skill.py Format

Defines executable logic.

Example:

def run(input):
    address = input["address"]

    balance = query_blockchain(address)

    return {
        "balance": balance
    }

Requirements:

- Must define run(input) function
- Must return JSON-serializable object
- Must not require user interaction

---

Input Schema Format

Example:

{
  "type": "object",
  "properties": {
    "address": {
      "type": "string"
    }
  },
  "required": ["address"]
}

---

Output Schema Format

Example:

{
  "type": "object",
  "properties": {
    "balance": {
      "type": "number"
    }
  }
}

---

Skill README.md Format

Each skill must include documentation.

Example:

# get_token_balance

Description:
Returns token balance.

Input:
address (string)

Output:
balance (number)

Example:
{
  "address": "0x123"
}

---

Skill Versioning

Skills use semantic versioning:

MAJOR.MINOR.PATCH

Examples:

1.0.0
1.1.0
2.0.0

Rules:

Major → breaking changes
Minor → new features
Patch → bug fixes

---

Skill Execution Model

Execution flow:

OpenClaw selects skill
OpenClaw loads skill.yaml
OpenClaw loads entrypoint
OpenClaw executes run(input)
OpenClaw receives output

---

Skill Constraints

Skills must:

- Be deterministic
- Be stateless unless explicitly required
- Return structured output
- Be secure
- Not require UI interaction

---

Skill Permissions

Skills must declare permissions if needed.

Examples:

network
filesystem
process
docker
blockchain

---

Skill Naming Rules

Skill names must:

- Use lowercase
- Use underscores
- Be descriptive

Examples:

get_balance
send_transaction
read_file
query_api

---

Adding a New Skill

Steps:

1. Create new folder:

skills/my_skill/

2. Create skill.yaml

3. Create skill.py

4. Create README.md

5. Add schemas if needed

6. Test skill

---

Skill Testing

Test locally:

from skill import run

result = run({
  "input": "example"
})

print(result)

---

Skill Best Practices

Always:

- Validate inputs
- Return structured outputs
- Handle errors gracefully
- Keep skills focused on one task

Do NOT:

- Combine unrelated tasks
- Require manual interaction
- Use hidden side effects

---

Example Skill

Directory:

skills/get_time/

skill.yaml:

name: get_time
version: 1.0.0
entrypoint: skill.py

skill.py:

import datetime

def run(input):
    return {
        "time": str(datetime.datetime.utcnow())
    }

---

Integration with OpenClaw

Skills are loaded automatically by OpenClaw when placed in skill directories.

OpenClaw core repository:
https://github.com/openclaw/openclaw

Skill directory reference:
https://github.com/openclaw/skills

Skill directory index:
https://github.com/openclaw/clawhub

---

Summary

This repository defines OpenClaw skills.

Skills provide modular, reusable capabilities.

Each skill must include:

- skill.yaml
- skill.py
- README.md

Optional:

- schemas
- examples

Skills extend OpenClaw functionality.

---

END OF FILE
