"""
Aggiunge OCR Google Vision al workflow RAG JobCourier.
Flusso aggiunto:
  Auto Download New File → Check IF PDF → [false] → Auto Upsert to Pinecone
                                        → [true]  → OCR via Google Vision → Prepare OCR Binary → Auto Upsert to Pinecone
"""
import json, requests, uuid

N8N_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIwMmRmNzQ5NC1hNjVjLTRjOTAtOTE5MC00NmViOWI4ODg5OGIiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzY4NTEyOTE5fQ.T-W7tlxC7dAA0dPHusS7yuZLpX-qAzuzYCUT653cC0k"
WORKFLOW_ID = "XmCaI5Q9MxNf0EP_65UvB"
GOOGLE_VISION_KEY = "AIzaSyAboPvQoOb3fgvnUlVXV6jR-53jOWTjfEM"
HEADERS = {"X-N8N-API-KEY": N8N_API_KEY, "Content-Type": "application/json"}
BASE = "https://emanueleserra.app.n8n.cloud/api/v1"

# ── Fetch workflow ────────────────────────────────────────────────────────────
print("📥 Fetch workflow...")
r = requests.get(f"{BASE}/workflows/{WORKFLOW_ID}", headers=HEADERS)
wf = r.json()
nodes = wf["nodes"]
connections = wf["connections"]

# ── Posizioni di riferimento ──────────────────────────────────────────────────
# Auto Download New File: [4736, 1472]  → Auto Upsert to Pinecone: [5040, 1456]
# Nuovi nodi intercalati:
POS_CHECK   = [4900, 1472]
POS_OCR     = [5040, 1680]
POS_PREPARE = [5240, 1680]

# ── IDs nuovi nodi ────────────────────────────────────────────────────────────
ID_CHECK   = str(uuid.uuid4())
ID_OCR     = str(uuid.uuid4())
ID_PREPARE = str(uuid.uuid4())

# ── Nuovo nodo 1: Check IF PDF ────────────────────────────────────────────────
node_check = {
    "id": ID_CHECK,
    "name": "Check IF PDF",
    "type": "n8n-nodes-base.if",
    "typeVersion": 2.2,
    "position": POS_CHECK,
    "parameters": {
        "conditions": {
            "options": {"caseSensitive": True, "leftValue": "", "typeValidation": "strict"},
            "conditions": [{
                "id": str(uuid.uuid4()),
                "leftValue": "={{ $json.mimeType }}",
                "rightValue": "application/pdf",
                "operator": {"type": "string", "operation": "equals"}
            }],
            "combinator": "and"
        }
    }
}

# ── Nuovo nodo 2: OCR via Google Vision ───────────────────────────────────────
ocr_body = (
    '={{ JSON.stringify({'
    '"requests": [{'
    '"inputConfig": {"content": $binary.data.data, "mimeType": "application/pdf"},'
    '"features": [{"type": "DOCUMENT_TEXT_DETECTION"}],'
    '"pages": [1,2,3,4,5]'
    '}]'
    '}) }}'
)

node_ocr = {
    "id": ID_OCR,
    "name": "OCR via Google Vision",
    "type": "n8n-nodes-base.httpRequest",
    "typeVersion": 4.2,
    "position": POS_OCR,
    "parameters": {
        "method": "POST",
        "url": f"https://vision.googleapis.com/v1/files:annotate?key={GOOGLE_VISION_KEY}",
        "sendBody": True,
        "specifyBody": "json",
        "jsonBody": ocr_body,
        "options": {}
    }
}

# ── Nuovo nodo 3: Prepare OCR Binary ─────────────────────────────────────────
code_ocr = """
const items = $input.all();
const result = [];

for (const item of items) {
  const response = item.json;
  const responses = response.responses || [];

  let fullText = '';
  for (const resp of responses) {
    const text = resp.fullTextAnnotation?.text || '';
    fullText += text + '\\n\\n';
  }

  if (!fullText.trim()) {
    fullText = '[Nessun testo estratto dal PDF tramite OCR]';
  }

  const originalFileName = item.json.fileName || 'document.pdf';
  const txtFileName = originalFileName.replace(/\\.pdf$/i, '') + '_ocr.txt';
  const binaryData = Buffer.from(fullText).toString('base64');

  result.push({
    json: {
      ...item.json,
      mimeType: 'text/plain',
      fileName: txtFileName,
      ocrProcessed: true,
      originalFileName: originalFileName,
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
  });
}

return result;
""".strip()

