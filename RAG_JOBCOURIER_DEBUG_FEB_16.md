# RAG JobCourier Debug - 16 Febbraio 2026

## 🎯 Executive Summary

**Problema**: Execution #7244 del workflow RAG ha prodotto solo 6 chunk (di cui 3 duplicati) nell'index `rag-jobcourier-db` invece dei 20-50+ chunk attesi da file multipli (PDFs + MD).

**Root Cause Identificato**: Il Text Splitter non era connesso al flusso "Auto" → il chunking NON veniva eseguito correttamente.

**Fix Applicato**: Connesso "Recursive Character Text Splitter1" (chunkSize=1500, chunkOverlap=200) al nodo "Auto Upsert to Pinecone".

**Risultato**: Workflow fixato e deployato ✅, index pulito ✅, pronto per re-indexing.

---

## 📊 Analisi del Problema

### 1. Stato Iniziale dei Chunk

**Index**: `rag-jobcourier-db`
**Total vectors**: 6 (3 unici + 3 duplicati)

| Chunk | Dimensione | Status | Contenuto |
|-------|------------|--------|-----------|
| 1, 2  | 1481 chars | DUPLICATI | "# Job Courier\n\n## Summary..." |
| 3, 4  | 74 chars | DUPLICATI ⚠️ | "Il tuo partner strategico..." |
| 5, 6  | 1414 chars | DUPLICATI | "Piattaforma online che facilita..." |

**Problemi critici**:
1. ❌ Solo 3 chunk unici da multipli file (PDFs + MD)
2. ❌ 2 chunk troppo piccoli (74 caratteri)
3. ❌ Source: "blob" per tutti i chunk (nome file mancante)
4. ❌ 3 coppie di duplicati (buffer di 5 minuti tra execution)

### 2. Investigazione del Workflow

**Workflow ID**: `XmCaI5Q9MxNf0EP_65UvB`
**Nome**: "RAG | Google Drive to Pinecone via OpenRouter & Gemini | Chat with RAG"
**Total nodes**: 63

**Flusso "Auto" (per JobCourier)**:
```
Auto Scheduled Check / Manual Trigger
  → Auto Generate Timestamp
    → Auto Find RAG Folders
      → Auto List Files In RAG
        → Pass Through Data
          → Check If Files Found
            → Auto Determine Index
              → Auto Download New File
                → Auto Upsert to Pinecone ❌ PROBLEMA QUI!
                  ↑ ai_document: Auto Data Loader ✅
                  ↑ ai_embedding: Auto Embeddings OpenAI ✅
                  ↑ ai_textSplitter: ??? MANCANTE ❌
                  ↑ main: Auto Download New File ✅
```

**ROOT CAUSE TROVATO**:
Il nodo "Recursive Character Text Splitter1" esisteva con la configurazione corretta (chunkSize=1500, chunkOverlap=200) ma **NON era connesso** a "Auto Upsert to Pinecone"!

**Risultato**: I documenti venivano processati SENZA chunking (o con chunking primitivo di default), producendo solo 3 chunk mal formattati invece di 20-50+ chunk corretti.

### 3. Configurazione Nodi

#### Text Splitter Esistente (ma non connesso)
```json
{
  "name": "Recursive Character Text Splitter1",
  "type": "@n8n/n8n-nodes-langchain.textSplitterRecursiveCharacterTextSplitter",
  "id": "c5ac9ba7-4191-4cae-a082-f003bda1299a",
  "parameters": {
    "chunkSize": 1500,
    "chunkOverlap": 200,
    "options": {}
  },
  "position": [5248, 1936]
}
```

#### Auto Upsert to Pinecone
```json
{
  "name": "Auto Upsert to Pinecone",
  "type": "@n8n/n8n-nodes-langchain.vectorStorePinecone",
  "id": "54ac5538-9767-4f1e-b66c-01aa6a1fca35",
  "parameters": {
    "mode": "insert",
    "pineconeIndex": {
      "__rl": true,
      "value": "={{ $json.targetIndex }}",
      "mode": "id"
    },
    "options": {
      "pineconeNamespace": ""
    }
  },
  "position": [5040, 1456]
}
```

**Prima del fix - Connessioni a "Auto Upsert to Pinecone"**:
- ✅ Auto Data Loader (ai_document)
- ✅ Auto Embeddings OpenAI (ai_embedding)
- ✅ Auto Download New File (main)
- ❌ **Text Splitter MANCANTE** (ai_textSplitter)

---

## 🔧 Fix Applicato

### 1. Connessione Text Splitter

**Script utilizzato**: `fix_workflow_text_splitter.py`

