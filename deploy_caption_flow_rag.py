"""
Deploy Caption Flow V.2 with RAG Integration to N8N
"""

import json
import requests
import sys

# Configuration
N8N_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIwMmRmNzQ5NC1hNjVjLTRjOTAtOTE5MC00NmViOWI4ODg5OGIiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzY4NTEyOTE5fQ.T-W7tlxC7dAA0dPHusS7yuZLpX-qAzuzYCUT653cC0k"
N8N_BASE_URL = "https://emanueleserra.app.n8n.cloud/api/v1"
WORKFLOW_ID = "oRYSQ9tk63yPJaqt"
WORKFLOW_FILE = "backup_workflows/Caption_Flow_V2_oRYSQ9tk63yPJaqt_UPDATED.json"

def load_workflow_file():
    """Load the modified workflow JSON file"""
    print(f"📂 Loading workflow file: {WORKFLOW_FILE}")
    try:
        with open(WORKFLOW_FILE, 'r', encoding='utf-8-sig') as f:
            workflow_data = json.load(f)
        print(f"   ✅ Loaded {len(workflow_data.get('nodes', []))} nodes")
        return workflow_data
    except Exception as e:
        print(f"   ❌ Error loading file: {e}")
        sys.exit(1)

def get_current_workflow():
    """Fetch the current workflow from N8N to verify"""
    print(f"\n🔍 Fetching current workflow from N8N...")
    try:
        response = requests.get(
            f"{N8N_BASE_URL}/workflows/{WORKFLOW_ID}",
            headers={"X-N8N-API-KEY": N8N_API_KEY}
        )
        response.raise_for_status()
        current = response.json()
        print(f"   ✅ Current workflow: {current.get('name')}")
        print(f"   ℹ️  Current nodes: {len(current.get('nodes', []))}")
        return current
    except Exception as e:
        print(f"   ❌ Error fetching workflow: {e}")
        sys.exit(1)

def prepare_update_payload(workflow_data):
    """Prepare the payload for N8N API update"""
    print(f"\n📦 Preparing update payload...")

    # N8N API accepts these fields for update
    allowed_fields = ["name", "nodes", "connections", "settings"]
    payload = {k: v for k, v in workflow_data.items() if k in allowed_fields}

    # Clean settings - only keep allowed fields
    if "settings" in payload and payload["settings"]:
        allowed_settings = ["executionOrder", "saveManualExecutions", "callerPolicy", "errorWorkflow"]
        payload["settings"] = {k: v for k, v in payload["settings"].items() if k in allowed_settings}

    print(f"   ✅ Payload prepared")
    print(f"   ℹ️  Fields: {list(payload.keys())}")
    print(f"   ℹ️  Nodes: {len(payload.get('nodes', []))}")
    print(f"   ℹ️  Connections: {len(payload.get('connections', {}))}")

    return payload

