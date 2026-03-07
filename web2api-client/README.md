## Web2API Client

Use the Web2API service to scrape websites via installed recipes.

### Quick Start

```python
import httpx

BASE = "http://localhost:8020"

# List installed recipes
sites = httpx.get(f"{BASE}/api/sites", timeout=30).json()
for site in sites:
    print(site["slug"], "->", [e["name"] for e in site["endpoints"]])

# Scrape endpoint
data = httpx.get(f"{BASE}/hackernews/read", params={"page": 1}, timeout=90).json()
print(len(data.get("items", [])))
```

### Core API

- `GET /api/sites` — list installed recipes + endpoints
- `GET /{slug}/{endpoint}` — scrape data (supports `page`, `q`, and declared endpoint params)
- `POST /{slug}/{endpoint}` — scrape with multipart file upload (`files[]`)
- `GET /api/recipes/manage` — catalog + installed status
- `POST /api/recipes/manage/install/{name}` — install recipe
- `POST /api/recipes/manage/update/{slug}` — update recipe
- `POST /api/recipes/manage/uninstall/{slug}` — uninstall recipe
- `POST /api/recipes/manage/enable/{slug}` — enable recipe
- `POST /api/recipes/manage/disable/{slug}` — disable recipe

### MCP Support (new in Web2API 0.4.x)

- Native MCP server (Streamable HTTP): `/mcp/`
- HTTP MCP bridge for non-MCP clients:
  - `GET /mcp/tools`
  - `POST /mcp/tools/{tool_name}`
  - optional filters: `only`, `exclude`, or path-style `/mcp/only/{slugs}/tools`

Each installed recipe endpoint is automatically exposed as an MCP tool.
If an endpoint defines `tool_name` in recipe config, that custom name is used.

### Service

**Production:** `http://localhost:8020`  
**Health:** `GET /health`  
**Docs/UI:** `GET /`

See [SKILL.md](SKILL.md) for full usage + examples.