node_prepare = {
    "id": ID_PREPARE,
    "name": "Prepare OCR Binary",
    "type": "n8n-nodes-base.code",
    "typeVersion": 2,
    "position": POS_PREPARE,
    "parameters": {
        "mode": "runOnceForEachItem",
        "jsCode": code_ocr
    }
}

# ── Aggiunge nodi ─────────────────────────────────────────────────────────────
nodes.extend([node_check, node_ocr, node_prepare])
print(f"✅ Aggiunti 3 nodi: Check IF PDF, OCR via Google Vision, Prepare OCR Binary")

# ── Modifica connessioni ──────────────────────────────────────────────────────
# PRIMA: Auto Download New File → Auto Upsert to Pinecone (main[0])
# DOPO:  Auto Download New File → Check IF PDF (main[0])
#        Check IF PDF [false=1] → Auto Upsert to Pinecone (main[0])
#        Check IF PDF [true=0]  → OCR via Google Vision (main[0])
#        OCR via Google Vision  → Prepare OCR Binary (main[0])
#        Prepare OCR Binary     → Auto Upsert to Pinecone (main[0]) ← secondo input

# Rimuovi connessione Auto Download → Auto Upsert
old_dl_conn = connections.get("Auto Download New File", {})
if "main" in old_dl_conn:
    old_dl_conn["main"][0] = [c for c in old_dl_conn["main"][0]
                               if c.get("node") != "Auto Upsert to Pinecone"]
print("✅ Rimossa connessione Auto Download → Auto Upsert")

# Auto Download New File → Check IF PDF
if "Auto Download New File" not in connections:
    connections["Auto Download New File"] = {}
if "main" not in connections["Auto Download New File"]:
    connections["Auto Download New File"]["main"] = [[]]
connections["Auto Download New File"]["main"][0].append({
    "node": "Check IF PDF", "type": "main", "index": 0
})
print("✅ Auto Download New File → Check IF PDF")

# Check IF PDF [true=0] → OCR via Google Vision
connections["Check IF PDF"] = {
    "main": [
        # branch 0 = true (è PDF)
        [{"node": "OCR via Google Vision", "type": "main", "index": 0}],
        # branch 1 = false (non è PDF) → va diretto a Upsert
        [{"node": "Auto Upsert to Pinecone", "type": "main", "index": 0}]
    ]
}
print("✅ Check IF PDF → OCR Vision (true) + Auto Upsert (false)")

# OCR via Google Vision → Prepare OCR Binary
connections["OCR via Google Vision"] = {
    "main": [[{"node": "Prepare OCR Binary", "type": "main", "index": 0}]]
}
print("✅ OCR via Google Vision → Prepare OCR Binary")

# Prepare OCR Binary → Auto Upsert to Pinecone (secondo ingresso main)
connections["Prepare OCR Binary"] = {
    "main": [[{"node": "Auto Upsert to Pinecone", "type": "main", "index": 0}]]
}
print("✅ Prepare OCR Binary → Auto Upsert to Pinecone")

# ── Push workflow ─────────────────────────────────────────────────────────────
print("\n📤 Push workflow modificato...")
wf["nodes"] = nodes
wf["connections"] = connections

# Solo i campi accettati dalla PUT API
settings = wf.get("settings", {})
# Rimuovi campi non accettati da PUT /settings
for k in ["timeSavedMode", "availableInMCP"]:
    settings.pop(k, None)

payload = {
    "name": wf["name"],
    "nodes": wf["nodes"],
    "connections": wf["connections"],
    "settings": settings,
    "staticData": wf.get("staticData")
}

r2 = requests.put(f"{BASE}/workflows/{WORKFLOW_ID}",
                  headers=HEADERS, json=payload)

if r2.status_code == 200:
    print(f"\n✅ WORKFLOW AGGIORNATO CON SUCCESSO!")
    print(f"   Nodi totali: {len(r2.json().get('nodes', []))}")
    print(f"   URL: https://emanueleserra.app.n8n.cloud/workflow/{WORKFLOW_ID}")
else:
    print(f"\n❌ ERRORE {r2.status_code}: {r2.text[:500]}")
