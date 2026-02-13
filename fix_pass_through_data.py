#!/usr/bin/env python3
"""
Fix the Pass Through Data node in the RAG workflow
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
    print("🔧 FIXING PASS THROUGH DATA NODE")
    print("=" * 70)

    # Load current workflow
    with open('/tmp/current_workflow.json', 'r') as f:
        workflow = json.load(f)

    print(f"📄 Workflow: {workflow['name']}")
    print(f"🆔 ID: {workflow['id']}")

    # Find and fix the Pass Through Data node
    fixed = False
    for node in workflow['nodes']:
        if node['name'] == 'Pass Through Data':
            print(f"\n🎯 Found node: {node['name']} (ID: {node['id']})")
            print("📝 Current code:")
            print(node['parameters']['jsCode'])
            print()

            # New fixed code
            new_code = """// Always return data, even if input is empty
const items = $input.all();

if (items.length === 0) {
  // Return a single item with isEmpty flag
  return [{ json: { isEmpty: true, checkedAt: new Date().toISOString() } }];
}

// FIX: Add isEmpty: false to each item so Check If Files Found node works correctly
return items.map(item => ({
  ...item,
  json: {
    ...item.json,
    isEmpty: false
  }
}));"""

            node['parameters']['jsCode'] = new_code
            fixed = True

            print("✅ Updated code:")
            print(new_code)
            print()
            break

    if not fixed:
        print("❌ Pass Through Data node not found!")
        return

    # Save backup
    backup_file = 'backup_workflows/RAG_workflow_BEFORE_FIX_PASS_THROUGH.json'
    with open(backup_file, 'w') as f:
        json.dump(workflow, f, indent=2)
    print(f"💾 Backup saved: {backup_file}")

    # Update workflow via API
    print("\n🚀 Updating workflow via API...")

    headers = {
        "X-N8N-API-KEY": api_key,
        "Content-Type": "application/json"
    }

    # Prepare payload (minimal required fields)
    payload = {
        "name": workflow['name'],
        "nodes": workflow['nodes'],
        "connections": workflow['connections'],
        "settings": {
            "executionOrder": workflow.get('settings', {}).get('executionOrder', 'v1')
        }
    }

    response = requests.put(
        f"{base_url}/workflows/{workflow_id}",
        headers=headers,
        json=payload
    )

    if response.status_code == 200:
        print("✅ Workflow updated successfully!")
        print("\n" + "=" * 70)
        print("✅ FIX APPLIED")
        print("=" * 70)
        print("\n📋 What was fixed:")
        print("  • Pass Through Data node now sets isEmpty: false for items")
        print("  • Check If Files Found will now correctly route to false branch")
        print("  • No more getting stuck at Auto Determine Index\n")
    else:
        print(f"❌ Failed to update workflow: {response.status_code}")
        print(f"Response: {response.text}")

if __name__ == "__main__":
    main()
