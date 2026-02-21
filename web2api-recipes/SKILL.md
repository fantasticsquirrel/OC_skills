## Web2API Recipe Creator Skill

Create Web2API scraping recipes to turn any website into a REST API. Recipes use declarative YAML for simple scraping or custom Python for interactive sites.

### Recipe Structure

```
recipes/<slug>/
  recipe.yaml      # REQUIRED - endpoint definitions
  scraper.py       # OPTIONAL - custom Python scraper
  plugin.yaml      # OPTIONAL - dependency metadata
  README.md        # OPTIONAL - documentation
```

**Rules:**
- Folder name must match `slug` in `recipe.yaml`
- `slug` must be lowercase alphanumeric + hyphens (`[a-z0-9-]+`)
- `slug` cannot be reserved routes: `api`, `health`, `docs`, `openapi`, `redoc`
- Recipes with `.disabled` file are skipped
- Invalid recipes log warnings but don't crash the service

### Basic Recipe (YAML-only)

**File:** `recipes/hackernews/recipe.yaml`

```yaml
name: "Hacker News"
slug: "hackernews"
base_url: "https://news.ycombinator.com"
description: "Scrapes Hacker News front page and search"

endpoints:
  read:
    description: "Browse front page stories"
    url: "https://news.ycombinator.com/?p={page}"
    actions:
      - type: wait
        selector: ".athing"
        timeout: 10000
    items:
      container: ".athing"
      fields:
        title:
          selector: ".titleline > a"
          attribute: "text"
        url:
          selector: ".titleline > a"
          attribute: "href"
          transform: "absolute_url"
        score:
          selector: "~ tr .score"
          attribute: "text"
          transform: "regex_int"
          context: "next_sibling"
        author:
          selector: "~ tr .hnuser"
          attribute: "text"
          context: "next_sibling"
    pagination:
      type: "page_param"
      param: "p"
      start: 1
      step: 1

  search:
    description: "Search Hacker News stories"
    requires_query: true
    url: "https://hn.algolia.com/?query={query}&page={page_zero}"
    items:
      container: ".Story_story__wG0Fq"
      fields:
        title:
          selector: ".Story_title__tPUHE"
          attribute: "text"
        url:
          selector: ".Story_title__tPUHE a"
          attribute: "href"
          transform: "absolute_url"
    pagination:
      type: "page_param"
      param: "page"
      start: 0
      step: 1
```

### Endpoint Configuration

| Field | Required | Description |
|-------|----------|-------------|
| `url` | yes | URL template with `{page}`, `{page_zero}`, `{query}` |
| `description` | no | Human-readable description |
| `requires_query` | no | If `true`, `q` parameter is mandatory (default: `false`) |
| `actions` | no | Playwright actions before extraction |
| `items` | yes | Container selector + field definitions |
| `pagination` | yes | Pagination strategy |

**URL placeholders:**
- `{page}` — Resolves to `start + ((api_page - 1) * step)`
- `{page_zero}` — Resolves to `api_page - 1` (for zero-indexed pagination)
- `{query}` — User's search query (when `requires_query: true`)

### Actions (Pre-extraction Steps)

Execute before scraping items:

**Wait for selector:**
```yaml
- type: wait
  selector: ".item"
  timeout: 10000  # optional, default 15000ms
```

**Click element:**
```yaml
- type: click
  selector: "button.load-more"
```

**Scroll page:**
```yaml
- type: scroll
  direction: down  # or up
  amount: 500      # pixels, or "bottom"
```

**Type text:**
```yaml
- type: type
  selector: "input.search"
  text: "{query}"  # can use placeholders
```

**Sleep:**
```yaml
- type: sleep
  ms: 2000
```

**Execute JavaScript:**
```yaml
- type: evaluate
  script: "window.scrollTo(0, document.body.scrollHeight)"
```

### Field Extraction

**Container:** CSS selector for each item block  
**Fields:** Named extractions from each container

**Field definition:**
```yaml
field_name:
  selector: "a.title"       # CSS selector (relative to container)
  attribute: "text"         # text | href | src | data-* | any attribute
  transform: "absolute_url" # optional transform
  context: "self"           # self | next_sibling | parent
```

**Available transforms:**
- `strip` — Remove leading/trailing whitespace
- `strip_html` — Remove HTML tags
- `regex_int` — Extract first integer (e.g., "123 points" → 123)
- `regex_float` — Extract first float (e.g., "$19.99" → 19.99)
- `iso_date` — Parse ISO 8601 date
- `absolute_url` — Convert relative URLs to absolute

**Context options:**
- `self` (default) — Selector within current item container
- `next_sibling` — Selector in next sibling element (for adjacent data)
- `parent` — Selector in parent element

### Pagination Strategies

