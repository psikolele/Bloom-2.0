#!/usr/bin/env python3
"""
Fix del workflow RAG: connettere Recursive Character Text Splitter1 al flusso Auto
"""
import json
import sys

def fix_workflow_connections(workflow_file):
    """
    Aggiunge la connessione ai_textSplitter da 'Recursive Character Text Splitter1'
    a 'Auto Upsert to Pinecone'
    """
    print("=" * 70)
    print("🔧 FIX WORKFLOW: Connettere Text Splitter al flusso Auto")
    print("=" * 70)

    # Carica workflow
    with open(workflow_file, 'r', encoding='utf-8') as f:
        workflow = json.load(f)

    print(f"\n📂 Workflow caricato: {workflow.get('name')}")
    print(f"   ID: {workflow.get('id')}")
    print(f"   Nodi totali: {len(workflow.get('nodes', []))}")

    # Trova i nodi rilevanti
    text_splitter_node = None
    auto_upsert_node = None

    for node in workflow['nodes']:
        if node['name'] == 'Recursive Character Text Splitter1':
            text_splitter_node = node
            print(f"\n✅ Trovato: {node['name']}")
            print(f"   ID: {node['id']}")
            print(f"   Config: chunkSize={node['parameters'].get('chunkSize')}, chunkOverlap={node['parameters'].get('chunkOverlap')}")
        elif node['name'] == 'Auto Upsert to Pinecone':
            auto_upsert_node = node
            print(f"\n✅ Trovato: {node['name']}")
            print(f"   ID: {node['id']}")

    if not text_splitter_node:
        print("\n❌ ERRORE: Nodo 'Recursive Character Text Splitter1' non trovato!")
        return False

    if not auto_upsert_node:
        print("\n❌ ERRORE: Nodo 'Auto Upsert to Pinecone' non trovato!")
        return False

    # Verifica connessioni esistenti
    connections = workflow.get('connections', {})
    splitter_name = text_splitter_node['name']

    print(f"\n{'='*70}")
    print("📊 ANALISI CONNESSIONI ESISTENTI")
    print(f"{'='*70}")

    if splitter_name in connections:
        print(f"\n⚠️  '{splitter_name}' ha già connessioni:")
        print(json.dumps(connections[splitter_name], indent=2))
    else:
        print(f"\n❌ '{splitter_name}' non ha connessioni (nodo orfano)")

    # Crea la connessione ai_textSplitter
    if splitter_name not in connections:
        connections[splitter_name] = {}

    if 'ai_textSplitter' not in connections[splitter_name]:
        connections[splitter_name]['ai_textSplitter'] = []

    # Aggiungi connessione a Auto Upsert to Pinecone
    new_connection = {
        "node": "Auto Upsert to Pinecone",
        "type": "ai_textSplitter",
        "index": 0
    }

    # Check se già esiste
    existing_connections = connections[splitter_name]['ai_textSplitter']
    if existing_connections and len(existing_connections) > 0:
        for conn_list in existing_connections:
            if any(c.get('node') == 'Auto Upsert to Pinecone' for c in conn_list):
                print(f"\n⚠️  Connessione già esistente!")
                return False

    # Aggiungi nuova connessione
    if not existing_connections or len(existing_connections) == 0:
        connections[splitter_name]['ai_textSplitter'] = [[new_connection]]
    else:
        connections[splitter_name]['ai_textSplitter'][0].append(new_connection)

    print(f"\n{'='*70}")
    print("✅ NUOVA CONNESSIONE AGGIUNTA")
    print(f"{'='*70}")
    print(f"Da: {splitter_name}")
    print(f"A: Auto Upsert to Pinecone")
    print(f"Tipo: ai_textSplitter")
    print(f"\nDettagli:")
    print(json.dumps(connections[splitter_name], indent=2))

    # Salva workflow modificato
    output_file = 'workflow_attivo_FIXED.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(workflow, f, ensure_ascii=False, indent=2)

    print(f"\n{'='*70}")
    print(f"💾 WORKFLOW SALVATO")
    print(f"{'='*70}")
    print(f"File: {output_file}")
    print(f"\n📝 Prossimi passi:")
    print(f"   1. Verificare il diff tra workflow originale e fixato")
    print(f"   2. Testare localmente (se possibile)")
    print(f"   3. Deploy su N8N via API o UI")
    print(f"   4. Triggerare workflow con file di test")
    print(f"   5. Verificare che vengano creati più chunk (15-20+)")

    return True

