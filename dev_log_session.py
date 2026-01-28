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

def create_dev_log_page(project_id):
    """Create a dev log page in Notion with the specified content"""
    url = "https://api.notion.com/v1/pages"
    
    # Build the page content blocks following the example style
    blocks = [
        # 📋 Argomenti Trattati
        {
            "object": "block",
            "type": "heading_1",
            "heading_1": {"rich_text": [{"type": "text", "text": {"content": "📋 Argomenti Trattati"}}]}
        },
        
        # Session 1: Updating Caption Flow Workflow
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {"rich_text": [{"type": "text", "text": {"content": "1. Aggiornamento Caption Flow Workflow (N8N)"}}]}
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {"rich_text": [
                {"type": "text", "text": {"content": "Contesto"}, "annotations": {"bold": True}},
                {"type": "text", "text": {"content": ": Modifica del workflow CaptionFlow N8N per migliorare la comunicazione con il frontend."}}
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
            "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Backup del workflow esistente prima delle modifiche"}}]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Configurazione responseMode: \"responseNode\" sul nodo CaptionFlow Webhook"}}]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Aggiunta nuovo nodo \"Respond to Frontend\" dopo Upload Image to Cloudinary"}}]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Configurazione risposta JSON con: success, message, caption, image_url"}}]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Aggiornamento connessioni workflow per routing corretto"}}]}
        },
        
        {
            "object": "block",
            "type": "divider",
            "divider": {}
        },
        
        # Session 2: Fixing Google Sheets Integration
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {"rich_text": [{"type": "text", "text": {"content": "2. Fix Integrazione Google Sheets (N8N)"}}]}
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {"rich_text": [
                {"type": "text", "text": {"content": "Contesto"}, "annotations": {"bold": True}},
                {"type": "text", "text": {"content": ": Risoluzione problema di scrittura dati su Google Sheets nel workflow N8N."}}
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
            "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Analisi execution 5463 per identificare la root cause del fallimento"}}]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Implementazione fix nel workflow N8N"}}]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Verifica persistenza dati corretta su Google Sheets"}}]}
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
                {"type": "text", "text": {"content": "Response Node Pattern"}, "annotations": {"bold": True}},
                {"type": "text", "text": {"content": ": Adottato responseMode \"responseNode\" per maggiore controllo sulle risposte webhook"}}
            ]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [
                {"type": "text", "text": {"content": "Backup Strategy"}, "annotations": {"bold": True}},
                {"type": "text", "text": {"content": ": Sempre effettuare backup dei workflow prima di modifiche significative"}}
            ]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [
                {"type": "text", "text": {"content": "Error Handling"}, "annotations": {"bold": True}},
                {"type": "text", "text": {"content": ": Analisi dettagliata delle execution per debug efficace"}}
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
                {"type": "text", "text": {"content": "Workflow modificato"}, "annotations": {"bold": True}},
                {"type": "text", "text": {"content": ": Caption Flow v2 (ID: LDko1nSj5LhLnEDndqSSo)"}}
            ]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [
                {"type": "text", "text": {"content": "Tool utilizzati"}, "annotations": {"bold": True}},
                {"type": "text", "text": {"content": ": N8N, Cloudinary, Google Sheets API"}}
            ]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [
                {"type": "text", "text": {"content": "Nodi N8N creati/modificati"}, "annotations": {"bold": True}},
                {"type": "text", "text": {"content": ": CaptionFlow Webhook, Respond to Frontend, Upload Image to Cloudinary"}}
            ]}
        }
    ]

    properties = {
        "Descrizione Breve": {"title": [{"text": {"content": "Caption Flow & Google Sheets - N8N Workflow Updates"}}]},
        "Data Sessione": {"date": {"start": "2026-01-27"}},
        "Minuti Lavorati": {"number": 180},
        "Categoria": {"select": {"name": "Sviluppo"}},
        "Note": {"rich_text": [{"text": {"content": "Aggiornamento Caption Flow workflow con nuovo nodo Respond to Frontend, fix integrazione Google Sheets, backup workflow prima delle modifiche."}}]}
    }

    if project_id:
        properties["Progetto Collegato"] = {"relation": [{"id": project_id}]}

    payload = {
        "parent": {"database_id": DATABASE_ID},
        "icon": {"type": "emoji", "emoji": "💻"},
        "properties": properties,
        "children": blocks
    }

    response = requests.post(url, json=payload, headers=HEADERS)
    if response.status_code == 200:
        page_data = response.json()
        print("✅ Success! Dev log page created.")
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

    print("\n📝 Creating dev log page...")
    create_dev_log_page(project_id)
