# GUIDA MANUALE - FIX RAG (DOMINIO CORRETTO)

## ⚠️ LINK CORRETTO

**n8n:** https://emanueleserra.app.n8n.cloud/

---

## 🎯 APPLICARE IL FIX MANUALMENTE (5 minuti)

### STEP 1: Apri n8n

1. Vai su: **https://emanueleserra.app.n8n.cloud/**
2. Login se necessario
3. Dovresti vedere la lista dei workflow

---

### STEP 2: Apri il workflow RAG

1. Cerca il workflow con **"RAG"** nel nome
2. Clicca per aprirlo
3. Dovresti vedere il canvas con i nodi

---

### STEP 3: Trova "Auto Data Loader"

**Opzione A:** Scorri il canvas e cercalo visivamente

**Opzione B (più veloce):**
1. Premi **Ctrl+F** (o Cmd+F su Mac)
2. Digita: `Auto Data Loader`
3. Dovrebbe evidenziarsi

---

### STEP 4: Modifica "Auto Data Loader"

1. **Clicca** sul nodo "Auto Data Loader"
2. Si apre il pannello a destra
3. Cerca il campo **"Data Type"**
4. Seleziona **"Binary"** dal dropdown
5. Chiudi il pannello (clicca fuori o sulla X)

---

### STEP 5: Cambia la connessione

#### A. Trova questi 2 nodi:
- **"Auto Download New File"**
- **"Auto Upsert to Pinecone"**

#### B. Se c'è una freccia diretta tra loro:
1. **Clicca sulla freccia** per selezionarla
2. Premi **Delete** o **Backspace**
3. La freccia scompare

#### C. Crea la nuova connessione:
1. Clicca sul **pallino destro** di "Auto Download New File"
2. **Trascina** verso "Auto Data Loader"
3. Rilascia sul **pallino sinistro** di "Auto Data Loader"
4. Dovrebbe apparire una freccia

#### D. Verifica:
- Deve esserci già una freccia da "Auto Data Loader" a "Auto Upsert to Pinecone"
- Se non c'è, creala come sopra

---

### STEP 6: Salva

1. Clicca **Save** (💾 in alto a destra)
2. Aspetta "Workflow saved"

---

### STEP 7: Re-triggera il workflow

Apri nel browser:
```
https://emanueleserra.app.n8n.cloud/webhook/manual-ingest-trigger-fix
```

---

### STEP 8: Aspetta 2-3 minuti ⏳

Il workflow sta processando i PDF.

Puoi verificare in n8n:
1. Sidebar → **Executions**
2. Guarda l'esecuzione più recente
3. Deve essere verde (Success)

---

### STEP 9: Testa la chat 💬

Fai questa domanda sulla chat RAG Pessina:
```
Quali corsi offre l'Istituto Pessina?
```

**PRIMA del fix:**
```
❌ "Non ho trovato informazioni specifiche..."
```

**DOPO il fix:**
```
✅ "L'Istituto Pessina offre:
    1. Servizi Commerciali - ...
    2. Servizi Socio-Sanitari - ...
    [dettagli completi]"
```

---

## ✅ FATTO!

Se la chat risponde con informazioni dettagliate, il fix ha funzionato! 🎉

---

## 🔄 Se qualcosa va storto

1. Torna su n8n
2. Vai su Executions
3. Clicca sull'esecuzione fallita
4. Leggi l'errore
5. Dimmi l'errore e ti aiuto

---

## 📞 Link Utili

- **n8n:** https://emanueleserra.app.n8n.cloud/
- **Webhook trigger:** https://emanueleserra.app.n8n.cloud/webhook/manual-ingest-trigger-fix
