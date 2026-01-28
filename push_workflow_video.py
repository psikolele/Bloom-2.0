import json
import requests
import sys
import os

# Configuration paths
CONFIG_PATH = r"c:\Users\psiko\Desktop\Antigravity\n8n_config.json"
WORKFLOW_PATH = r"c:\Users\psiko\Desktop\Antigravity\Bloom 2.0\backup_workflows\Caption_Flow_V3_VIDEO_MOD.json"
WORKFLOW_ID = "oRYSQ9tk63yPJaqt" # Caption Flow V.2 ID

def load_config():
    if not os.path.exists(CONFIG_PATH):
        print(f"Error: Config file not found at {CONFIG_PATH}")
        sys.exit(1)
    with open(CONFIG_PATH, 'r') as f:
        return json.load(f)

def push_workflow():
    config = load_config()
    api_key = config.get('api_key')
    base_url = config.get('base_url')

    if not api_key:
        print("Error: API Key missing in config")
        sys.exit(1)

    # Load the modified workflow
    try:
        with open(WORKFLOW_PATH, 'r', encoding='utf-8') as f:
            workflow_data = json.load(f)
    except Exception as e:
        print(f"Error loading workflow file: {e}")
        sys.exit(1)

    # Prepare payload (N8N API expects 'nodes' and 'connections', and optionally 'name')
    # Use the retrieved ID to ensure we update the correct workflow
    url = f"{base_url}/workflows/{WORKFLOW_ID}"
    
    headers = {
        "X-N8N-API-KEY": api_key,
        "Content-Type": "application/json"
    }

    payload = {
        "nodes": workflow_data['nodes'],
        "connections": workflow_data['connections'],
        "settings": {
            "executionOrder": "v1",
            "saveDataErrorExecution": "all",
            "saveDataSuccessExecution": "all",
            "saveExecutionProgress": True,
            "saveManualExecutions": True,
            "timezone": "Europe/Rome"
        },
        "name": workflow_data.get('name', 'Caption Flow V.2 (Video Updated)')
    }

    print(f"Pushing update to N8N Workflow ID: {WORKFLOW_ID}...")
    
    try:
        response = requests.put(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            print("Successfully updated workflow!")
            print(f"Response: {response.json().get('name')}")
        else:
            print(f"Failed to update workflow. Status: {response.status_code}")
            print(f"Response: {response.text}")

    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    push_workflow()
