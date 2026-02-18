"""
Fix OCR: aggiunge nodo 'Read PDF to Base64' tra Check IF PDF e OCR Vision.
Risolve il problema binaryDataMode=filesystem dove $binary.data.data non è base64.
"""
import json, requests, uuid

N8N_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIwMmRmNzQ5NC1hNjVjLTRjOTAtOTE5MC00NmViOWI4ODg5OGIiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzY4NTEyOTE5fQ.T-W7tlxC7dAA0dPHusS7yuZLpX-qAzuzYCUT653cC0k"
WORKFLOW_ID  = "XmCaI5Q9MxNf0EP_65UvB"
GOOGLE_VISION_KEY = "AIzaSyAboPvQoOb3fgvnUlVXV6jR-53jOWTjfEM"
HEADERS = {"X-N8N-API-KEY": N8N_API_KEY, "Content-Type": "application/json"}
BASE    = "https://emanueleserra.app.n8n.cloud/api/v1"

print("📥 Fetch workflow...")
r  = requests.get(f"{BASE}/workflows/{WORKFLOW_ID}", headers=HEADERS)
wf = r.json()
nodes       = wf["nodes"]
connections = wf["connections"]

# ── ID nuovo nodo ──────────────────────────────────────────────────────────────
ID_READ_B64 = str(uuid.uuid4())
# Posizione: tra Check IF PDF [-1456,1120] e OCR [-1232,1200]
POS_READ_B64 = [-1344, 1200]

# ── Nuovo nodo: Read PDF to Base64 (Code) ─────────────────────────────────────
code_read = """
// Legge il binary data dal filesystem di N8N e lo converte in base64
// Necessario perché binaryDataMode=filesystem non espone il base64 direttamente

const items = $input.all();
const result = [];

for (const item of items) {
  const binaryBuffer = await this.helpers.getBinaryDataBuffer(item, 'data');
  const base64 = binaryBuffer.toString('base64');

  result.push({
    json: {
      ...item.json,
      fileBase64: base64
    },
    binary: item.binary
  });
}

return result;
""".strip()

node_read_b64 = {
    "id":          ID_READ_B64,
    "name":        "Read PDF to Base64",
    "type":        "n8n-nodes-base.code",
    "typeVersion": 2,
    "position":    POS_READ_B64,
    "parameters": {
        "mode":   "runOnceForAllItems",
        "jsCode": code_read
    }
}
nodes.append(node_read_b64)
print("✅ Aggiunto nodo: Read PDF to Base64")

# ── Aggiorna body OCR: usa $json.fileBase64 invece di $binary.data.data ────────
for n in nodes:
    if n["name"] == "OCR via Google Vision":
        n["parameters"]["jsonBody"] = (
            '={{ JSON.stringify({'
            '"requests": [{'
            '"inputConfig": {"content": $json.fileBase64, "mimeType": "application/pdf"},'
            '"features": [{"type": "DOCUMENT_TEXT_DETECTION"}],'
            '"pages": [1,2,3,4,5]'
            '}]'
            '}) }}'
        )
        print("✅ Aggiornato body OCR: usa $json.fileBase64")
        break

# ── Modifica connessioni ───────────────────────────────────────────────────────
# PRIMA: Check IF PDF [true] → OCR via Google Vision
# DOPO:  Check IF PDF [true] → Read PDF to Base64 → OCR via Google Vision

# Check IF PDF branch[0] (true): cambia da OCR a Read PDF to Base64
check_conns = connections["Check IF PDF"]["main"]
check_conns[0] = [{"node": "Read PDF to Base64", "type": "main", "index": 0}]
print("✅ Check IF PDF [true] → Read PDF to Base64")

# Read PDF to Base64 → OCR via Google Vision
connections["Read PDF to Base64"] = {
    "main": [[{"node": "OCR via Google Vision", "type": "main", "index": 0}]]
}
print("✅ Read PDF to Base64 → OCR via Google Vision")

# ── Push ───────────────────────────────────────────────────────────────────────
print("\n📤 Push workflow...")
settings = wf.get("settings", {})
for k in ["timeSavedMode", "availableInMCP"]:
    settings.pop(k, None)

payload = {
    "name":        wf["name"],
    "nodes":       nodes,
    "connections": connections,
    "settings":    settings,
    "staticData":  wf.get("staticData")
}

r2 = requests.put(f"{BASE}/workflows/{WORKFLOW_ID}", headers=HEADERS, json=payload)

if r2.status_code == 200:
    print(f"\n✅ WORKFLOW AGGIORNATO!")
    print(f"   Nodi totali: {len(r2.json().get('nodes', []))}")
else:
    print(f"\n❌ ERRORE {r2.status_code}: {r2.text[:500]}")