def update_workflow(payload):
    """Push the updated workflow to N8N"""
    print(f"\n🚀 Deploying to N8N...")

    try:
        response = requests.put(
            f"{N8N_BASE_URL}/workflows/{WORKFLOW_ID}",
            headers={
                "X-N8N-API-KEY": N8N_API_KEY,
                "Content-Type": "application/json"
            },
            json=payload
        )
        response.raise_for_status()
        result = response.json()

        print(f"   ✅ Deployment successful!")
        print(f"   ℹ️  Workflow: {result.get('name')}")
        print(f"   ℹ️  Version ID: {result.get('versionId', 'N/A')}")
        print(f"   ℹ️  Updated at: {result.get('updatedAt', 'N/A')}")

        return result

    except requests.exceptions.HTTPError as e:
        print(f"   ❌ HTTP Error: {e}")
        if e.response is not None:
            print(f"   Status: {e.response.status_code}")
            print(f"   Response: {e.response.text}")
        sys.exit(1)
    except Exception as e:
        print(f"   ❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

def verify_deployment():
    """Verify that RAG nodes are present in deployed workflow"""
    print(f"\n🔍 Verifying RAG nodes deployment...")

    try:
        response = requests.get(
            f"{N8N_BASE_URL}/workflows/{WORKFLOW_ID}",
            headers={"X-N8N-API-KEY": N8N_API_KEY}
        )
        response.raise_for_status()
        deployed = response.json()

        # Check for RAG nodes
        rag_nodes = [
            "Map Account to RAG DB",
            "Prepare Company Knowledge Query",
            "Query Company Knowledge",
            "Company Knowledge LLM",
            "Company Knowledge Vector Store",
            "Company Knowledge Embeddings",
            "Combine RAG with Input Data"
        ]

        deployed_nodes = [node.get('name') for node in deployed.get('nodes', [])]

        found_rag_nodes = [node for node in rag_nodes if node in deployed_nodes]
        missing_rag_nodes = [node for node in rag_nodes if node not in deployed_nodes]

        if missing_rag_nodes:
            print(f"   ⚠️  Warning: Some RAG nodes not found:")
            for node in missing_rag_nodes:
                print(f"      - {node}")
        else:
            print(f"   ✅ All {len(rag_nodes)} RAG nodes verified!")
            for node in found_rag_nodes:
                print(f"      ✓ {node}")

        return len(missing_rag_nodes) == 0

    except Exception as e:
        print(f"   ⚠️  Could not verify: {e}")
        return False

def main():
    print("=" * 70)
    print("🚀 DEPLOY CAPTION FLOW V.2 WITH RAG INTEGRATION")
    print("=" * 70)

    # Step 1: Load modified workflow file
    workflow_data = load_workflow_file()

    # Step 2: Get current workflow (for comparison)
    current_workflow = get_current_workflow()

    # Show diff
    current_node_count = len(current_workflow.get('nodes', []))
    new_node_count = len(workflow_data.get('nodes', []))
    diff = new_node_count - current_node_count

    print(f"\n📊 Changes Summary:")
    print(f"   Current nodes: {current_node_count}")
    print(f"   New nodes: {new_node_count}")
    print(f"   Difference: +{diff} nodes")

    # Step 3: Prepare payload
    payload = prepare_update_payload(workflow_data)

    # Step 4: Confirm deployment
    print(f"\n⚠️  READY TO DEPLOY")
    print(f"   This will update workflow: {WORKFLOW_ID}")
    print(f"   Target: {N8N_BASE_URL}")

    # Check for --yes flag for non-interactive mode
    auto_confirm = '--yes' in sys.argv or '-y' in sys.argv

    if not auto_confirm:
        try:
            confirm = input("\n   Proceed with deployment? (yes/no): ").strip().lower()
            if confirm not in ['yes', 'y']:
                print("\n❌ Deployment cancelled by user")
                sys.exit(0)
        except (KeyboardInterrupt, EOFError):
            print("\n\n❌ Deployment cancelled")
            sys.exit(0)
    else:
        print("\n   ✅ Auto-confirm enabled, proceeding...")

    # Step 5: Deploy
    result = update_workflow(payload)

    # Step 6: Verify
    verification_ok = verify_deployment()

    # Summary
    print("\n" + "=" * 70)
    if verification_ok:
        print("✅ DEPLOYMENT SUCCESSFUL - RAG INTEGRATION ACTIVE")
    else:
        print("⚠️  DEPLOYMENT COMPLETED - PLEASE VERIFY MANUALLY")
    print("=" * 70)
    print(f"\n🌐 N8N Workflow URL:")
    print(f"   https://emanueleserra.app.n8n.cloud/workflow/{WORKFLOW_ID}")
    print(f"\n📖 Documentation:")
    print(f"   CAPTION_FLOW_RAG_INTEGRATION.md")
    print("\n")

if __name__ == "__main__":
    main()
