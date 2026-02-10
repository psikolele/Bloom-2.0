#!/usr/bin/env python3
"""
Fix and upload the Bloom AI Unified Auth workflow (uYNin7KcptmBF8Nw).

Issues fixed:
1. Registration path disconnected (Set Email has no output connections)
2. Respond Registration Success missing "success": true
3. 9 phantom/duplicate nodes (old Forgot/Reset copies)
4. Get Marketing Profile orphaned node
5. Respond Login Success fragile expressions (no fallback)
6. Clean visual layout
"""

import json
import requests
import sys

N8N_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIwMmRmNzQ5NC1hNjVjLTRjOTAtOTE5MC00NmViOWI4ODg5OGIiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzY4NTEyOTE5fQ.T-W7tlxC7dAA0dPHusS7yuZLpX-qAzuzYCUT653cC0k"
N8N_BASE_URL = "https://emanueleserra.app.n8n.cloud/api/v1"
HEADERS = {
    "X-N8N-API-KEY": N8N_API_KEY,
    "Content-Type": "application/json"
}
WF_ID = "uYNin7KcptmBF8Nw"

# --- Load live backup ---
with open("backup_workflows/Bloom_AI_Unified_Auth_LIVE_BACKUP_20260210_0634.json") as f:
    live = json.load(f)

print(f"Live workflow: {live['name']}")
print(f"Total nodes: {len(live['nodes'])}")
print(f"Version: {live.get('versionCounter', '?')}")

# --- Identify phantom/duplicate node IDs to REMOVE ---
# OLD duplicates (first set - same names as second set)
REMOVE_IDS = {
    "c1b780f9-5f0c-4d38-8bc3-4c09bb093502",  # Check User (Forgot) - OLD
    "9b391ba0-5aeb-444f-8b41-74c45fdbb591",  # If User Exists (Forgot) - OLD
    "835fec1f-70ab-41f2-9cca-7dea6ad8c174",  # Generate Token - OLD
    "c491f652-b31a-4b85-8b1d-fdde3792b95e",  # Send Reset Email - OLD
    "feac77d4-ade3-4c88-89bc-89467498aa13",  # Respond Success (Forgot) - OLD
    "932936ee-7e15-4e3b-b73e-f5b2c1aab4b1",  # Verify Token - OLD
    "0c87a384-9d96-408e-bd91-1026486b4c4b",  # Get User To Update - OLD
    "fd907f39-0a05-4cd1-a906-47699ccdd2d2",  # Update Password - OLD
    "e78f9d47-0077-4955-83bc-e8ac9e66761f",  # Respond Success (Reset) - OLD
    # Orphaned node
    "get-marketing-profile",                    # Get Marketing Profile - orphaned
}

# --- Filter out phantom nodes ---
clean_nodes = [n for n in live["nodes"] if n["id"] not in REMOVE_IDS]
removed_count = len(live["nodes"]) - len(clean_nodes)
print(f"Removed {removed_count} phantom/duplicate nodes")
print(f"Remaining nodes: {len(clean_nodes)}")

# --- Fix node definitions ---
for node in clean_nodes:
    nid = node["id"]

    # Fix 1: Respond Login Success - add fallbacks and rename
    if nid == "respond-success":
        node["name"] = "Respond Login Success"
        node["parameters"]["responseBody"] = (
            '={\n'
            '  "success": true,\n'
            '  "message": "Login successful",\n'
            '  "username": "{{ $json.user.property_username || $json.user.property_name || $json.user.Name || $json.user.Username || $(\'Webhook\').item.json.body.username }}"\n'
            '}'
        )

    # Fix 2: Respond Registration Success - add success: true + username
    if nid == "respond-reg-success-v65":
        node["parameters"]["responseBody"] = (
            '={\n'
            '  "success": true,\n'
            '  "message": "Registrazione completata",\n'
            '  "username": "{{ $(\'Webhook\').first().json.body.username }}",\n'
            '  "email": "{{ $(\'Webhook\').first().json.body.email }}"\n'
            '}'
        )
        node["parameters"]["options"] = {"responseCode": 200}

