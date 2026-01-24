import os
import json
import requests

# Reuse extraction logic or just hardcode for this step
ENV_PATH = r"c:\Users\psiko\Desktop\Antigravity\Bloom AI\.env"

def load_api_key():
    try:
        with open(ENV_PATH, 'r') as f:
            for line in f:
                if line.startswith("N8N_API_KEY="):
                    return line.strip().split("=", 1)[1]
    except Exception as e:
        print(f"Error reading .env: {e}")
        return None

API_KEY = load_api_key()
N8N_BASE_URL = "https://emanueleserra.app.n8n.cloud/api/v1"
HEADERS = {
    "X-N8N-API-KEY": API_KEY,
    "Content-Type": "application/json"
}

def get_workflows():
    try:
        response = requests.get(f"{N8N_BASE_URL}/workflows", headers=HEADERS)
        response.raise_for_status()
        return response.json()['data']
    except Exception as e:
        print(f"Error fetching workflows: {e}")
        return []

def get_workflow_details(workflow_id):
    try:
        response = requests.get(f"{N8N_BASE_URL}/workflows/{workflow_id}", headers=HEADERS)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching workflow {workflow_id}: {e}")
        return None

def main():
    if not API_KEY:
        print("API Key not found.")
        return

    workflows = get_workflows()
    v2_workflows = [w for w in workflows if "_V.2" in w['name']]
    
    print(f"Found {len(v2_workflows)} V.2 workflows.")
    
    webhook_map = {}

    for w in v2_workflows:
        print(f"Inspecting: {w['name']}")
        details = get_workflow_details(w['id'])
        if not details:
            continue
            
        # Find Webhook nodes
        for node in details['nodes']:
            if 'webhook' in node['type'].lower():
                # Check for path parameter
                path = "NOT_FOUND"
                if 'parameters' in node and 'path' in node['parameters']:
                    path = node['parameters']['path']
                
                # Construct URL
                # Production URL structure: https://emanueleserra.app.n8n.cloud/webhook/[path]
                # Test URL structure: https://emanueleserra.app.n8n.cloud/webhook-test/[path]
                
                # Note: N8N also uses UUIDs for webhooks sometimes if not explicitly set path?
                # Usually it's /webhook/ID or /webhook/path
                
                url = f"https://emanueleserra.app.n8n.cloud/webhook/{path}"
                print(f"  -> Found Webhook: {node['name']} -> {url}")
                webhook_map[w['name']] = url
                
    # Save to file
    with open(r"c:\Users\psiko\Desktop\Antigravity\Bloom 2.0\v2_webhooks.json", "w") as f:
        json.dump(webhook_map, f, indent=2)

if __name__ == "__main__":
    main()
