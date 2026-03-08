#!/usr/bin/env python3
"""
push_workflow_video.py — Deploy N8N workflow to cloud instance.

Pushes backup_workflows/Caption_Flow_V3_VIDEO_MOD.json to the N8N cloud
instance using the REST API (PUT /api/v1/workflows/{id}).

Cross-platform: works on Linux, macOS, and Windows.

Configuration (in order of precedence):
  1. Environment variable  N8N_API_KEY
  2. .env file in the project root

Usage:
    python push_workflow_video.py              # deploy
    python push_workflow_video.py --dry-run    # preview payload only
"""

import json
import os
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent
WORKFLOW_PATH = PROJECT_ROOT / "backup_workflows" / "Caption_Flow_V3_VIDEO_MOD.json"
WORKFLOW_ID = "oRYSQ9tk63yPJaqt"  # Caption Flow V.2 ID
N8N_BASE_URL = "https://emanueleserra.app.n8n.cloud/api/v1"


def load_env_file(env_path: Path) -> dict:
    """Parse a .env file into a dict. Ignores comments and blank lines."""
    env_vars = {}
    if not env_path.is_file():
        return env_vars
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, _, value = line.partition("=")
                key = key.strip()
                value = value.strip().strip("\"'")
                env_vars[key] = value
    return env_vars


def get_api_key() -> str:
    """Retrieve N8N_API_KEY from environment or .env file."""
    # 1. Environment variable
    api_key = os.environ.get("N8N_API_KEY", "").strip()
    if api_key:
        return api_key

    # 2. .env file in project root
    env_vars = load_env_file(PROJECT_ROOT / ".env")
    api_key = env_vars.get("N8N_API_KEY", "").strip()
    if api_key:
        return api_key

    return ""


def load_workflow() -> dict:
    """Load and return the workflow JSON from disk."""
    if not WORKFLOW_PATH.is_file():
        print(f"Error: Workflow file not found at {WORKFLOW_PATH}")
        sys.exit(1)

    try:
        with open(WORKFLOW_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in workflow file: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error loading workflow file: {e}")
        sys.exit(1)


def build_payload(workflow_data: dict) -> dict:
    """
    Build the API payload from the workflow data.

    Extracts nodes, connections, settings, and name. Merges sensible
    defaults into settings.
    """
    raw_settings = workflow_data.get("settings", {})

    # Only keep settings accepted by the n8n API (strip cloud-only props)
    allowed_keys = {
        "executionOrder", "saveDataErrorExecution", "saveDataSuccessExecution",
        "saveExecutionProgress", "saveManualExecutions", "timezone",
        "errorWorkflow",
    }
    settings = {k: v for k, v in raw_settings.items() if k in allowed_keys}

    # Merge defaults (don't overwrite what the file already has)
    setting_defaults = {
        "saveDataErrorExecution": "all",
        "saveDataSuccessExecution": "all",
        "saveExecutionProgress": True,
        "saveManualExecutions": True,
        "timezone": "Europe/Rome",
    }
    for key, value in setting_defaults.items():
        settings.setdefault(key, value)

    return {
        "name": workflow_data.get("name", "Caption Flow V.2"),
        "nodes": workflow_data.get("nodes", []),
        "connections": workflow_data.get("connections", {}),
        "settings": settings,
    }


def push_workflow(dry_run: bool = False) -> None:
    """Main entry point: load, build, and deploy the workflow."""
    # --- API key ---
    api_key = get_api_key()
    if not api_key:
        print("Error: N8N_API_KEY is not set.")
        print(f"Set it as an environment variable or add it to {PROJECT_ROOT / '.env'}")
        print("See .env.example for the expected format.")
        sys.exit(1)

    print(f"N8N_API_KEY loaded ({len(api_key)} chars)")

    # --- Load workflow ---
    workflow_data = load_workflow()
    payload = build_payload(workflow_data)

    node_count = len(payload.get("nodes", []))
    print(f"Workflow: \"{payload['name']}\" ({node_count} nodes)")

    # --- Dry run ---
    if dry_run:
        print("\n--- DRY RUN (not sending to N8N) ---")
        preview = json.dumps(payload, indent=2, ensure_ascii=False)
        # Print first 80 lines
        lines = preview.split("\n")
        for line in lines[:80]:
            print(line)
        if len(lines) > 80:
            print(f"  ... ({len(lines) - 80} more lines)")
        print(f"\nTarget: PUT {N8N_BASE_URL}/workflows/{WORKFLOW_ID}")
        return

    # --- Deploy ---
    # Use urllib so we don't require 'requests' to be installed
    try:
        import requests

        _push_with_requests(api_key, payload)
    except ImportError:
        print("'requests' library not found, falling back to urllib...")
        _push_with_urllib(api_key, payload)


def _push_with_requests(api_key: str, payload: dict) -> None:
    """Deploy using the requests library."""
    import requests

    url = f"{N8N_BASE_URL}/workflows/{WORKFLOW_ID}"
    headers = {
        "X-N8N-API-KEY": api_key,
        "Content-Type": "application/json",
    }

    print(f"Deploying to {url} ...")

    try:
        response = requests.put(url, headers=headers, json=payload, timeout=30)

        if response.status_code == 200:
            resp_data = response.json()
            print(f"Successfully deployed workflow!")
            print(f"  Name: {resp_data.get('name', 'N/A')}")
            print(f"  ID:   {resp_data.get('id', 'N/A')}")
        elif response.status_code == 401:
            print(f"Error: Authentication failed (HTTP 401). Check your N8N_API_KEY.")
            print(f"Response: {response.text}")
            sys.exit(1)
        elif response.status_code == 404:
            print(f"Error: Workflow not found (HTTP 404). Check WORKFLOW_ID={WORKFLOW_ID}")
            print(f"Response: {response.text}")
            sys.exit(1)
        else:
            print(f"Error: Unexpected response (HTTP {response.status_code})")
            print(f"Response: {response.text}")
            sys.exit(1)

    except requests.exceptions.ConnectionError as e:
        print(f"Error: Could not connect to {url}")
        print(f"Details: {e}")
        sys.exit(1)
    except requests.exceptions.Timeout:
        print(f"Error: Request timed out after 30 seconds.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: Request failed: {e}")
        sys.exit(1)


def _push_with_urllib(api_key: str, payload: dict) -> None:
    """Deploy using the standard library (no external deps)."""
    import urllib.request
    import urllib.error

    url = f"{N8N_BASE_URL}/workflows/{WORKFLOW_ID}"
    data = json.dumps(payload).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=data,
        method="PUT",
        headers={
            "X-N8N-API-KEY": api_key,
            "Content-Type": "application/json",
        },
    )

    print(f"Deploying to {url} ...")

    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            body = response.read().decode("utf-8")
            resp_data = json.loads(body)
            print(f"Successfully deployed workflow!")
            print(f"  Name: {resp_data.get('name', 'N/A')}")
            print(f"  ID:   {resp_data.get('id', 'N/A')}")
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(f"Error: HTTP {e.code} — {e.reason}")
        print(f"Response: {body}")
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"Error: Could not connect to {url}")
        print(f"Details: {e.reason}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: Request failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    dry = "--dry-run" in sys.argv
    push_workflow(dry_run=dry)
