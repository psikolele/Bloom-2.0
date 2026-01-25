
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

    # 1. Read Workflow JSON
    try:
        with open(WORKFLOW_FILE, 'r') as f:
            workflow_data = json.load(f)
    except Exception as e:
        print(f"❌ Failed to read workflow file: {e}")
        return

    # 2. Inject API Key
    print("🔑 Injecting OpenRouter API Key...")
    nodes = workflow_data['nodes']
    key_injected = False
    for node in nodes:
        if node['name'] == "Call OpenRouter":
            params = node['parameters']['headerParameters']['parameters']
            for param in params:
                if param['name'] == "Authorization":
                    param['value'] = f"Bearer {OPENROUTER_KEY}"
                    key_injected = True
                    print("   -> Key injected into 'Call OpenRouter' node.")
    
    if not key_injected:
        print("⚠️ Warning: Could not find 'Authorization' param in 'Call OpenRouter' node.")

    # 3. Check if workflow already exists to update it, or create new
    # We'll search by name "Bloom AI Proxy"
    existing_id = None
    try:
        res = requests.get(f"{N8N_BASE_URL}/workflows", headers=HEADERS)
        res.raise_for_status()
        workflows = res.json()['data']
        for w in workflows:
            if w['name'] == "Bloom AI Proxy":
                existing_id = w['id']
                print(f"📋 Found existing workflow: {existing_id}")
                break
    except Exception as e:
        print(f"⚠️ Error listing workflows: {e}")

    # 4. Create or Update - TRY 1
    # Remove 'active' from payload for creation, activate later
    payload = {
        "name": "Bloom AI Proxy",
        "nodes": nodes,
        "connections": workflow_data['connections'],
        "settings": {} 
    }

    try:
        if existing_id:
            print(f"🔄 Updating existing workflow {existing_id}...")
            res = requests.put(f"{N8N_BASE_URL}/workflows/{existing_id}", headers=HEADERS, json=payload)
        else:
            print("✨ Creating new workflow...")
            res = requests.post(f"{N8N_BASE_URL}/workflows", headers=HEADERS, json=payload)
        
        if not res.ok:
            print(f"   [!] Status Code: {res.status_code}")
            print(f"   [!] Response: {res.text}")
            res.raise_for_status()

        result = res.json()
        new_id = result['id']
        print(f"✅ Workflow Created/Updated! ID: {new_id}")

        # 5. Activate
        print(f"   -> Activating workflow {new_id}...")
        res_act = requests.post(f"{N8N_BASE_URL}/workflows/{new_id}/activate", headers=HEADERS)
        if not res_act.ok:
             print(f"   [!] Activation Failed: {res_act.text}")
        else:
             print("   -> Activated.")

        # 6. Webhook
        print("\n🎉 Webhook URL Construction:")
        prod_url = "https://emanueleserra.app.n8n.cloud/webhook/ai-proxy"
        print(f"   Production URL: {prod_url}")
        
    except Exception as e:
        print(f"❌ Deploy failed exception: {e}")

if __name__ == "__main__":
    main()
