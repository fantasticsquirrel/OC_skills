---
name: multi-app-hosting
description: Set up and maintain reusable multi-application hosting on one server using reverse proxy routing, per-app internal ports, and future-proof app onboarding steps. Use when adding a new hosted app, changing nginx routes, preparing internet access, or documenting deployment topology for parallel app hosting.
---

# Multi-App Hosting Skill

1. Map current topology before changes.
   - Check running app processes and bound ports.
   - Check nginx upstream/location blocks.

2. Keep one public ingress.
   - Public: nginx on 80/443 only.
   - Private: app services on local/internal ports.

3. Add apps with predictable pattern.
   - Choose unique internal port.
   - Start app process.
   - Add nginx `upstream` and `location` route.
   - Run `nginx -t` then reload.
   - Verify local + public health.

4. Prefer safety defaults.
   - Never remove existing app routes while adding a new one.
   - Keep auth at app level and optionally at proxy level.
   - Document route, port, process command, and health URL.

5. Update documentation after every routing change.
   - Update `MULTI_APP_HOSTING_PATTERN.md` with current topology and onboarding checklist.

## Quick Commands

```bash
# Verify services
ps aux | grep -E "uvicorn|next-server|server.py" | grep -v grep

# Verify nginx config
sudo nginx -t && sudo systemctl reload nginx

# Route checks
curl -I http://95.111.254.161/
curl -I http://95.111.254.161/eoh/
```

## Current Known Routes
- `/` → OpenClaw frontend
- `/api/` → OpenClaw backend
- `/obsidian/` → OpenClaw Obsidian host
- `/eoh/` → Echoes of Hyperion
