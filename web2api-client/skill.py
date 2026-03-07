#!/usr/bin/env python3
"""Web2API client helper functions."""

from __future__ import annotations

from pathlib import Path

import httpx

BASE_URL = "http://localhost:8020"


def _client(timeout: float = 90.0) -> httpx.Client:
    return httpx.Client(timeout=timeout)


def health() -> dict:
    """Return service health payload."""
    with _client(30.0) as client:
        response = client.get(f"{BASE_URL}/health")
        response.raise_for_status()
        return response.json()


def list_sites() -> list[dict]:
    """List all installed Web2API recipes/sites."""
    with _client() as client:
        response = client.get(f"{BASE_URL}/api/sites")
        response.raise_for_status()
        return response.json()


def scrape(slug: str, endpoint: str, page: int = 1, query: str | None = None, **extra_params) -> dict:
    """Scrape data from a recipe endpoint via GET /{slug}/{endpoint}."""
    params = {"page": page}
    if query:
        params["q"] = query
    params.update(extra_params)

    with _client() as client:
        response = client.get(f"{BASE_URL}/{slug}/{endpoint}", params=params)
        response.raise_for_status()
        return response.json()


def scrape_with_files(
    slug: str,
    endpoint: str,
    file_paths: list[str | Path],
    page: int = 1,
    query: str | None = None,
    **extra_params,
) -> dict:
    """Scrape via POST multipart with files[] uploads."""
    params = {"page": page}
    if query:
        params["q"] = query
    params.update(extra_params)

    files_payload = []
    handles = []
    try:
        for p in file_paths:
            handle = open(Path(p), "rb")
            handles.append(handle)
            files_payload.append(("files", (Path(p).name, handle, "application/octet-stream")))

        with _client(120.0) as client:
            response = client.post(f"{BASE_URL}/{slug}/{endpoint}", params=params, files=files_payload)
            response.raise_for_status()
            return response.json()
    finally:
        for handle in handles:
            handle.close()


def list_catalog() -> list[dict]:
    """List available recipes from catalog."""
    with _client(30.0) as client:
        response = client.get(f"{BASE_URL}/api/recipes/manage")
        response.raise_for_status()
        return response.json().get("catalog", [])


def list_installed() -> list[dict]:
    """List installed recipes."""
    with _client(30.0) as client:
        response = client.get(f"{BASE_URL}/api/recipes/manage")
        response.raise_for_status()
        return response.json().get("installed", [])


def install_recipe(name: str) -> dict:
    with _client(60.0) as client:
        response = client.post(f"{BASE_URL}/api/recipes/manage/install/{name}")
        response.raise_for_status()
        return response.json()


def update_recipe(slug: str) -> dict:
    with _client(60.0) as client:
        response = client.post(f"{BASE_URL}/api/recipes/manage/update/{slug}")
        response.raise_for_status()
        return response.json()


def uninstall_recipe(slug: str, force: bool = False) -> dict:
    with _client(60.0) as client:
        response = client.post(
            f"{BASE_URL}/api/recipes/manage/uninstall/{slug}",
            params={"force": str(force).lower()},
        )
        response.raise_for_status()
        return response.json()


def list_mcp_tools(only: str | None = None, exclude: str | None = None) -> list[dict]:
    """List tools exposed by the MCP HTTP bridge."""
    params = {}
    if only:
        params["only"] = only
    if exclude:
        params["exclude"] = exclude

    with _client(30.0) as client:
        response = client.get(f"{BASE_URL}/mcp/tools", params=params)
        response.raise_for_status()
        return response.json()


def call_mcp_tool(tool_name: str, **params) -> dict:
    """Call MCP bridge tool by name via POST /mcp/tools/{tool_name}."""
    with _client(120.0) as client:
        response = client.post(f"{BASE_URL}/mcp/tools/{tool_name}", json=params)
        response.raise_for_status()
        return response.json()


if __name__ == "__main__":
    print("Health:", health().get("status"))
    sites = list_sites()
    print(f"Installed sites: {len(sites)}")
    tools = list_mcp_tools()
    print(f"MCP bridge tools: {len(tools)}")
