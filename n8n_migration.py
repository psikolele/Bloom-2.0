import os
import json
import requests
import time

# Configuration
# Assuming .env is in parent directory or we manually set it for now based on previous reads
# I will try to read it from the Bloom AI folder since I saw it there
ENV_PATH = r"c:\Users\psiko\Desktop\Antigravity\Bloom AI\.env"
BACKUP_DIR = r"c:\Users\psiko\Desktop\Antigravity\Bloom 2.0\backup_workflows"

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
# Previous scripts used this URL
N8N_BASE_URL = "https://emanueleserra.app.n8n.cloud/api/v1"

if not API_KEY:
    # Fallback to hardcoded extracted key if file read fails (from previous context)
    # But try to rely on file first.
    print("Could not find API_KEY in .env file.")
    exit(1)

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

def create_workflow(name, nodes, connections, settings, tags=None):
    # Remove tags entirely as it seems to be read-only or problematic during create
    # Also, some settings might be read-only
    payload = {
        "name": name,
        "nodes": nodes,
        "connections": connections,
        "settings": settings
        # "tags": []  <-- Removed entirely
    }
    
    try:
        print(f"    Sending payload for {name}...")
        response = requests.post(f"{N8N_BASE_URL}/workflows", headers=HEADERS, json=payload)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        # Retry with sanitized settings if first attempt failed
        error_msg = ""
        if hasattr(e, 'response') and e.response is not None:
             error_msg = e.response.text
        
        print(f"    [!] Error with full settings: {error_msg}")
        
        if "settings" in error_msg or "additional properties" in error_msg or "read-only" in error_msg:
            print("    [->] Retrying with CLEAN settings...")
            payload['settings'] = {} # Fallback to empty settings
            if "tags" in error_msg:
                 if "tags" in payload: del payload['tags']

            try:
                response = requests.post(f"{N8N_BASE_URL}/workflows", headers=HEADERS, json=payload)
                response.raise_for_status()
                print("    [+] Success with clean settings!")
                return response.json()
            except Exception as e2:
                print(f"    [!!] Failed retry: {e2}")
                if hasattr(e2, 'response') and e2.response is not None:
                    print(f"    Server Response: {e2.response.text}")

        return None
    except Exception as e:
        print(f"Error creating workflow {name}: {e}")
        if hasattr(e, 'response') and e.response is not None:
             print(f"Server Response: {e.response.text}")
        return None

def main():
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)

    all_workflows = get_workflows()
    print(f"Found {len(all_workflows)} total workflows.")

    # Filter for Bloom related workflows
    # Strategy: Look for "Bloom" in name OR if the user said "duplicare le automazioni che ci sono dietro"
    # I'll look for workflows that seem relevant. Typically "Bloom AI" project workflows?
    # I'll backup ALL that contain "Bloom" or "Caption" or "Social" just to be safe, 
    # but I'll list them first for confirmation if I wasn't in auto-mode.
    # Since I need to act: I will backup anything with "Bloom" or "Auto" in title.
    
    bloom_workflows = [w for w in all_workflows if "bloom" in w['name'].lower() or "caption" in w['name'].lower() or "social" in w['name'].lower() or "brand" in w['name'].lower()]
    
    print(f"Identified {len(bloom_workflows)} potential Bloom/project workflows.")
    
    mapping = {}

    for w in bloom_workflows:
        print(f"Processing: {w['name']} ({w['id']})")
        
        # 1. Fetch Full Details
        details = get_workflow_details(w['id'])
        if not details:
            continue
            
        # 2. Backup
        safe_name = "".join([c for c in w['name'] if c.isalpha() or c.isdigit() or c==' ' or c=='-']).strip()
        backup_path = os.path.join(BACKUP_DIR, f"{safe_name}_{w['id']}.json")
        with open(backup_path, 'w', encoding='utf-8') as f:
            json.dump(details, f, indent=2)
        print(f"  -> Backed up to {backup_path}")

        # 3. Duplicate with _V.2
        new_name = f"{w['name']} _V.2"
        # Check if already exists to avoid double creation
        existing = [ex for ex in all_workflows if ex['name'] == new_name]
        if existing:
            print(f"  -> Workflow '{new_name}' already exists. Skipping creation.")
            mapping[w['name']] = existing[0]['id']
            continue
            
        new_workflow = create_workflow(new_name, details['nodes'], details['connections'], details['settings'], details.get('tags'))
        if new_workflow:
            print(f"  -> Created V.2: {new_workflow['name']} ({new_workflow['id']})")
            mapping[w['name']] = new_workflow['id']
            
            # Find Webhook URLs in the new workflow?
            # We can inspect the nodes for 'webhook' type
            for node in new_workflow['nodes']:
                if 'webhook' in node['type'].lower():
                    print(f"     [!] Contains Webhook Node: {node['name']}")
    
    # Save mapping
    with open(os.path.join(BACKUP_DIR, "migration_map.json"), 'w') as f:
        json.dump(mapping, f, indent=2)

if __name__ == "__main__":
    main()
