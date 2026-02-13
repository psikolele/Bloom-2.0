# Caption Flow V.2 - RAG Integration

## 📋 Panoramica Modifiche

**Data**: 2026-02-13
**Workflow ID**: #oRYSQ9tk63yPJaqt
**Workflow Name**: Caption Flow V.2

### Problema Risolto

Il workflow ora è in grado di:
1. ✅ Leggere il tipo di account dal payload webhook (`Account` field)
2. ✅ Mappare automaticamente l'account al database RAG corretto
3. ✅ Recuperare conoscenze aziendali specifiche dal database RAG
4. ✅ Utilizzare queste conoscenze per generare contenuti più rilevanti e personalizzati

---

## 🏗️ Architettura della Soluzione

### Mapping Account → Database RAG

Il sistema mappa automaticamente gli account Instagram ai rispettivi database RAG:

| Account (Input) | Database RAG | Azienda |
|----------------|--------------|---------|
| IG BLC, BLC, ig_blc, blc | `rag-blc-db` | BLC |
| IG Pessina, Pessina, ig_pessina, pessina | `rag-pessina-db` | Pessina |
| IG Foot_Easy, Foot Easy, foot_easy, footeasy | `rag-footeasy-db` | Foot Easy |
| IG JobCourier, Job Courier, jobcourier | `rag-jobcourier-db` | Job Courier |
| IG Walmoss, walmoss | `rag-walmoss-db` | Walmoss |

**Nota**: Il mapping è case-insensitive e gestisce automaticamente variazioni con underscore, spazi e prefissi "IG".

---

## 🔧 Nodi Aggiunti al Workflow

### 1. **Prepare Input Variables** (Modificato)
- **Tipo**: Set node
- **Modifica**: Aggiunto campo `Account` che estrae `{{ $json.body.Account || 'default' }}`

### 2. **Map Account to RAG DB** (Nuovo)
- **Tipo**: Code node
- **Funzione**: Mappa il nome account al database RAG corretto
- **Input**: Account name (varie forme)
- **Output**:
  - `ragDatabase`: Nome del database Pinecone (es: `rag-blc-db`)
  - `companyName`: Nome pulito dell'azienda (es: `BLC`)
  - `originalAccount`: Account originale dal payload

### 3. **Prepare Company Knowledge Query** (Nuovo)
- **Tipo**: Code node
- **Funzione**: Crea una query RAG basata sul Topic e sul contesto
- **Output**:
  - `chatInput`: Query formattata per il RAG
  - `targetIndex`: Database Pinecone da interrogare
  - `companyContext`: Contesto completo (topic, audience, voice, platform)

### 4. **Query Company Knowledge** (Nuovo)
- **Tipo**: AI Agent (LangChain)
- **Funzione**: Agente AI che interroga il knowledge base aziendale
- **System Message**: Configurato per estrarre informazioni rilevanti su valori, prodotti, servizi, brand voice

### 5. **Company Knowledge LLM** (Nuovo)
- **Tipo**: OpenRouter Chat LLM
- **Connessione**: Fornisce il modello linguistico all'agente RAG

### 6. **Company Knowledge Vector Store** (Nuovo)
- **Tipo**: Pinecone Vector Store
- **Modalità**: `retrieve-as-tool`
- **Index Dinamico**: `={{ $('Prepare Company Knowledge Query').first().json.targetIndex }}`
- **Funzione**: Recupera documenti rilevanti dal database Pinecone selezionato

### 7. **Company Knowledge Embeddings** (Nuovo)
- **Tipo**: OpenAI Embeddings
- **Funzione**: Fornisce gli embeddings per la ricerca vettoriale

### 8. **Combine RAG with Input Data** (Nuovo)
- **Tipo**: Code node
- **Funzione**: Combina i risultati RAG con i dati di input originali
- **Output**: Oggetto unificato con:
  - Tutti i campi originali (Topic, Audience, Voice, Platform)
  - `CompanyKnowledge`: Informazioni estratte dal RAG
  - `CompanyName`: Nome dell'azienda
  - `hasRAGData`: Flag booleano

---

## 📝 Prompt Modificati

### 3a. Generate Content Concept (Gemini)
**Aggiunto**:
```
<param name="CompanyKnowledge">{{ $json.CompanyKnowledge }}</param>
```

**Istruzione aggiunta**:
> **IMPORTANTE: Hai accesso alle conoscenze aziendali specifiche in `CompanyKnowledge`. Usa queste informazioni per rendere il concept più rilevante e allineato con il brand, i prodotti e i valori dell'azienda.**

### 3b. Generate Image Prompt Options (Gemini)
**Aggiunto**:
```
<param name="CompanyKnowledge">{{ $('Combine RAG with Input Data').item.json.CompanyKnowledge }}</param>
```