**Page parameter (most common):**
```yaml
pagination:
  type: "page_param"
  param: "page"     # URL query param name
  start: 1          # first page number
  step: 1           # increment per page
```

**Offset parameter:**
```yaml
pagination:
  type: "offset_param"
  param: "offset"
  start: 0
  step: 25          # items per page
```

**Next link (follow "Next" button):**
```yaml
pagination:
  type: "next_link"
  selector: "a.next-page"
  attribute: "href"
```

### Custom Python Scraper

For interactive sites (login, dynamic content, complex flows):

**File:** `recipes/example/scraper.py`

```python
from playwright.async_api import Page
from web2api.scraper import BaseScraper, ScrapeResult


class Scraper(BaseScraper):
    def supports(self, endpoint: str) -> bool:
        """Declare which endpoints use custom scraping."""
        return endpoint in {"search", "profile"}

    async def scrape(
        self,
        endpoint: str,
        page: Page,
        params: dict
    ) -> ScrapeResult:
        """
        Custom scrape logic.
        
        Args:
            endpoint: endpoint name (e.g., "search")
            page: blank Playwright page (must call page.goto yourself)
            params: {
                "page": int (always present),
                "query": str | None (when requires_query=true),
                ...extra validated query params
            }
        
        Returns:
            ScrapeResult with items, current_page, has_next, etc.
        """
        # Navigate (page is blank)
        await page.goto(f"https://example.com/search?q={params['query']}")
        
        # Wait for dynamic content
        await page.wait_for_selector(".result", timeout=10000)
        
        # Interact with page
        load_more = await page.query_selector("button.load-more")
        if load_more:
            await load_more.click()
            await page.wait_for_timeout(1000)
        
        # Extract data
        results = await page.query_selector_all(".result")
        items = []
        for result in results:
            title = await result.query_selector("h3")
            link = await result.query_selector("a")
            items.append({
                "title": await title.text_content() if title else None,
                "url": await link.get_attribute("href") if link else None,
                "fields": {
                    "source": "custom_scraper"
                }
            })
        
        # Return pagination info
        next_btn = await page.query_selector("a.next-page")
        has_next = next_btn is not None
        
        return ScrapeResult(
            items=items,
            current_page=params["page"],
            has_next=has_next,
            has_prev=params["page"] > 1,
            total_pages=None,  # optional
            total_items=None   # optional
        )
```

**Notes:**
- `supports(endpoint)` returns `True` for custom-scraped endpoints
- Endpoints not in `supports()` fall back to YAML declarative extraction
- `page` is always blank — you must call `page.goto()` yourself
- `params` always contains `page` (int) and `query` (str | None)
- Extra query params are validated and passed through

### Plugin Metadata (Optional)

Declare runtime requirements:

**File:** `recipes/example/plugin.yaml`

```yaml
version: "1.0.0"
web2api:
  min: "0.2.0"  # minimum compatible web2api version
  max: "1.0.0"  # maximum compatible version

requires_env:
  - EXAMPLE_API_KEY
  - EXAMPLE_AUTH_TOKEN

dependencies:
  commands:
    - jq
    - curl
  python:
    - httpx
    - beautifulsoup4
  apt:
    - nodejs
  npm:
    - "@example/tool"

healthcheck:
  command: ["curl", "--version"]
```

**Version compatibility:**
- Uses numeric `major.minor.patch` comparison
- Set `PLUGIN_ENFORCE_COMPATIBILITY=true` to skip incompatible recipes

**Dependency installation:**
```bash
# Install Python dependencies only
web2api recipes install <slug> --yes

# Include apt packages (requires sudo/root)
web2api recipes install <slug> --apt --yes

# Generate Dockerfile snippet instead
web2api recipes install <slug> --target docker --apt
```

### Example: Multi-Endpoint Recipe

```yaml
name: "Reddit"
slug: "reddit"
base_url: "https://www.reddit.com"
description: "Reddit scraper with browse and search"

endpoints:
  popular:
    description: "Browse r/popular"
    url: "https://www.reddit.com/r/popular/"
    actions:
      - type: wait
        selector: "shreddit-post"
        timeout: 10000
    items:
      container: "shreddit-post"
      fields:
        title:
          selector: "a[slot='title']"
          attribute: "text"
        url:
          selector: "a[slot='title']"
          attribute: "href"
          transform: "absolute_url"
        subreddit:
          selector: "a[slot='subreddit-prefixed-name']"
          attribute: "text"
        score:
          selector: "shreddit-post"
          attribute: "score"
          transform: "regex_int"
    pagination:
      type: "next_link"
      selector: "faceplate-partial[loading] a[href*='after=']"
      attribute: "href"

  search:
    description: "Search Reddit"
    requires_query: true
    url: "https://www.reddit.com/search/?q={query}&type=link"
    items:
      container: "shreddit-post"
      fields:
        title:
          selector: "a[slot='title']"
          attribute: "text"
        url:
          selector: "a[slot='title']"
          attribute: "href"
          transform: "absolute_url"
    pagination:
      type: "next_link"
      selector: "faceplate-partial[loading] a[href*='after=']"
      attribute: "href"
```

