#!/usr/bin/env python3
"""
Redesign Bloom AI Unified Auth workflow layout for n8n.
Adds sticky notes, node descriptions, clean positioning, and visual grouping.
"""

import json
import requests
import sys

N8N_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIwMmRmNzQ5NC1hNjVjLTRjOTAtOTE5MC00NmViOWI4ODg5OGIiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzY4NTEyOTE5fQ.T-W7tlxC7dAA0dPHusS7yuZLpX-qAzuzYCUT653cC0k"
N8N_BASE_URL = "https://emanueleserra.app.n8n.cloud/api/v1"
HEADERS = {"X-N8N-API-KEY": N8N_API_KEY, "Content-Type": "application/json"}
WF_ID = "uYNin7KcptmBF8Nw"

# --- Fetch current live workflow ---
print("Fetching current workflow from n8n cloud...")
resp = requests.get(f"{N8N_BASE_URL}/workflows/{WF_ID}", headers=HEADERS)
if not resp.ok:
    print(f"FAILED to fetch: {resp.status_code}")
    sys.exit(1)
live = resp.json()
print(f"  Name: {live['name']}")
print(f"  Nodes: {len(live['nodes'])}")

# ===================================================================
# LAYOUT DESIGN
# ===================================================================
# 4 clear horizontal lanes, each with a colored sticky note header
# Wide spacing (260px H, 180px V between nodes)
# Sticky notes as section backgrounds
#
#  [Webhook] --> [Switch Mode]
#                    |
#       +-----------+----------+-----------+
#       |           |          |           |
#    LOGIN      REGISTER    FORGOT      RESET
#   (green)     (blue)     (orange)    (purple)
# ===================================================================

# --- Node positions (well-spaced grid) ---
POSITIONS = {
    # === CORE ENTRY ===
    "webhook-trigger":          [180,  500],
    "switch-mode":              [480,  500],

    # === LOGIN PATH (y: 60-360) ===
    "get-user-brand":           [760,  100],
    "get-user-marketing":       [760,  300],
    "merge-users":              [1040, 190],
    "validate-user":            [1300, 190],
    "check-auth":               [1560, 190],
    "respond-success":          [1820, 80],   # Respond Login Success
    "respond-error":            [1820, 320],

    # === REGISTER PATH (y: 500-760) ===
    "set-email-v65":            [760,  600],
    "check-email-notion-v65":   [1040, 600],
    "check-logic-v65":          [1300, 600],
    "if-exists-v65":            [1560, 600],
    "respond-conflict-v65":     [1820, 500],
    "create-user":              [1820, 720],
    "respond-reg-success-v65":  [2100, 720],

    # === FORGOT PASSWORD PATH (y: 920-1160) ===
    "8460384d-880d-453c-ad9f-3c625c32449c": [760,  1060],
    "99538615-df29-4828-8756-c9efadcd04fe": [1040, 1060],
    "63bbcd7f-80f7-4a9c-8afa-e85fc76d0f84": [1300, 980],
    "35701625-7808-4416-9413-acfd33bceb0a": [1560, 980],
    "cefb7535-e480-4bc0-aa75-c8934dde3cd4": [1820, 1060],

    # === RESET PASSWORD PATH (y: 1340-1520) ===
    "b9a5fea1-2495-4723-bc9b-3e572a70df69": [760,  1440],
    "5be755a2-d95c-437b-9cd7-0be74bd314a3": [1040, 1440],
    "2021582d-83fa-4fd4-9554-2b28c712ce64": [1300, 1440],
    "55a208b8-df5c-406e-851a-77c866ff533a": [1560, 1440],
}

# --- Node descriptions ---
DESCRIPTIONS = {
    "webhook-trigger":  "POST /webhook/auth\nRiceve: { mode, username, password, email }",
    "switch-mode":      "Instrada verso Login, Register, Forgot o Reset in base al campo 'mode'",
    "get-user-brand":   "Cerca utente nel DB Brand Profiles (Bloom 2.0) per username",
    "get-user-marketing": "Cerca utente nel DB Marketing Profile per username",
    "merge-users":      "Unisce i risultati da Brand + Marketing DB",
    "validate-user":    "Confronta la password inviata con quella salvata su Notion (3 strategie di lettura)",
    "check-auth":       "Verifica il flag 'authorized' dal nodo Validate User",
    "respond-success":  "200 OK - Restituisce success + username",
    "respond-error":    "401 Unauthorized - Credenziali non valide",
    "set-email-v65":    "Estrae l'email dal body del Webhook",
    "check-email-notion-v65": "Scarica tutti i profili dal Marketing DB per confronto email",
    "check-logic-v65":  "Verifica se l'email esiste gia' confrontando con i record Notion",
    "if-exists-v65":    "True = email gia' registrata, False = nuova registrazione",
    "respond-conflict-v65": "409 Conflict - Email gia' esistente",
    "create-user":      "Crea nuovo record in Marketing Profile DB con Username, Password, Email",
    "respond-reg-success-v65": "200 OK - Registrazione completata con success + username + email",
    "8460384d-880d-453c-ad9f-3c625c32449c": "Cerca utente nel Brand DB per email",
    "99538615-df29-4828-8756-c9efadcd04fe": "Verifica se l'utente esiste per procedere con il recupero",
    "63bbcd7f-80f7-4a9c-8afa-e85fc76d0f84": "Genera token HMAC-SHA256 con scadenza 1h e costruisce il link di reset",
    "35701625-7808-4416-9413-acfd33bceb0a": "Invia email con link di reset via SMTP Gmail",
    "cefb7535-e480-4bc0-aa75-c8934dde3cd4": "Risponde al frontend (messaggio generico per sicurezza)",
    "b9a5fea1-2495-4723-bc9b-3e572a70df69": "Valida il token: firma HMAC, scadenza, corrispondenza email",
    "5be755a2-d95c-437b-9cd7-0be74bd314a3": "Cerca l'utente nel Marketing DB per aggiornare la password",
    "2021582d-83fa-4fd4-9554-2b28c712ce64": "Aggiorna il campo Password nel record Notion",
    "55a208b8-df5c-406e-851a-77c866ff533a": "200 OK - Password aggiornata con successo",
}

