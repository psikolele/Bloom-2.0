# Fix: RAG Workflow - Auto Data Loader Connection Issue

## Data: 2024-02-12

## 🔴 Problema Identificato

I chunk salvati in Pinecone (rag-pessina-db e rag-jobcourier-db) contenevano **solo metadati** invece del contenuto reale dei documenti:

```
❌ Chunk 1: 33 caratteri → "Volantino-Servizi-commerciali.pdf"
❌ Chunk 2: 32 caratteri → "Servizi-sanita-e-ass-sociale.pdf"
❌ Chunk 3: 14 caratteri → "rag-pessina-db"
```

Invece di:
```
✅ Chunk 1: 1500 caratteri → "ISTITUTO PESSINA - COMO\n\nCorsi disponibili:\n\n1. SERVIZI COMMERCIALI..."
```

## 🔍 Causa Root

**Il nodo "Auto Data Loader" NON riceveva i dati binari dei PDF!**

### Flusso SBAGLIATO (prima del fix):

```
Auto Download New File ──main──────────> Auto Upsert to Pinecone ❌
                                                ↑
Auto Data Loader ────────────────ai_document───┘
     ↑
Auto Recursive Splitter ──ai_textSplitter
```

**Problema**:
- "Auto Download New File" passava i dati **direttamente** a "Auto Upsert to Pinecone"
- "Auto Data Loader" NON riceveva il file binario, solo il text splitter
- "Auto Upsert to Pinecone" vettorizzava i **metadati JSON** invece del contenuto estratto dal PDF

### Flusso CORRETTO (dopo il fix):

```
Auto Download New File ──main──> Auto Data Loader ──ai_document──> Auto Upsert to Pinecone ✅
                                       ↑
                   Auto Recursive Splitter ──ai_textSplitter
```

**Soluzione**:
- "Auto Download New File" passa il file binario a "Auto Data Loader"
- "Auto Data Loader" (con `dataType: 'binary'`) estrae il testo dal PDF
- "Auto Recursive Splitter" divide il testo in chunk da 1500 caratteri
- "Auto Upsert to Pinecone" salva i chunk con il contenuto reale

## 🔧 Modifiche Applicate

### 1. Parametri di Auto Data Loader

**Prima:**
```json
{
  "parameters": {
    "options": {}
  }
}
```

**Dopo:**
```json
{
  "parameters": {
    "dataType": "binary",
    "options": {}
  }
}
```

### 2. Connessioni

**Prima:**
- `Auto Download New File` → `Auto Upsert to Pinecone` (main)

**Dopo:**
- `Auto Download New File` → `Auto Data Loader` (main)
- `Auto Data Loader` → `Auto Upsert to Pinecone` (ai_document) ← già esistente

## 📁 File Creato

Il workflow corretto è stato salvato in:
```
backup_workflows/RAG_workflow_FIXED_DATA_LOADER.json
```

## 🔄 Come Applicare il Fix

### Opzione 1: Importare il workflow corretto in n8n

1. Accedi a n8n: https://n8n.bloom-ai.it
2. Apri il workflow RAG esistente
3. Vai su **Workflow** → **Settings** → prendi nota dell'ID del workflow
4. Apri `backup_workflows/RAG_workflow_FIXED_DATA_LOADER.json`
5. Sostituisci il workflow in n8n:
   - Vai su **Workflow** → **Download** per fare un backup dell'attuale
   - Vai su **Workflow** → **Import from File**
   - Seleziona `RAG_workflow_FIXED_DATA_LOADER.json`
   - Salva

### Opzione 2: Modificare manualmente il workflow

1. Accedi a n8n
2. Apri il workflow RAG
3. Trova il nodo **"Auto Data Loader"**:
   - Clicca sul nodo
   - Nelle impostazioni, imposta **Data Type** = `Binary`
   - Salva
4. Trova il nodo **"Auto Download New File"**:
   - Rimuovi la connessione diretta a "Auto Upsert to Pinecone"
   - Connetti "Auto Download New File" a "Auto Data Loader" (output main)
5. Verifica che "Auto Data Loader" sia connesso a "Auto Upsert to Pinecone" (output ai_document)
6. Salva il workflow

## ✅ Verifica del Fix

Dopo aver applicato il fix:

1. **Cancella gli indici Pinecone** (già fatto):
   ```
   rag-pessina-db: 0 vettori
   rag-jobcourier-db: 0 vettori
   ```

2. **Ri-triggera il workflow**:
   - Vai su n8n
   - Esegui il workflow manualmente tramite webhook:
     ```bash
     curl -X POST https://n8n.bloom-ai.it/webhook/manual-ingest-trigger-fix
     ```

3. **Verifica i chunk in Pinecone**:
   - I chunk dovrebbero avere **1000-1500 caratteri** di contenuto reale
   - Non dovrebbero essere solo nomi di file

4. **Testa la chat**:
   - Fai una domanda sui corsi del Pessina
   - La risposta dovrebbe contenere informazioni reali estratte dai PDF

## 📊 Test Effettuati

### ✅ Test 1: Chunking manuale
- Chunk size: 1500 caratteri ✓
- Overlap: 200 caratteri ✓
- Contenuto ricercabile ✓

### ✅ Test 2: Verifica Pinecone
- Totale vettori prima del fix: 20
- Contenuto: solo metadati (nomi file) ❌
- Lunghezza media: 14-33 caratteri ❌

### ✅ Test 3: Analisi workflow
- Auto Data Loader senza dataType: binary ❌
- Connessione mancante da Auto Download → Auto Data Loader ❌
- Fix applicato ✓

## 🎯 Impatto

**Prima del fix:**
- Chat non trova informazioni sui corsi
- Risposta: "Non ho trovato informazioni specifiche sui corsi del Pessina"

**Dopo il fix (atteso):**
- Chat trova informazioni dettagliate
- Risposta con elenco corsi, materie, contatti, etc.

## 📝 Note

- Il problema affliggeva **TUTTI** gli indici RAG (jobcourier, pessina, etc.)
- Il fix deve essere applicato una sola volta al workflow
- Dopo il fix, tutti i documenti devono essere **re-indicizzati**
- I Pinecone indices sono già stati svuotati e sono pronti per la re-indicizzazione

## 🔗 File Correlati

- `backup_workflows/RAG_workflow_FIXED_DATA_LOADER.json` - Workflow corretto
- `backup_workflows/RAG_workflow_FIXED_CHUNKING.json` - Workflow prima del fix
- `RAG_FIXES_SUMMARY.md` - Riepilogo di tutti i fix RAG
