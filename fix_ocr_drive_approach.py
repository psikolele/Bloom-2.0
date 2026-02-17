"""
Sostituisce Read PDF to Base64 + OCR via Google Vision con:
  Convert PDF to GDoc OCR  → Export GDoc as Text → Prepare OCR Binary → Delete Temp GDoc

Usa Google Drive API per OCR nativo (nessun problema di binary data in N8N task runner).
"""
import json, requests, uuid

N8N_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIwMmRmNzQ5NC1hNjVjLTRjOTAtOTE5MC00NmViOWI4ODg5OGIiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzY4NTEyOTE5fQ.T-W7tlxC7dAA0dPHusS7yuZLpX-qAzuzYCUT653cC0k"
WORKFLOW_ID = "XmCaI5Q9MxNf0EP_65UvB"
HEADERS = {"X-N8N-API-KEY": N8N_API_KEY, "Content-Type": "application/json"}
BASE = "https://emanueleserra.app.n8n.cloud/api/v1"

print("📥 Fetch workflow...")
wf = requests.get(f"{BASE}/workflows/{WORKFLOW_ID}", headers=HEADERS).json()
nodes = wf["nodes"]
connections = wf["connections"]

# ── IDs nodi esistenti da rimuovere ──────────────────────────────────────────
ID_READ_B64 = "63b24149-5ca7-4b0f-b41a-11f719c64121"
ID_OCR_VIS  = "f95c89ee-f267-4c66-b8f4-0e2659f94ab5"

# ── Rimuovi nodi vecchi ───────────────────────────────────────────────────────
nodes = [n for n in nodes if n["id"] not in (ID_READ_B64, ID_OCR_VIS)]
connections.pop("Read PDF to Base64", None)
connections.pop("OCR via Google Vision", None)
print("🗑️  Rimossi: Read PDF to Base64, OCR via Google Vision")

# ── IDs nuovi nodi ────────────────────────────────────────────────────────────
ID_CONVERT = str(uuid.uuid4())
ID_EXPORT  = str(uuid.uuid4())
ID_DELETE  = str(uuid.uuid4())

# ── Nodo 1: Convert PDF to GDoc OCR ──────────────────────────────────────────
# POST /drive/v3/files/{fileId}/copy con mimeType=GDoc → Drive fa OCR automatico
node_convert = {
    "id": ID_CONVERT,
    "name": "Convert PDF to GDoc OCR",
    "type": "n8n-nodes-base.httpRequest",
    "typeVersion": 4.2,
    "position": [-1296, 1072],
    "parameters": {
        "method": "POST",
        "url": "={{ 'https://www.googleapis.com/drive/v3/files/' + $json.fileId + '/copy' }}",
        "authentication": "predefinedCredentialType",
        "nodeCredentialType": "googleDriveOAuth2Api",
        "sendBody": True,
        "specifyBody": "json",
        "jsonBody": '={"mimeType": "application/vnd.google-apps.document"}',
        "options": {}
    }
}

# ── Nodo 2: Export GDoc as Text ───────────────────────────────────────────────
# GET /drive/v3/files/{gdocId}/export?mimeType=text/plain → testo grezzo in $json.data
node_export = {
    "id": ID_EXPORT,
    "name": "Export GDoc as Text",
    "type": "n8n-nodes-base.httpRequest",
    "typeVersion": 4.2,
    "position": [-1152, 1072],
    "parameters": {
        "method": "GET",
        "url": "={{ 'https://www.googleapis.com/drive/v3/files/' + $json.id + '/export?mimeType=text%2Fplain' }}",
        "authentication": "predefinedCredentialType",
        "nodeCredentialType": "googleDriveOAuth2Api",
        "options": {
            "response": {
                "response": {
                    "responseFormat": "text"
                }
            }
        }
    }
}

# ── Aggiorna Prepare OCR Binary: legge $json.data invece di Vision API ────────
code_prepare = """
// Testo estratto da Google Drive OCR (via Export GDoc as Text)
const fullText = $('Export GDoc as Text').item.json.data || '[Nessun testo estratto]';

// Metadata originali dal file PDF
const originalFileName = $('Check IF PDF').item.json.fileName || 'document.pdf';
const targetIndex = $('Check IF PDF').item.json.targetIndex || '';
const parentFolder = $('Check IF PDF').item.json.parentFolder || '';
const gdocId = $('Convert PDF to GDoc OCR').item.json.id || '';

const txtFileName = originalFileName.replace(/\\.pdf$/i, '') + '_ocr.txt';
const binaryData = Buffer.from(fullText).toString('base64');

return [{
  json: {
    targetIndex,
    parentFolder,
    fileName: txtFileName,
    originalFileName,
    mimeType: 'text/plain',
    gdocId,
    ocrProcessed: true,
    ocrChars: fullText.length
  },
  binary: {
    data: {
      data: binaryData,
      mimeType: 'text/plain',
      fileName: txtFileName,
      fileExtension: 'txt'
    }
  }
}];
""".strip()

