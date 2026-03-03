# Current Hosting Inventory (Live Server Reference)

Last verified: 2026-03-03
Host: `95.111.254.161`
Primary ingress: `nginx` on `:80/:443`

## Public HTTPS Routes

- `/` → OpenClaw Family Hub frontend (Next.js)
- `/api/` → OpenClaw Family Hub backend (FastAPI)
- `/eoh/` → Echoes of Hyperion
- `/ralph/` → Ralph Dashboard SPA
- `/web2api/` → Web2API service
- `/chore/` → Chore Tracker frontend (Vite static)
- `/chore-api/` → Chore Tracker backend API
- `/sdo-images/` → static SDO image files
- `/static/schumann/` → static Schumann chart files

### Route Health Snapshot

- `/` ✅
- `/api/health` ⚠️ returns `401` publicly (auth protected by app)
- `/obsidian/` ❌ currently `502` (configured in nginx but upstream not available)
- `/eoh/` ✅
- `/ralph/` ✅
- `/web2api/` ✅
- `/chore/` ✅
- `/chore-api/health` ✅

## Internal Upstreams / Ports

- `127.0.0.1:3000` → openclaw-frontend.service
- `127.0.0.1:8000` → openclaw-backend.service
- `127.0.0.1:3100` → obsidian upstream configured (currently not healthy)
- `127.0.0.1:5001` → eoh.service
- `127.0.0.1:8420` → ralph-dashboard.service
- `127.0.0.1:8020` → web2api.service
- `127.0.0.1:8501` → chore-tracker.service

## Core Services Related to Hosting

- `nginx.service` (reverse proxy)
- `openclaw-backend.service`
- `openclaw-frontend.service`
- `chore-tracker.service`
- `eoh.service`
- `ralph-dashboard.service`
- `web2api.service`
- `openclaw-gateway.service` (OpenClaw infra, local control plane)
- `postgresql@16-main.service` (database infra)

## Canonical Config Paths

- Nginx site: `/etc/nginx/sites-enabled/openclaw`
- Nginx global: `/etc/nginx/nginx.conf`
- Multi-app pattern doc: `/root/.openclaw/workspace/MULTI_APP_HOSTING_PATTERN.md`

## Notes

- `obsidian` route is configured but currently unhealthy (`502`).
- This file is intended as the quick universal reference. Update it whenever routes/services change.