**Modifica effettuata**:
```json
// Connessioni di "Recursive Character Text Splitter1"
{
  "ai_textSplitter": [
    [
      {
        "node": "Auto Data Loader",
        "type": "ai_textSplitter",
        "index": 0
      },
      {
        "node": "Auto Upsert to Pinecone",  // ← AGGIUNTA QUESTA CONNESSIONE
        "type": "ai_textSplitter",
        "index": 0
      }
    ]
  ]
}
```

**Risultato**: Il Text Splitter è ora connesso correttamente al flusso Auto.

### 2. Deploy su N8N

**Metodo**: API PUT /api/v1/workflows/{id}
**Status**: ✅ 200 OK - Deploy completato con successo
**Timestamp**: 2026-02-16 12:13

**Payload usato** (campi essenziali):
```json
{
  "name": "RAG | Google Drive to Pinecone...",
  "nodes": [...],
  "connections": {...},
  "settings": {}
}
```

**Note**: Il payload iniziale con tutti i campi `settings` causava errore 400. Risolto utilizzando solo campi base.

### 3. Backup e Pulizia Index

**Backup creato**: `backup_jobcourier_chunks_20260216_121348.json`
- 6 chunk salvati con metadata completi
- Timestamp: 2026-02-16 12:13:48

**Pulizia index**:
```bash
python3 clean_jobcourier_index.py
```
- Status: ✅ Completata
- Eliminati: 6 vettori
- Stato finale: 0 vettori nell'index rag-jobcourier-db

---

## 📝 File Creati

### Script

1. **`backup_jobcourier_chunks.py`**
   - Backup dei chunk esistenti da Pinecone
   - Analisi duplicati e dimensioni
   - Output: JSON con tutti i chunk

2. **`fix_workflow_text_splitter.py`**
   - Modifica workflow per connettere Text Splitter
   - Deploy automatico via API N8N
   - Validazione e rollback su errore

3. **`clean_jobcourier_index.py`**
   - Pulizia index Pinecone prima del re-indexing
   - Conferma utente richiesta
   - Verifica stato pre/post pulizia

### Backup

1. **`backup_jobcourier_chunks_20260216_121348.json`**
   - Backup completo dei 6 chunk esistenti
   - Include metadata, text, scores, IDs
   - Timestamp e summary

2. **`workflow_attivo.json`**
   - Workflow originale scaricato da N8N
   - Prima delle modifiche

3. **`workflow_attivo_FIXED.json`**
   - Workflow modificato con Text Splitter connesso
   - Pronto per deploy

### Documentazione

1. **`RAG_JOBCOURIER_DEBUG_FEB_16.md`** (questo file)
   - Analisi completa del problema
   - Root cause identificato
   - Fix applicati
   - Prossimi passi

---

## ✅ Verifica End-to-End

### Test 1: Chunking Corretto

**Stato attuale**: ✅ Workflow fixato e deployato

**Prossimi passi per testare**:

1. **Carica file di test su Google Drive**:
   - Cartella: "RAG Database JobCourier" (o equivalente)
   - File: PDFs o MD con contenuto significativo (3-10 pagine)
   - Esempio: documento JobCourier con descrizione servizi, prezzi, etc.

2. **Triggerare workflow**:
   - **Opzione A (Automatica)**: Attendi il prossimo schedule (ogni 30 minuti)
   - **Opzione B (Manuale)**:
     ```
     1. Apri N8N UI: https://emanueleserra.app.n8n.cloud
     2. Apri workflow "RAG | Google Drive to Pinecone..."
     3. Click su "Execute Workflow"
     ```

3. **Monitorare execution**:
   - Verifica che completa con successo
   - Check logs per vedere:
     - Quanti file sono stati trovati
     - Quanti chunk sono stati generati
     - Se ci sono errori

4. **Verificare risultati in Pinecone**:
   ```bash
   python3 scripts/verify_rag_chunks.py
   ```

**Expected results**:
```
rag-jobcourier-db:
  Total vectors: 15-50+ (dipende dalla dimensione dei file)
  Valid chunks (>500 chars): 100% (tranne eventualmente l'ultimo)
  Metadata-only chunks (<100 chars): 0%
  Source field: Nome file reale (es: "jobcourier-info.md", non "blob")
```

