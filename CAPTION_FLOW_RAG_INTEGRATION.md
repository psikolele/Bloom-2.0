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

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    ACCOUNT → RAG DATABASE MAPPING                       │
└─────────────────────────────────────────────────────────────────────────┘

  📱 ACCOUNT INPUT (varianti supportate)     🗄️  RAG DATABASE     🏢 AZIENDA
  ═══════════════════════════════════════     ═══════════════     ═══════════

  IG BLC
  BLC                  ╲
  ig_blc                ╲
  blc                    ├─────────────────▶  rag-blc-db          BLC
  IG_BLC                ╱
  Ig Blc               ╱

  ───────────────────────────────────────────────────────────────────────────

  IG Pessina
  Pessina              ╲
  ig_pessina            ╲
  pessina                ├─────────────────▶  rag-pessina-db      Pessina
  IG_PESSINA            ╱
  Ig Pessina           ╱

  ───────────────────────────────────────────────────────────────────────────

  IG Foot_Easy
  Foot Easy            ╲
  foot_easy             ╲
  footeasy               ├─────────────────▶  rag-footeasy-db     Foot Easy
  IG_FOOT_EASY          ╱
  Ig Foot Easy         ╱

  ───────────────────────────────────────────────────────────────────────────

  IG JobCourier
  Job Courier          ╲
  jobcourier            ╲
  job_courier            ├─────────────────▶  rag-jobcourier-db   Job Courier
  IG_JOBCOURIER         ╱
  Ig Job Courier       ╱

  ───────────────────────────────────────────────────────────────────────────

  IG Walmoss
  Walmoss              ╲
  walmoss               ╲
  ig_walmoss             ├─────────────────▶  rag-walmoss-db      Walmoss
  IG_WALMOSS            ╱
  Ig Walmoss           ╱

  ───────────────────────────────────────────────────────────────────────────

  (default/unknown)    ───────────────────▶   rag-pessina-db      Pessina
                                               (fallback)

┌─────────────────────────────────────────────────────────────────────────┐
│  LOGICA DI PARSING                                                      │
└─────────────────────────────────────────────────────────────────────────┘

  1. Converti in lowercase
  2. Rimuovi prefissi: "ig", "ig_", "ig-", "ig " (case-insensitive)
  3. Rimuovi: underscore, spazi, trattini
  4. Match con keyword azienda:
     • "blc" → rag-blc-db
     • "pessina" → rag-pessina-db
     • "foot" o "easy" → rag-footeasy-db
     • "job" o "courier" → rag-jobcourier-db
     • "walmoss" → rag-walmoss-db
  5. Default: rag-pessina-db

┌─────────────────────────────────────────────────────────────────────────┐
│  ESEMPI DI CONVERSIONE                                                  │
└─────────────────────────────────────────────────────────────────────────┘

  Input                Processing Steps                    Output
  ──────────────────   ────────────────────────────────    ────────────────
  "IG BLC"          →  "ig blc" → "blc" → match "blc"  →  rag-blc-db
  "ig_pessina"      →  "pessina" → match "pessina"      →  rag-pessina-db
  "Foot Easy"       →  "foot easy" → "footeasy"         →  rag-footeasy-db
                       → match "foot" OR "easy"
  "JOBCOURIER"      →  "jobcourier" → match "job"       →  rag-jobcourier-db
  "IG_WALMOSS"      →  "walmoss" → match "walmoss"      →  rag-walmoss-db
  null / ""         →  no match                         →  rag-pessina-db
  "Unknown"         →  no match                         →  rag-pessina-db

