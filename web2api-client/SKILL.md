---
name: web2api-client
description: Client for the Web2API service to scrape websites via installed recipes. Web2API turns websites into REST APIs using Playwright browser automation. Use when scraping structured data from web pages using existing recipes.
---

## Web2API Client Skill

Use Web2API to execute installed scraping recipes over HTTP.

### Service Location (this host)

- Base URL: `http://localhost:8020`
- Health: `GET /health`
- Index/UI: `GET /`
- Installed recipes: `GET /api/sites`

### Core Endpoints

- `GET /{slug}/{endpoint}` — normal scraping (`page`, `q`, plus declared endpoint params)
- `POST /{slug}/{endpoint}` — multipart scraping with `files[]` upload support
- `GET /api/recipes/manage` — catalog + installed inventory
- `POST /api/recipes/manage/install/{name}`
- `POST /api/recipes/manage/update/{slug}`
- `POST /api/recipes/manage/uninstall/{slug}` (supports `force=true`)
- `POST /api/recipes/manage/enable/{slug}` / `disable/{slug}`

### MCP Integration (Web2API 0.4.x)

Web2API now exposes recipes as MCP tools in two ways:

1) **Native MCP protocol server** (for MCP clients)
- Endpoint: `/mcp/`
- Transport: Streamable HTTP
- Tools are auto-generated from installed recipe endpoints

2) **HTTP MCP bridge** (for non-MCP clients)
- `GET /mcp/tools`
- `POST /mcp/tools/{tool_name}`
- Filters:
  - `GET /mcp/tools?only=slug1,slug2`
  - `GET /mcp/tools?exclude=slug1`
  - `GET /mcp/only/{slugs}/tools`
  - `GET /mcp/exclude/{slugs}/tools`

If recipe endpoints define `tool_name`, that custom name is used in MCP.

### Quick Usage

```bash
# List installed recipes
curl -s http://localhost:8020/api/sites | jq

# Call a scrape endpoint
curl -s "http://localhost:8020/hackernews/read?page=1" | jq '.items[0]'

# File upload scrape (multipart)
curl -s -X POST "http://localhost:8020/some-recipe/read?page=1" \
  -F "files=@/tmp/input.png" | jq

# MCP bridge: list tools
curl -s http://localhost:8020/mcp/tools | jq

# MCP bridge: call tool
curl -s -X POST http://localhost:8020/mcp/tools/hackernews__read \
  -H 'Content-Type: application/json' \
  -d '{"page":"1"}' | jq
```

### Operational Notes

- Recipe install/update/uninstall automatically refreshes the in-memory registry.
- MCP tools are rebuilt automatically when recipes change.
- `SCRAPE_TIMEOUT` defaults to `30` seconds unless overridden in service env.
- Cache behavior and browser pool health are visible in `/health`.
