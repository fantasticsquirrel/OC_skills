## Web2API Recipe Creator

Create Web2API recipes to turn websites into REST APIs.

### Quick Start

1. **Create recipe folder:**
   ```bash
   mkdir -p /var/lib/web2api/recipes/mysite
   ```

2. **Write `recipe.yaml`:**
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
           url:
             selector: "a"
             attribute: "href"
             transform: "absolute_url"
       pagination:
         type: "page_param"
         param: "page"
         start: 1
   ```

3. **Restart service:**
   ```bash
   systemctl restart web2api
   ```

4. **Test:**
   ```bash
   curl "http://localhost:8020/mysite/read?page=1" | jq
   ```

### Recipe Types

**Declarative (YAML-only):**
- Simple scraping with CSS selectors
- Pre-built actions (wait, click, scroll)
- Automatic pagination
- Field transforms (integers, URLs, dates)

**Custom Python Scraper:**
- Interactive sites (login, dynamic content)
- Complex flows (multi-step navigation)
- Custom data processing
- Full Playwright control

### Development Workflow

1. Inspect target site with browser DevTools
2. Find CSS selectors for data containers
3. Create minimal `recipe.yaml`
4. Test and iterate
5. Add complexity (actions, custom scraper) as needed

### Examples

See [SKILL.md](SKILL.md) for:
- Complete recipe examples
- Field extraction patterns
- Pagination strategies
- Custom scraper template
- Plugin metadata format

### Testing

```bash
# Verify recipe discovered
curl http://localhost:8020/api/sites | jq '.[] | select(.slug=="mysite")'

# Test endpoint
curl "http://localhost:8020/mysite/read?page=1" | jq

# Check logs
journalctl -u web2api -f
```

### Best Practices

- Use specific CSS selectors
- Wait for dynamic content
- Test pagination logic
- Use transforms for type safety
- Document env vars in plugin.yaml
- Respect site TOS

### Publishing

Contribute to the official catalog:
https://github.com/Endogen/web2api-recipes

Or use locally without publishing (copy to `recipes/` folder).
