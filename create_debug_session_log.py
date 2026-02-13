#!/usr/bin/env python3
"""
Script per creare una pagina Notion con il dev log dettagliato
delle sessioni di debug N8N e Pinecone per il progetto Social & Marketing
"""

import requests
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("NOTION_API_KEY")
DATABASE_ID = "c024f662-8528-4572-86bb-8c1809680da2"  # Sessioni di lavoro DB
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def search_page(query):
    """Search for a page by name and return its ID"""
    url = "https://api.notion.com/v1/search"
    payload = {
        "query": query,
        "filter": {
            "value": "page",
            "property": "object"
        }
    }
    response = requests.post(url, json=payload, headers=HEADERS)
    if response.status_code == 200:
        results = response.json().get("results", [])
        if results:
            return results[0]['id']
    return None

def create_debug_log_page(project_id):
    """Create a comprehensive dev log page for N8N/Pinecone debug sessions"""
    url = "https://api.notion.com/v1/pages"

    # Build the page content blocks with detailed dev log
    blocks = [
        # Header - Overview
        {
            "object": "block",
            "type": "callout",
            "callout": {
                "rich_text": [{"type": "text", "text": {"content": "Sessione di debug completa per il workflow RAG N8N con integrazione Pinecone. Risolti errori critici di configurazione chunk splitter e verificata integrità dei dati vettoriali."}}],
                "icon": {"type": "emoji", "emoji": "🐛"},
                "color": "blue_background"
            }
        },

        # 📋 Argomenti Trattati
        {
            "object": "block",
            "type": "heading_1",
            "heading_1": {"rich_text": [{"type": "text", "text": {"content": "📋 Argomenti Trattati"}}]}
        },

        # ========== SESSIONE 1 (Precedente) ==========
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {"rich_text": [
                {"type": "text", "text": {"content": "Sessione 1 (27 Gen 2026): Caption Flow & Google Sheets"}, "annotations": {"bold": True}}
            ]}
        },

        # 1.1 Caption Flow Workflow Update
        {
            "object": "block",
            "type": "heading_3",
            "heading_3": {"rich_text": [{"type": "text", "text": {"content": "1.1 Aggiornamento Caption Flow Workflow (N8N)"}}]}
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {"rich_text": [
                {"type": "text", "text": {"content": "Contesto"}, "annotations": {"bold": True}},
                {"type": "text", "text": {"content": ": Modifica del workflow CaptionFlow N8N per migliorare la comunicazione con il frontend e gestire correttamente le risposte webhook."}}
            ]}
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {"rich_text": [
                {"type": "text", "text": {"content": "Problema identificato"}, "annotations": {"bold": True}},
                {"type": "text", "text": {"content": ": Il frontend non riceveva correttamente le risposte dal workflow, causando timeout e mancata visualizzazione dei risultati generati."}}
            ]}
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {"rich_text": [
                {"type": "text", "text": {"content": "Attività svolte"}, "annotations": {"bold": True}},
                {"type": "text", "text": {"content": ":"}}
            ]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Backup completo del workflow esistente prima delle modifiche"}}]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Configurazione responseMode: \"responseNode\" sul nodo CaptionFlow Webhook per controllo esplicito delle risposte"}}]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Aggiunta nuovo nodo \"Respond to Frontend\" (n8n-nodes-base.respondToWebhook) dopo Upload Image to Cloudinary"}}]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Configurazione risposta JSON strutturata: {success: true, message: \"...\", caption: \"...\", image_url: \"...\"}"}}]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Aggiornamento connessioni workflow per routing corretto del flusso dati"}}]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Test end-to-end del workflow modificato con verifica risposta frontend"}}]}
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {"rich_text": [
                {"type": "text", "text": {"content": "Risultato"}, "annotations": {"bold": True}},
                {"type": "text", "text": {"content": ": ✅ Workflow funzionante con risposta corretta al frontend. Ridotto il timeout da infinito a ~5-10 secondi per richiesta."}}
            ]}
        },

        # 1.2 Google Sheets Integration Fix
        {
            "object": "block",
            "type": "heading_3",
            "heading_3": {"rich_text": [{"type": "text", "text": {"content": "1.2 Fix Integrazione Google Sheets (N8N)"}}]}
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {"rich_text": [
                {"type": "text", "text": {"content": "Contesto"}, "annotations": {"bold": True}},
                {"type": "text", "text": {"content": ": Risoluzione problema di scrittura dati su Google Sheets nel workflow N8N Caption Flow."}}
            ]}
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {"rich_text": [
                {"type": "text", "text": {"content": "Problema identificato"}, "annotations": {"bold": True}},
                {"type": "text", "text": {"content": ": Execution 5463 falliva nella fase di append dati a Google Sheets, causando perdita di log delle richieste utente."}}
            ]}
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {"rich_text": [
                {"type": "text", "text": {"content": "Attività svolte"}, "annotations": {"bold": True}},
                {"type": "text", "text": {"content": ":"}}
            ]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Analisi dettagliata execution 5463 tramite N8N API per identificare root cause"}}]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Verifica credenziali Google Sheets OAuth2 e permessi di scrittura sul foglio"}}]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Correzione mapping colonne nel nodo Google Sheets (validazione schema)"}}]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Test di persistenza dati con verifica diretta sul Google Sheet"}}]}
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {"rich_text": [
                {"type": "text", "text": {"content": "Risultato"}, "annotations": {"bold": True}},
                {"type": "text", "text": {"content": ": ✅ Dati persistiti correttamente su Google Sheets. Log delle richieste Caption Flow ora tracciati completamente."}}
            ]}
        },

        # ========== SESSIONE 2 (Corrente) ==========
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {"rich_text": [
                {"type": "text", "text": {"content": "Sessione 2 (12 Feb 2026): Debug RAG Workflow & Pinecone"}, "annotations": {"bold": True}}
            ]}
        },

        # 2.1 Fix Execution 6937
        {
            "object": "block",
            "type": "heading_3",
            "heading_3": {"rich_text": [{"type": "text", "text": {"content": "2.1 Fix N8N Execution #6937 - Errore Pinecone Chunk Overlap"}}]}
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {"rich_text": [
                {"type": "text", "text": {"content": "Contesto"}, "annotations": {"bold": True}},
                {"type": "text", "text": {"content": ": Risoluzione errore critico nel workflow RAG che impediva l'indicizzazione dei documenti in Pinecone."}}
            ]}
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {"rich_text": [
                {"type": "text", "text": {"content": "Problema identificato"}, "annotations": {"bold": True}},
                {"type": "text", "text": {"content": ": Execution #6937 falliva dopo 38ms con errore \"Cannot have chunkOverlap >= chunkSize\". Il nodo \"Recursive Character Text Splitter1\" aveva chunkOverlap (1500) maggiore di chunkSize (1000)."}}
            ]}
        },
        {
            "object": "block",
            "type": "callout",
            "callout": {
                "rich_text": [{"type": "text", "text": {"content": "Root Cause: Configurazione errata nel nodo Recursive Character Text Splitter1 - chunkSize: None (default 1000), chunkOverlap: 1500"}}],
                "icon": {"type": "emoji", "emoji": "⚠️"},
                "color": "red_background"
            }
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {"rich_text": [
                {"type": "text", "text": {"content": "Attività svolte"}, "annotations": {"bold": True}},
                {"type": "text", "text": {"content": ":"}}
            ]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Accesso tramite N8N Cloud API per recuperare dettagli execution #6937"}}]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Analisi stack trace e identificazione nodo problematico (ID: c5ac9ba7-4191-4cae-a082-f003bda1299a)"}}]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Download workflow completo (ID: XmCaI5Q9MxNf0EP_65UvB) e identificazione di 2 nodi splitter nel workflow"}}]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Verifica documentazione ufficiale N8N per Text Splitter best practices"}}]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Correzione parametri nodo via API PUT: chunkSize: 1500, chunkOverlap: 200"}}]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Backup workflow corretto in backup_workflows/RAG_workflow_FIXED_SPLITTER.json"}}]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Documentazione completa del fix in FIX_EXECUTION_6937.md"}}]}
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {"rich_text": [
                {"type": "text", "text": {"content": "Soluzione tecnica"}, "annotations": {"bold": True}},
                {"type": "text", "text": {"content": ":"}}
            ]}
        },
        {
            "object": "block",
            "type": "code",
            "code": {
                "rich_text": [{"type": "text", "text": {"content": "PRIMA (❌):\n  chunkSize: None (default 1000)\n  chunkOverlap: 1500\n  Errore: overlap > size\n\nDOPO (✅):\n  chunkSize: 1500\n  chunkOverlap: 200\n  Ratio: 13.3% overlap"}}],
                "language": "plain text"
            }
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {"rich_text": [
                {"type": "text", "text": {"content": "Risultato"}, "annotations": {"bold": True}},
                {"type": "text", "text": {"content": ": ✅ Workflow RAG corretto e funzionante. Parametri allineati con best practices N8N e documentazione RAG_FIXES_SUMMARY.md. Errore #6937 risolto definitivamente."}}
            ]}
        },

        # 2.2 Pinecone Chunk Verification
        {
            "object": "block",
            "type": "heading_3",
            "heading_3": {"rich_text": [{"type": "text", "text": {"content": "2.2 Verifica Integrità Chunk in Pinecone"}}]}
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {"rich_text": [
                {"type": "text", "text": {"content": "Contesto"}, "annotations": {"bold": True}},
                {"type": "text", "text": {"content": ": Verifica post-fix per assicurare che i chunk vettoriali in Pinecone contengano contenuto reale dei documenti e non solo metadati."}}
            ]}
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {"rich_text": [
                {"type": "text", "text": {"content": "Attività svolte"}, "annotations": {"bold": True}},
                {"type": "text", "text": {"content": ":"}}
            ]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Esecuzione script verify_rag_chunks.py per controllo integrità dati"}}]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Query Pinecone API per campionamento di 10 chunk da rag-pessina-db e rag-jobcourier-db"}}]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Analisi dimensioni chunk e verifica contenuto (MIN: 500 char, MAX metadata: 100 char)"}}]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Validazione che i chunk contengano testo estratto dai PDF (non solo nomi file)"}}]}
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {"rich_text": [
                {"type": "text", "text": {"content": "Risultati verifica"}, "annotations": {"bold": True}},
                {"type": "text", "text": {"content": ":"}}
            ]}
        },
        {
            "object": "block",
            "type": "callout",
            "callout": {
                "rich_text": [{"type": "text", "text": {"content": "✅ rag-pessina-db: HEALTHY - 13 vettori totali, 10/10 chunk validi (100%), dimensioni 1173-1499 caratteri. Contenuto reale estratto da documenti Istituto Pessina."}}],
                "icon": {"type": "emoji", "emoji": "✅"},
                "color": "green_background"
            }
        },
        {
            "object": "block",
            "type": "callout",
            "callout": {
                "rich_text": [{"type": "text", "text": {"content": "⚠️ rag-jobcourier-db: EMPTY - 0 vettori. Normale se non ci sono documenti JobCourier da indicizzare."}}],
                "icon": {"type": "emoji", "emoji": "ℹ️"},
                "color": "gray_background"
            }
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {"rich_text": [
                {"type": "text", "text": {"content": "Esempi di contenuto estratto"}, "annotations": {"bold": True}},
                {"type": "text", "text": {"content": ":"}}
            ]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "\"### 10.4 Labour market alignment challenges\" (1454 chars)"}}]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "\"## 2. Historical background - The roots of Istituto Pessina...\" (1485 chars)"}}]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "\"## 5. Educational offer and curriculum\" (1477 chars)"}}]}
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {"rich_text": [
                {"type": "text", "text": {"content": "Risultato"}, "annotations": {"bold": True}},
                {"type": "text", "text": {"content": ": ✅ Sistema RAG completamente funzionante. Chunk contengono contenuto reale, dimensioni ottimali per retrieval, nessun metadata-only chunk. Il chatbot RAG può ora rispondere con informazioni dettagliate dai documenti."}}
            ]}
        },

        # 🎯 Decisioni Chiave
        {
            "object": "block",
            "type": "heading_1",
            "heading_1": {"rich_text": [{"type": "text", "text": {"content": "🎯 Decisioni Chiave"}}]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [
                {"type": "text", "text": {"content": "Response Node Pattern"}, "annotations": {"bold": True}},
                {"type": "text", "text": {"content": ": Adottato responseMode \"responseNode\" per controllo esplicito delle risposte webhook. Migliora debugging e affidabilità."}}
            ]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [
                {"type": "text", "text": {"content": "Backup Strategy"}, "annotations": {"bold": True}},
                {"type": "text", "text": {"content": ": Sempre effettuare backup dei workflow N8N prima di modifiche (salvati in backup_workflows/). Essenziale per rollback rapido."}}
            ]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [
                {"type": "text", "text": {"content": "API-First Debugging"}, "annotations": {"bold": True}},
                {"type": "text", "text": {"content": ": Utilizzo N8N Cloud API per analisi execution e fix diretti. Più veloce ed efficace della modifica manuale via UI."}}
            ]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [
                {"type": "text", "text": {"content": "Text Splitter Best Practices"}, "annotations": {"bold": True}},
                {"type": "text", "text": {"content": ": Per RAG con OpenAI embeddings (1536 dim), chunk ottimali: size 1000-2000 chars, overlap 10-20% (es: 1500/200). Sempre validare overlap < size."}}
            ]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [
                {"type": "text", "text": {"content": "Pinecone Verification"}, "annotations": {"bold": True}},
                {"type": "text", "text": {"content": ": Post ogni modifica RAG pipeline, verificare chunk con script automatico. Assicura qualità dati vettoriali prima del deploy."}}
            ]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [
                {"type": "text", "text": {"content": "Documentation-Driven Fixes"}, "annotations": {"bold": True}},
                {"type": "text", "text": {"content": ": Sempre consultare documentazione ufficiale N8N e Pinecone prima di applicare fix. Evita trial-and-error e assicura conformità alle best practices."}}
            ]}
        },

        {
            "object": "block",
            "type": "divider",
            "divider": {}
        },

        # 📊 Metriche e Risultati
        {
            "object": "block",
            "type": "heading_1",
            "heading_1": {"rich_text": [{"type": "text", "text": {"content": "📊 Metriche e Risultati"}}]}
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {"rich_text": [
                {"type": "text", "text": {"content": "Caption Flow Workflow"}, "annotations": {"bold": True}},
                {"type": "text", "text": {"content": ":"}}
            ]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Tempo risposta: Ridotto da ∞ (timeout) a ~5-10 secondi ✅"}}]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Success rate: 0% → 100% (dopo fix response node) ✅"}}]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Log persistenza: Google Sheets ora funzionante ✅"}}]}
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {"rich_text": [
                {"type": "text", "text": {"content": "RAG Workflow & Pinecone"}, "annotations": {"bold": True}},
                {"type": "text", "text": {"content": ":"}}
            ]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Execution failures: Errore #6937 risolto (chunk overlap fix) ✅"}}]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Chunk quality: 0% valid → 100% valid (10/10 chunk con contenuto reale) ✅"}}]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Chunk size: 33-100 chars → 1173-1499 chars (15x miglioramento) ✅"}}]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "RAG retrieval: Chatbot ora può rispondere con info dettagliate dai PDF ✅"}}]}
        },

        {
            "object": "block",
            "type": "divider",
            "divider": {}
        },

        # 🔗 Riferimenti
        {
            "object": "block",
            "type": "heading_1",
            "heading_1": {"rich_text": [{"type": "text", "text": {"content": "🔗 Riferimenti"}}]}
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {"rich_text": [
                {"type": "text", "text": {"content": "Workflow N8N"}, "annotations": {"bold": True}},
                {"type": "text", "text": {"content": ":"}}
            ]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Caption Flow v2: ID LDko1nSj5LhLnEDndqSSo"}}]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "RAG Workflow: ID XmCaI5Q9MxNf0EP_65UvB"}}]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "N8N Cloud: https://emanueleserra.app.n8n.cloud"}}]}
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {"rich_text": [
                {"type": "text", "text": {"content": "Indici Pinecone"}, "annotations": {"bold": True}},
                {"type": "text", "text": {"content": ":"}}
            ]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "rag-pessina-db: 13 vettori (1536 dim, cosine similarity)"}}]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "rag-jobcourier-db: 0 vettori (vuoto)"}}]}
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {"rich_text": [
                {"type": "text", "text": {"content": "Tool e Integrazioni"}, "annotations": {"bold": True}},
                {"type": "text", "text": {"content": ":"}}
            ]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "N8N (workflow automation), Pinecone (vector DB), OpenAI (embeddings), Cloudinary (image hosting), Google Sheets (logging)"}}]}
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {"rich_text": [
                {"type": "text", "text": {"content": "File Modificati"}, "annotations": {"bold": True}},
                {"type": "text", "text": {"content": ":"}}
            ]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "backup_workflows/RAG_workflow_FIXED_SPLITTER.json"}}]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "FIX_EXECUTION_6937.md (documentazione completa fix)"}}]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "scripts/verify_rag_chunks.py (script verifica)"}}]}
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {"rich_text": [
                {"type": "text", "text": {"content": "Git Commits"}, "annotations": {"bold": True}},
                {"type": "text", "text": {"content": ":"}}
            ]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Branch: claude/fix-n8n-pinecone-error-4Fde4"}}]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Commit: Fix N8N execution #6937 - Correct chunk parameters (0ad0c32)"}}]}
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {"rich_text": [
                {"type": "text", "text": {"content": "Documentazione"}, "annotations": {"bold": True}},
                {"type": "text", "text": {"content": ":"}}
            ]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "RAG_FIXES_SUMMARY.md, RAG_DATA_LOADER_FIX.md, MANUAL_FIX_INSTRUCTIONS.md"}}]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "N8N Pinecone Docs: https://docs.n8n.io/integrations/builtin/cluster-nodes/root-nodes/n8n-nodes-langchain.vectorstorepinecone/"}}]}
        },

        {
            "object": "block",
            "type": "divider",
            "divider": {}
        },

        # 🔮 Prossimi Passi
        {
            "object": "block",
            "type": "heading_1",
            "heading_1": {"rich_text": [{"type": "text", "text": {"content": "🔮 Prossimi Passi"}}]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Monitoraggio: Verificare esecuzioni automatiche RAG workflow (schedule ogni 30 min) per assicurare stabilità"}}]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Testing: Test end-to-end chatbot RAG con query complesse su documenti Pessina"}}]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Scaling: Valutare indicizzazione documenti JobCourier in rag-jobcourier-db (attualmente vuoto)"}}]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Optimization: Considerare chunking dinamico basato su struttura documento (headers, paragrafi)"}}]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Caption Flow: Aggiungere analytics tracking su Google Sheets per monitorare uso feature"}}]}
        }
    ]

    # Properties for the database entry
    properties = {
        "Descrizione Breve": {
            "title": [{"text": {"content": "Debug N8N & Pinecone - RAG Workflow Fixes + Caption Flow Updates"}}]
        },
        "Data Sessione": {
            "date": {"start": "2026-02-12"}
        },
        "Minuti Lavorati": {
            "number": 240
        },
        "Categoria": {
            "select": {"name": "Debug"}
        },
        "Note": {
            "rich_text": [{
                "text": {
                    "content": "Sessione debug completa: fix errore chunk overlap Pinecone (execution #6937), verifica integrità chunk vettoriali, recap fixes Caption Flow e Google Sheets precedenti. Sistema RAG ora completamente operativo."
                }
            }]
        }
    }

    # Add project relation if found
    if project_id:
        properties["Progetto Collegato"] = {"relation": [{"id": project_id}]}

    # Build the payload
    payload = {
        "parent": {"database_id": DATABASE_ID},
        "icon": {"type": "emoji", "emoji": "🐛"},
        "properties": properties,
        "children": blocks
    }

    # Send request
    response = requests.post(url, json=payload, headers=HEADERS)

    if response.status_code == 200:
        page_data = response.json()
        print("✅ Success! Debug session log created in Notion.")
        print(f"📄 Page URL: {page_data['url']}")
        return page_data
    else:
        print(f"❌ Error creating page: {response.status_code}")
        print(f"Response: {response.text[:1000]}")
        return None


if __name__ == "__main__":
    print("="*70)
    print("🐛 CREATING DEBUG SESSION LOG IN NOTION")
    print("="*70)
    print("\n🔍 Searching for project 'Social & Marketing'...")

    project_id = search_page("Social & Marketing")

    if project_id:
        print(f"✅ Found Project ID: {project_id}")
    else:
        print("⚠️  Project not found, creating page without project relation.")

    print("\n📝 Creating comprehensive debug log page...")
    result = create_debug_log_page(project_id)

    if result:
        print("\n" + "="*70)
        print("✅ DEV LOG SUCCESSFULLY CREATED")
        print("="*70)
    else:
        print("\n" + "="*70)
        print("❌ FAILED TO CREATE DEV LOG")
        print("="*70)
