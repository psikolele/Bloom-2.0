#!/usr/bin/env python3
"""
Script standalone per applicare il fix RAG.
Non richiede file esterni - tutto è embedded.

USAGE:
  python3 apply_fix_standalone.py

Puoi copiare questo script ovunque sul tuo computer ed eseguirlo.
"""

import requests
import json
import sys

# Configurazione
N8N_API_KEY = "n8n_api_8f8d3c6e1a5b7d9f2e4c6a8b0d2f4e6a8c0b2d4f6e8a0c2d4f6e8a0c2d4f6e8"
N8N_BASE_URL = "https://n8n.bloom-ai.it/api/v1"

# Le modifiche da applicare (embedded)
FIX_MODIFICATIONS = {
    "auto_data_loader": {
        "add_parameter": {
            "dataType": "binary"
        }
    },
    "connections": {
        "change": {
            "from": "Auto Download New File -> Auto Upsert to Pinecone",
            "to": "Auto Download New File -> Auto Data Loader -> Auto Upsert to Pinecone"
        }
    }
}

def main():
    print("="*70)
    print("RAG FIX - STANDALONE SCRIPT")
    print("="*70)

    # 1. Find workflow
    print("\n📋 Step 1: Finding RAG workflow")
    print("-"*70)

    try:
        resp = requests.get(
            f"{N8N_BASE_URL}/workflows",
            headers={"X-N8N-API-KEY": N8N_API_KEY},
            timeout=30
        )
        resp.raise_for_status()
    except Exception as e:
        print(f"❌ Cannot connect to n8n: {e}")
        print("\nMake sure:")
        print("  - n8n.bloom-ai.it is reachable")
        print("  - You have internet connection")
        sys.exit(1)

    workflows = resp.json().get('data', [])

    # Find RAG workflow
    rag_wf = None
    for wf in workflows:
        if 'rag' in wf.get('name', '').lower():
            rag_wf = wf
            print(f"✓ Found: {wf['name']} (ID: {wf['id']})")
            break

    if not rag_wf:
        print("❌ No RAG workflow found")
        sys.exit(1)

    wf_id = rag_wf['id']

    # 2. Download current workflow
    print("\n📥 Step 2: Downloading current workflow")
    print("-"*70)

    resp = requests.get(
        f"{N8N_BASE_URL}/workflows/{wf_id}",
        headers={"X-N8N-API-KEY": N8N_API_KEY},
        timeout=30
    )
    resp.raise_for_status()

    workflow = resp.json().get('data', resp.json())

    # Backup
    backup_file = f"workflow_backup_{wf_id}.json"
    with open(backup_file, 'w') as f:
        json.dump(workflow, f, indent=2)

    print(f"✓ Backup saved: {backup_file}")

    # 3. Apply fix
    print("\n🔧 Step 3: Applying fix")
    print("-"*70)

    # Fix 1: Add dataType to Auto Data Loader
    for node in workflow.get('nodes', []):
        if node.get('name') == 'Auto Data Loader':
            if 'parameters' not in node:
                node['parameters'] = {}
            node['parameters']['dataType'] = 'binary'
            print("✓ Modified Auto Data Loader: added dataType=binary")

    # Fix 2: Change connections
    connections = workflow.get('connections', {})

    if 'Auto Download New File' in connections:
        for output_type, conns in connections['Auto Download New File'].items():
            for conn_list in conns:
                for conn in conn_list:
                    if conn.get('node') == 'Auto Upsert to Pinecone':
                        conn['node'] = 'Auto Data Loader'
                        print("✓ Changed connection: Auto Download -> Auto Data Loader")

    # 4. Confirm
    print("\n⚠️  Ready to update workflow")
    print(f"   Name: {workflow.get('name')}")
    print(f"   ID: {wf_id}")
    print("\nChanges:")
    print("  1. Auto Data Loader: dataType = binary")
    print("  2. Connection: Download -> Data Loader -> Pinecone")

    response = input("\nContinue? [y/N]: ")

    if response.lower() not in ['y', 'yes']:
        print("\n❌ Aborted")
        print(f"   Backup at: {backup_file}")
        sys.exit(0)

    # 5. Upload
    print("\n🚀 Step 4: Uploading fixed workflow")
    print("-"*70)

    resp = requests.patch(
        f"{N8N_BASE_URL}/workflows/{wf_id}",
        headers={
            "X-N8N-API-KEY": N8N_API_KEY,
            "Content-Type": "application/json"
        },
        json=workflow,
        timeout=60
    )

    if resp.status_code not in [200, 201]:
        print(f"❌ Failed: HTTP {resp.status_code}")
        print(resp.text)
        sys.exit(1)

    print("✅ Success!")

    # 6. Next steps
    print("\n" + "="*70)
    print("✅ FIX APPLIED!")
    print("="*70)
    print("\n📄 Backup:", backup_file)
    print("\n🔄 NEXT STEPS:")
    print("\n1. Re-trigger workflow:")
    print("   curl -X POST https://n8n.bloom-ai.it/webhook/manual-ingest-trigger-fix")
    print("\n2. Wait 2-3 minutes")
    print("\n3. Test the chat with: 'Quali corsi offre il Pessina?'")
    print("\n" + "="*70)


if __name__ == "__main__":
    main()
