## Web2API Client

Use the Web2API service to scrape websites via installed recipes.

### Quick Start

```python
import httpx

# List available recipes
response = httpx.get("http://localhost:8020/api/sites")
sites = response.json()

for site in sites:
    print(f"{site['slug']}: {site['name']}")
    for endpoint in site['endpoints']:
        print(f"  - {endpoint['name']}: {endpoint['description']}")

# Scrape Hacker News
response = httpx.get("http://localhost:8020/hackernews/read?page=1")
data = response.json()

for item in data['items']:
    print(f"{item['title']}: {item['url']}")
```

### Command Line

```bash
# Install a recipe
curl -X POST http://localhost:8020/api/recipes/manage/install/hackernews

# Scrape data
curl "http://localhost:8020/hackernews/read?page=1" | jq '.items[] | {title, url}'

# Search
curl "http://localhost:8020/reddit/search?q=python&page=1" | jq '.items[].title'
```

### Features

- **REST API** — All scraped data via HTTP GET
- **Caching** — 30s fresh + 120s stale-while-revalidate
- **Pagination** — Standard `page` parameter
- **Search** — Query parameter for search endpoints
- **Management API** — Install/update/uninstall recipes dynamically

### Service

**Production:** http://localhost:8020  
**Health:** GET /health  
**Docs:** GET / (HTML index)

See [SKILL.md](SKILL.md) for full API documentation.