```

**Caratteristiche**:
- ✅ **Case-insensitive**: "BLC" = "blc" = "Blc"
- ✅ **Gestione underscore**: "foot_easy" = "footeasy"
- ✅ **Gestione spazi**: "Foot Easy" = "footeasy"
- ✅ **Rimozione prefissi**: "IG_BLC" → "BLC"
- ✅ **Fallback sicuro**: account sconosciuti → rag-pessina-db

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

### Diagramma Completo del Workflow

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                         CAPTION FLOW V.2 - RAG INTEGRATION               ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

┌─────────────────────────────────────────────────────────────────────────┐
│  FASE 1: INGRESSO WEBHOOK & PREPARAZIONE DATI                          │
└─────────────────────────────────────────────────────────────────────────┘

    📥 [1] CaptionFlow Webhook
         │  Endpoint: POST /webhook/caption-flow
         │  Payload: {Topic, Platform, Audience, Voice, Account, ...}
         │
         ├──[main]──▶
         │
         ▼
    📝 [2] Prepare Input Variables
         │  Tipo: Set Node
         │  Estrae: Topic, Audience, Voice, Platform, Account
         │  Output: 5 variabili strutturate
         │
         ├──[main]──▶
         │
         ▼

┌─────────────────────────────────────────────────────────────────────────┐
│  FASE 2: MAPPING ACCOUNT → DATABASE RAG                                │
└─────────────────────────────────────────────────────────────────────────┘

    🗺️  [3] Map Account to RAG DB
         │  Tipo: Code Node
         │  Funzione: Parsing & Mapping intelligente
         │
         │  Input: Account (varianti: "IG BLC", "blc", "BLC", "ig_blc")
         │  Logica:
         │    • Rimuove prefissi: "IG", "IG_", "IG-"
         │    • Normalizza: lowercase, rimuove underscore/spazi
         │    • Mappa:
         │      └─ blc       → rag-blc-db
         │      └─ pessina   → rag-pessina-db
         │      └─ footeasy  → rag-footeasy-db
         │      └─ jobcourier→ rag-jobcourier-db
         │      └─ walmoss   → rag-walmoss-db
         │
         │  Output:
         │    • ragDatabase: "rag-blc-db"
         │    • companyName: "BLC"
         │    • originalAccount: "IG BLC"
         │
         ├──[main]──▶
         │
         ▼

┌─────────────────────────────────────────────────────────────────────────┐
│  FASE 3: PREPARAZIONE QUERY RAG                                         │
└─────────────────────────────────────────────────────────────────────────┘

    🔍 [4] Prepare Company Knowledge Query
         │  Tipo: Code Node
         │  Funzione: Genera query ottimizzata per RAG
         │
         │  Input: Topic, Audience, Voice, Platform, ragDatabase, companyName
         │  Genera:
         │    chatInput: "Fornisci informazioni su {company} relative a:
         │                {topic}. Includi dettagli su prodotti, servizi,
         │                valori aziendali e informazioni rilevanti per
         │                creare contenuti social per {platform}."
         │
         │  Output:
         │    • chatInput: Query formulata
         │    • targetIndex: "rag-blc-db"
         │    • companyContext: {name, topic, audience, voice, platform}
         │
         ├──[main]──▶
         │
         ▼

┌─────────────────────────────────────────────────────────────────────────┐
│  FASE 4: QUERY RAG - AI AGENT CON VECTOR SEARCH                        │
└─────────────────────────────────────────────────────────────────────────┘

    🤖 [5] Query Company Knowledge
         │  Tipo: AI Agent (LangChain)
         │  System Message: "You are a company knowledge assistant..."
         │
         │  Connessioni AI:
         │    ┌────────────────────────────────────────────────┐
         │    │                                                │
         │    ├──[ai_languageModel]──▶ 💬 Company Knowledge LLM
         │    │                           Tipo: OpenRouter Chat LLM
         │    │                           Modello: Default (gemini-2.0-flash-exp)
         │    │                           Credentials: OpenRouter API
         │    │
         │    ├──[ai_tool]───────────▶ 📊 Company Knowledge Vector Store
         │    │                           Tipo: Pinecone Vector Store
         │    │                           Mode: retrieve-as-tool
         │    │                           Index: ={{ $('Prepare Company Knowledge Query')
         │    │                                      .first().json.targetIndex }}
         │    │                           Namespace: '' (default)
         │    │                           Tool Description: "Use this tool to retrieve
         │    │                             company-specific information, brand guidelines,
         │    │                             products, services..."
         │    │                           Credentials: PineconeApi account Didattica BLC
         │    │                           │
         │    │                           ├──[ai_embedding]──▶ 🔢 Company Knowledge Embeddings
         │    │                                                  Tipo: OpenAI Embeddings
         │    │                                                  Model: text-embedding-3-small
         │    │                                                  Credentials: OpenRouter_Auto_Fixed
         │    └────────────────────────────────────────────────┘
         │
         │  Processo:
         │    1. Riceve chatInput con query
         │    2. LLM genera strategia di ricerca
         │    3. Vector Store cerca documenti rilevanti in Pinecone
         │    4. Embeddings convertono query in vettori
         │    5. Ritorna top-K documenti più rilevanti
         │    6. LLM sintetizza risposta finale
         │
         │  Output:
         │    • output: "BLC offre abbigliamento sostenibile..."
         │    • text: Risposta formattata
         │
         ├──[main]──▶
         │
         ▼

┌─────────────────────────────────────────────────────────────────────────┐
│  FASE 5: COMBINAZIONE DATI RAG + INPUT ORIGINALI                       │
└─────────────────────────────────────────────────────────────────────────┘

    🔗 [6] Combine RAG with Input Data
         │  Tipo: Code Node
         │  Funzione: Merge intelligente di tutti i dati
         │
         │  Input:
         │    • Da Query Company Knowledge: output RAG, companyContext
         │    • Da Prepare Input Variables: Topic, Audience, Voice, Platform
         │
         │  Output Unificato:
         │    {
         │      Topic: "Nuova collezione primavera",
         │      TargetAudience: "Fashion lovers 25-40",
         │      BrandVoice: "Casual e amichevole",
         │      Platform: "Instagram",
         │      CompanyKnowledge: "BLC è un brand di moda sostenibile...",
         │      CompanyName: "BLC",
         │      RAGDatabase: "rag-blc-db",
         │      hasRAGData: true
         │    }
         │
         ├──[main]──▶
         │
         ▼

┌─────────────────────────────────────────────────────────────────────────┐
│  FASE 6: GENERAZIONE CONTENUTI CON COMPANY KNOWLEDGE                   │
└─────────────────────────────────────────────────────────────────────────┘

    ✨ [7] 3a. Generate Content Concept (Gemini)
         │  Tipo: LangChain Chain LLM
         │  LLM: Gemini 2.0 Flash via OpenRouter
         │
         │  Prompt Template (Modificato):
         │    <input_context>
         │      <param name="CompanyKnowledge">{{ $json.CompanyKnowledge }}</param>
         │      <param name="Topic">{{ $json.Topic }}</param>
         │      <param name="TargetAudience">{{ $json.TargetAudience }}</param>
         │      <param name="BrandVoice">{{ $json.BrandVoice }}</param>
         │      <param name="Platform">{{ $json.Platform }}</param>
         │    </input_context>
         │
         │  Istruzione Aggiunta:
         │    "IMPORTANTE: Hai accesso alle conoscenze aziendali specifiche
         │     in CompanyKnowledge. Usa queste informazioni per rendere il
         │     concept più rilevante e allineato con il brand, i prodotti
         │     e i valori dell'azienda."
         │
         │  Output: {ideas: [{concept: "...", suggested_format: "Single Image"}]}
         │
         ├──[main]──▶
         │
         ▼

    🎨 [8] 3b. Generate Image Prompt Options (Gemini)
         │  Tipo: LangChain Chain LLM
         │  LLM: Gemini 2.0 Flash via OpenRouter
         │
         │  Prompt Template (Modificato):
         │    <input_context>
         │      <param name="CompanyKnowledge">
         │        {{ $('Combine RAG with Input Data').item.json.CompanyKnowledge }}
         │      </param>
         │      <param name="ChosenIdea">{{ $json.output.ideas[0].concept }}</param>
         │      ...
         │    </input_context>
         │
         │  Istruzione Aggiunta:
         │    "IMPORTANTE: Usa le informazioni in CompanyKnowledge per creare
         │     prompt immagine coerenti con il brand, i prodotti e lo stile
         │     visuale dell'azienda."
         │
         │  Output: {
         │    expanded_post_concept: "...",
         │    prompt_options: [
         │      {option_description: "...", prompts: ["..."]},
         │      {option_description: "...", prompts: ["..."]}
         │    ]
         │  }
         │
         ├──[main]──▶
         │
         ▼

    📝 [9] 3c. Generate Post Caption (Gemini)
         │  Tipo: LangChain Chain LLM
         │  LLM: Gemini 2.0 Flash via OpenRouter
         │
         │  Prompt Template (Modificato):
         │    DETTAGLI:
         │    - Company Knowledge: {{ $('Combine RAG with Input Data')
         │                            .item.json.CompanyKnowledge }}
         │    - Concept: {{ $('3a. Generate Content Concept (Gemini)')
         │                   .item.json.output.ideas[0].concept }}
         │    - Topic: {{ $('2. Prepare Input Variables').item.json.Topic }}
         │    ...
         │
         │  Istruzione Aggiunta:
         │    "USA le Company Knowledge per rendere la caption più rilevante,
         │     menzionando prodotti/servizi specifici e valori aziendali
         │     quando pertinente."
         │
         │  Output: {Caption: "Scopri la nuova collezione BLC sostenibile..."}
         │
         ├──[main]──▶
         │
         ▼

    [... resto del workflow: generazione immagine, upload, email ...]


┌─────────────────────────────────────────────────────────────────────────┐
│  LEGENDA CONNESSIONI                                                    │
└─────────────────────────────────────────────────────────────────────────┘

  [main]           → Connessione principale (flusso dati)
  [ai_languageModel] → Connessione LLM all'AI Agent
  [ai_tool]        → Connessione Tool (Vector Store) all'AI Agent
  [ai_embedding]   → Connessione Embeddings al Vector Store

┌─────────────────────────────────────────────────────────────────────────┐
│  METRICHE                                                               │
└─────────────────────────────────────────────────────────────────────────┘

  • Nodi Totali: 38 (31 originali + 7 RAG)
  • Connessioni Main: 29
  • Connessioni AI: 3 (ai_languageModel, ai_tool, ai_embedding)
  • Database RAG Supportati: 5 (BLC, Pessina, Foot Easy, JobCourier, Walmoss)
  • Tempo Aggiunto: ~5-10s per query RAG
  • Modelli AI Usati:
    ✓ Gemini 2.0 Flash (via OpenRouter) - Content generation
    ✓ OpenAI text-embedding-3-small - Vector embeddings
    ✓ Pinecone - Vector database storage & retrieval

┌─────────────────────────────────────────────────────────────────────────┐
│  NOTE TECNICHE                                                          │
└─────────────────────────────────────────────────────────────────────────┘

  1. Il Vector Store usa "retrieve-as-tool" mode, permettendo all'AI Agent
     di decidere dinamicamente quando interrogare il RAG

  2. L'indice Pinecone è selezionato dinamicamente tramite espressione N8N:
     ={{ $('Prepare Company Knowledge Query').first().json.targetIndex }}

  3. Il namespace Pinecone è '' (stringa vuota) per compatibilità con
     l'indicizzazione esistente

  4. Il fallback default per account non riconosciuti è: rag-pessina-db

  5. Tutte le risposte RAG sono in Italiano, come richiesto dal system message

```

