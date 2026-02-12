# Come Applicare il Fix RAG Automaticamente

Hai **2 script** per applicare automaticamente il fix a n8n.

## 📋 Prerequisiti

- Accesso a una macchina che può raggiungere `n8n.bloom-ai.it`
- Le credenziali API sono già incluse negli script

## 🚀 Metodo 1: Script Python (Consigliato)

### Vantaggi
- ✅ Più robusto
- ✅ Gestione errori migliore
- ✅ Conferma prima di applicare

### Esecuzione

```bash
# Dal root del progetto Bloom-2.0
python3 scripts/apply_rag_fix_to_n8n.py
```

### Output Atteso

```
======================================================================
APPLYING RAG WORKFLOW FIX TO N8N
======================================================================

📋 Step 1: Finding RAG workflow in n8n
----------------------------------------------------------------------
✓ Found 12 workflows
  Found RAG workflow: RAG Didattica (ID: abc123)

📥 Step 2: Backing up current workflow
----------------------------------------------------------------------
✓ Current workflow backed up to: workflow_backup_abc123.json
  Name: RAG Didattica
  ID: abc123
  Nodes: 62
  Active: True

📂 Step 3: Loading fixed workflow
----------------------------------------------------------------------
✓ Loaded fixed workflow from: backup_workflows/RAG_workflow_FIXED_DATA_LOADER.json
  Nodes in fixed workflow: 62

🔧 Step 4: Merging configurations
----------------------------------------------------------------------
✓ Preserved workflow metadata:
  ID: abc123
  Name: RAG Didattica
  Active: True

📊 Step 5: Changes to be applied
----------------------------------------------------------------------

🔧 MODIFICATIONS:
  1. Auto Data Loader: Added 'dataType: binary'
  2. Connection changed: Auto Download → Auto Data Loader
  3. Flow: Download → Data Loader → Splitter → Pinecone

⚠️  This will UPDATE workflow 'RAG Didattica' (ID: abc123)
Continue? [y/N]: y

🚀 Step 6: Uploading fixed workflow to n8n
----------------------------------------------------------------------
✅ Workflow updated successfully!
   Name: RAG Didattica
   ID: abc123
   Nodes: 62

======================================================================
✅ FIX APPLIED SUCCESSFULLY!
======================================================================
```

---

## 🔧 Metodo 2: Script Bash

### Vantaggi
- ✅ Non richiede Python
- ✅ Usa solo curl e bash standard

### Esecuzione

```bash
# Dal root del progetto Bloom-2.0
./scripts/apply_rag_fix_to_n8n.sh
```

**Nota**: Se `jq` è installato, lo script farà parsing JSON più accurato. Altrimenti usa `sed` (meno affidabile ma funziona).

---

## ⚠️ Errori Comuni

### "Could not resolve host: n8n.bloom-ai.it"

**Causa**: n8n non è raggiungibile dal tuo computer

**Soluzione**:
1. Verifica che n8n.bloom-ai.it sia raggiungibile:
   ```bash
   ping n8n.bloom-ai.it
   ```
2. Se sei dietro VPN, connettiti alla VPN
3. Se n8n è su rete interna, esegui lo script da quella rete

### "Failed to update workflow: HTTP 401"

**Causa**: API key non valida o scaduta

**Soluzione**:
1. Verifica l'API key in n8n: Settings → API
2. Aggiorna l'API key negli script se necessario

### "No RAG workflow found"

**Causa**: Il workflow non ha "RAG" nel nome

**Soluzione**:
1. Lo script mostrerà tutti i workflow disponibili
2. Modifica lo script e cerca il workflow corretto
3. Oppure applica il fix manualmente (vedi `MANUAL_FIX_INSTRUCTIONS.md`)

---

## ✅ Dopo aver Applicato il Fix

### 1. Verifica in n8n

1. Vai su n8n.bloom-ai.it
2. Apri il workflow RAG
3. Controlla il nodo "Auto Data Loader"
   - Deve avere **Data Type: Binary**
4. Controlla le connessioni:
   - Auto Download → Auto Data Loader ✅
   - Auto Data Loader → Auto Upsert to Pinecone ✅

### 2. Re-indicizza i Documenti

```bash
curl -X POST https://n8n.bloom-ai.it/webhook/manual-ingest-trigger-fix
```

Oppure apri nel browser:
```
https://n8n.bloom-ai.it/webhook/manual-ingest-trigger-fix
```

### 3. Verifica i Chunk

Dopo 2-3 minuti (tempo per indicizzare):

```bash
python3 scripts/verify_rag_chunks.py
```

**Output atteso:**
```
✅ rag-pessina-db is HEALTHY
   Chunks contain real content from documents

✅ rag-jobcourier-db is HEALTHY
   Chunks contain real content from documents
```

### 4. Testa la Chat

Fai una domanda tipo:
```
Quali corsi offre l'Istituto Pessina?
```

**Prima del fix:**
```
❌ "Non ho trovato informazioni specifiche..."
```

**Dopo il fix:**
```
✅ "L'Istituto Pessina offre i seguenti corsi:
    1. Servizi Commerciali - ...
    2. Servizi Socio-Sanitari - ...
    [dettagli dai PDF]"
```

---

## 🔄 Rollback (se qualcosa va storto)

Se il fix causa problemi, puoi ripristinare il backup:

```bash
# Lo script ha creato un backup: workflow_backup_abc123.json

# Ripristina manualmente in n8n:
# 1. Vai su n8n
# 2. Workflow → Import from File
# 3. Seleziona workflow_backup_abc123.json
```

---

## 📞 Aiuto

Se gli script non funzionano:
1. Controlla i prerequisiti (connessione a n8n)
2. Leggi i messaggi di errore
3. Usa il metodo manuale: `MANUAL_FIX_INSTRUCTIONS.md`

---

## 📁 File Correlati

- `apply_rag_fix_to_n8n.py` - Script Python (consigliato)
- `apply_rag_fix_to_n8n.sh` - Script Bash (alternativo)
- `verify_rag_chunks.py` - Verifica che i chunk siano corretti
- `../backup_workflows/RAG_workflow_FIXED_DATA_LOADER.json` - Workflow corretto
- `../MANUAL_FIX_INSTRUCTIONS.md` - Guida per applicare il fix manualmente
- `../RAG_DATA_LOADER_FIX.md` - Documentazione tecnica del problema
