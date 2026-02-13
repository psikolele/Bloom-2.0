#!/usr/bin/env python3
"""
Fix RAG workflow to use correct Pinecone namespace
Currently the workflow doesn't use namespaces, so all chunks are in the default '' namespace.
We need to configure the Pinecone nodes to use the correct namespace.
"""
import json
import os
import requests
from dotenv import load_dotenv

load_dotenv()

def main():
    api_key = os.getenv("N8N_API_KEY")
    workflow_id = "XmCaI5Q9MxNf0EP_65UvB"
    base_url = "https://emanueleserra.app.n8n.cloud/api/v1"

    print("=" * 70)
    print("🔧 FIXING RAG NAMESPACE CONFIGURATION")
    print("=" * 70)

    # Download current workflow
    headers = {
        "X-N8N-API-KEY": api_key,
        "Accept": "application/json"
    }

    response = requests.get(f"{base_url}/workflows/{workflow_id}", headers=headers)
    workflow = response.json()

    print(f"📄 Workflow: {workflow['name']}")
    print(f"🆔 ID: {workflow['id']}\n")

    # Find and fix the Pinecone nodes
    fixed_nodes = []

    for node in workflow['nodes']:
        if node['name'] == 'RAG Query Pinecone':
            print(f"🎯 Found: {node['name']}")
            print(f"   Current options: {node['parameters'].get('options', {})}")

            # Add namespace option to use default namespace ''
            # This matches where the chunks actually are
            node['parameters']['options'] = {
                "pineconeNamespace": ""
            }

            print(f"   ✅ Updated options: {node['parameters']['options']}")
            fixed_nodes.append(node['name'])

        elif node['name'] == 'Auto Upsert to Pinecone':
            print(f"🎯 Found: {node['name']}")
            print(f"   Current options: {node['parameters'].get('options', {})}")

            # Keep using default namespace '' for consistency
            node['parameters']['options'] = {
                "pineconeNamespace": ""
            }

            print(f"   ✅ Updated options: {node['parameters']['options']}")
            fixed_nodes.append(node['name'])

    if not fixed_nodes:
        print("❌ No Pinecone nodes found to fix!")
        return

    print(f"\n📋 Fixed {len(fixed_nodes)} nodes:")
    for name in fixed_nodes:
        print(f"   • {name}")

    # Save backup
    backup_file = 'backup_workflows/RAG_workflow_BEFORE_NAMESPACE_FIX.json'
    with open(backup_file, 'w') as f:
        json.dump(workflow, f, indent=2)
    print(f"\n💾 Backup saved: {backup_file}")

    # Update workflow
    print("\n🚀 Updating workflow...")

    payload = {
        "name": workflow['name'],
        "nodes": workflow['nodes'],
        "connections": workflow['connections'],
        "settings": {
            "executionOrder": workflow.get('settings', {}).get('executionOrder', 'v1')
        }
    }

    headers['Content-Type'] = 'application/json'
    response = requests.put(
        f"{base_url}/workflows/{workflow_id}",
        headers=headers,
        json=payload
    )

    if response.status_code == 200:
        print("✅ Workflow updated successfully!")
        print("\n" + "=" * 70)
        print("✅ NAMESPACE FIX APPLIED")
        print("=" * 70)
        print("\n📋 What was fixed:")
        print("  • RAG Query Pinecone now uses default namespace ''")
        print("  • Auto Upsert to Pinecone configured to use default namespace ''")
        print("  • RAG queries will now find chunks in the default namespace")
        print("\n🎯 Next steps:")
        print("  • Upload organigramma-pessina.md to Google Drive folder")
        print("  • Trigger workflow to index it")
        print("  • Test RAG query: 'chi è il dirigente del pessina?'\n")
    else:
        print(f"❌ Failed: {response.status_code}")
        print(f"Response: {response.text}")

if __name__ == "__main__":
    main()
