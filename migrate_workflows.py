
import requests
import json
import os

# Conf
N8N_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIwMmRmNzQ5NC1hNjVjLTRjOTAtOTE5MC00NmViOWI4ODg5OGIiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzY4NTEyOTE5fQ.T-W7tlxC7dAA0dPHusS7yuZLpX-qAzuzYCUT653cC0k"
N8N_BASE_URL = "https://emanueleserra.app.n8n.cloud/api/v1"
HEADERS = { "X-N8N-API-KEY": N8N_API_KEY }

# IDs mappings
V1_IDS = {
    "Registration": "2WKzb93sJnfLO1Bv",
    "Auth": "uYNin7KcptmBF8Nw",
    "CaptionReceiver": "ZZ-ucA6GG-z6sW2c1UOPa",
    "CaptionFlow": "LDko1nSj5LhLnEDndqSSo" 
}

V2_IDS = {
    "Registration": "6Lp12hzkw1T8XM8B",  # _V.2
    "Auth": "iqViiw0WOcdt3gxp", # _V.2
    "CaptionReceiver": "603psUgFjVUJ1GLu", # _V.2
    "CaptionFlow": "oRYSQ9tk63yPJaqt", # _V.2
    "BrandProfile": "oQm0QOBN0w6TGzsu" # _V.2
}

def toggle_workflow(wf_id, active):
    try:
        url = f"{N8N_BASE_URL}/workflows/{wf_id}{'/activate' if active else '/deactivate'}"
        res = requests.post(url, headers=HEADERS)
        
        # If activate fails (e.g. conflict), list current status
        if not res.ok:
             print(f"   ⚠️ Failed to set {wf_id} to active={active}: {res.text}")
        else:
             print(f"   ✅ {wf_id} -> Active: {active}")
    except Exception as e:
        print(f"   ❌ Error {wf_id}: {e}")

def inspect_workflow(wf_id, name):
    print(f"\n🔍 Inspecting {name} ({wf_id})...")
    try:
        res = requests.get(f"{N8N_BASE_URL}/workflows/{wf_id}", headers=HEADERS)
        data = res.json()
        
        webhooks = []
        for node in data.get('nodes', []):
            if 'webhook' in node['type'].lower() and 'respond' not in node['type'].lower():
                path = node['parameters'].get('path', 'NOT_SET')
                method = node['parameters'].get('httpMethod', 'GET')
                webhooks.append(f"{method} /webhook/{path}")
        
        for w in webhooks:
            print(f"   -> {w}")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")

def main():
    print("🚀 Migrating to Bloom 2.0 Workflows...")
    
    # 1. Deactivate V1
    print("\n🛑 Deactivating V1 Workflows...")
    for name, uid in V1_IDS.items():
        toggle_workflow(uid, False)
        
    # 2. Activate V2
    print("\n🟢 Activating V2 Workflows...")
    for name, uid in V2_IDS.items():
        toggle_workflow(uid, True)
        
    # 3. Inspect Paths
    print("\n📋 Getting V2 Webhook Paths for Config...")
    for name, uid in V2_IDS.items():
        inspect_workflow(uid, name)

if __name__ == "__main__":
    main()
