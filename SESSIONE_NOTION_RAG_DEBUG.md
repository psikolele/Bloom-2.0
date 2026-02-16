# 🔍 Debug RAG JobCourier - Fix Text Splitter Non Connesso

**📅 Data Sessione**: 16 Febbraio 2026
**⏱️ Minuti Lavorati**: 90
**🏷️ Categoria**: Debug
**🔗 Branch**: `claude/debug-vector-db-chunks-1luT7`

---

## 📋 Argomenti Trattati

### 1. Investigazione Problema Chunking RAG JobCourier

**Contesto**: Execution #7244 del workflow RAG ha prodotto solo 6 chunk (3 unici + 3 duplicati) nell'index rag-jobcourier-db invece dei 20-50+ chunk attesi da file multipli (PDFs + MD).

- Analisi stato chunk in Pinecone: 6 vettori totali (3 unici + 3 duplicati)
- Identificati chunk troppo piccoli (74 caratteri) e source metadata mancante ("blob")
- Backup dei 6 chunk esistenti prima della pulizia (backup_jobcourier_chunks_20260216_121348.json)

---

### 2. Analisi Workflow N8N RAG (ID: XmCaI5Q9MxNf0EP_65UvB)

**Contesto**: Scaricamento e analisi del workflow attivo da N8N per identificare il problema nel flusso di chunking.

- Download workflow attivo via API N8N (63 nodi totali)
- Tracciamento connessioni dei nodi per identificare il flusso "Auto" usato da JobCourier
- Verifica configurazione Text Splitter (chunkSize=1500, chunkOverlap=200) ✅

> **🔴 ROOT CAUSE TROVATO**: Il Text Splitter non era connesso al nodo "Auto Upsert to Pinecone" → il chunking NON veniva eseguito!

---

### 3. Implementazione Fix Workflow

**Contesto**: Modifica del workflow per connettere il Text Splitter al flusso Auto e deploy su N8N.

- Creazione script fix_workflow_text_splitter.py per automazione fix
- Aggiunta connessione ai_textSplitter da "Recursive Character Text Splitter1" a "Auto Upsert to Pinecone"
- Deploy workflow fixato su N8N via API PUT (status 200 OK) ✅

---

### 4. Pulizia Index Pinecone e Preparazione Re-indexing

**Contesto**: Pulizia dell'index rag-jobcourier-db per rimuovere i chunk mal formattati prima del re-indexing con il workflow fixato.

- Creazione script clean_jobcourier_index.py con conferma utente
- Esecuzione pulizia: 6 vettori eliminati → 0 vettori nell'index
- Index pronto per re-indexing con chunking corretto

---

## 🎯 Decisioni Chiave

- **Connessione Text Splitter**: Priorità assoluta - il chunking è essenziale per RAG efficace
- **Backup Strategy**: Sempre backuppare chunk esistenti prima di pulizie massive
- **Workflow Analysis**: Verificare connessioni nodi, non solo configurazioni - nodi orfani sono invisibili ma critici
- **Testing Pattern**: Deploy → Test con file reale → Verifica chunk count e dimensioni

---

## 📊 Metriche Pre/Post Fix

| Metrica | PRIMA | DOPO (atteso) |
|---------|-------|---------------|
| Total chunks | 6 (3 unici) | 20-50+ |
| Chunk size | 74-1481 chars | 1400-1500 chars |
| Source metadata | "blob" | Nome file reale |
| Duplicati | 50% | 0% |

---

## 🔗 Riferimenti

- **Workflow**: RAG | Google Drive to Pinecone (ID: XmCaI5Q9MxNf0EP_65UvB)
- **Branch Git**: claude/debug-vector-db-chunks-1luT7
- **Commit**: 947032d - Fix RAG JobCourier chunking
- **Documentazione**: RAG_JOBCOURIER_DEBUG_FEB_16.md
- **Tool utilizzati**: N8N, Pinecone, OpenAI Embeddings, LangChain, Python
- **Script creati**: backup_jobcourier_chunks.py, clean_jobcourier_index.py, fix_workflow_text_splitter.py

---

## 🚀 Prossimi Passi

1. Caricare file di test su Google Drive (cartella RAG Database JobCourier)
2. Triggerare workflow (automatico ogni 30 min o manuale da N8N UI)
3. Verificare risultati: `python3 scripts/verify_rag_chunks.py`
4. Testare query RAG dalla web app Bloom 2.0
5. Aggiornare RAG_FIXES_SUMMARY.md con questo fix (#3)

---

> **✅ Fix completato e deployato**. Index pulito e pronto per re-indexing. Expected: 20-50+ chunk con dimensioni corrette (1400-1500 chars).

---

## 📝 Note Tecniche

**Root Cause Dettagliato**:
```
PRIMA del fix:
Auto Download New File → Auto Upsert to Pinecone
  ↑ Auto Data Loader ✅
  ↑ Auto Embeddings ✅
  ↑ Text Splitter ❌ MANCANTE!

DOPO il fix:
Auto Download New File → Auto Upsert to Pinecone
  ↑ Auto Data Loader ✅
  ↑ Auto Embeddings ✅
  ↑ Text Splitter (1500/200) ✅ CONNESSO!
```

**File Committati** (7 totali):
- RAG_JOBCOURIER_DEBUG_FEB_16.md (documentazione completa)
- backup_jobcourier_chunks.py
- clean_jobcourier_index.py
- fix_workflow_text_splitter.py
- backup_jobcourier_chunks_20260216_121348.json
- workflow_attivo.json
- workflow_attivo_FIXED.json

**Pull Request**: https://github.com/psikolele/Bloom-2.0/pull/new/claude/debug-vector-db-chunks-1luT7

---

**Session URL**: https://claude.ai/code/session_01Q5eCMGpRPJ369rusyw2iYc