**Istruzione aggiunta**:
> **IMPORTANTE: Usa le informazioni in `CompanyKnowledge` per creare prompt immagine coerenti con il brand, i prodotti e lo stile visuale dell'azienda.**

### 3c. Generate Post Caption (Gemini)
**Aggiunto nei DETTAGLI**:
```
- Company Knowledge: {{ $('Combine RAG with Input Data').item.json.CompanyKnowledge }}
```

**Istruzione aggiunta**:
> **USA le Company Knowledge per rendere la caption più rilevante, menzionando prodotti/servizi specifici e valori aziendali quando pertinente.**

---

## 🔄 Flusso del Workflow Aggiornato

```
CaptionFlow Webhook (POST /caption-flow)
    ↓
2. Prepare Input Variables (Topic, Audience, Voice, Platform, Account)
    ↓
Map Account to RAG DB
    ↓
Prepare Company Knowledge Query
    ↓
Query Company Knowledge (AI Agent)
    ├── Company Knowledge LLM (OpenRouter)
    ├── Company Knowledge Vector Store (Pinecone)
    └── Company Knowledge Embeddings (OpenAI)
    ↓
Combine RAG with Input Data
    ↓
3a. Generate Content Concept (Gemini) ← include Company Knowledge
    ↓
3b. Generate Image Prompt Options (Gemini) ← include Company Knowledge
    ↓
3c. Generate Post Caption (Gemini) ← include Company Knowledge
    ↓
[resto del workflow...]
```

---

## 📤 Payload Webhook Esempio

```json
{
  "Topic": "Nuova collezione primavera 2026",
  "Platform": "Instagram",
  "Audience": "Fashion lovers 25-40",
  "Voice": "Casual e amichevole",
  "Account": "IG BLC",
  "ReferenceLink": null,
  "format": "image",
  "timestamp": "2026-02-13T10:30:00.000Z",
  "source": "CaptionFlow Web App"
}
```

**Output del mapping**:
- `ragDatabase`: `rag-blc-db`
- `companyName`: `BLC`
- Query RAG: "Fornisci informazioni su BLC relative a: Nuova collezione primavera 2026..."

---

## ✅ Vantaggi dell'Integrazione RAG

1. **Contenuti Personalizzati**: I post generati includono informazioni specifiche dell'azienda
2. **Brand Consistency**: Mantiene coerenza con valori e tono di voce aziendale
3. **Informazioni Accurate**: Utilizza dati reali dai documenti aziendali
4. **Flessibilità**: Supporta varianti multiple del nome account
5. **Scalabilità**: Facile aggiungere nuovi account mappando nuovi database RAG

---

## 🔧 Come Aggiungere un Nuovo Account

Per aggiungere un nuovo account (es: "IG NewCompany"):

1. Creare il database Pinecone: `rag-newcompany-db`
2. Modificare il nodo **Map Account to RAG DB**:
   ```javascript
   } else if (cleanAccount.includes('newcompany') || cleanAccount.includes('new')) {
       ragDatabase = 'rag-newcompany-db';
       companyName = 'New Company';
   }
   ```
3. Popolare il database con i documenti aziendali usando il workflow RAG esistente

---

## 📁 File Modificati

- `backup_workflows/Caption_Flow_V2_oRYSQ9tk63yPJaqt_UPDATED.json` - Workflow principale
- Creato backup: `Caption_Flow_V2_oRYSQ9tk63yPJaqt_BACKUP_[timestamp].json`

---

## 🧪 Test Consigliati

1. ✅ **Test con Account BLC**:
   - Payload con `"Account": "IG BLC"`
   - Verificare che usi `rag-blc-db`
   - Verificare che il contenuto menzioni prodotti/servizi BLC

2. ✅ **Test con Account Pessina**:
   - Payload con `"Account": "Pessina"`
   - Verificare che usi `rag-pessina-db`
   - Verificare conoscenze specifiche Pessina

3. ✅ **Test con varianti nome**:
   - `"IG_Foot_Easy"`, `"foot easy"`, `"FOOTEASY"`
   - Tutte dovrebbero mappare a `rag-footeasy-db`

4. ✅ **Test senza Account** (default):
   - Payload senza campo Account o `null`
   - Dovrebbe usare `rag-pessina-db` come fallback

---

## 📞 Supporto

Per problemi o domande:
- Issue tracker: https://github.com/anthropics/claude-code/issues
- Session: https://claude.ai/code/session_01QtQ2DncTTpYsWWAhDtRdNM

---

**Autore**: Claude Code
**Ultima modifica**: 2026-02-13
