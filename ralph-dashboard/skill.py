#!/usr/bin/env python3
"""Ralph Dashboard API client helpers."""

import httpx
from typing import Optional, Dict, Any, List


class RalphDashboardClient:
    """Simple client for Ralph Dashboard REST API."""
    
    def __init__(self, base_url: str = "http://localhost:8420"):
        self.base_url = base_url.rstrip("/")
        self.token: Optional[str] = None
        
    def login(self, username: str, password: str) -> Dict[str, Any]:
        """Authenticate and store access token."""
        response = httpx.post(
            f"{self.base_url}/api/auth/login",
            json={"username": username, "password": password},
            timeout=10.0
        )
        response.raise_for_status()
        data = response.json()
        self.token = data["access_token"]
        return data
    
    def _headers(self) -> Dict[str, str]:
        """Get auth headers."""
        if not self.token:
            raise ValueError("Not authenticated. Call login() first.")
        return {"Authorization": f"Bearer {self.token}"}
    
    def list_projects(self) -> List[Dict[str, Any]]:
        """List all Ralph projects."""
        response = httpx.get(
            f"{self.base_url}/api/projects",
            headers=self._headers(),
            timeout=10.0
        )
        response.raise_for_status()
        return response.json()
    
    def get_project(self, project_id: str) -> Dict[str, Any]:
        """Get detailed project info."""
        response = httpx.get(
            f"{self.base_url}/api/projects/{project_id}",
            headers=self._headers(),
            timeout=10.0
        )
        response.raise_for_status()
        return response.json()
    
    def get_stats(self, project_id: str) -> Dict[str, Any]:
        """Get project statistics."""
        response = httpx.get(
            f"{self.base_url}/api/projects/{project_id}/stats",
            headers=self._headers(),
            timeout=10.0
        )
        response.raise_for_status()
        return response.json()
    
    def start_loop(self, project_id: str) -> Dict[str, Any]:
        """Start a Ralph loop."""
        response = httpx.post(
            f"{self.base_url}/api/projects/{project_id}/start",
            headers=self._headers(),
            timeout=10.0
        )
        response.raise_for_status()
        return response.json()
    
    def stop_loop(self, project_id: str) -> Dict[str, Any]:
        """Stop a Ralph loop."""
        response = httpx.post(
            f"{self.base_url}/api/projects/{project_id}/stop",
            headers=self._headers(),
            timeout=10.0
        )
        response.raise_for_status()
        return response.json()
    
    def pause_loop(self, project_id: str) -> Dict[str, Any]:
        """Pause a Ralph loop."""
        response = httpx.post(
            f"{self.base_url}/api/projects/{project_id}/pause",
            headers=self._headers(),
            timeout=10.0
        )
        response.raise_for_status()
        return response.json()
    
    def resume_loop(self, project_id: str) -> Dict[str, Any]:
        """Resume a paused Ralph loop."""
        response = httpx.post(
            f"{self.base_url}/api/projects/{project_id}/resume",
            headers=self._headers(),
            timeout=10.0
        )
        response.raise_for_status()
        return response.json()
    
    def inject_instruction(self, project_id: str, instruction: str) -> Dict[str, Any]:
        """Inject an instruction for the next loop iteration."""
        response = httpx.post(
            f"{self.base_url}/api/projects/{project_id}/inject",
            headers=self._headers(),
            json={"instruction": instruction},
            timeout=10.0
        )
        response.raise_for_status()
        return response.json()
    
    def get_iterations(self, project_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Get recent iterations."""
        response = httpx.get(
            f"{self.base_url}/api/projects/{project_id}/iterations",
            headers=self._headers(),
            params={"limit": limit},
            timeout=10.0
        )
        response.raise_for_status()
        return response.json()
    
    def get_plan(self, project_id: str) -> Dict[str, Any]:
        """Get implementation plan."""
        response = httpx.get(
            f"{self.base_url}/api/projects/{project_id}/plan",
            headers=self._headers(),
            timeout=10.0
        )
        response.raise_for_status()
        return response.json()


# Convenience functions for quick one-off calls

def login(base_url: str, username: str, password: str) -> str:
    """Login and return access token."""
    client = RalphDashboardClient(base_url)
    data = client.login(username, password)
    return data["access_token"]


def list_projects(base_url: str, token: str) -> List[Dict[str, Any]]:
    """List all projects (pre-authenticated)."""
    response = httpx.get(
        f"{base_url.rstrip('/')}/api/projects",
        headers={"Authorization": f"Bearer {token}"},
        timeout=10.0
    )
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 4:
        print("Usage: python skill.py <base_url> <username> <password>")
        sys.exit(1)
    
    base_url = sys.argv[1]
    username = sys.argv[2]
    password = sys.argv[3]
    
    client = RalphDashboardClient(base_url)
    
    print("Logging in...")
    client.login(username, password)
    
    print("\nProjects:")
    projects = client.list_projects()
    for p in projects:
        print(f"  - {p['id']}: {p['status']}")
        
        stats = client.get_stats(p['id'])
        print(f"    Iterations: {stats.get('iteration_count', 0)}")
        print(f"    Tasks done: {stats.get('tasks_done', 0)}")