# --- Sticky Notes (section labels) ---
STICKY_NOTES = [
    {
        "parameters": {
            "content": "## Bloom AI Unified Auth\n**Endpoint:** `POST /webhook/auth`\n\nGestisce 4 modalita':\n- `login` - Autenticazione utente\n- `register` - Registrazione nuovo account\n- `forgot_password` - Invio email di recupero\n- `reset_password` - Reset con token",
            "height": 260,
            "width": 320,
            "color": 1
        },
        "id": "sticky-header",
        "name": "Sticky Note",
        "type": "n8n-nodes-base.stickyNote",
        "typeVersion": 1,
        "position": [100, 340]
    },
    {
        "parameters": {
            "content": "## LOGIN\nCerca l'utente in entrambi i DB (Brand + Marketing), valida la password e risponde con success/error.",
            "height": 420,
            "width": 1340,
            "color": 4
        },
        "id": "sticky-login",
        "name": "Sticky Note1",
        "type": "n8n-nodes-base.stickyNote",
        "typeVersion": 1,
        "position": [680, 20]
    },
    {
        "parameters": {
            "content": "## REGISTRAZIONE\nVerifica se l'email esiste gia'. Se no, crea il profilo su Notion e risponde con successo.",
            "height": 420,
            "width": 1620,
            "color": 5
        },
        "id": "sticky-register",
        "name": "Sticky Note2",
        "type": "n8n-nodes-base.stickyNote",
        "typeVersion": 1,
        "position": [680, 440]
    },
    {
        "parameters": {
            "content": "## RECUPERO PASSWORD\nGenera un token sicuro, costruisce il link di reset e invia l'email via SMTP.",
            "height": 400,
            "width": 1340,
            "color": 2
        },
        "id": "sticky-forgot",
        "name": "Sticky Note3",
        "type": "n8n-nodes-base.stickyNote",
        "typeVersion": 1,
        "position": [680, 880]
    },
    {
        "parameters": {
            "content": "## RESET PASSWORD\nValida il token (firma + scadenza), trova l'utente e aggiorna la password su Notion.",
            "height": 340,
            "width": 1080,
            "color": 6
        },
        "id": "sticky-reset",
        "name": "Sticky Note4",
        "type": "n8n-nodes-base.stickyNote",
        "typeVersion": 1,
        "position": [680, 1320]
    },
]

# --- Apply positions and descriptions to nodes ---
for node in live["nodes"]:
    nid = node["id"]
    if nid in POSITIONS:
        node["position"] = POSITIONS[nid]
    if nid in DESCRIPTIONS:
        node["notes"] = DESCRIPTIONS[nid]

# --- Add sticky notes to nodes list ---
live["nodes"].extend(STICKY_NOTES)

print(f"\nRedesigned layout:")
print(f"  Nodes (incl. sticky notes): {len(live['nodes'])}")
print(f"  Sticky notes added: {len(STICKY_NOTES)}")
print(f"  Node descriptions added: {len(DESCRIPTIONS)}")

# --- Build payload ---
payload = {
    "name": "Bloom AI Unified Auth V7.1",
    "nodes": live["nodes"],
    "connections": live["connections"],
    "settings": live.get("settings", {})
}

# --- Verify ---
node_names = {n["name"] for n in payload["nodes"]}
conn_targets = set()
for src, data in payload["connections"].items():
    conn_targets.add(src)
    for outputs in data.get("main", []):
        for conn in outputs:
            conn_targets.add(conn["node"])
missing = conn_targets - node_names
if missing:
    print(f"ERROR: Missing nodes in connections: {missing}")
    sys.exit(1)
print(f"  All connections valid: YES")

# --- Save locally ---
with open("backup_workflows/Bloom_AI_Unified_Auth_V7.1_LAYOUT.json", "w") as f:
    json.dump(payload, f, indent=2)
print(f"\nSaved to backup_workflows/Bloom_AI_Unified_Auth_V7.1_LAYOUT.json")

# --- Upload ---
print(f"\nUploading to n8n cloud...")
resp = requests.put(f"{N8N_BASE_URL}/workflows/{WF_ID}", headers=HEADERS, json=payload)
if resp.ok:
    result = resp.json()
    print(f"Upload SUCCESS!")
    print(f"  Name: {result.get('name')}")
    print(f"  Active: {result.get('active')}")
    print(f"  Nodes: {len(result.get('nodes', []))}")
    print(f"  Version: {result.get('versionId', '?')}")
    if not result.get("active"):
        print("Activating...")
        act = requests.patch(f"{N8N_BASE_URL}/workflows/{WF_ID}/activate", headers=HEADERS)
        print("ACTIVATED!" if act.ok else f"Activation failed: {act.text}")
else:
    print(f"Upload FAILED: {resp.status_code}")
    print(resp.text[:1000])
    sys.exit(1)