# --- Fix layout positions ---
POSITIONS = {
    # Core
    "webhook-trigger":          [460,  360],
    "switch-mode":              [680,  360],
    # Login path (y=200)
    "get-user-brand":           [900,  160],
    "get-user-marketing":       [900,  300],
    "merge-users":              [1100, 220],
    "validate-user":            [1280, 220],
    "check-auth":               [1460, 220],
    "respond-success":          [1660, 160],  # renamed to Respond Login Success
    "respond-error":            [1660, 320],
    # Register path (y=520)
    "set-email-v65":            [900,  520],
    "check-email-notion-v65":   [1100, 520],
    "check-logic-v65":          [1280, 520],
    "if-exists-v65":            [1460, 520],
    "respond-conflict-v65":     [1660, 440],
    "create-user":              [1660, 600],
    "respond-reg-success-v65":  [1880, 600],
    # Forgot path (y=780)
    "8460384d-880d-453c-ad9f-3c625c32449c": [900,  780],  # Check User (Forgot)
    "99538615-df29-4828-8756-c9efadcd04fe": [1100, 780],  # If User Exists (Forgot)
    "63bbcd7f-80f7-4a9c-8afa-e85fc76d0f84": [1280, 720],  # Generate Token
    "35701625-7808-4416-9413-acfd33bceb0a": [1460, 720],  # Send Reset Email
    "cefb7535-e480-4bc0-aa75-c8934dde3cd4": [1660, 780],  # Respond Success (Forgot)
    # Reset path (y=980)
    "b9a5fea1-2495-4723-bc9b-3e572a70df69": [900,  980],  # Verify Token
    "5be755a2-d95c-437b-9cd7-0be74bd314a3": [1100, 980],  # Get User To Update
    "2021582d-83fa-4fd4-9554-2b28c712ce64": [1280, 980],  # Update Password
    "55a208b8-df5c-406e-851a-77c866ff533a": [1460, 980],  # Respond Success (Reset)
}

for node in clean_nodes:
    if node["id"] in POSITIONS:
        node["position"] = POSITIONS[node["id"]]

# --- Fix connections ---
connections = {
    "Webhook": {
        "main": [[
            {"node": "Switch Mode", "type": "main", "index": 0}
        ]]
    },
    "Switch Mode": {
        "main": [
            # Output 0: Login
            [
                {"node": "Get User (Brand)", "type": "main", "index": 0},
                {"node": "Get User (Marketing)", "type": "main", "index": 0}
            ],
            # Output 1: Register
            [
                {"node": "Set Email", "type": "main", "index": 0}
            ],
            # Output 2: Forgot
            [
                {"node": "Check User (Forgot)", "type": "main", "index": 0}
            ],
            # Output 3: Reset
            [
                {"node": "Verify Token", "type": "main", "index": 0}
            ]
        ]
    },
    # --- LOGIN PATH ---
    "Get User (Brand)": {
        "main": [[
            {"node": "Merge Users", "type": "main", "index": 0}
        ]]
    },
    "Get User (Marketing)": {
        "main": [[
            {"node": "Merge Users", "type": "main", "index": 1}
        ]]
    },
    "Merge Users": {
        "main": [[
            {"node": "Validate User", "type": "main", "index": 0}
        ]]
    },
    "Validate User": {
        "main": [[
            {"node": "If Authorized", "type": "main", "index": 0}
        ]]
    },
    "If Authorized": {
        "main": [
            [{"node": "Respond Login Success", "type": "main", "index": 0}],
            [{"node": "Respond Error", "type": "main", "index": 0}]
        ]
    },
    # --- REGISTER PATH (FIXED!) ---
    "Set Email": {
        "main": [[
            {"node": "Check Existing Email (Marketing DB)", "type": "main", "index": 0}
        ]]
    },
    "Check Existing Email (Marketing DB)": {
        "main": [[
            {"node": "Check Logic", "type": "main", "index": 0}
        ]]
    },
    "Check Logic": {
        "main": [[
            {"node": "If Exists", "type": "main", "index": 0}
        ]]
    },
    "If Exists": {
        "main": [
            [{"node": "Respond Conflict", "type": "main", "index": 0}],
            [{"node": "Create User", "type": "main", "index": 0}]
        ]
    },
    "Create User": {
        "main": [[
            {"node": "Respond Registration Success", "type": "main", "index": 0}
        ]]
    },
    # --- FORGOT PATH ---
    "Check User (Forgot)": {
        "main": [[
            {"node": "If User Exists (Forgot)", "type": "main", "index": 0}
        ]]
    },
    "If User Exists (Forgot)": {
        "main": [
            [{"node": "Generate Token", "type": "main", "index": 0}],
            [{"node": "Respond Success (Forgot)", "type": "main", "index": 0}]
        ]
    },
    "Generate Token": {
        "main": [[
            {"node": "Send Reset Email", "type": "main", "index": 0}
        ]]
    },
    "Send Reset Email": {
        "main": [[
            {"node": "Respond Success (Forgot)", "type": "main", "index": 0}
        ]]
    },
    # --- RESET PATH ---
    "Verify Token": {
        "main": [[
            {"node": "Get User To Update", "type": "main", "index": 0}
        ]]
    },
    "Get User To Update": {
        "main": [[
            {"node": "Update Password", "type": "main", "index": 0}
        ]]
    },
    "Update Password": {
        "main": [[
            {"node": "Respond Success (Reset)", "type": "main", "index": 0}
        ]]
    }
}

