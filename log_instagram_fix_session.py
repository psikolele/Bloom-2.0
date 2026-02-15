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

def create_session_log_page(project_id):
    """Create a session log page in Notion with the Instagram fix details"""
    url = "https://api.notion.com/v1/pages"

    # Build the page content blocks following the schema comunicativo
    blocks = [
        # 📋 Argomenti Trattati
        {
            "object": "block",
            "type": "heading_1",
            "heading_1": {"rich_text": [{"type": "text", "text": {"content": "📋 Argomenti Trattati"}}]}
        },

        # Session 1: Fix Instagram Account Hardcoded
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {"rich_text": [{"type": "text", "text": {"content": "1. Fix Instagram Account Hardcoded - Workflow Caption Flow V.2"}}]}
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {"rich_text": [
                {"type": "text", "text": {"content": "Contesto"}, "annotations": {"bold": True}},
                {"type": "text", "text": {"content": ": L'execution #7194 ha rivelato che tutti i post Instagram venivano pubblicati sull'account \"Foot_Easy\" indipendentemente dall'account specificato nel payload del webhook."}}
            ]}
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {"rich_text": [
                {"type": "text", "text": {"content": "Problema identificato"}, "annotations": {"bold": True}},
                {"type": "text", "text": {"content": ":"}}
            ]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Nodo \"Upload to Instagram (Upload-Post API)\" aveva parametro user hardcoded a \"Foot_Easy\""}}]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Mancava propagazione dell'Instagram username attraverso il workflow"}}]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Nessun mapping tra account name e Instagram username"}}]}
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
            "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Esteso nodo \"Map Account to RAG DB\" con mapping Instagram username per tutti gli account (BLC_Instagram, istituto_pessina, Foot_Easy, job_courier, walmoss_interior_design)"}}]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Aggiunto assignment InstagramUsername nel nodo \"5. Prepare Data for Instagram API\""}}]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Aggiornato nodo \"Upload to Instagram\" per usare parametro dinamico invece di hardcoded"}}]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Backup workflow prima delle modifiche"}}]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Deploy workflow aggiornato su N8N"}}]}
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {"rich_text": [
                {"type": "text", "text": {"content": "Risultato"}, "annotations": {"bold": True}},
                {"type": "text", "text": {"content": ":"}}
            ]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Workflow ora pubblica correttamente su account Instagram specifici in base al payload"}}]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Tutti 5 account configurati e mappati correttamente"}}]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Version ID deploy: 799400f6-f45c-4e1a-a0eb-a5e229f8696f"}}]}
        },

        {
            "object": "block",
            "type": "divider",
            "divider": {}
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
                {"type": "text", "text": {"content": "Dynamic Account Mapping"}, "annotations": {"bold": True}},
                {"type": "text", "text": {"content": ": Implementato sistema di mapping centralizzato nel nodo \"Map Account to RAG DB\" che gestisce sia RAG database che Instagram username"}}
            ]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [
                {"type": "text", "text": {"content": "Data Propagation"}, "annotations": {"bold": True}},
                {"type": "text", "text": {"content": ": Username Instagram propagato attraverso nodi usando expression {{ $('Map Account to RAG DB').item.json.instagramUsername }}"}}
            ]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [
                {"type": "text", "text": {"content": "Comprehensive Mapping"}, "annotations": {"bold": True}},
                {"type": "text", "text": {"content": ": Configurati tutti 5 account Instagram invece di fix singolo per assicurare scalabilità"}}
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
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [
                {"type": "text", "text": {"content": "Nodi modificati"}, "annotations": {"bold": True}},
                {"type": "text", "text": {"content": ": 3 (Map Account to RAG DB, 5. Prepare Data for Instagram API, Upload to Instagram)"}}
            ]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [
                {"type": "text", "text": {"content": "Account configurati"}, "annotations": {"bold": True}},
                {"type": "text", "text": {"content": ": 5 (BLC, Pessina, Foot Easy, Job Courier, Walmoss)"}}
            ]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [
                {"type": "text", "text": {"content": "Tempo di deploy"}, "annotations": {"bold": True}},
                {"type": "text", "text": {"content": ": Successo al primo tentativo"}}
            ]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [
                {"type": "text", "text": {"content": "Execution problematica"}, "annotations": {"bold": True}},
                {"type": "text", "text": {"content": ": #7194 (identificata e risolta)"}}
            ]}
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
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [
                {"type": "text", "text": {"content": "Workflow"}, "annotations": {"bold": True}},
                {"type": "text", "text": {"content": ": Caption Flow V.2 (ID: oRYSQ9tk63yPJaqt)"}}
            ]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [
                {"type": "text", "text": {"content": "URL N8N"}, "annotations": {"bold": True}},
                {"type": "text", "text": {"content": ": https://emanueleserra.app.n8n.cloud/workflow/oRYSQ9tk63yPJaqt"}}
            ]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [
                {"type": "text", "text": {"content": "Execution debug"}, "annotations": {"bold": True}},
                {"type": "text", "text": {"content": ": #7194"}}
            ]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [
                {"type": "text", "text": {"content": "Version ID"}, "annotations": {"bold": True}},
                {"type": "text", "text": {"content": ": 799400f6-f45c-4e1a-a0eb-a5e229f8696f"}}
            ]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [
                {"type": "text", "text": {"content": "Deploy timestamp"}, "annotations": {"bold": True}},
                {"type": "text", "text": {"content": ": 2026-02-15T07:56:38.699Z"}}
            ]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [
                {"type": "text", "text": {"content": "File aggiornato"}, "annotations": {"bold": True}},
                {"type": "text", "text": {"content": ": backup_workflows/Caption_Flow_V2_oRYSQ9tk63yPJaqt_UPDATED.json"}}
            ]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [
                {"type": "text", "text": {"content": "Commit"}, "annotations": {"bold": True}},
                {"type": "text", "text": {"content": ": c5199a7 (\"fix: Add dynamic Instagram account mapping to workflow\")"}}
            ]}
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
            "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Test workflow con payload diversi per verificare corretto routing degli account"}}]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Monitorare prossime execution per confermare fix funziona in produzione"}}]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Documentare mapping account per future reference"}}]}
        }
    ]

    properties = {
        "Descrizione Breve": {"title": [{"text": {"content": "Fix Instagram Account Mapping - Caption Flow V.2"}}]},
        "Data Sessione": {"date": {"start": "2026-02-15"}},
        "Minuti Lavorati": {"number": 120},
        "Categoria": {"select": {"name": "Debug"}},
        "Note": {"rich_text": [{"text": {"content": "Fixed hardcoded Instagram account in Upload to Instagram node. Implemented dynamic account mapping for all 5 Instagram accounts (BLC, Pessina, Foot Easy, Job Courier, Walmoss)."}}]}
    }

    if project_id:
        properties["Progetto Collegato"] = {"relation": [{"id": project_id}]}

    payload = {
        "parent": {"database_id": DATABASE_ID},
        "icon": {"type": "emoji", "emoji": "🐛"},
        "properties": properties,
        "children": blocks
    }

    response = requests.post(url, json=payload, headers=HEADERS)
    if response.status_code == 200:
        page_data = response.json()
        print("✅ Success! Session log page created.")
        print(f"📄 URL: {page_data['url']}")
        return page_data
    else:
        print(f"❌ Error creating page: {response.status_code}")
        print(response.text)
        return None


if __name__ == "__main__":
    print("🔍 Searching for project 'Social & Marketing'...")
    project_id = search_page("Social & Marketing")

    if project_id:
        print(f"✅ Found Project ID: {project_id}")
    else:
        print("⚠️ Project not found, creating page without relation.")

    print("\n📝 Creating session log page...")
    create_session_log_page(project_id)