### Testing a Recipe

1. **Create recipe folder:**
   ```bash
   mkdir -p /var/lib/web2api/recipes/mysite
   ```

2. **Write `recipe.yaml`** (see examples above)

3. **Restart service to reload:**
   ```bash
   systemctl restart web2api
   ```

4. **Verify discovery:**
   ```bash
   curl http://localhost:8020/api/sites | jq '.[] | select(.slug=="mysite")'
   ```

5. **Test scraping:**
   ```bash
   curl "http://localhost:8020/mysite/read?page=1" | jq
   ```

6. **Check logs for errors:**
   ```bash
   journalctl -u web2api -f
   ```

### Recipe Development Workflow

1. **Inspect target site:**
   - Use browser DevTools to find CSS selectors
   - Check pagination pattern (URL params, next links, infinite scroll)
   - Test selectors in browser console: `document.querySelectorAll('.item')`

2. **Start with minimal YAML:**
   ```yaml
   name: "My Site"
   slug: "mysite"
   base_url: "https://example.com"
   endpoints:
     read:
       url: "https://example.com/page/{page}"
       items:
         container: ".item"
         fields:
           title:
             selector: "h2"
             attribute: "text"
       pagination:
         type: "page_param"
         param: "page"
         start: 1
   ```

3. **Test and iterate:**
   - Add fields one at a time
   - Test transforms on sample data
   - Verify pagination works across pages

4. **Add complexity as needed:**
   - Actions for dynamic content
   - Custom scraper for interactions
   - Plugin metadata for dependencies

### Common Patterns

**Waiting for AJAX content:**
```yaml
actions:
  - type: wait
    selector: ".dynamic-item"
    timeout: 15000
```

**Clicking "Load More":**
```yaml
actions:
  - type: click
    selector: "button.load-more"
  - type: sleep
    ms: 1000
```

**Extracting adjacent data:**
```yaml
fields:
  title:
    selector: "h2"
    attribute: "text"
  metadata:
    selector: "~ .meta"  # next sibling
    attribute: "text"
    context: "next_sibling"
```

**Converting relative URLs:**
```yaml
fields:
  link:
    selector: "a"
    attribute: "href"
    transform: "absolute_url"  # /path → https://example.com/path
```

**Parsing numbers from text:**
```yaml
fields:
  score:
    selector: ".points"
    attribute: "text"       # "123 points"
    transform: "regex_int"  # → 123
```

### Debugging Tips

1. **Check service logs:**
   ```bash
   journalctl -u web2api -f
   ```

2. **Validate YAML syntax:**
   ```bash
   python3 -c "import yaml; yaml.safe_load(open('recipe.yaml'))"
   ```

3. **Test selectors in browser console:**
   ```javascript
   document.querySelectorAll('.item').length
   document.querySelector('.item h2').textContent
   ```

4. **Use health check:**
   ```bash
   curl http://localhost:8020/health | jq
   ```

5. **Inspect raw response:**
   ```bash
   curl "http://localhost:8020/mysite/read?page=1" | jq .
   ```

### Recipe Best Practices

- ✅ Use specific CSS selectors (`.post-title` not just `.title`)
- ✅ Add `wait` actions for dynamic content
- ✅ Test pagination to verify `has_next` logic
- ✅ Use transforms to normalize data types
- ✅ Document required env vars in `plugin.yaml`
- ✅ Include `README.md` with setup instructions
- ❌ Don't use brittle selectors (nth-child, positions)
- ❌ Don't scrape login-required content without auth handling
- ❌ Don't violate site TOS or robots.txt

### Publishing to Catalog

To contribute recipes to the official catalog:

1. Fork `https://github.com/Endogen/web2api-recipes`
2. Add your recipe to `recipes/<slug>/`
3. Add catalog entry to `catalog.yaml`:
   ```yaml
   - name: mysite
     slug: mysite
     description: "Description of the site scraper"
     path: recipes/mysite
     requires_env:
       - MYSITE_API_KEY
     docs_url: https://github.com/you/web2api-recipes/blob/main/recipes/mysite/README.md
   ```
4. Submit pull request

### Local-Only Recipes

To use recipes without publishing:

```bash
# Install from local path
web2api recipes add ./my-custom-recipe --yes

# Or copy directly
cp -r ./my-custom-recipe /var/lib/web2api/recipes/

# Restart to discover
systemctl restart web2api
```

Local recipes show as `origin: unmanaged` in `/api/recipes/manage`.
