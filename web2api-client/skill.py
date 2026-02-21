#!/usr/bin/env python3
"""Web2API client helper functions."""

import httpx

BASE_URL = "http://localhost:8020"


def list_sites():
    """List all available Web2API sites/recipes."""
    response = httpx.get(f"{BASE_URL}/api/sites")
    response.raise_for_status()
    return response.json()


def scrape(slug: str, endpoint: str, page: int = 1, query: str = None, **extra_params):
    """Scrape data from a Web2API endpoint.
    
    Args:
        slug: Recipe slug (e.g., "hackernews")
        endpoint: Endpoint name (e.g., "read", "search")
        page: Page number (default 1)
        query: Search query (required if endpoint needs it)
        **extra_params: Additional recipe-specific parameters
        
    Returns:
        Scraped data response dict
    """
    params = {"page": page}
    if query:
        params["q"] = query
    params.update(extra_params)
    
    response = httpx.get(f"{BASE_URL}/{slug}/{endpoint}", params=params, timeout=60.0)
    response.raise_for_status()
    return response.json()


def install_recipe(name: str):
    """Install a recipe from the catalog."""
    response = httpx.post(f"{BASE_URL}/api/recipes/manage/install/{name}")
    response.raise_for_status()
    return response.json()


def uninstall_recipe(slug: str):
    """Uninstall a recipe."""
    response = httpx.post(f"{BASE_URL}/api/recipes/manage/uninstall/{slug}")
    response.raise_for_status()
    return response.json()


def list_catalog():
    """List available recipes from catalog."""
    response = httpx.get(f"{BASE_URL}/api/recipes/manage")
    response.raise_for_status()
    data = response.json()
    return data.get("catalog", [])


def list_installed():
    """List installed recipes."""
    response = httpx.get(f"{BASE_URL}/api/recipes/manage")
    response.raise_for_status()
    data = response.json()
    return data.get("installed", [])


if __name__ == "__main__":
    # Example usage
    sites = list_sites()
    print(f"Available sites: {len(sites)}")
    for site in sites:
        print(f"  {site['slug']}: {site['name']}")
        for ep in site['endpoints']:
            print(f"    - {ep['name']}: {ep['description']}")
