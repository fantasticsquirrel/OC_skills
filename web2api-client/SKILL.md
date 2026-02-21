## Web2API Client Skill

Use the Web2API service to scrape websites via installed recipes. Web2API turns websites into REST APIs using Playwright browser automation and YAML recipe definitions.

### Service Location

**Production:** `http://localhost:8020` (systemd service)  
**Health:** `GET /health`  
**Docs:** `GET /` (HTML recipe index)

### Core Concepts

- **Recipe**: A site integration with scraping rules (`recipe.yaml` + optional `scraper.py`)
- **Slug**: Unique recipe identifier (e.g., `hackernews`, `reddit`)
- **Endpoint**: Named scrape action (e.g., `read`, `search`, `latest`)
- **Catalog**: Official recipe repository at `https://github.com/Endogen/web2api-recipes.git`

### Discovery Endpoints

**List all installed recipes:**
```bash
curl http://localhost:8020/api/sites | jq
```

Response includes:
- `slug`: recipe identifier
- `name`: human-readable name
- `base_url`: target website
- `endpoints[]`: array of available endpoints
  - `name`: endpoint identifier
  - `description`: what it does
  - `requires_query`: whether `q` param is mandatory
  - `url_template`: example request path

**Recipe management UI/API:**
```bash
curl http://localhost:8020/api/recipes/manage | jq
```

Shows:
- `catalog[]`: available recipes from catalog source
- `installed[]`: currently installed recipes with status

### Scraping Endpoints

All scrape endpoints follow: `GET /{slug}/{endpoint}`

**Common parameters:**
- `page` (int, default 1): Pagination page number
- `q` (string): Search query (required if `requires_query: true`)

**Example requests:**
```bash
# Browse Hacker News front page (page 1)
curl "http://localhost:8020/hackernews/read?page=1" | jq

# Search Reddit (requires query)
curl "http://localhost:8020/reddit/search?q=python&page=1" | jq

# Get latest articles
curl "http://localhost:8020/news/latest?page=1" | jq
```

**Response schema:**
```json
{
  "site": {
    "name": "Hacker News",
    "slug": "hackernews",
    "url": "https://news.ycombinator.com"
  },
  "endpoint": "read",
  "query": null,
  "items": [
    {
      "title": "Example Title",
      "url": "https://example.com",
      "fields": {
        "score": 153,
        "author": "pg",
        "comments": 42
      }
    }
  ],
  "pagination": {
    "current_page": 1,
    "has_next": true,
    "has_prev": false,
    "total_pages": null,
    "total_items": null
  },
  "metadata": {
    "scraped_at": "2026-02-22T00:15:34Z",
    "response_time_ms": 1832,
    "item_count": 30,
    "cached": false
  },
  "error": null
}
```

### Recipe Management

**List available recipes from catalog:**
```bash
curl http://localhost:8020/api/recipes/manage | jq '.catalog'
```

**Install recipe:**
```bash
curl -X POST http://localhost:8020/api/recipes/manage/install/hackernews
```

**Update installed recipe:**
```bash
curl -X POST http://localhost:8020/api/recipes/manage/update/hackernews
```

**Uninstall recipe:**
```bash
curl -X POST http://localhost:8020/api/recipes/manage/uninstall/hackernews
```

**Enable/disable recipe:**
```bash
curl -X POST http://localhost:8020/api/recipes/manage/enable/hackernews
curl -X POST http://localhost:8020/api/recipes/manage/disable/hackernews
```

### CLI Management (via systemd)

**List installed recipes:**
```bash
sudo -u www-data /opt/web2api/.venv/bin/web2api recipes list
```

**Browse catalog:**
```bash
sudo -u www-data /opt/web2api/.venv/bin/web2api recipes catalog list
```

**Install from catalog:**
```bash
sudo -u www-data /opt/web2api/.venv/bin/web2api recipes catalog add hackernews --yes
```

**Check recipe health:**
```bash
sudo -u www-data /opt/web2api/.venv/bin/web2api recipes doctor hackernews
```

**Update recipe:**
```bash
sudo -u www-data /opt/web2api/.venv/bin/web2api recipes update hackernews --yes
```

**Uninstall recipe:**
```bash
sudo -u www-data /opt/web2api/.venv/bin/web2api recipes uninstall hackernews --yes
```

### Error Handling

| HTTP | Code | Meaning |
|------|------|---------|
| 400 | `INVALID_PARAMS` | Missing required `q` or invalid params |
| 404 | — | Unknown recipe or endpoint |
| 502 | `SCRAPE_FAILED` | Browser/upstream failure |
| 504 | `SCRAPE_TIMEOUT` | Scrape exceeded timeout |

**Example error response:**
```json
{
  "site": { "slug": "x", "name": "X", "url": "https://x.com" },
  "endpoint": "read",
  "query": null,
  "items": [],
  "pagination": { "current_page": 1, "has_next": false, "has_prev": false },
  "metadata": { "scraped_at": "2026-02-22T00:15:34Z", "item_count": 0 },
  "error": "SCRAPE_FAILED: Navigation timeout exceeded"
}
```

### Caching

- Responses are cached in-memory by `(slug, endpoint, page, q, extra_params)`
- Default TTL: 30 seconds fresh, 120 seconds stale-while-revalidate
- Cache hits include `metadata.cached: true`
- Stale entries serve immediately while background refresh updates cache

### Configuration

Service environment (systemd):
- `RECIPES_DIR=/var/lib/web2api/recipes` (persistent recipe storage)
- `CACHE_TTL_SECONDS=30` (fresh cache duration)
- `CACHE_STALE_TTL_SECONDS=120` (stale-while-revalidate window)
- `SCRAPE_TIMEOUT=30` (overall scrape timeout in seconds)
- `POOL_MAX_CONTEXTS=5` (max browser contexts)

### Workflow: Using a Recipe

1. **Discover available recipes:**
   ```bash
   curl http://localhost:8020/api/sites | jq -r '.[] | "\(.slug): \(.name) — \(.base_url)"'
   ```

2. **Check recipe endpoints:**
   ```bash
   curl http://localhost:8020/api/sites | jq '.[] | select(.slug=="hackernews") | .endpoints'
   ```

3. **Scrape data:**
   ```bash
   curl "http://localhost:8020/hackernews/read?page=1" | jq '.items[] | {title, url}'
   ```

4. **Paginate through results:**
   ```bash
   for page in {1..5}; do
     curl -s "http://localhost:8020/hackernews/read?page=$page" | jq '.items[].title'
   done
   ```

### Example Use Cases

**Monitor Hacker News front page:**
```bash
curl -s "http://localhost:8020/hackernews/read?page=1" | \
  jq '.items[] | select(.fields.score > 100) | {title, url, score: .fields.score}'
```

**Search Reddit for topics:**
```bash
curl -s "http://localhost:8020/reddit/search?q=ai+agents&page=1" | \
  jq '.items[] | {title, url, subreddit: .fields.subreddit}'
```

**Aggregate news sources:**
```bash
for slug in news tech science; do
  curl -s "http://localhost:8020/$slug/latest?page=1" | \
    jq -r '.items[] | .title'
done
```

### Service Status

```bash
# Check service health
curl http://localhost:8020/health | jq

# Check systemd status
systemctl status web2api

# View logs
journalctl -u web2api -f
```

### Notes

- Scraping respects site TOS via recipe definitions
- Some recipes require environment variables (API keys, auth tokens)
- Recipe compatibility checked against web2api version
- Browser pool limits concurrent scrapes (default 5 contexts)
- Results are snapshot-in-time (not real-time streaming)
