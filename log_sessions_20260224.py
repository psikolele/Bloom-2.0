#!/usr/bin/env python3
"""
Registra due sessioni di lavoro su Notion — 2026-02-24
  A) Oggi (2026-02-24): Access Control N8N - Accesso Limitato Webstoreplus
     Progetto: Social & Marketing | 60 min | Sviluppo
  B) Ieri (2026-02-23): Formazione Javier
     Progetto: BLC | 150 min | Formazione
"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("NOTION_API_KEY")
DATABASE_ID = "c024f662-8528-4572-86bb-8c1809680da2"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}


def search_project(query):
    """Cerca un progetto su Notion per nome e restituisce il suo ID."""
    url = "https://api.notion.com/v1/search"
    payload = {"query": query, "filter": {"value": "page", "property": "object"}}
    response = requests.post(url, json=payload, headers=HEADERS)
    if response.status_code == 200:
        results = response.json().get("results", [])
        if results:
            page_id = results[0]["id"]
            print(f"  Trovato: '{query}' → {page_id}")
            return page_id
    print(f"  Progetto '{query}' non trovato — pagina creata senza collegamento")
    return None


# ---------------------------------------------------------------------------
# SESSIONE A — Oggi 2026-02-24
# ---------------------------------------------------------------------------

def create_session_today(project_id=None):
    blocks = [
        # ── Argomenti Trattati ──────────────────────────────────────────────
        {
            "object": "block", "type": "heading_1",
            "heading_1": {"rich_text": [{"type": "text", "text": {"content": "📋 Argomenti Trattati"}}]}
        },

        # 1. Access Control Webstoreplus
        {
            "object": "block", "type": "heading_2",
            "heading_2": {"rich_text": [{"type": "text", "text": {"content": "1. Implementazione Accesso Limitato per Utente Webstoreplus"}}]}
        },
        {
            "object": "block", "type": "paragraph",
            "paragraph": {"rich_text": [{"type": "text", "text": {"content": "Contesto: Creazione di un account 'admin livello 2' per il cliente Webstoreplus che, pur avendo accesso al dropdown RAG e Caption Flow, vede esclusivamente le folder Foot Easy e Walmoss."}}]}
        },
        {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Creazione utenza webstoreplus su Notion tramite webhook N8N (password: webstore2026!)"}}]}},
        {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Logica di filtraggio: allowedNames = ['RAG Database Foot Easy', 'RAG Database Walmoss']"}}]}},
        {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Frontend: rimozione dinamica delle opzioni non consentite nel dropdown Caption Flow"}}]}},

        {"object": "block", "type": "divider", "divider": {}},

        # 2. Aggiornamento N8N live
        {
            "object": "block", "type": "heading_2",
            "heading_2": {"rich_text": [{"type": "text", "text": {"content": "2. Aggiornamento Nodo 'Aggregate Folders' su N8N Cloud (live)"}}]}
        },
        {
            "object": "block", "type": "paragraph",
            "paragraph": {"rich_text": [{"type": "text", "text": {"content": "Contesto: Modifica diretta del workflow attivo su N8N Cloud via API REST (PUT /workflows/{id}) senza passare per il file locale."}}]}
        },
        {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Fetch del workflow live (74 nodi, ID: XmCaI5Q9MxNf0EP_65UvB)"}}]}},
        {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Aggiunta blocco 'webstoreplus' al jsCode del nodo Aggregate Folders (id: s2kcwppr9lib5x8fq6zp8)"}}]}},
        {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "PUT riuscito: updatedAt 2026-02-24T13:02:13.521Z — verifica live confermata ✅"}}]}},

        {
            "object": "block", "type": "callout",
            "callout": {
                "rich_text": [{"type": "text", "text": {"content": "Nota tecnica: il body del PUT N8N richiede solo name, nodes, connections, settings (con campi standard). Le proprietà extra del GET (id, createdAt, versionId, ecc.) vanno escluse per evitare HTTP 400."}, "annotations": {"bold": False}}],
                "icon": {"type": "emoji", "emoji": "💡"}
            }
        },

        {"object": "block", "type": "divider", "divider": {}},

        # 3. Frontend
        {
            "object": "block", "type": "heading_2",
            "heading_2": {"rich_text": [{"type": "text", "text": {"content": "3. Aggiornamento Frontend React/TypeScript"}}]}
        },
        {
            "object": "block", "type": "paragraph",
            "paragraph": {"rich_text": [{"type": "text", "text": {"content": "Contesto: Adattamento dell'interfaccia utente per esporre il dropdown RAG/Caption Flow a webstoreplus con le sole opzioni consentite."}}]}
        },
        {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Dashboard.tsx: isLimitedAdmin per webstoreplus → setIsAdmin(true), effectiveUsername passato come username reale al webhook N8N"}}]}},
        {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "app.js Caption Flow: DOM init filtra il <select> lasciando solo Foot_Easy e walmoss_interior_design"}}]}},

        {"object": "block", "type": "divider", "divider": {}},

        # ── Decisioni Chiave ────────────────────────────────────────────────
        {
            "object": "block", "type": "heading_1",
            "heading_1": {"rich_text": [{"type": "text", "text": {"content": "🎯 Decisioni Chiave"}}]}
        },
        {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Pattern admin livello 2: l'N8N filtra lato server, il frontend filtra lato client — doppia protezione"}}]}},
        {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Deploy diretto su N8N Cloud: aggiornamento immediato senza restart, senza downtime"}}]}},
        {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "effectiveUsername preservato: super admin usa 'admin', limited admin usa il proprio username per il filtering"}}]}},

        {"object": "block", "type": "divider", "divider": {}},

        # ── Riferimenti ─────────────────────────────────────────────────────
        {
            "object": "block", "type": "heading_1",
            "heading_1": {"rich_text": [{"type": "text", "text": {"content": "🔗 Riferimenti"}}]}
        },
        {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Branch Git: claude/notion-limited-user-access-OtNUI"}}]}},
        {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Workflow N8N: RAG | Google Drive to Pinecone | Chat with RAG [ACCESS CONTROL] (XmCaI5Q9MxNf0EP_65UvB)"}}]}},
        {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "File modificati: workflow_attivo.json, public/caption-flow/js/app.js, src/pages/Dashboard.tsx"}}]}},
        {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Tool utilizzati: N8N REST API, Python urllib, React/TypeScript"}}]}},
    ]

    properties = {
        "Descrizione Breve": {"title": [{"text": {"content": "Access Control N8N - Accesso Limitato Webstoreplus"}}]},
        "Data Sessione": {"date": {"start": "2026-02-24"}},
        "Minuti Lavorati": {"number": 60},
        "Categoria": {"select": {"name": "Sviluppo"}},
        "Note": {"rich_text": [{"text": {"content": "Implementato admin livello 2 per webstoreplus: vede solo Foot Easy e Walmoss. Deploy live su N8N Cloud via PUT API. Frontend aggiornato (Dashboard.tsx + app.js). Branch: claude/notion-limited-user-access-OtNUI"}}]}
    }
    if project_id:
        properties["Progetto Collegato"] = {"relation": [{"id": project_id}]}

    payload = {
        "parent": {"database_id": DATABASE_ID},
        "icon": {"type": "emoji", "emoji": "🔒"},
        "properties": properties,
        "children": blocks
    }

    response = requests.post("https://api.notion.com/v1/pages", json=payload, headers=HEADERS)
    if response.status_code == 200:
        url = response.json()["url"]
        print(f"  ✅ Sessione A creata: {url}")
        return url
    else:
        print(f"  ❌ Errore: {response.status_code} — {response.text[:300]}")
        return None


# ---------------------------------------------------------------------------
# SESSIONE B — Ieri 2026-02-23
# ---------------------------------------------------------------------------

def create_session_yesterday(project_id=None):
    blocks = [
        # ── Argomenti Trattati ──────────────────────────────────────────────
        {
            "object": "block", "type": "heading_1",
            "heading_1": {"rich_text": [{"type": "text", "text": {"content": "📋 Argomenti Trattati"}}]}
        },

        # 1. Introduzione Bloom
        {
            "object": "block", "type": "heading_2",
            "heading_2": {"rich_text": [{"type": "text", "text": {"content": "1. Introduzione al Progetto Bloom"}}]}
        },
        {
            "object": "block", "type": "paragraph",
            "paragraph": {"rich_text": [{"type": "text", "text": {"content": "Contesto: Panoramica della piattaforma Bloom 2.0 per Javier, partendo dalla vision fino all'architettura tecnica."}}]}
        },
        {
            "object": "block", "type": "paragraph",
            "paragraph": {"rich_text": [{"type": "text", "text": {"content": "Bloom 2.0 è una piattaforma AI multitenancy pensata per le PMI italiane. L'idea centrale è offrire a ogni cliente un assistente AI addestrato esclusivamente sui propri documenti aziendali, senza condivisione di dati tra clienti diversi. Ogni azienda (JobCourier, Pessina, Walmoss, Foot Easy, BLC, Webstoreplus) carica i propri documenti in una cartella Google Drive dedicata: questa cartella diventa la knowledge base privata da cui il sistema impara."}}]}
        },
        {
            "object": "block", "type": "paragraph",
            "paragraph": {"rich_text": [{"type": "text", "text": {"content": "Il sistema è costruito su quattro pilastri tecnologici: N8N come orchestratore dei workflow (nessun codice custom per il pipeline principale), Pinecone come vector database per lo storage degli embeddings, OpenAI per la generazione degli embeddings e le risposte AI, e un frontend React/TypeScript con autenticazione per l'accesso controllato. Il progetto include inoltre Caption Flow, un secondo workflow N8N dedicato alla generazione automatica di contenuti social media (caption, post, ecc.) partendo da immagini caricate."}}]}
        },
        {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Multi-tenancy: ogni cliente ha namespace Pinecone isolato → zero cross-contamination dei dati"}}]}},
        {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Zero infrastruttura per il cliente: Google Drive già conosciuto e usato dalle PMI"}}]}},
        {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Aggiornamento knowledge base: basta caricare/modificare file su Drive, nessun re-training"}}]}},
        {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Access control granulare: la mappa utente → folder è gestita lato N8N (nodo Aggregate Folders)"}}]}},

        {"object": "block", "type": "divider", "divider": {}},

        # 2. Considerazioni e implementation plan
        {
            "object": "block", "type": "heading_2",
            "heading_2": {"rich_text": [{"type": "text", "text": {"content": "2. Considerazioni e Implementation Plan con Gabriele"}}]}
        },
        {
            "object": "block", "type": "paragraph",
            "paragraph": {"rich_text": [{"type": "text", "text": {"content": "Contesto: Sessione di pianificazione tecnica e strategica insieme a Gabriele per definire le priorità di sviluppo e le scelte architetturali chiave."}}]}
        },
        {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Architettura multi-tenant: namespace isolation in Pinecone — ogni cliente ha il proprio spazio vettoriale isolato"}}]}},
        {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Strategia di chunking: chunkSize 1500 chars, overlap 200 — bilanciamento tra contesto e precisione del retrieval"}}]}},
        {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Access control: webhook N8N con autenticazione username/password, logica di filtraggio folder lato server"}}]}},
        {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Roadmap priorità: stabilizzazione RAG (chunking corretto, namespace) → accesso clienti (auth, dropdown) → nuove feature (Caption Flow, admin livelli)"}}]}},
        {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Best practice deploy: backup workflow N8N prima di ogni modifica, verifica via API dopo il deploy"}}]}},
        {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Testing pattern: deploy → trigger workflow con file reale → verifica chunk count e dimensioni in Pinecone"}}]}},

        {
            "object": "block", "type": "callout",
            "callout": {
                "rich_text": [{"type": "text", "text": {"content": "Decisione chiave: N8N come orchestratore principale riduce la complessità operativa. Modifiche al pipeline sono configurazione, non codice — accessibile anche a figure non-dev."}, "annotations": {"bold": False}}],
                "icon": {"type": "emoji", "emoji": "🎯"}
            }
        },

        {"object": "block", "type": "divider", "divider": {}},

        # 3. RAG
        {
            "object": "block", "type": "heading_2",
            "heading_2": {"rich_text": [{"type": "text", "text": {"content": "3. Concetti di Base sul RAG (Retrieval-Augmented Generation)"}}]}
        },
        {
            "object": "block", "type": "paragraph",
            "paragraph": {"rich_text": [{"type": "text", "text": {"content": "Contesto: Spiegazione della tecnica RAG a Javier, con focus sul flusso implementato in Bloom e sui vantaggi pratici per le PMI."}}]}
        },
        {
            "object": "block", "type": "paragraph",
            "paragraph": {"rich_text": [{"type": "text", "text": {"content": "RAG (Retrieval-Augmented Generation) è una tecnica che augmenta i Large Language Models con il recupero di informazioni da knowledge base esterne. Il problema che risolve è fondamentale: un LLM (es. GPT-4) conosce il mondo fino alla sua data di training, ma non conosce i documenti interni dell'azienda. Con RAG, invece di 'insegnare' quei documenti al modello (costoso e lento), li cerchiamo dinamicamente a ogni domanda e li passiamo come contesto al LLM."}}]}
        },
        {
            "object": "block", "type": "paragraph",
            "paragraph": {"rich_text": [{"type": "text", "text": {"content": "Flusso RAG in Bloom (fase di indicizzazione — avviene una volta per ogni documento):"}}]}
        },
        {"object": "block", "type": "numbered_list_item", "numbered_list_item": {"rich_text": [{"type": "text", "text": {"content": "Google Drive Watch → rileva nuovi file caricati nella folder del cliente"}}]}},
        {"object": "block", "type": "numbered_list_item", "numbered_list_item": {"rich_text": [{"type": "text", "text": {"content": "Document Loader → legge il contenuto del file (PDF, DOCX, MD, TXT)"}}]}},
        {"object": "block", "type": "numbered_list_item", "numbered_list_item": {"rich_text": [{"type": "text", "text": {"content": "Text Splitter → divide il documento in chunk (1400-1500 chars con overlap di 200 chars per continuità semantica)"}}]}},
        {"object": "block", "type": "numbered_list_item", "numbered_list_item": {"rich_text": [{"type": "text", "text": {"content": "OpenAI Embeddings → trasforma ogni chunk in un vettore numerico ad alta dimensionalità (1536 dimensioni)"}}]}},
        {"object": "block", "type": "numbered_list_item", "numbered_list_item": {"rich_text": [{"type": "text", "text": {"content": "Pinecone Upsert → salva i vettori nel namespace del cliente (es. 'rag-blc-db')"}}]}},
        {
            "object": "block", "type": "paragraph",
            "paragraph": {"rich_text": [{"type": "text", "text": {"content": "Flusso RAG in Bloom (fase di query — avviene ad ogni domanda dell'utente):"}}]}
        },
        {"object": "block", "type": "numbered_list_item", "numbered_list_item": {"rich_text": [{"type": "text", "text": {"content": "Utente pone una domanda via chat → N8N riceve la query via webhook"}}]}},
        {"object": "block", "type": "numbered_list_item", "numbered_list_item": {"rich_text": [{"type": "text", "text": {"content": "OpenAI genera l'embedding della domanda (stesso spazio vettoriale dei documenti)"}}]}},
        {"object": "block", "type": "numbered_list_item", "numbered_list_item": {"rich_text": [{"type": "text", "text": {"content": "Pinecone similarity search → trova i k chunk più simili semanticamente alla domanda (nel namespace del cliente)"}}]}},
        {"object": "block", "type": "numbered_list_item", "numbered_list_item": {"rich_text": [{"type": "text", "text": {"content": "I chunk recuperati vengono inseriti nel prompt come contesto: 'Basandoti su questi documenti, rispondi a...'"}}]}},
        {"object": "block", "type": "numbered_list_item", "numbered_list_item": {"rich_text": [{"type": "text", "text": {"content": "LLM (via OpenRouter) genera la risposta finale usando il contesto aziendale specifico"}}]}},
        {
            "object": "block", "type": "paragraph",
            "paragraph": {"rich_text": [{"type": "text", "text": {"content": "Vantaggi concreti per le PMI:"}}]}
        },
        {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Risposte accurate e specifiche al dominio aziendale, non risposte generiche"}}]}},
        {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Knowledge base sempre aggiornata: basta caricare il nuovo file su Drive"}}]}},
        {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Riduzione allucinazioni: il LLM risponde solo su ciò che è scritto nei documenti"}}]}},
        {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Trasparenza: possibile citare il chunk sorgente ('risposta tratta da documento X, pagina Y')"}}]}},
        {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Costo contenuto: nessun fine-tuning del modello — si paga solo per le API call"}}]}},

        {"object": "block", "type": "divider", "divider": {}},

        # ── Decisioni Chiave ────────────────────────────────────────────────
        {
            "object": "block", "type": "heading_1",
            "heading_1": {"rich_text": [{"type": "text", "text": {"content": "🎯 Decisioni Chiave"}}]}
        },
        {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Namespace Pinecone per cliente: isolamento dati garantito, scalabilità lineare all'aggiunta di nuovi clienti"}}]}},
        {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "N8N come orchestratore: nessuna dipendenza da framework Python custom, modifiche tramite UI visuale"}}]}},
        {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Google Drive come knowledge base: zero onboarding per i clienti, familiarità immediata"}}]}},

        {"object": "block", "type": "divider", "divider": {}},

        # ── Note Formazione ─────────────────────────────────────────────────
        {
            "object": "block", "type": "heading_1",
            "heading_1": {"rich_text": [{"type": "text", "text": {"content": "📌 Note di Formazione"}}]}
        },
        {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Javier ha una buona base tecnica: sessione orientata ai concetti architetturali e alle scelte di design"}}]}},
        {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Priorità: capire il flusso end-to-end (Drive → Pinecone → LLM) prima di approfondire i singoli nodi N8N"}}]}},
        {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Prossima sessione: hands-on su N8N — analisi workflow live, trigger manuale, verifica chunk in Pinecone"}}]}},
    ]

    properties = {
        "Descrizione Breve": {"title": [{"text": {"content": "Formazione Javier"}}]},
        "Data Sessione": {"date": {"start": "2026-02-23"}},
        "Minuti Lavorati": {"number": 150},
        "Categoria": {"select": {"name": "Formazione"}},
        "Note": {"rich_text": [{"text": {"content": "Prima sessione formativa per Javier. Temi: architettura Bloom 2.0 multi-tenant, flusso RAG end-to-end (Drive→Pinecone→LLM), implementation plan con Gabriele, best practice deploy N8N."}}]}
    }
    if project_id:
        properties["Progetto Collegato"] = {"relation": [{"id": project_id}]}

    payload = {
        "parent": {"database_id": DATABASE_ID},
        "icon": {"type": "emoji", "emoji": "🎓"},
        "properties": properties,
        "children": blocks
    }

    response = requests.post("https://api.notion.com/v1/pages", json=payload, headers=HEADERS)
    if response.status_code == 200:
        url = response.json()["url"]
        print(f"  ✅ Sessione B creata: {url}")
        return url
    else:
        print(f"  ❌ Errore: {response.status_code} — {response.text[:300]}")
        return None


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 65)
    print("📝 REGISTRAZIONE SESSIONI DI LAVORO SU NOTION")
    print("=" * 65)

    print("\n🔍 [A] Ricerca progetto 'Social & Marketing'...")
    pid_social = search_project("Social & Marketing")

    print("\n📝 [A] Creazione sessione oggi (2026-02-24)...")
    url_a = create_session_today(pid_social)

    print("\n🔍 [B] Ricerca progetto 'BLC'...")
    pid_blc = search_project("BLC")

    print("\n📝 [B] Creazione sessione ieri (2026-02-23) — Formazione Javier...")
    url_b = create_session_yesterday(pid_blc)

    print("\n" + "=" * 65)
    if url_a and url_b:
        print("✅ ENTRAMBE LE SESSIONI CREATE CON SUCCESSO!")
        print(f"\n🔗 Sessione A (oggi):  {url_a}")
        print(f"🔗 Sessione B (ieri):  {url_b}")
    elif url_a:
        print("⚠️  Solo Sessione A creata. Controlla gli errori per B.")
    elif url_b:
        print("⚠️  Solo Sessione B creata. Controlla gli errori per A.")
    else:
        print("❌ Nessuna sessione creata. Controlla API key e connessione.")
    print("=" * 65)
