
import requests
import json
import os

# Configuration
N8N_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIwMmRmNzQ5NC1hNjVjLTRjOTAtOTE5MC00NmViOWI4ODg5OGIiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzY4NTEyOTE5fQ.T-W7tlxC7dAA0dPHusS7yuZLpX-qAzuzYCUT653cC0k"
N8N_BASE_URL = "https://emanueleserra.app.n8n.cloud/api/v1"
OPENROUTER_KEY = "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"

WORKFLOW_FILE = r"c:\Users\psiko\Desktop\Antigravity\Bloom 2.0\backup_workflows\Bloom_AI_Proxy.json"

HEADERS = {
    "X-N8N-API-KEY": N8N_API_KEY,
    "Content-Type": "application/json"
}

def main():
    print("🚀 Deploying Bloom AI Proxy Workflow to N8N...")

    try:
        with open(WORKFLOW_FILE, 'r') as f:
            workflow_data = json.load(f)
    except Exception as e:
        print(f"❌ Failed to read workflow file: {e}")
        return

    # Inject API Key
    print("🔑 Injecting OpenRouter API Key...")
    nodes = workflow_data['nodes']
    for node in nodes:
        if node['name'] == "Call OpenRouter":
            params = node['parameters']['headerParameters']['parameters']
            for param in params:
                if param['name'] == "Authorization":
                    param['value'] = f"Bearer {OPENROUTER_KEY}"
                    print("   -> Key injected into 'Call OpenRouter' node.")
    
    # Check existing
    existing_id = None
    try:
        res = requests.get(f"{N8N_BASE_URL}/workflows", headers=HEADERS)
        workflows = res.json()['data']
        for w in workflows:
            if w['name'] == "Bloom AI Proxy":
                existing_id = w['id']
                print(f"📋 Found existing workflow: {existing_id}")
                break
    except Exception as e:
        print(f"⚠️ Error listing workflows: {e}")

    # Create or Update
    payload = {
        "name": "Bloom AI Proxy",
        "nodes": nodes,
        "connections": workflow_data['connections'],
        "settings": {}
        # "active": True  <-- Removed to avoid read-only error on update
    }

    try:
        if existing_id:
            print(f"🔄 Updating existing workflow {existing_id}...")
            res = requests.put(f"{N8N_BASE_URL}/workflows/{existing_id}", headers=HEADERS, json=payload)
        else:
            print("✨ Creating new workflow...")
            res = requests.post(f"{N8N_BASE_URL}/workflows", headers=HEADERS, json=payload)
        
        if not res.ok:
            print(f"   [!] Error {res.status_code}: {res.text}")
            res.raise_for_status()

        result = res.json()
        new_id = result['id']
        print(f"✅ Workflow Deployed! ID: {new_id}")
        
    except Exception as e:
        print(f"❌ Deploy failed: {e}")

if __name__ == "__main__":
    main()
