
import requests
import json
import os

# Conf
N8N_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIwMmRmNzQ5NC1hNjVjLTRjOTAtOTE5MC00NmViOWI4ODg5OGIiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzY4NTEyOTE5fQ.T-W7tlxC7dAA0dPHusS7yuZLpX-qAzuzYCUT653cC0k"
N8N_BASE_URL = "https://emanueleserra.app.n8n.cloud/api/v1"
HEADERS = { "X-N8N-API-KEY": N8N_API_KEY }

def get_workflows():
    print("🔍 Fetching N8N Workflows...")
    try:
        res = requests.get(f"{N8N_BASE_URL}/workflows", headers=HEADERS)
        res.raise_for_status()
        workflows = res.json()['data']
        
        bloom_wfs = []
        print("\n📋 Bloom 2.0 Workflows Found:")
        for w in workflows:
            # Filter loosely by name or tags if possible, but user said they are in project Bloom 2.0
            # The API might not return project info directly in list, but we can guess by name
            # Looking for _V.2 suffix as seen in screenshot
            if "Bloom" in w['name'] or "Caption" in w['name'] or "_V.2" in w['name']:
                print(f"   - {w['name']} (ID: {w['id']}, Active: {w['active']})")
                bloom_wfs.append(w)
        
        return bloom_wfs
    except Exception as e:
        print(f"❌ Error: {e}")
        return []

def detailed_inspection(workflows):
    print("\n🕵️ Inspecting Webhook Paths...")
    results = {}
    for wf in workflows:
        try:
            res = requests.get(f"{N8N_BASE_URL}/workflows/{wf['id']}", headers=HEADERS)
            data = res.json()
            
            webhooks = []
            for node in data['nodes']:
                if 'webhook' in node['type'].lower() and 'respond' not in node['type'].lower():
                    path = node['parameters'].get('path', '')
                    method = node['parameters'].get('httpMethod', 'GET')
                    webhooks.append(f"{method} /webhook/{path}")
            
            if webhooks:
                print(f"   🔹 {wf['name']}: {', '.join(webhooks)}")
                results[wf['name']] = webhooks
            else:
                 print(f"   🔸 {wf['name']}: No public webhooks found.")
                 
        except Exception as e:
            print(f"   ❌ Error inspecting {wf['name']}: {e}")
    return results

if __name__ == "__main__":
    wfs = get_workflows()
    if wfs:
        detailed_inspection(wfs)
