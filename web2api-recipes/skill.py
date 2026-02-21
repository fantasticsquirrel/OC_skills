#!/usr/bin/env python3
"""Web2API recipe creation helpers."""

import os
import yaml
from pathlib import Path


RECIPE_TEMPLATE = """name: "{name}"
slug: "{slug}"
base_url: "{base_url}"
description: "{description}"

endpoints:
  read:
    description: "Browse {name}"
    url: "{base_url}/page/{{page}}"
    actions:
      - type: wait
        selector: ".item"
        timeout: 10000
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
      step: 1
"""

SCRAPER_TEMPLATE = '''"""Custom scraper for {slug}."""

from playwright.async_api import Page
from web2api.scraper import BaseScraper, ScrapeResult


class Scraper(BaseScraper):
    def supports(self, endpoint: str) -> bool:
        """Declare which endpoints use custom scraping."""
        return endpoint in {{"read", "search"}}

    async def scrape(
        self,
        endpoint: str,
        page: Page,
        params: dict
    ) -> ScrapeResult:
        """Custom scrape logic."""
        # Navigate (page is blank)
        await page.goto("{base_url}")
        
        # Wait for content
        await page.wait_for_selector(".item", timeout=10000)
        
        # Extract data
        items = []
        results = await page.query_selector_all(".item")
        for result in results:
            title_el = await result.query_selector("h2")
            link_el = await result.query_selector("a")
            items.append({{
                "title": await title_el.text_content() if title_el else None,
                "url": await link_el.get_attribute("href") if link_el else None,
                "fields": {{}}
            }})
        
        # Pagination
        next_btn = await page.query_selector("a.next")
        has_next = next_btn is not None
        
        return ScrapeResult(
            items=items,
            current_page=params["page"],
            has_next=has_next,
            has_prev=params["page"] > 1,
        )
'''

README_TEMPLATE = """## {name} Recipe

Scrapes {base_url}

### Endpoints

- `read` — Browse {name} pages

### Usage

```bash
curl "http://localhost:8020/{slug}/read?page=1" | jq
```

### Setup

No special requirements.

### Notes

Generated from Web2API recipe template.
"""


def create_recipe(
    slug: str,
    name: str,
    base_url: str,
    description: str = None,
    recipes_dir: str = "/var/lib/web2api/recipes",
    include_scraper: bool = False
):
    """Create a new Web2API recipe skeleton.
    
    Args:
        slug: Recipe identifier (lowercase, alphanumeric + hyphens)
        name: Human-readable name
        base_url: Target website URL
        description: Optional description
        recipes_dir: Recipes directory path
        include_scraper: Whether to generate scraper.py template
    """
    recipe_path = Path(recipes_dir) / slug
    recipe_path.mkdir(parents=True, exist_ok=True)
    
    # recipe.yaml
    desc = description or f"Scrapes {name}"
    recipe_yaml = RECIPE_TEMPLATE.format(
        name=name,
        slug=slug,
        base_url=base_url,
        description=desc
    )
    (recipe_path / "recipe.yaml").write_text(recipe_yaml)
    print(f"Created {recipe_path}/recipe.yaml")
    
    # README.md
    readme = README_TEMPLATE.format(
        name=name,
        base_url=base_url,
        slug=slug
    )
    (recipe_path / "README.md").write_text(readme)
    print(f"Created {recipe_path}/README.md")
    
    # Optional scraper.py
    if include_scraper:
        scraper = SCRAPER_TEMPLATE.format(slug=slug, base_url=base_url)
        (recipe_path / "scraper.py").write_text(scraper)
        print(f"Created {recipe_path}/scraper.py")
    
    print(f"\\nRecipe created at {recipe_path}")
    print(f"\\nNext steps:")
    print(f"1. Edit {recipe_path}/recipe.yaml with correct selectors")
    print(f"2. Test scraping: systemctl restart web2api")
    print(f"3. Verify: curl http://localhost:8020/api/sites | jq '.[] | select(.slug==\\"{slug}\\")'")


def validate_recipe(recipe_path: str):
    """Validate a recipe.yaml file."""
    with open(recipe_path) as f:
        data = yaml.safe_load(f)
    
    required = ["name", "slug", "base_url", "endpoints"]
    for field in required:
        if field not in data:
            raise ValueError(f"Missing required field: {field}")
    
    if not data["endpoints"]:
        raise ValueError("At least one endpoint required")
    
    for ep_name, ep in data["endpoints"].items():
        if "url" not in ep:
            raise ValueError(f"Endpoint '{ep_name}' missing URL")
        if "items" not in ep:
            raise ValueError(f"Endpoint '{ep_name}' missing items config")
        if "pagination" not in ep:
            raise ValueError(f"Endpoint '{ep_name}' missing pagination config")
    
    print("Recipe validation passed ✓")
    return data


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 4:
        print("Usage: python skill.py <slug> <name> <base_url> [--with-scraper]")
        print("Example: python skill.py mysite 'My Site' https://example.com")
        sys.exit(1)
    
    slug = sys.argv[1]
    name = sys.argv[2]
    base_url = sys.argv[3]
    include_scraper = "--with-scraper" in sys.argv
    
    create_recipe(slug, name, base_url, include_scraper=include_scraper)
