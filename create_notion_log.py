import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("NOTION_API_KEY")
DATABASE_ID = "c024f662-8528-4572-86bb-8c1809680da2"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def search_page(query):
    url = "https://api.notion.com/v1/search"
    payload = {"query": query, "filter": {"value": "page", "property": "object"}}
    response = requests.post(url, json=payload, headers=HEADERS)
    if response.status_code == 200:
        results = response.json().get("results", [])
        if results:
            return results[0]['id']
    return None

def create_page(project_id):
    url = "https://api.notion.com/v1/pages"
    
    blocks = [
        {"object": "block", "type": "heading_1", "heading_1": {"rich_text": [{"type": "text", "text": {"content": "📋 Argomenti Trattati"}}]}},
        {"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"type": "text", "text": {"content": "1. Aggiornamento Caption Flow Workflow (N8N)"}}]}},
        {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": "Contesto: Modifica del workflow CaptionFlow N8N per migliorare la comunicazione con il frontend."}}]}},
        {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Backup del workflow esistente prima delle modifiche"}}]}},
        {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Configurazione responseMode: responseNode sul nodo CaptionFlow Webhook"}}]}},
        {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Aggiunta nuovo nodo Respond to Frontend dopo Upload Image to Cloudinary"}}]}},
        {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Configurazione risposta JSON con: success, message, caption, image_url"}}]}},
        {"object": "block", "type": "divider", "divider": {}},
        {"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"type": "text", "text": {"content": "2. Fix Integrazione Google Sheets (N8N)"}}]}},
        {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": "Contesto: Risoluzione problema di scrittura dati su Google Sheets nel workflow N8N."}}]}},
        {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Analisi execution 5463 per identificare la root cause del fallimento"}}]}},
        {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Implementazione fix nel workflow N8N"}}]}},
        {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Verifica persistenza dati corretta su Google Sheets"}}]}},
        {"object": "block", "type": "divider", "divider": {}},
        {"object": "block", "type": "heading_1", "heading_1": {"rich_text": [{"type": "text", "text": {"content": "🎯 Decisioni Chiave"}}]}},
        {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Response Node Pattern: Adottato responseMode responseNode per maggiore controllo"}}]}},
        {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Backup Strategy: Sempre effettuare backup dei workflow prima di modifiche"}}]}},
        {"object": "block", "type": "divider", "divider": {}},
        {"object": "block", "type": "heading_1", "heading_1": {"rich_text": [{"type": "text", "text": {"content": "🔗 Riferimenti"}}]}},
        {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Workflow modificato: Caption Flow v2 (ID: LDko1nSj5LhLnEDndqSSo)"}}]}},
        {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Tool utilizzati: N8N, Cloudinary, Google Sheets API"}}]}}
    ]

    properties = {
        "Descrizione Breve": {"title": [{"text": {"content": "Caption Flow & Google Sheets - N8N Workflow Updates"}}]},
        "Data Sessione": {"date": {"start": "2026-01-27"}},
        "Minuti Lavorati": {"number": 180},
        "Categoria": {"select": {"name": "Sviluppo"}},
        "Note": {"rich_text": [{"text": {"content": "Aggiornamento Caption Flow workflow con nuovo nodo Respond to Frontend, fix integrazione Google Sheets."}}]}
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
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"SUCCESS! Page URL: {data['url']}")
    else:
        print(f"ERROR: {response.text[:500]}")

if __name__ == "__main__":
    print("Searching for Social & Marketing...")
    pid = search_page("Social & Marketing")
    print(f"Project ID: {pid}")
    print("Creating page...")
    create_page(pid)
