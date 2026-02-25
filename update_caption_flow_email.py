#!/usr/bin/env python3
"""
Aggiunge javier@webstoreplus.ch come secondo destinatario dell'email
di approvazione nel workflow Caption Flow V.3 (nodo "Check via Email").
"""

import json
import requests
import sys

N8N_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIwMmRmNzQ5NC1hNjVjLTRjOTAtOTE5MC00NmViOWI4ODg5OGIiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzY4NTEyOTE5fQ.T-W7tlxC7dAA0dPHusS7yuZLpX-qAzuzYCUT653cC0k"
N8N_BASE_URL = "https://emanueleserra.app.n8n.cloud/api/v1"
WF_ID = "oRYSQ9tk63yPJaqt"
HEADERS = {
    "X-N8N-API-KEY": N8N_API_KEY,
    "Content-Type": "application/json"
}
NEW_TO_EMAIL = "serra.emanuele09@gmail.com,javier@webstoreplus.ch"

# --- Fetch live workflow ---
print(f"Fetching workflow {WF_ID} from n8n...")
resp = requests.get(f"{N8N_BASE_URL}/workflows/{WF_ID}", headers=HEADERS)
if resp.status_code != 200:
    print(f"ERROR fetching workflow: {resp.status_code} {resp.text}")
    sys.exit(1)

wf = resp.json()
print(f"Workflow name: {wf['name']}")

# --- Find and update "Check via Email" node ---
updated = 0
for node in wf.get("nodes", []):
    if node.get("name") == "Check via Email":
        old_email = node["parameters"].get("toEmail", "")
        node["parameters"]["toEmail"] = NEW_TO_EMAIL
        print(f"Updated node '{node['name']}': '{old_email}' -> '{NEW_TO_EMAIL}'")
        updated += 1

if updated == 0:
    print("ERROR: 'Check via Email' node not found in workflow!")
    sys.exit(1)

print(f"Total nodes updated: {updated}")

# --- Prepare API-safe payload (only accepted fields) ---
payload = {
    "name": wf["name"],
    "nodes": wf["nodes"],
    "connections": wf["connections"],
    "settings": {"executionOrder": "v1"}
}

# --- Push updated workflow ---
print("Pushing updated workflow to n8n...")
put_resp = requests.put(
    f"{N8N_BASE_URL}/workflows/{WF_ID}",
    headers=HEADERS,
    json=payload
)
if put_resp.status_code not in (200, 201):
    print(f"ERROR pushing workflow: {put_resp.status_code} {put_resp.text}")
    sys.exit(1)

result = put_resp.json()
print(f"SUCCESS! Workflow '{result['name']}' aggiornato.")
print(f"Destinatari email approvazione: {NEW_TO_EMAIL}")
