# Ralph Dashboard Skill

Monitor and control [Ralph Loop](https://ghuntley.com/ralph/) AI agent sessions via the Ralph Dashboard REST API.

## Quick Start

```python
from skill import RalphDashboardClient

# Initialize client
client = RalphDashboardClient("https://ralph.example.com")

# Login
client.login("admin", "password")

# List all projects
projects = client.list_projects()
for project in projects:
    print(f"{project['id']}: {project['status']}")

# Get project details
details = client.get_project("my-project")
print(f"Path: {details['path']}")
print(f"Status: {details['status']}")

# Check stats
stats = client.get_stats("my-project")
print(f"Iterations: {stats['iteration_count']}")
print(f"Tasks done: {stats['tasks_done']}")
print(f"Success rate: {stats['success_rate']}%")

# Process control
client.start_loop("my-project")
client.pause_loop("my-project")
client.resume_loop("my-project")
client.stop_loop("my-project")

# Inject instruction for next iteration
client.inject_instruction("my-project", "Fix the login bug before continuing")

# View recent iterations
iterations = client.get_iterations("my-project", limit=10)
for it in iterations:
    print(f"Iteration {it['number']}: {it['status']}")

# Get implementation plan
plan = client.get_plan("my-project")
print(f"Phases: {len(plan['phases'])}")
print(f"Total tasks: {plan['total_tasks']}")
```

## Command Line

```bash
# Test connection
python skill.py https://ralph.example.com admin password
```

## Features

- **Authentication** — JWT login and token refresh
- **Project management** — list, register, get details
- **Process control** — start, stop, pause, resume loops
- **Instruction injection** — send messages to the next iteration
- **Iteration tracking** — view history, stats, logs
- **Plan management** — read/update implementation plans
- **Spec management** — browse/edit spec files
- **Git history** — view commits and diffs
- **System metrics** — process stats, resource usage

## Installation

See [SKILL.md](SKILL.md) for full API reference and deployment instructions.

## Production Setup

On your server:

```bash
git clone https://github.com/fantasticsquirrel/ralph-dashboard.git
cd ralph-dashboard
./scripts/install.sh
ralph-dashboard init
ralph-dashboard service install --user --start
```

Default port: 8420  
Default credentials: set during `init`

For reverse proxy setup with nginx + TLS, see the [README](https://github.com/fantasticsquirrel/ralph-dashboard#server-setup).

## Current Deployment

**Production:** https://95.111.254.161/ralph/  
**Login:** admin / admin123  
**Projects dir:** /var/ralph-projects

## API Endpoints

See [SKILL.md](SKILL.md) for complete endpoint documentation including:

- `/api/auth/login` — authenticate
- `/api/projects` — list/register projects
- `/api/projects/{id}` — project details
- `/api/projects/{id}/stats` — statistics
- `/api/projects/{id}/start` — start loop
- `/api/projects/{id}/stop` — stop loop
- `/api/projects/{id}/pause` — pause loop
- `/api/projects/{id}/resume` — resume loop
- `/api/projects/{id}/inject` — inject instruction
- `/api/projects/{id}/iterations` — iteration history
- `/api/projects/{id}/plan` — implementation plan
- `/api/projects/{id}/specs` — spec files
- `/api/projects/{id}/git/history` — git commits

And many more — see full docs in SKILL.md.

## License

Part of the OpenClaw project.