**Criteri di successo**:
- ✅ Total vectors >> 6 (almeno 15-20 per un documento medio)
- ✅ Ogni chunk ha 1400-1500 caratteri (tranne l'ultimo che può essere più piccolo)
- ✅ Source = nome file reale, NON "blob"
- ✅ NO chunk < 100 caratteri (metadata-only)
- ✅ NO duplicati (stessi chunk con ID diversi)

### Test 2: Query RAG Funzionante

**Dopo aver verificato che i chunk sono corretti**:

1. **Accedi alla web app Bloom 2.0**:
   ```
   URL: https://bloom-2-0.vercel.app/
   ```

2. **Seleziona cartella JobCourier**

3. **Fai query sul contenuto del documento**:
   - Esempio: "Quali servizi offre Job Courier?"
   - Esempio: "Come funziona la piattaforma Job Courier?"

4. **Verifica risposta**:
   - ✅ Il RAG trova i chunk rilevanti
   - ✅ La risposta è completa e accurata
   - ✅ Il chatbot cita la source corretta (nome file, non "blob")

---

## 🔍 Lessons Learned

### 1. Problema di Connessioni Orfane

**Problema**: Il workflow aveva nodi configurati correttamente ma non connessi al flusso principale.

**Lesson**: Quando si aggiungono nuovi nodi a un workflow complesso:
1. Verificare sempre che siano effettivamente connessi
2. Testare con un file di esempio prima di usare in produzione
3. Monitorare gli execution logs per vedere quali nodi vengono eseguiti

### 2. Source Metadata Mancante

**Problema**: I chunk avevano tutti source: "blob" invece del nome file.

**Possibile causa**: Il Data Loader non sta preservando i metadata dal nodo Google Drive.

**Follow-up** (da verificare in futuro):
- Controllare se il problema persiste dopo il fix del chunking
- Se sì, aggiungere un nodo Code per arricchire i metadata prima del Data Loader
- Configurare il Data Loader per leggere `source` da `$json.name`

### 3. Duplicati da Buffer

**Problema**: Il workflow viene triggerato due volte nel buffer di 5 minuti, creando duplicati.

**Possibile soluzione** (da implementare in futuro):
- Cambiare modalità Pinecone da "insert" a "update"
- Usare ID deterministici basati su: hash(filename + chunk_index)
- Questo previene duplicati anche se il workflow viene eseguito più volte

---

## 📊 Confronto Pre/Post Fix

| Metrica | PRIMA del Fix | DOPO il Fix (atteso) |
|---------|---------------|----------------------|
| Total chunks | 6 (3 unici) | 20-50+ |
| Chunk size | 74-1481 chars | 1400-1500 chars (costante) |
| Chunk < 100 chars | 2 chunk (33%) | 0% |
| Source metadata | "blob" | Nome file reale |
| Duplicati | 3 coppie (50%) | 0% (dopo fix upsert mode) |
| Chunking strategy | Default/nessuno | Recursive (1500/200) |

---

## 🚀 Prossimi Passi Immediati

### Per l'Utente

1. ✅ **Fix applicato**: Workflow aggiornato e index pulito

2. **Carica file di test**:
   - Vai su Google Drive
   - Apri cartella "RAG Database JobCourier"
   - Carica uno o più file (PDFs o MD)
   - Consigliato: file con 3-10 pagine di contenuto

3. **Triggerare workflow**:
   - Attendi 30 minuti per trigger automatico
   - O triggera manualmente da N8N UI

4. **Verifica risultati**:
   ```bash
   cd /home/user/Bloom-2.0
   python3 scripts/verify_rag_chunks.py
   ```

5. **Testa RAG query**:
   - Accedi a https://bloom-2-0.vercel.app/
   - Seleziona cartella JobCourier
   - Fai query sul contenuto caricato

### Per il Monitoraggio

**Script disponibili**:
```bash
# Verifica salute index
python3 scripts/verify_rag_chunks.py

# Backup chunk (prima di pulizie future)
python3 backup_jobcourier_chunks.py

# Pulizia index (se necessario ri-processare)
python3 clean_jobcourier_index.py

# Check executions recenti
python3 check_executions.py
```

---

## 📞 Supporto

**Session**: https://claude.ai/code/session_01Q5eCMGpRPJ369rusyw2iYc
**Branch**: `claude/debug-vector-db-chunks-1luT7`
**Data**: 16 Febbraio 2026

**Contatti**:
- N8N UI: https://emanueleserra.app.n8n.cloud
- Bloom 2.0 App: https://bloom-2-0.vercel.app/
- Pinecone Console: https://app.pinecone.io

---

## ✅ Checklist Completamento

- [x] Root cause identificato (Text Splitter non connesso)
- [x] Workflow fixato (connessione aggiunta)
- [x] Deploy su N8N completato (status 200)
- [x] Backup chunk esistenti creato
- [x] Index rag-jobcourier-db pulito
- [x] Script di verifica creati
- [x] Documentazione completa
- [ ] File di test caricato su Google Drive
- [ ] Workflow triggerato e testato
- [ ] Verifica chunks post-fix (>15 chunk, dimensioni corrette)
- [ ] Test query RAG funzionante

---

**🎯 Status**: Fix applicato, pronto per test
**🔄 Next Action**: Caricare file di test e triggerare workflow
