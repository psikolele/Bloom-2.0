#!/usr/bin/env python3
"""
Script per applicare automaticamente il fix RAG a n8n.
Esegui questo script da un computer che può raggiungere n8n.bloom-ai.it
"""

import requests
import json
import sys
from pathlib import Path

# Configurazione
N8N_API_KEY = "n8n_api_8f8d3c6e1a5b7d9f2e4c6a8b0d2f4e6a8c0b2d4f6e8a0c2d4f6e8a0c2d4f6e8"
N8N_BASE_URL = "https://n8n.bloom-ai.it/api/v1"
WORKFLOW_FILE = "backup_workflows/RAG_workflow_FIXED_DATA_LOADER.json"

def main():
    print("="*70)
    print("APPLYING RAG WORKFLOW FIX TO N8N")
    print("="*70)

    # 1. Find RAG workflow
    print("\n📋 Step 1: Finding RAG workflow in n8n")
    print("-"*70)

    try:
        resp = requests.get(
            f"{N8N_BASE_URL}/workflows",
            headers={"X-N8N-API-KEY": N8N_API_KEY},
            timeout=30
        )
        resp.raise_for_status()

        workflows = resp.json().get('data', [])
        print(f"✓ Found {len(workflows)} workflows")

        # Find RAG workflow
        rag_workflow = None
        for wf in workflows:
            name = wf.get('name', '').lower()
            if 'rag' in name:
                print(f"  Found RAG workflow: {wf['name']} (ID: {wf['id']})")
                rag_workflow = wf
                break

        if not rag_workflow:
            print("\n❌ No RAG workflow found!")
            print("Available workflows:")
            for wf in workflows[:10]:
                print(f"  - {wf['name']} (ID: {wf['id']})")
            sys.exit(1)

        workflow_id = rag_workflow['id']
        workflow_name = rag_workflow['name']

    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to n8n: {e}")
        print("\nMake sure:")
        print("  1. n8n.bloom-ai.it is reachable from this machine")
        print("  2. The API key is correct")
        print("  3. You have network access to n8n")
        sys.exit(1)

    # 2. Download current workflow (backup)
    print(f"\n📥 Step 2: Backing up current workflow")
    print("-"*70)

    resp = requests.get(
        f"{N8N_BASE_URL}/workflows/{workflow_id}",
        headers={"X-N8N-API-KEY": N8N_API_KEY},
        timeout=30
    )
    resp.raise_for_status()

    current_workflow = resp.json().get('data', resp.json())

    # Save backup
    backup_file = f"workflow_backup_{workflow_id}.json"
    with open(backup_file, 'w') as f:
        json.dump(current_workflow, f, indent=2)

    print(f"✓ Current workflow backed up to: {backup_file}")
    print(f"  Name: {workflow_name}")
    print(f"  ID: {workflow_id}")
    print(f"  Nodes: {len(current_workflow.get('nodes', []))}")
    print(f"  Active: {current_workflow.get('active', False)}")

    # 3. Load fixed workflow
    print(f"\n📂 Step 3: Loading fixed workflow")
    print("-"*70)

    workflow_path = Path(WORKFLOW_FILE)
    if not workflow_path.exists():
        print(f"❌ Fixed workflow file not found: {WORKFLOW_FILE}")
        print("Make sure you're running this from the project root directory")
        sys.exit(1)

    with open(workflow_path, 'r') as f:
        fixed_workflow = json.load(f)

    print(f"✓ Loaded fixed workflow from: {WORKFLOW_FILE}")
    print(f"  Nodes in fixed workflow: {len(fixed_workflow.get('nodes', []))}")

    # 4. Merge configurations
    print(f"\n🔧 Step 4: Merging configurations")
    print("-"*70)

    # Preserve important properties from current workflow
    fixed_workflow['id'] = workflow_id
    fixed_workflow['name'] = workflow_name
    fixed_workflow['active'] = current_workflow.get('active', False)

    # Preserve timestamps if they exist
    if 'createdAt' in current_workflow:
        fixed_workflow['createdAt'] = current_workflow['createdAt']
    if 'updatedAt' in current_workflow:
        fixed_workflow['updatedAt'] = current_workflow['updatedAt']

    # Preserve settings (credentials, etc.)
    if 'settings' in current_workflow:
        fixed_workflow['settings'] = current_workflow['settings']

    print(f"✓ Preserved workflow metadata:")
    print(f"  ID: {workflow_id}")
    print(f"  Name: {workflow_name}")
    print(f"  Active: {fixed_workflow['active']}")

    # 5. Show what will be changed
    print(f"\n📊 Step 5: Changes to be applied")
    print("-"*70)

    print("\n🔧 MODIFICATIONS:")
    print("  1. Auto Data Loader: Added 'dataType: binary'")
    print("  2. Connection changed: Auto Download → Auto Data Loader (instead of direct to Pinecone)")
    print("  3. Flow: Download → Data Loader → Splitter → Pinecone")

    # Ask for confirmation
    print(f"\n⚠️  This will UPDATE workflow '{workflow_name}' (ID: {workflow_id})")
    response = input("Continue? [y/N]: ")

    if response.lower() not in ['y', 'yes']:
        print("\n❌ Aborted by user")
        print(f"   Backup saved at: {backup_file}")
        sys.exit(0)

    # 6. Upload fixed workflow
    print(f"\n🚀 Step 6: Uploading fixed workflow to n8n")
    print("-"*70)

    resp = requests.patch(
        f"{N8N_BASE_URL}/workflows/{workflow_id}",
        headers={
            "X-N8N-API-KEY": N8N_API_KEY,
            "Content-Type": "application/json"
        },
        json=fixed_workflow,
        timeout=60
    )

    if resp.status_code not in [200, 201]:
        print(f"❌ Failed to update workflow: HTTP {resp.status_code}")
        print(resp.text)
        print(f"\nYour backup is safe at: {backup_file}")
        sys.exit(1)

    updated = resp.json().get('data', resp.json())

    print(f"✅ Workflow updated successfully!")
    print(f"   Name: {updated.get('name')}")
    print(f"   ID: {updated.get('id')}")
    print(f"   Nodes: {len(updated.get('nodes', []))}")

    # 7. Summary
    print("\n" + "="*70)
    print("✅ FIX APPLIED SUCCESSFULLY!")
    print("="*70)

    print(f"\n📄 Backup: {backup_file}")

    print("\n🔄 NEXT STEPS:")
    print("  1. Re-trigger the workflow to re-index documents:")
    print(f"     curl -X POST https://n8n.bloom-ai.it/webhook/manual-ingest-trigger-fix")
    print("\n  2. Wait 2-3 minutes for indexing to complete")
    print("\n  3. Verify chunks are correct:")
    print("     python3 scripts/verify_rag_chunks.py")
    print("\n  4. Test the chat with a question about Pessina courses")

    print("\n" + "="*70)


if __name__ == "__main__":
    main()