# --- Build update payload ---
payload = {
    "name": "Bloom AI Unified Auth V7 (Registration Fix)",
    "nodes": clean_nodes,
    "connections": connections,
    "settings": live.get("settings", {})
}

# Verify node names match connections
node_names = {n["name"] for n in clean_nodes}
conn_targets = set()
for src, data in connections.items():
    conn_targets.add(src)
    for outputs in data.get("main", []):
        for conn in outputs:
            conn_targets.add(conn["node"])

missing = conn_targets - node_names
if missing:
    print(f"ERROR: Connection references missing nodes: {missing}")
    sys.exit(1)

orphaned = node_names - conn_targets
if orphaned:
    print(f"WARNING: Orphaned nodes (not in any connection): {orphaned}")

print(f"\nNode count: {len(clean_nodes)}")
print(f"Connection sources: {len(connections)}")
print(f"All connections valid: YES")

# --- Save corrected workflow locally ---
with open("backup_workflows/Bloom_AI_Unified_Auth_V7_CORRECTED.json", "w") as f:
    json.dump(payload, f, indent=2)
print("\nSaved corrected workflow to backup_workflows/Bloom_AI_Unified_Auth_V7_CORRECTED.json")

# --- Upload to n8n ---
print(f"\nUploading to n8n cloud (workflow {WF_ID})...")
resp = requests.put(
    f"{N8N_BASE_URL}/workflows/{WF_ID}",
    headers=HEADERS,
    json=payload
)

if resp.ok:
    result = resp.json()
    print(f"Upload SUCCESS!")
    print(f"  Name: {result.get('name')}")
    print(f"  Active: {result.get('active')}")
    print(f"  Nodes: {len(result.get('nodes', []))}")
    print(f"  Version: {result.get('versionId', '?')}")

    # Activate if not already active
    if not result.get("active"):
        print("Activating workflow...")
        act_resp = requests.patch(
            f"{N8N_BASE_URL}/workflows/{WF_ID}/activate",
            headers=HEADERS
        )
        if act_resp.ok:
            print("Workflow ACTIVATED!")
        else:
            print(f"Activation failed: {act_resp.status_code} - {act_resp.text}")
else:
    print(f"Upload FAILED: {resp.status_code}")
    print(resp.text[:1000])
    sys.exit(1)