for n in nodes:
    if n["name"] == "Prepare OCR Binary":
        n["parameters"]["mode"]   = "runOnceForEachItem"
        n["parameters"]["jsCode"] = code_prepare
        print("✅ Aggiornato: Prepare OCR Binary (legge $json.data)")
        break

# ── Nodo 3: Delete Temp GDoc ──────────────────────────────────────────────────
# Cleanup: elimina il Google Doc temporaneo creato per OCR
node_delete = {
    "id": ID_DELETE,
    "name": "Delete Temp GDoc",
    "type": "n8n-nodes-base.httpRequest",
    "typeVersion": 4.2,
    "position": [-832, 1072],
    "parameters": {
        "method": "DELETE",
        "url": "={{ 'https://www.googleapis.com/drive/v3/files/' + $json.gdocId }}",
        "authentication": "predefinedCredentialType",
        "nodeCredentialType": "googleDriveOAuth2Api",
        "options": {
            "response": {
                "response": {
                    "responseFormat": "text"
                }
            }
        }
    }
}

nodes.extend([node_convert, node_export, node_delete])
print("✅ Aggiunti: Convert PDF to GDoc OCR, Export GDoc as Text, Delete Temp GDoc")

# ── Aggiorna connessioni ──────────────────────────────────────────────────────
# Check IF PDF [true] → Convert PDF to GDoc OCR
connections["Check IF PDF"]["main"][0] = [
    {"node": "Convert PDF to GDoc OCR", "type": "main", "index": 0}
]
# Convert → Export
connections["Convert PDF to GDoc OCR"] = {
    "main": [[{"node": "Export GDoc as Text", "type": "main", "index": 0}]]
}
# Export → Prepare OCR Binary
connections["Export GDoc as Text"] = {
    "main": [[{"node": "Prepare OCR Binary", "type": "main", "index": 0}]]
}
# Prepare OCR Binary → Delete Temp GDoc
connections["Prepare OCR Binary"] = {
    "main": [[{"node": "Delete Temp GDoc", "type": "main", "index": 0}]]
}
# Delete Temp GDoc → Auto Upsert to Pinecone
connections["Delete Temp GDoc"] = {
    "main": [[{"node": "Auto Upsert to Pinecone", "type": "main", "index": 0}]]
}
print("✅ Connessioni aggiornate")

# ── Push ──────────────────────────────────────────────────────────────────────
print("\n📤 Push workflow...")
settings = wf.get("settings", {})
for k in ["timeSavedMode", "availableInMCP"]:
    settings.pop(k, None)

payload = {
    "name":       wf["name"],
    "nodes":      nodes,
    "connections": connections,
    "settings":   settings,
    "staticData": wf.get("staticData")
}
r2 = requests.put(f"{BASE}/workflows/{WORKFLOW_ID}", headers=HEADERS, json=payload)

if r2.status_code == 200:
    print(f"\n✅ WORKFLOW AGGIORNATO! Nodi totali: {len(r2.json().get('nodes',[]))}")
    print(f"   Flusso: Check IF PDF → Convert→Export→Prepare→Delete→Upsert")
else:
    print(f"\n❌ ERRORE {r2.status_code}: {r2.text[:500]}")

# Patch: add credential ID to all 3 new HTTP Request nodes
# Applied inline after initial deploy due to "Credentials not found" error

# v2: Properly added 5 OCR nodes to workflow (were missing from canvas):
# Is PDF? (IF) → Convert PDF to GDoc OCR (HTTP copy) → Export GDoc as Text (HTTP export)
# → Restore OCR Metadata (Code, preserves targetIndex) → Auto Upsert to Pinecone
#                                                       → Delete Temp GDoc (HTTP delete)
# Non-PDF branch: Is PDF? false → Auto Upsert to Pinecone (unchanged)
