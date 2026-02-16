#!/usr/bin/env python3
"""
Crea una sessione di lavoro su Notion per il debug RAG JobCourier
"""
import requests
import os
from datetime import datetime
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
    """Cerca un progetto su Notion"""
    url = "https://api.notion.com/v1/search"
    payload = {"query": query, "filter": {"value": "page", "property": "object"}}
    response = requests.post(url, json=payload, headers=HEADERS)
    if response.status_code == 200:
        results = response.json().get("results", [])
        if results:
            print(f"✅ Trovato progetto: {results[0].get('properties', {}).get('title', {}).get('title', [{}])[0].get('text', {}).get('content', query)}")
            return results[0]['id']
    print(f"⚠️  Progetto '{query}' non trovato - sessione creata senza collegamento")
    return None

def create_rag_debug_session(project_id=None):
    """Crea la sessione di lavoro per il debug RAG JobCourier"""
    url = "https://api.notion.com/v1/pages"

    # Contenuto strutturato della sessione
    blocks = [
        # Sezione: Argomenti Trattati
        {
            "object": "block",
            "type": "heading_1",
            "heading_1": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "📋 Argomenti Trattati"}
                }]
            }
        },

        # Topic 1: Investigazione Problema Chunking
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "1. Investigazione Problema Chunking RAG JobCourier"}
                }]
            }
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{
                    "type": "text",
                    "text": {
                        "content": "Contesto: Execution #7244 del workflow RAG ha prodotto solo 6 chunk (3 unici + 3 duplicati) nell'index rag-jobcourier-db invece dei 20-50+ chunk attesi da file multipli (PDFs + MD)."
                    }
                }]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "Analisi stato chunk in Pinecone: 6 vettori totali (3 unici + 3 duplicati)"}
                }]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "Identificati chunk troppo piccoli (74 caratteri) e source metadata mancante (\"blob\")"}
                }]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "Backup dei 6 chunk esistenti prima della pulizia (backup_jobcourier_chunks_20260216_121348.json)"}
                }]
            }
        },

        # Divider
        {"object": "block", "type": "divider", "divider": {}},

        # Topic 2: Analisi Workflow N8N
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "2. Analisi Workflow N8N RAG (ID: XmCaI5Q9MxNf0EP_65UvB)"}
                }]
            }
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{
                    "type": "text",
                    "text": {
                        "content": "Contesto: Scaricamento e analisi del workflow attivo da N8N per identificare il problema nel flusso di chunking."
                    }
                }]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "Download workflow attivo via API N8N (63 nodi totali)"}
                }]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "Tracciamento connessioni dei nodi per identificare il flusso \"Auto\" usato da JobCourier"}
                }]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "Verifica configurazione Text Splitter (chunkSize=1500, chunkOverlap=200) ✅"}
                }]
            }
        },
        {
            "object": "block",
            "type": "callout",
            "callout": {
                "rich_text": [{
                    "type": "text",
                    "text": {
                        "content": "🔴 ROOT CAUSE TROVATO: Il Text Splitter non era connesso al nodo \"Auto Upsert to Pinecone\" → il chunking NON veniva eseguito!"
                    },
                    "annotations": {"bold": True}
                }],
                "icon": {"type": "emoji", "emoji": "🔍"}
            }
        },

        # Divider
        {"object": "block", "type": "divider", "divider": {}},

        # Topic 3: Implementazione Fix
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "3. Implementazione Fix Workflow"}
                }]
            }
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{
                    "type": "text",
                    "text": {
                        "content": "Contesto: Modifica del workflow per connettere il Text Splitter al flusso Auto e deploy su N8N."
                    }
                }]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "Creazione script fix_workflow_text_splitter.py per automazione fix"}
                }]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "Aggiunta connessione ai_textSplitter da \"Recursive Character Text Splitter1\" a \"Auto Upsert to Pinecone\""}
                }]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "Deploy workflow fixato su N8N via API PUT (status 200 OK) ✅"}
                }]
            }
        },

        # Divider
        {"object": "block", "type": "divider", "divider": {}},

        # Topic 4: Pulizia Index e Preparazione Re-indexing
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "4. Pulizia Index Pinecone e Preparazione Re-indexing"}
                }]
            }
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{
                    "type": "text",
                    "text": {
                        "content": "Contesto: Pulizia dell'index rag-jobcourier-db per rimuovere i chunk mal formattati prima del re-indexing con il workflow fixato."
                    }
                }]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "Creazione script clean_jobcourier_index.py con conferma utente"}
                }]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "Esecuzione pulizia: 6 vettori eliminati → 0 vettori nell'index"}
                }]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "Index pronto per re-indexing con chunking corretto"}
                }]
            }
        },

        # Divider
        {"object": "block", "type": "divider", "divider": {}},

        # Sezione: Decisioni Chiave
        {
            "object": "block",
            "type": "heading_1",
            "heading_1": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "🎯 Decisioni Chiave"}
                }]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "Connessione Text Splitter: Priorità assoluta - il chunking è essenziale per RAG efficace"}
                }]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "Backup Strategy: Sempre backuppare chunk esistenti prima di pulizie massive"}
                }]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "Workflow Analysis: Verificare connessioni nodi, non solo configurazioni - nodi orfani sono invisibili ma critici"}
                }]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "Testing Pattern: Deploy → Test con file reale → Verifica chunk count e dimensioni"}
                }]
            }
        },

        # Divider
        {"object": "block", "type": "divider", "divider": {}},

        # Sezione: Metriche Pre/Post Fix
        {
            "object": "block",
            "type": "heading_1",
            "heading_1": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "📊 Metriche Pre/Post Fix"}
                }]
            }
        },
        {
            "object": "block",
            "type": "table",
            "table": {
                "table_width": 3,
                "has_column_header": True,
                "has_row_header": False,
                "children": [
                    {
                        "type": "table_row",
                        "table_row": {
                            "cells": [
                                [{"type": "text", "text": {"content": "Metrica"}}],
                                [{"type": "text", "text": {"content": "PRIMA"}}],
                                [{"type": "text", "text": {"content": "DOPO (atteso)"}}]
                            ]
                        }
                    },
                    {
                        "type": "table_row",
                        "table_row": {
                            "cells": [
                                [{"type": "text", "text": {"content": "Total chunks"}}],
                                [{"type": "text", "text": {"content": "6 (3 unici)"}}],
                                [{"type": "text", "text": {"content": "20-50+"}}]
                            ]
                        }
                    },
                    {
                        "type": "table_row",
                        "table_row": {
                            "cells": [
                                [{"type": "text", "text": {"content": "Chunk size"}}],
                                [{"type": "text", "text": {"content": "74-1481 chars"}}],
                                [{"type": "text", "text": {"content": "1400-1500 chars"}}]
                            ]
                        }
                    },
                    {
                        "type": "table_row",
                        "table_row": {
                            "cells": [
                                [{"type": "text", "text": {"content": "Source metadata"}}],
                                [{"type": "text", "text": {"content": "\"blob\""}}],
                                [{"type": "text", "text": {"content": "Nome file reale"}}]
                            ]
                        }
                    },
                    {
                        "type": "table_row",
                        "table_row": {
                            "cells": [
                                [{"type": "text", "text": {"content": "Duplicati"}}],
                                [{"type": "text", "text": {"content": "50%"}}],
                                [{"type": "text", "text": {"content": "0%"}}]
                            ]
                        }
                    }
                ]
            }
        },

        # Divider
        {"object": "block", "type": "divider", "divider": {}},

        # Sezione: Riferimenti
        {
            "object": "block",
            "type": "heading_1",
            "heading_1": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "🔗 Riferimenti"}
                }]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "Workflow: RAG | Google Drive to Pinecone (ID: XmCaI5Q9MxNf0EP_65UvB)"}
                }]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "Branch Git: claude/debug-vector-db-chunks-1luT7"}
                }]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "Commit: 947032d - Fix RAG JobCourier chunking"}
                }]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "Documentazione: RAG_JOBCOURIER_DEBUG_FEB_16.md"}
                }]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "Tool utilizzati: N8N, Pinecone, OpenAI Embeddings, LangChain, Python"}
                }]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "Script creati: backup_jobcourier_chunks.py, clean_jobcourier_index.py, fix_workflow_text_splitter.py"}
                }]
            }
        },

        # Divider
        {"object": "block", "type": "divider", "divider": {}},

        # Sezione: Prossimi Passi
        {
            "object": "block",
            "type": "heading_1",
            "heading_1": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "🚀 Prossimi Passi"}
                }]
            }
        },
        {
            "object": "block",
            "type": "numbered_list_item",
            "numbered_list_item": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "Caricare file di test su Google Drive (cartella RAG Database JobCourier)"}
                }]
            }
        },
        {
            "object": "block",
            "type": "numbered_list_item",
            "numbered_list_item": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "Triggerare workflow (automatico ogni 30 min o manuale da N8N UI)"}
                }]
            }
        },
        {
            "object": "block",
            "type": "numbered_list_item",
            "numbered_list_item": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "Verificare risultati: python3 scripts/verify_rag_chunks.py"}
                }]
            }
        },
        {
            "object": "block",
            "type": "numbered_list_item",
            "numbered_list_item": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "Testare query RAG dalla web app Bloom 2.0"}
                }]
            }
        },
        {
            "object": "block",
            "type": "numbered_list_item",
            "numbered_list_item": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "Aggiornare RAG_FIXES_SUMMARY.md con questo fix (#3)"}
                }]
            }
        },

        # Callout finale
        {
            "object": "block",
            "type": "callout",
            "callout": {
                "rich_text": [{
                    "type": "text",
                    "text": {
                        "content": "✅ Fix completato e deployato. Index pulito e pronto per re-indexing. Expected: 20-50+ chunk con dimensioni corrette (1400-1500 chars)."
                    },
                    "annotations": {"bold": True}
                }],
                "icon": {"type": "emoji", "emoji": "🎯"}
            }
        }
    ]

    # Properties della pagina
    properties = {
        "Descrizione Breve": {
            "title": [{
                "text": {
                    "content": "Debug RAG JobCourier - Fix Text Splitter Non Connesso"
                }
            }]
        },
        "Data Sessione": {
            "date": {
                "start": datetime.now().strftime("%Y-%m-%d")
            }
        },
        "Minuti Lavorati": {
            "number": 90
        },
        "Categoria": {
            "select": {
                "name": "Debug"
            }
        },
        "Note": {
            "rich_text": [{
                "text": {
                    "content": "ROOT CAUSE: Text Splitter non connesso al flusso Auto → chunking non eseguito. FIX: Connesso Text Splitter a Auto Upsert to Pinecone, deployato workflow, pulito index (6→0 vettori). Branch: claude/debug-vector-db-chunks-1luT7"
                }
            }]
        }
    }

    # Aggiungi relazione al progetto se fornito
    if project_id:
        properties["Progetto Collegato"] = {
            "relation": [{"id": project_id}]
        }

    # Payload finale
    payload = {
        "parent": {"database_id": DATABASE_ID},
        "icon": {"type": "emoji", "emoji": "🔍"},
        "properties": properties,
        "children": blocks
    }

    # Invia richiesta
    response = requests.post(url, json=payload, headers=HEADERS)

    print("=" * 70)
    print("📝 CREAZIONE SESSIONE NOTION")
    print("=" * 70)
    print(f"\nStatus: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        print(f"\n✅ SUCCESS! Sessione creata su Notion")
        print(f"\n📄 Page URL: {data['url']}")
        print(f"\n📊 Dettagli Sessione:")
        print(f"   Titolo: Debug RAG JobCourier - Fix Text Splitter Non Connesso")
        print(f"   Data: {datetime.now().strftime('%Y-%m-%d')}")
        print(f"   Durata: 90 minuti")
        print(f"   Categoria: Debug")
        print(f"   Icona: 🔍")

        return data['url']
    else:
        print(f"\n❌ ERROR: {response.text[:500]}")
        return None

if __name__ == "__main__":
    print("\n🔍 Step 1: Ricerca progetto Bloom 2.0...")
    project_id = search_project("Bloom 2.0")

    print("\n📝 Step 2: Creazione sessione di lavoro...")
    page_url = create_rag_debug_session(project_id)

    if page_url:
        print("\n" + "=" * 70)
        print("✅ SESSIONE CREATA CON SUCCESSO!")
        print("=" * 70)
        print(f"\n🔗 Apri la sessione qui: {page_url}")
        print("\n💡 La sessione include:")
        print("   - 📋 4 argomenti trattati dettagliati")
        print("   - 🎯 4 decisioni chiave")
        print("   - 📊 Tabella metriche pre/post fix")
        print("   - 🔗 6 riferimenti (workflow, branch, commit, docs)")
        print("   - 🚀 5 prossimi passi actionable")
    else:
        print("\n❌ Creazione fallita - controlla gli errori sopra")