def deploy_to_n8n(workflow_file):
    """
    Deploy del workflow modificato su N8N via API
    """
    import requests

    API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIwMmRmNzQ5NC1hNjVjLTRjOTAtOTE5MC00NmViOWI4ODg5OGIiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzY4NTEyOTE5fQ.T-W7tlxC7dAA0dPHusS7yuZLpX-qAzuzYCUT653cC0k"
    BASE_URL = "https://emanueleserra.app.n8n.cloud/api/v1"

    with open(workflow_file, 'r') as f:
        workflow = json.load(f)

    workflow_id = workflow['id']

    print(f"\n{'='*70}")
    print("🚀 DEPLOY WORKFLOW SU N8N")
    print(f"{'='*70}")
    print(f"Workflow ID: {workflow_id}")
    print(f"Nome: {workflow['name']}")

    # Prepara payload (rimuovi campi read-only)
    deploy_data = {
        'name': workflow['name'],
        'nodes': workflow['nodes'],
        'connections': workflow['connections'],
        'settings': workflow.get('settings', {}),
        'staticData': workflow.get('staticData'),
        'tags': workflow.get('tags', [])
    }

    response = requests.put(
        f"{BASE_URL}/workflows/{workflow_id}",
        headers={
            "X-N8N-API-KEY": API_KEY,
            "Content-Type": "application/json"
        },
        json=deploy_data
    )

    if response.status_code in [200, 201]:
        print(f"\n✅ Deploy completato con successo!")
        print(f"   Status code: {response.status_code}")
        return True
    else:
        print(f"\n❌ Deploy fallito!")
        print(f"   Status code: {response.status_code}")
        print(f"   Response: {response.text[:500]}")
        return False

if __name__ == "__main__":
    workflow_file = "/home/user/Bloom-2.0/workflow_attivo.json"

    print("\n🔍 Step 1: Fix delle connessioni nel workflow")
    print("="*70)

    if not fix_workflow_connections(workflow_file):
        print("\n❌ Fix fallito")
        sys.exit(1)

    print("\n\n🚀 Step 2: Deploy su N8N")
    print("="*70)

    user_input = input("\n⚠️  Vuoi procedere con il deploy su N8N? (yes/no): ")

    if user_input.lower() in ['yes', 'y', 'si', 'sì']:
        if deploy_to_n8n("workflow_attivo_FIXED.json"):
            print("\n✅ TUTTO COMPLETATO!")
            print("\n📝 Prossimi passi:")
            print("   1. Pulire index: python3 clean_jobcourier_index.py")
            print("   2. Caricare file di test su Google Drive")
            print("   3. Triggerare workflow manualmente o attendere schedule")
            print("   4. Verificare chunks: python3 scripts/verify_rag_chunks.py")
        else:
            print("\n❌ Deploy fallito - controlla gli errori sopra")
            print("\n💡 Puoi anche deployare manualmente:")
            print("   1. Apri N8N UI")
            print("   2. Apri il workflow RAG")
            print("   3. Connetti 'Recursive Character Text Splitter1' a 'Auto Upsert to Pinecone'")
            print("   4. Salva il workflow")
    else:
        print("\n⏸️  Deploy saltato - puoi farlo manualmente più tardi")
        print(f"\n💡 Il workflow fixato è salvato in: workflow_attivo_FIXED.json")
        print("\n📝 Per deployare manualmente:")
        print("   1. Apri N8N UI: https://emanueleserra.app.n8n.cloud")
        print("   2. Apri il workflow RAG")
        print("   3. Connetti 'Recursive Character Text Splitter1' a 'Auto Upsert to Pinecone':")
        print("      - Drag from 'Recursive Character Text Splitter1' output")
        print("      - Drop to 'Auto Upsert to Pinecone' input (ai_textSplitter)")
        print("   4. Salva il workflow")
        print("\nOppure esegui di nuovo questo script e scegli 'yes' al prompt")
