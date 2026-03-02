#!/usr/bin/env python3
"""Utility helpers for deterministic screenshot pathing."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path


def capture_dir(project: str, root: str = "/tmp/ui-captures") -> Path:
    date = datetime.utcnow().strftime("%Y-%m-%d")
    out = Path(root) / project / date
    out.mkdir(parents=True, exist_ok=True)
    return out


if __name__ == "__main__":
    import sys

    project = sys.argv[1] if len(sys.argv) > 1 else "default"
    print(capture_dir(project))