---

## 📊 Diagramma Rapido - Solo Flusso RAG

Per una vista rapida del sistema RAG integrato:

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃         SISTEMA RAG - KNOWLEDGE RETRIEVAL DINAMICO             ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

                  Account Field (dal webhook)
                           │
                           │ "IG BLC" / "Pessina" / "foot_easy"
                           ▼
              ┌────────────────────────────┐
              │   Map Account to RAG DB    │◀── Parsing intelligente
              │                            │    • Case-insensitive
              │  Input: "IG BLC"           │    • Rimuove prefissi/underscore
              │  Output: "rag-blc-db"      │    • 5 database supportati
              └────────────┬───────────────┘
                           │
                           │ ragDatabase + companyName
                           ▼
              ┌────────────────────────────┐
              │ Prepare Knowledge Query    │◀── Genera query ottimizzata
              │                            │    "Fornisci info su {company}
              │  Topic: "Nuova collezione" │     relative a: {topic}..."
              │  Company: "BLC"            │
              └────────────┬───────────────┘
                           │
                           │ chatInput + targetIndex
                           ▼
    ╔═══════════════════════════════════════════════════════════╗
    ║         🤖 AI AGENT - QUERY COMPANY KNOWLEDGE             ║
    ╠═══════════════════════════════════════════════════════════╣
    ║                                                           ║
    ║  ┌──────────────┐      ┌─────────────────────────────┐  ║
    ║  │   LLM Model  │      │   Vector Store (Pinecone)   │  ║
    ║  │  OpenRouter  │      │   Index: {{ targetIndex }}  │  ║
    ║  │  Gemini 2.0  │      │   Mode: retrieve-as-tool    │  ║
    ║  └──────┬───────┘      └──────────┬──────────────────┘  ║
    ║         │                         │                     ║
    ║         │  Genera strategia       │  Cerca docs        ║
    ║         │  di ricerca             │  rilevanti         ║
    ║         │                         │                     ║
    ║         │                    ┌────▼────────┐           ║
    ║         │                    │  Embeddings │           ║
    ║         │                    │   OpenAI    │           ║
    ║         │                    └─────────────┘           ║
    ║         │                         │                     ║
    ║         │◀────────────────────────┤                     ║
    ║         │   Top-K documenti       │                     ║
    ║         │                         │                     ║
    ║         ▼                         │                     ║
    ║   Sintetizza risposta finale      │                     ║
    ║                                   │                     ║
    ╚═══════════════════════════════════════════════════════════╝
                           │
                           │ CompanyKnowledge output
                           ▼
              ┌────────────────────────────┐
              │  Combine RAG with Data     │◀── Merge dati
              │                            │
              │  + Topic, Audience, Voice  │    Dati originali
              │  + CompanyKnowledge (RAG)  │  + Conoscenze RAG
              │  + CompanyName             │  = Input completo
              └────────────┬───────────────┘
                           │
                           │ Tutti i dati combinati
                           ▼
              ┌────────────────────────────┐
              │                            │
              │  🎨 Content Generation     │◀── 3a, 3b, 3c con RAG
              │                            │
              │  ✓ Concept (con RAG)       │    Usa CompanyKnowledge
              │  ✓ Image Prompt (con RAG)  │    per personalizzare
              │  ✓ Caption (con RAG)       │    ogni output
              │                            │
              └────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  ESEMPIO PRATICO                                                │
└─────────────────────────────────────────────────────────────────┘

  Input:
    Account: "IG BLC"
    Topic: "Sostenibilità nella moda"

  Flusso:
    1. Map: "IG BLC" → "rag-blc-db" (BLC)
    2. Query: "Fornisci info su BLC relative a: sostenibilità..."
    3. RAG trova: "BLC usa cotone biologico, produzione etica..."
    4. Combine: Topic + RAG Knowledge
    5. Generate:
       - Concept: "Racconta la filiera sostenibile di BLC"
       - Image: "Cotone biologico BLC, toni earth, etico"
       - Caption: "La nostra collezione BLC è 100% sostenibile..."

  Risultato: Contenuto personalizzato con info reali BLC!

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
