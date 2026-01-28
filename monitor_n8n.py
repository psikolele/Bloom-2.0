
import requests
import json
import time
import sys
import os

def load_env(path=".env"):
    env = {}
    try:
        with open(path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'): continue
                if '=' in line:
                    key, val = line.split('=', 1)
                    env[key] = val
    except:
        pass
    return env

env = load_env()
N8N_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIwMmRmNzQ5NC1hNjVjLTRjOTAtOTE5MC00NmViOWI4ODg5OGIiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzY4NTEyOTE5fQ.T-W7tlxC7dAA0dPHusS7yuZLpX-qAzuzYCUT653cC0k"

N8N_BASE_URL = "https://emanueleserra.app.n8n.cloud/api/v1"
HEADERS = { "X-N8N-API-KEY": N8N_API_KEY }
WF_ID = "7KzNvq6NjRbyQ0j9"

NOTION_TOKEN = env.get("NOTION_API_KEY", "")
NOTION_HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}
NOTION_DB_ID = "2f5fa85c-0d03-81b5-b333-cdb74b8ce81b"

def get_latest_execution_id():
    try:
        res = requests.get(f"{N8N_BASE_URL}/executions?workflowId={WF_ID}&limit=1", headers=HEADERS)
        if res.ok:
            data = res.json().get('data', [])
            if data:
                return int(data[0]['id'])
    except:
        pass
    return 0

def monitor():
    print("Monitor N8N Attivo...")
    initial_last_id = get_latest_execution_id()
    print(f"Ultima Esecuzione ID: {initial_last_id}")
    print("In attesa di azione sul sito...")
    
    timeout = 300 # 5 minutes
    start = time.time()
    
    new_exec_id = None
    
    while time.time() - start < timeout:
        latest = get_latest_execution_id()
        if latest > initial_last_id:
            new_exec_id = latest
            print(f"\n🚀 NUOVA ESECUZIONE RILEVATA! ID: {new_exec_id}")
            break
        time.sleep(2)
        sys.stdout.write(".")
        sys.stdout.flush()
        
    if not new_exec_id:
        return

    # Wait for completion
    time.sleep(5) 
    
    # Inspect
    res = requests.get(f"{N8N_BASE_URL}/executions/{new_exec_id}", headers=HEADERS)
    data = res.json()
    status = data.get('finished', False)
    
    print(f"Status N8N: {'✅ Completato' if status else '⚠️ In corso/Errore'}")
    
    # Check Verification
    print("Verifica Notion in corso...")
    time.sleep(2)
    query_payload = {
        "page_size": 1,
        "sorts": [
            {
                "timestamp": "created_time",
                "direction": "descending"
            }
        ]
    }
    
    if NOTION_TOKEN:
        n_res = requests.post(f"https://api.notion.com/v1/databases/{NOTION_DB_ID}/query", headers=NOTION_HEADERS, json=query_payload)
        if n_res.ok:
            results = n_res.json().get('results', [])
            if results:
                page = results[0]
                props = page['properties']
                name = props['Name']['title'][0]['text']['content']
                print(f"✅ Trovato record Notion: '{name}'")
            else:
                print("❌ Record non trovato su Notion.")
        else:
            print(f"Errore query Notion: {n_res.text}")

if __name__ == "__main__":
    monitor()
