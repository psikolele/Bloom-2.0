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

def create_training_session_page(project_id):
    """Create a training session page for Gloria about Pivot Tables"""
    url = "https://api.notion.com/v1/pages"

    # Build the page content blocks following the training schema comunicativo
    blocks = [
        # 📋 Argomenti Trattati
        {
            "object": "block",
            "type": "heading_1",
            "heading_1": {"rich_text": [{"type": "text", "text": {"content": "📋 Argomenti Trattati"}}]}
        },

        # Session 1: Introduzione alle Tabelle Pivot
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {"rich_text": [{"type": "text", "text": {"content": "1. Introduzione alle Tabelle Pivot"}}]}
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {"rich_text": [
                {"type": "text", "text": {"content": "Concetti fondamentali"}, "annotations": {"bold": True}},
                {"type": "text", "text": {"content": ": Cos'è una tabella pivot e perché è uno strumento essenziale per l'analisi dati. Differenza tra dati grezzi e dati aggregati."}}
            ]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Definizione: Strumento per sintetizzare, analizzare ed esplorare grandi quantità di dati"}}]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Vantaggi: Aggregazione dinamica, riorganizzazione flessibile, calcoli automatici"}}]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "Applicazioni: Report vendite, analisi performance, dashboard KPI"}}]}
        },

        # Session 2: Creazione di Tabelle Pivot
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {"rich_text": [{"type": "text", "text": {"content": "2. Creazione di Tabelle Pivot in Excel/Google Sheets"}}]}
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {"rich_text": [
                {"type": "text", "text": {"content": "Procedura step-by-step"}, "annotations": {"bold": True}},
                {"type": "text", "text": {"content": ":"}}
            ]}
        },
        {
            "object": "block",
            "type": "numbered_list_item",
            "numbered_list_item": {"rich_text": [{"type": "text", "text": {"content": "Selezione dei dati sorgente - verificare che i dati siano puliti e strutturati"}}]}
        },
        {
            "object": "block",
            "type": "numbered_list_item",
            "numbered_list_item": {"rich_text": [{"type": "text", "text": {"content": "Inserimento tabella pivot - Menu Inserisci > Tabella Pivot"}}]}
        },
        {
            "object": "block",
            "type": "numbered_list_item",
            "numbered_list_item": {"rich_text": [{"type": "text", "text": {"content": "Configurazione campi - Righe, Colonne, Valori, Filtri"}}]}
        },
        {
            "object": "block",
            "type": "numbered_list_item",
            "numbered_list_item": {"rich_text": [{"type": "text", "text": {"content": "Scelta delle funzioni di aggregazione - SOMMA, MEDIA, CONTEGGIO, MIN, MAX"}}]}
        },
        {
            "object": "block",
            "type": "numbered_list_item",
            "numbered_list_item": {"rich_text": [{"type": "text", "text": {"content": "Personalizzazione layout e formattazione"}}]}
        },

        # Session 3: Gestione Avanzata
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {"rich_text": [{"type": "text", "text": {"content": "3. Gestione e Tecniche Avanzate"}}]}
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {"rich_text": [
                {"type": "text", "text": {"content": "Funzionalità avanzate trattate"}, "annotations": {"bold": True}},
                {"type": "text", "text": {"content": ":"}}
            ]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [
                {"type": "text", "text": {"content": "Raggruppamento dati"}, "annotations": {"bold": True}},
                {"type": "text", "text": {"content": ": Per data (mese/trimestre/anno), per intervalli numerici, per categorie custom"}}
            ]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [
                {"type": "text", "text": {"content": "Campi calcolati"}, "annotations": {"bold": True}},
                {"type": "text", "text": {"content": ": Creazione di nuovi campi basati su formule (es. margine = ricavi - costi)"}}
            ]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [
                {"type": "text", "text": {"content": "Filtri e Slicers"}, "annotations": {"bold": True}},
                {"type": "text", "text": {"content": ": Filtri dinamici per analisi interattive e dashboard"}}
            ]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [
                {"type": "text", "text": {"content": "Aggiornamento dati"}, "annotations": {"bold": True}},
                {"type": "text", "text": {"content": ": Refresh automatico e manuale quando i dati sorgente cambiano"}}
            ]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [
                {"type": "text", "text": {"content": "Grafici pivot"}, "annotations": {"bold": True}},
                {"type": "text", "text": {"content": ": Visualizzazione grafica dei dati aggregati per comunicazione efficace"}}
            ]}
        },

        {
            "object": "block",
            "type": "divider",
            "divider": {}
        },

        # 🎯 Competenze Acquisite
        {
            "object": "block",
            "type": "heading_1",
            "heading_1": {"rich_text": [{"type": "text", "text": {"content": "🎯 Competenze Acquisite"}}]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [
                {"type": "text", "text": {"content": "Analisi dati strutturati"}, "annotations": {"bold": True}},
                {"type": "text", "text": {"content": ": Capacità di analizzare dataset complessi e identificare pattern significativi"}}
            ]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [
                {"type": "text", "text": {"content": "Creazione report dinamici"}, "annotations": {"bold": True}},
                {"type": "text", "text": {"content": ": Costruzione di report che si aggiornano automaticamente con nuovi dati"}}
            ]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [
                {"type": "text", "text": {"content": "Problem solving analitico"}, "annotations": {"bold": True}},
                {"type": "text", "text": {"content": ": Rispondere a domande business attraverso aggregazione e drill-down dei dati"}}
            ]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [
                {"type": "text", "text": {"content": "Best practices"}, "annotations": {"bold": True}},
                {"type": "text", "text": {"content": ": Preparazione dati, naming conventions, documentazione analisi"}}
            ]}
        },

        {
            "object": "block",
            "type": "divider",
            "divider": {}
        },

        # 💼 Esempi Pratici
        {
            "object": "block",
            "type": "heading_1",
            "heading_1": {"rich_text": [{"type": "text", "text": {"content": "💼 Esempi Pratici"}}]}
        },
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {"rich_text": [{"type": "text", "text": {"content": "Caso 1: Analisi Vendite per Regione e Prodotto"}}]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [
                {"type": "text", "text": {"content": "Dataset"}, "annotations": {"bold": True}},
                {"type": "text", "text": {"content": ": 5000 righe di transazioni di vendita con campi: Data, Regione, Prodotto, Quantità, Ricavo"}}
            ]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [
                {"type": "text", "text": {"content": "Obiettivo"}, "annotations": {"bold": True}},
                {"type": "text", "text": {"content": ": Identificare prodotti top-performer per ciascuna regione"}}
            ]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [
                {"type": "text", "text": {"content": "Configurazione"}, "annotations": {"bold": True}},
                {"type": "text", "text": {"content": ": Righe=Regione, Colonne=Prodotto, Valori=SOMMA(Ricavo)"}}
            ]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [
                {"type": "text", "text": {"content": "Risultato"}, "annotations": {"bold": True}},
                {"type": "text", "text": {"content": ": Matrice che mostra ricavi totali per ogni combinazione regione-prodotto"}}
            ]}
        },

        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {"rich_text": [{"type": "text", "text": {"content": "Caso 2: Trend Mensile Performance Team"}}]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [
                {"type": "text", "text": {"content": "Dataset"}, "annotations": {"bold": True}},
                {"type": "text", "text": {"content": ": Log attività team con campi: Data, Membro Team, Ore Lavorate, Progetti Completati"}}
            ]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [
                {"type": "text", "text": {"content": "Obiettivo"}, "annotations": {"bold": True}},
                {"type": "text", "text": {"content": ": Analizzare trend produttività nel tempo"}}
            ]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [
                {"type": "text", "text": {"content": "Configurazione"}, "annotations": {"bold": True}},
                {"type": "text", "text": {"content": ": Righe=Data(raggruppata per mese), Colonne=Membro Team, Valori=SOMMA(Progetti Completati)"}}
            ]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [
                {"type": "text", "text": {"content": "Visualizzazione"}, "annotations": {"bold": True}},
                {"type": "text", "text": {"content": ": Grafico a linee pivot per visualizzare trend temporali"}}
            ]}
        },

        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {"rich_text": [{"type": "text", "text": {"content": "Caso 3: Dashboard Metriche Social Media"}}]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [
                {"type": "text", "text": {"content": "Dataset"}, "annotations": {"bold": True}},
                {"type": "text", "text": {"content": ": Metriche post social con campi: Data, Piattaforma, Account, Impressioni, Engagement, Click"}}
            ]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [
                {"type": "text", "text": {"content": "Obiettivo"}, "annotations": {"bold": True}},
                {"type": "text", "text": {"content": ": Dashboard interattiva con filtri per analisi multi-dimensionale"}}
            ]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [
                {"type": "text", "text": {"content": "Configurazione"}, "annotations": {"bold": True}},
                {"type": "text", "text": {"content": ": Multiple pivot tables + Slicers per Piattaforma e Account + Grafici pivot collegati"}}
            ]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [
                {"type": "text", "text": {"content": "Campi calcolati"}, "annotations": {"bold": True}},
                {"type": "text", "text": {"content": ": Engagement Rate = (Engagement/Impressioni)*100, CTR = (Click/Impressioni)*100"}}
            ]}
        },

        {
            "object": "block",
            "type": "divider",
            "divider": {}
        },

        # 📚 Risorse e Riferimenti
        {
            "object": "block",
            "type": "heading_1",
            "heading_1": {"rich_text": [{"type": "text", "text": {"content": "📚 Risorse e Riferimenti"}}]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [
                {"type": "text", "text": {"content": "Documentazione ufficiale"}, "annotations": {"bold": True}},
                {"type": "text", "text": {"content": ": Microsoft Excel Pivot Tables Guide, Google Sheets Pivot Table Documentation"}}
            ]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [
                {"type": "text", "text": {"content": "Dataset di esercitazione"}, "annotations": {"bold": True}},
                {"type": "text", "text": {"content": ": File Excel condiviso su OneDrive con esempi pratici discussi"}}
            ]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [
                {"type": "text", "text": {"content": "Video tutorial"}, "annotations": {"bold": True}},
                {"type": "text", "text": {"content": ": Playlist YouTube salvata con tutorial avanzati consigliati"}}
            ]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [
                {"type": "text", "text": {"content": "Cheat sheet"}, "annotations": {"bold": True}},
                {"type": "text", "text": {"content": ": PDF con shortcuts e funzioni più comuni per riferimento rapido"}}
            ]}
        },

        {
            "object": "block",
            "type": "divider",
            "divider": {}
        },

        # 🚀 Prossimi Passi
        {
            "object": "block",
            "type": "heading_1",
            "heading_1": {"rich_text": [{"type": "text", "text": {"content": "🚀 Prossimi Passi"}}]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [
                {"type": "text", "text": {"content": "Esercitazione pratica"}, "annotations": {"bold": True}},
                {"type": "text", "text": {"content": ": Creare 3 pivot tables diverse usando dataset aziendali reali entro fine settimana"}}
            ]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [
                {"type": "text", "text": {"content": "Applicazione al progetto corrente"}, "annotations": {"bold": True}},
                {"type": "text", "text": {"content": ": Integrare pivot tables nel report mensile performance social media"}}
            ]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [
                {"type": "text", "text": {"content": "Approfondimento Power Pivot"}, "annotations": {"bold": True}},
                {"type": "text", "text": {"content": ": Prossima sessione formazione su Power Pivot e DAX per analisi più complesse"}}
            ]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [
                {"type": "text", "text": {"content": "Revisione follow-up"}, "annotations": {"bold": True}},
                {"type": "text", "text": {"content": ": Call di 30 minuti tra una settimana per discutere dubbi e casi d'uso specifici"}}
            ]}
        }
    ]

    properties = {
        "Descrizione Breve": {"title": [{"text": {"content": "Formazione Gloria - Creazione e Gestione Tabelle Pivot"}}]},
        "Data Sessione": {"date": {"start": "2026-02-09"}},
        "Minuti Lavorati": {"number": 100},
        "Categoria": {"select": {"name": "Formazione"}},
        "Note": {"rich_text": [{"text": {"content": "Sessione formativa completa su creazione e gestione tabelle pivot in Excel/Google Sheets. Trattati concetti base, tecniche avanzate (raggruppamento, campi calcolati, slicers) e 3 casi pratici applicativi. Gloria ha acquisito competenze per analisi dati e creazione report dinamici."}}]}
    }

    if project_id:
        properties["Progetto Collegato"] = {"relation": [{"id": project_id}]}

    payload = {
        "parent": {"database_id": DATABASE_ID},
        "icon": {"type": "emoji", "emoji": "📊"},
        "properties": properties,
        "children": blocks
    }

    response = requests.post(url, json=payload, headers=HEADERS)
    if response.status_code == 200:
        page_data = response.json()
        print("✅ Success! Training session page created.")
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

    print("\n📝 Creating training session page...")
    create_training_session_page(project_id)
