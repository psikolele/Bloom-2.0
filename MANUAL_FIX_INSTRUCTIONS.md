# Guida Passo-Passo: Applicare il Fix RAG in n8n

## 🎯 Cosa farai

Modificherai 2 cose nel workflow n8n per far sì che i PDF vengano letti correttamente:
1. Aggiungere un parametro al nodo "Auto Data Loader"
2. Spostare una connessione tra nodi

**Tempo richiesto**: 5 minuti

---

## 📋 METODO 1: Import del Workflow (PIÙ VELOCE)

### Passo 1: Backup del workflow attuale

1. Vai su **https://n8n.bloom-ai.it**
2. Login se necessario
3. Apri il workflow **RAG** (o quello che contiene "Auto Data Loader")
4. Clicca su **Workflow** (menu in alto) → **Download**
5. Salva il file (backup di sicurezza)

### Passo 2: Trova il Workflow ID

1. Con il workflow aperto, guarda l'URL del browser
2. L'URL sarà tipo: `https://n8n.bloom-ai.it/workflow/ABC123XYZ`
3. Copia l'ID dopo `/workflow/` (es: `ABC123XYZ`)

### Passo 3: Modifica il workflow corretto con il tuo ID

1. Apri il file: `backup_workflows/RAG_workflow_FIXED_DATA_LOADER.json`
2. Trova la riga con `"id":` all'inizio del file (riga 2-3)
3. Sostituisci l'ID esistente con il tuo ID copiato al Passo 2
4. Salva il file

### Passo 4: Import del workflow

1. Torna su n8n
2. Clicca su **Workflow** → **Import from File**
3. Seleziona: `backup_workflows/RAG_workflow_FIXED_DATA_LOADER.json`
4. Clicca **Import**
5. Clicca **Save** (icona floppy disk in alto a destra)

### ✅ Passo 5: Verifica

1. Cerca il nodo **"Auto Data Loader"** nel canvas
2. Cliccaci sopra
3. Verifica che nelle impostazioni ci sia **Data Type: Binary**
4. Verifica la connessione: **Auto Download New File** → **Auto Data Loader** → **Auto Upsert to Pinecone**

**✅ FATTO! Vai alla sezione "Dopo il Fix" in fondo**

---

## 📋 METODO 2: Modifica Manuale (PIÙ CONTROLLO)

Se preferisci modificare manualmente:

### Passo 1: Apri il workflow

1. Vai su **https://n8n.bloom-ai.it**
2. Apri il workflow RAG

### Passo 2: Modifica "Auto Data Loader"

1. **Trova il nodo** "Auto Data Loader" nel canvas (usa Ctrl+F se il workflow è grande)
2. **Clicca sul nodo** per aprire le impostazioni
3. **Trova il campo "Data Type"** (potrebbe essere sotto "Parameters")
4. **Seleziona "Binary"** dal dropdown
5. **Chiudi** le impostazioni del nodo

**Cosa hai fatto**: Ora Auto Data Loader può leggere file binari (PDF) invece di solo JSON.

### Passo 3: Modifica le connessioni

#### A. Rimuovi la connessione sbagliata

1. **Trova il nodo** "Auto Download New File"
2. **Trova la freccia** che va da "Auto Download New File" direttamente a "Auto Upsert to Pinecone"
3. **Clicca sulla freccia** (diventa selezionata)
4. **Premi Delete** o **Backspace** per rimuoverla

#### B. Aggiungi la connessione corretta

1. **Clicca sull'output** di "Auto Download New File" (il pallino a destra del nodo)
2. **Trascina** fino all'input di "Auto Data Loader" (il pallino a sinistra)
3. **Rilascia** per creare la connessione

#### C. Verifica la seconda connessione

1. Controlla che ci sia una freccia da **"Auto Data Loader"** a **"Auto Upsert to Pinecone"**
2. Se non c'è, creala:
   - Clicca sull'output di "Auto Data Loader"
   - Trascina su "Auto Upsert to Pinecone"
   - Rilascia

### Passo 4: Salva

1. Clicca su **Save** (icona floppy disk in alto a destra)
2. Aspetta la conferma "Workflow saved"

**✅ FATTO! Vai alla sezione "Dopo il Fix" sotto**

---

## 🔄 DOPO IL FIX

Ora devi re-indicizzare i documenti per riempire Pinecone con i chunk corretti.

### Opzione A: Trigger manuale via browser

1. In n8n, con il workflow aperto
2. Trova il nodo **"Manual Trigger Webhook Fix"**
3. Clicca su **"Execute Node"** (sopra il nodo)
4. Il workflow partirà e processerà tutti i PDF

### Opzione B: Trigger via webhook (più affidabile)

Apri un terminale e esegui:

```bash
curl -X POST https://n8n.bloom-ai.it/webhook/manual-ingest-trigger-fix
```

O apri nel browser: `https://n8n.bloom-ai.it/webhook/manual-ingest-trigger-fix`

### Monitora l'esecuzione

1. Vai su **Executions** (sidebar sinistra in n8n)
2. Cerca l'esecuzione più recente
3. Dovrebbe completarsi senza errori
4. Durata attesa: 1-3 minuti (dipende da quanti file ci sono)

---

## ✅ VERIFICA CHE FUNZIONI

### Test 1: Controlla i chunk in Pinecone

Esegui lo script di verifica:

```bash
cd /home/user/Bloom-2.0
python3 scripts/verify_rag_chunks.py
```

**Output atteso:**
```
✅ rag-pessina-db is HEALTHY
   Chunks contain real content from documents

✅ rag-jobcourier-db is HEALTHY
   Chunks contain real content from documents
```

I chunk dovrebbero avere **1000-1500 caratteri** invece di 14-33.

### Test 2: Prova la chat

