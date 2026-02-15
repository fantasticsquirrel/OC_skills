# multi_app_hosting

## Description

Set up and maintain reusable multi-application hosting on one server using reverse proxy routing, per-app internal ports, and future-proof app onboarding steps.

Use when adding a new hosted app, changing nginx routes, preparing internet access, or documenting deployment topology for parallel app hosting.

## Input

```json
{
  "action": "guide|topology|add_app",
  "app_name": "optional-app-name",
  "port": 8080,
  "route": "/myapp/"
}
```

**Fields:**
- `action` (string, required): Action to perform
  - `guide` - Get full hosting setup guide
  - `topology` - Get current app routing map
  - `add_app` - Get steps to add a new app
- `app_name` (string, optional): Name of app being added
- `port` (number, optional): Internal port for new app (default: 8080)
- `route` (string, optional): Public route path (default: `/{app_name}/`)

## Output

```json
{
  "guide": "Multi-app hosting instructions...",
  "topology": { "/": "...", "/api/": "..." },
  "steps": ["1. ...", "2. ...", "..."],
  "next_steps": ["..."]
}
```

## Examples

### Get hosting guide
```json
{
  "action": "guide"
}
```

### Check current topology
```json
{
  "action": "topology"
}
```

### Add new app
```json
{
  "action": "add_app",
  "app_name": "myapp",
  "port": 9000,
  "route": "/myapp/"
}
```

## Permissions

- `network` - Check nginx config and test routes
- `filesystem` - Read/write nginx config files
- `process` - Verify running services

## Version History

- 1.0.0 - Initial release
