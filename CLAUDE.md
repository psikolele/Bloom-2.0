# CLAUDE.md — Note Tecniche per Claude

## ⚠️ Perché le modifiche al workflow N8N non funzionano tramite GitHub

### Il problema

Pushare un file `.json` di workflow su GitHub **NON aggiorna** il workflow live su N8N Cloud.
Le modifiche al workflow devono essere inviate **direttamente via N8N API**.

### Architettura attuale

```
GitHub Repository             N8N Cloud (emanueleserra.app.n8n.cloud)
──────────────────            ──────────────────────────────────────
backup_workflows/*.json  ≠    Workflow live (oRYSQ9tk63yPJaqt)
                              ↑
                              Aggiornabile solo via PUT /api/v1/workflows/{id}
```

### Motivi tecnici

1. **Il workflow vive nel cloud N8N** — non è nel repository Git. I file `.json` locali sono solo backup manuali, non la sorgente di verità.

2. **Non c'è sincronizzazione automatica** — pushare su GitHub non triggera alcun aggiornamento su N8N Cloud. Non esiste una GitHub Action configurata per questo.

3. **Le credenziali N8N non sono nei GitHub Secrets** — anche se si creasse una Action, servirebbe il token `N8N_API_KEY` configurato come secret nel repository.

4. **I backup locali sono spesso obsoleti** — ad esempio, il nodo `Combine RAG with Input Data` esiste solo nel workflow live e non in nessun backup locale (verificato il 21/02/2026).

5. **Alcune modifiche cambiano solo i prompt LLM** — non si riflettono nei file JSON locali a meno di un export manuale dal pannello N8N.

---

## Fix applicato il 21/02/2026 — Bug ReferenceLink (Execution 7709)

### Problema

Il nodo `Combine RAG with Input Data` leggeva `ReferenceContent` da `prepNode.ReferenceContent`, ma il nodo "2. Prepare Input Variables" non imposta mai questo campo → `ReferenceContent` sempre vuoto → `hasReferenceContent: false`.

Di conseguenza:
- I prompt LLM (3a, 3b, 3c) ricevevano `ReferenceLink` ✅ (il link è nelle variabili)
- Ma `ReferenceContent` era sempre `""` ❌ (nessun contenuto della pagina)
- La LLM usava solo i parametri URL per inferire il contesto

### Fix applicato via API

**File modificato nel workflow live:** nodo `Combine RAG with Input Data` (tipo: Code)

**Aggiunto:** web scraping del `ReferenceLink` con doppio tentativo:
1. **HTTP Request diretto** con header `User-Agent` browser-like (timeout 7s)
2. **Jina AI Reader** come fallback (`https://r.jina.ai/{url}`) per URL con anti-scraping

**Script utilizzato:** `fix_reference_link_workflow.py`

**Backup pre-fix:** `backup_workflows/Caption_Flow_V2_oRYSQ9tk63yPJaqt_FIX_REFERENCELINK_20260221_2050_BEFORE_FIX.json`

**Backup post-fix:** `backup_workflows/Caption_Flow_V2_oRYSQ9tk63yPJaqt_FIX_JINA_20260221_2113.json`

### Risultati test post-fix

| Execution | Account      | ReferenceLink | hasReferenceContent | Caption                                      |
|-----------|-------------|---------------|---------------------|----------------------------------------------|
| 7721      | job_courier | JobCourier URL | false (sito blocca)  | Menziona Randstad, Mezzovico, Ticino ✅       |
| 7722      | job_courier | JobCourier URL | false (sito blocca)  | Menziona Randstad SA, Ticino, JobCourier ✅   |

> **Nota:** Il sito `jobroom.jobcourier.ch` blocca sia il fetch diretto che Jina AI.
> Tuttavia la LLM estrae correttamente il contesto dai parametri URL (`job-title`, `company-name`, `location`).
> Per URL non bloccati, `ReferenceContent` viene popolato correttamente.

---

## Come aggiornare il workflow N8N (procedura corretta)

```bash
# 1. Modificare il codice in fix_reference_link_workflow.py
# 2. Eseguire lo script per applicare il fix via API
python3 fix_reference_link_workflow.py

# Oppure direttamente:
python3 -c "
import requests, json
API_KEY = '...'  # N8N API Key
BASE_URL = 'https://emanueleserra.app.n8n.cloud/api/v1'
WORKFLOW_ID = 'oRYSQ9tk63yPJaqt'
# 1. Fetch
wf = requests.get(f'{BASE_URL}/workflows/{WORKFLOW_ID}', headers={'X-N8N-API-KEY': API_KEY}).json()
# 2. Modifica wf['nodes']...
# 3. Push
requests.put(f'{BASE_URL}/workflows/{WORKFLOW_ID}', headers={...}, json={...})
"
```

## Soluzione raccomandata per GitHub

Creare `.github/workflows/sync-n8n.yml`:
```yaml
name: Sync N8N Workflow
on:
  push:
    paths: ['backup_workflows/Caption_Flow_V2_*.json']
jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Push workflow to N8N
        run: |
          curl -X PUT \
            -H "X-N8N-API-KEY: ${{ secrets.N8N_API_KEY }}" \
            -H "Content-Type: application/json" \
            -d @backup_workflows/Caption_Flow_V2_oRYSQ9tk63yPJaqt_FIX_JINA_20260221_2113.json \
            https://emanueleserra.app.n8n.cloud/api/v1/workflows/oRYSQ9tk63yPJaqt
```

---

## Struttura Workflow Caption Flow V.2 (oRYSQ9tk63yPJaqt)

```
CaptionFlow Webhook
├── 2. Prepare Input Variables (Topic, Audience, Voice, Platform, Account, ReferenceLink)
│   └── Map Account to RAG DB
│       └── Prepare Company Knowledge Query
│           └── Query Company Knowledge (AI Agent + Pinecone)
│               └── Combine RAG with Input Data  ← FIX QUI
│                   ├── ReferenceLink scraping (HTTP + Jina AI)
│                   └── 3a. Generate Content Concept (Gemini)
│                       └── 3b. Generate Image Prompt (Gemini)
│                           └── 3c. Generate Post Caption (Gemini)
│                               └── 4a. Create Image Task (Kie AI)
│                                   └── 4b/4c. Wait + Get Image
│                                       └── 5. Prepare Data
│                                           └── Upload Cloudinary
│                                               ├── Respond to Frontend
│                                               └── Check via Email
│                                                   └── If Approved → Upload Instagram
└── Elabora Dati Ricevuti → Salva su Google Sheets
```

---

## Account validi (Map Account to RAG DB)

`job_courier`, `pessina`, `blc`, `footeasy`, `walmoss`

> Account non in lista → errore: "ACCOUNT NON RICONOSCIUTO"

---

## API N8N — Riferimento rapido

```
Base URL:    https://emanueleserra.app.n8n.cloud/api/v1
Auth header: X-N8N-API-KEY: <token>
Workflow ID: oRYSQ9tk63yPJaqt
Webhook URL: https://emanueleserra.app.n8n.cloud/webhook/caption-flow

GET  /workflows/{id}              → fetch workflow
PUT  /workflows/{id}              → aggiorna workflow (body: {nodes, connections, settings, name})
GET  /executions?workflowId={id}  → lista executions
GET  /executions/{id}?includeData=true → dettaglio execution con runData
```