1. Vai sulla chat RAG Pessina
2. Fai una domanda tipo:
   ```
   Quali corsi offre l'Istituto Pessina?
   ```

**Prima del fix:**
```
❌ "Non ho trovato informazioni specifiche sui corsi del Pessina
    nei documenti a disposizione"
```

**Dopo il fix:**
```
✅ "L'Istituto Pessina offre i seguenti corsi:

    1. Servizi Commerciali
       - Durata: 5 anni
       - Diploma: Tecnico dei servizi commerciali
       ...

    2. Servizi Socio-Sanitari
       ...

    [informazioni dettagliate dai PDF]"
```

---

## 🎓 SPIEGAZIONE TECNICA

### Cosa era rotto

```
┌─────────────────────┐
│ Auto Download       │  Scarica PDF da Google Drive
│ New File            │  Output: file binario
└──────────┬──────────┘
           │
           │ ❌ Andava direttamente qui (sbagliato!)
           │
           ▼
┌─────────────────────┐
│ Auto Upsert to      │  Provava a vettorizzare
│ Pinecone            │  i metadati JSON invece
└─────────────────────┘  del contenuto del PDF!

Risultato: chunk con solo nomi file (33 caratteri)
```

### Cosa è stato fixato

```
┌─────────────────────┐
│ Auto Download       │  1. Scarica PDF (binario)
│ New File            │
└──────────┬──────────┘
           │
           │ ✅ Passa i dati binari qui
           ▼
┌─────────────────────┐
│ Auto Data Loader    │  2. Estrae il TESTO dal PDF
│ (dataType: binary)  │     usando PyPDF o simile
└──────────┬──────────┘
           │
           │ Testo estratto
           ▼
┌─────────────────────┐
│ Auto Recursive      │  3. Divide in chunk da
│ Splitter            │     1500 caratteri
└──────────┬──────────┘     con overlap di 200
           │
           │ Array di chunk testuali
           ▼
┌─────────────────────┐
│ Auto Upsert to      │  4. Crea vettori dai chunk
│ Pinecone            │     e li salva in Pinecone
└─────────────────────┘

Risultato: chunk con contenuto reale (1500 caratteri)
```

### Perché serve `dataType: 'binary'`

Il nodo "Default Data Loader" in n8n può ricevere:
- **JSON**: dati strutturati (oggetti, array) → legge solo metadati
- **Binary**: file (PDF, DOC, TXT) → estrae il contenuto reale

Senza `dataType: 'binary'`:
- Il loader vedeva: `{ id: "abc", name: "documento.pdf", mimeType: "application/pdf" }`
- Salvava in Pinecone: "documento.pdf" (33 caratteri)

Con `dataType: 'binary'`:
- Il loader vede: il contenuto binario del PDF
- Estrae il testo: "ISTITUTO PESSINA\n\nCorsi disponibili:\n1. Servizi Commerciali..."
- Salva in Pinecone: chunk da 1500 caratteri con contenuto reale

### Perché serviva cambiare la connessione

**Flusso sbagliato:**
- Download → Pinecone (direttamente)
- Pinecone riceveva il file binario raw
- Non sapeva cosa farne, usava i metadati

**Flusso corretto:**
- Download → Data Loader (estrae testo) → Splitter (chunka) → Pinecone (vettorizza)
- Ogni step fa il suo lavoro
- Pinecone riceve chunk testuali già pronti

---

## 🆘 Troubleshooting

### Problema: "Non trovo il nodo Auto Data Loader"

**Soluzione**: Cerca "Data Loader" o usa Ctrl+F nel canvas di n8n.

### Problema: "Il campo Data Type non c'è"

**Soluzione**:
1. Clicca sul nodo
2. Guarda nelle **Parameters** o **Settings**
3. Potrebbe chiamarsi "Input Type" o "Source Type"
4. Seleziona "Binary" o "File"

### Problema: "L'esecuzione fallisce con errore"

**Soluzione**:
1. Vai su **Executions** in n8n
2. Clicca sull'esecuzione fallita
3. Leggi l'errore
4. Errori comuni:
   - "No binary data": Auto Data Loader non riceve dati → controlla connessioni
   - "Cannot read property 'text'": Splitter non riceve testo → controlla dataType

### Problema: "I chunk sono ancora sbagliati dopo il fix"

**Soluzione**:
1. Verifica che Pinecone sia stato svuotato prima di re-triggerare
2. Svuota manualmente:
   ```bash
   python3 /tmp/clear_pinecone_indices.py
   ```
3. Re-triggera il workflow
4. Aspetta 2-3 minuti
5. Verifica di nuovo

---

## 📞 Aiuto

Se hai problemi:
1. Controlla i log dell'esecuzione in n8n (Executions → ultima esecuzione)
2. Esegui `python3 scripts/verify_rag_chunks.py` per diagnosticare
3. Verifica che il backup del workflow sia stato salvato prima di modificare

**File importanti:**
- `RAG_DATA_LOADER_FIX.md` - Spiegazione completa del problema
- `backup_workflows/RAG_workflow_FIXED_DATA_LOADER.json` - Workflow corretto
- `scripts/verify_rag_chunks.py` - Script di verifica

---

## ✅ Checklist Finale

Prima di considerare il fix completo:

- [ ] Workflow modificato e salvato in n8n
- [ ] Auto Data Loader ha `dataType: binary`
- [ ] Connessione: Auto Download → Auto Data Loader → Pinecone
- [ ] Pinecone svuotato (0 vettori)
- [ ] Workflow re-triggerato
- [ ] Esecuzione completata senza errori
- [ ] Script di verifica mostra chunk >500 caratteri
- [ ] Chat risponde con informazioni dettagliate

**Quando tutti i check sono ✅, il fix è completo!**
