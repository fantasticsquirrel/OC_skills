"""
Multi-app hosting skill - manages reverse proxy routing for multiple applications.
"""

def run(input):
    """
    Provides guidance for multi-app hosting setup and maintenance.
    
    Input:
    - action: "guide" (get setup guide), "topology" (get current topology), "add_app" (add new app)
    - app_name: (optional) name of app being added
    - port: (optional) internal port for new app
    - route: (optional) public route path (e.g., "/myapp/")
    
    Output:
    - guide: Multi-app hosting instructions
    - topology: Current app routing map
    - next_steps: Recommended actions
    """
    
    action = input.get("action", "guide")
    
    if action == "guide":
        return {
            "guide": get_hosting_guide(),
            "next_steps": [
                "Map current topology before changes",
                "Choose unique internal port for new app",
                "Add nginx upstream and location route",
                "Verify local + public health"
            ]
        }
    
    elif action == "topology":
        return {
            "current_routes": {
                "/": "OpenClaw frontend (port 3000)",
                "/api/": "OpenClaw backend (port 8000)",
                "/obsidian/": "Obsidian host (port 3100)",
                "/eoh/": "Echoes of Hyperion (port 5001)"
            },
            "nginx_config": "/etc/nginx/sites-available/openclaw",
            "verify_command": "sudo nginx -t && sudo systemctl reload nginx"
        }
    
    elif action == "add_app":
        app_name = input.get("app_name", "new_app")
        port = input.get("port", 8080)
        route = input.get("route", f"/{app_name}/")
        
        return {
            "app_name": app_name,
            "internal_port": port,
            "public_route": route,
            "steps": [
                f"1. Start {app_name} on port {port}",
                f"2. Add nginx upstream: upstream {app_name} {{ server 127.0.0.1:{port}; }}",
                f"3. Add location block: location {route} {{ proxy_pass http://{app_name}; }}",
                "4. Run: sudo nginx -t && sudo systemctl reload nginx",
                f"5. Test: curl -I http://your-domain{route}"
            ]
        }
    
    else:
        return {
            "error": f"Unknown action: {action}",
            "valid_actions": ["guide", "topology", "add_app"]
        }


def get_hosting_guide():
    """Return the full multi-app hosting guide."""
    return """
# Multi-App Hosting Pattern

1. Map current topology before changes.
   - Check running app processes and bound ports.
   - Check nginx upstream/location blocks.

2. Keep one public ingress.
   - Public: nginx on 80/443 only.
   - Private: app services on local/internal ports.

3. Add apps with predictable pattern.
   - Choose unique internal port.
   - Start app process.
   - Add nginx `upstream` and `location` route.
   - Run `nginx -t` then reload.
   - Verify local + public health.

4. Prefer safety defaults.
   - Never remove existing app routes while adding a new one.
   - Keep auth at app level and optionally at proxy level.
   - Document route, port, process command, and health URL.

5. Update documentation after every routing change.

## Quick Commands

```bash
# Verify services
ps aux | grep -E "uvicorn|next-server|server.py" | grep -v grep

# Verify nginx config
sudo nginx -t && sudo systemctl reload nginx

# Route checks
curl -I http://your-domain/
curl -I http://your-domain/eoh/
```
"""
