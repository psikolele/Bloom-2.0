"""
Update Caption Flow V.2 workflow to add Respond to Webhook node
"""

import json
import requests
import uuid

# Configuration
N8N_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIwMmRmNzQ5NC1hNjVjLTRjOTAtOTE5MC00NmViOWI4ODg5OGIiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzY4NTEyOTE5fQ.T-W7tlxC7dAA0dPHusS7yuZLpX-qAzuzYCUT653cC0k"
N8N_BASE_URL = "https://emanueleserra.app.n8n.cloud/api/v1"
WORKFLOW_ID = "oRYSQ9tk63yPJaqt"

def get_workflow():
    """Fetch the current workflow"""
    response = requests.get(
        f"{N8N_BASE_URL}/workflows/{WORKFLOW_ID}",
        headers={"X-N8N-API-KEY": N8N_API_KEY}
    )
    response.raise_for_status()
    return response.json()

def update_workflow(workflow_data):
    """Update the workflow via API"""
    response = requests.put(
        f"{N8N_BASE_URL}/workflows/{WORKFLOW_ID}",
        headers={
            "X-N8N-API-KEY": N8N_API_KEY,
            "Content-Type": "application/json"
        },
        json=workflow_data
    )
    response.raise_for_status()
    return response.json()

def modify_workflow(workflow):
    """Modify the workflow to add Respond to Webhook functionality"""
    
    nodes = workflow.get("nodes", [])
    connections = workflow.get("connections", {})
    
    # 1. Find and modify the CaptionFlow Webhook node to use responseNode mode
    webhook_modified = False
    for node in nodes:
        if node.get("name") == "CaptionFlow Webhook":
            node["parameters"]["responseMode"] = "responseNode"
            webhook_modified = True
            print(f"✅ Modified webhook node to use responseNode mode")
            break
    
    if not webhook_modified:
        print("❌ Could not find CaptionFlow Webhook node!")
        return None
    
    # 2. Create the new "Respond to Frontend" node
    respond_node_id = str(uuid.uuid4())
    respond_node = {
        "parameters": {
            "options": {},
            "respondWith": "json",
            "responseBody": "={{ {\n  \"success\": true,\n  \"message\": \"Post generato con successo! Controlla la tua email per approvare.\",\n  \"data\": {\n    \"caption\": $('5. Prepare Data for Instagram API').item.json.Caption,\n    \"image_url\": $('Upload Image to Cloudinary').item.json.secure_url\n  }\n} }}"
        },
        "id": respond_node_id,
        "name": "Respond to Frontend",
        "type": "n8n-nodes-base.respondToWebhook",
        "typeVersion": 1.1,
        "position": [880, 1600]  # Position it between Cloudinary and Email
    }
    
    # 3. Add the new node to the nodes list
    nodes.append(respond_node)
    print(f"✅ Added 'Respond to Frontend' node with ID: {respond_node_id}")
    
    # 4. Update connections:
    # Current: Upload Image to Cloudinary -> Check via Email
    # New: Upload Image to Cloudinary -> Respond to Frontend -> Check via Email
    
    if "Upload Image to Cloudinary" in connections:
        cloudinary_connections = connections["Upload Image to Cloudinary"]
        if "main" in cloudinary_connections and len(cloudinary_connections["main"]) > 0:
            # Save the original next node (should be Check via Email)
            original_next = cloudinary_connections["main"][0].copy()
            
            # Point Cloudinary to Respond to Frontend
            connections["Upload Image to Cloudinary"]["main"] = [[
                {
                    "node": "Respond to Frontend",
                    "type": "main",
                    "index": 0
                }
            ]]
            print(f"✅ Updated connection: Upload Image to Cloudinary -> Respond to Frontend")
            
            # Point Respond to Frontend to the original next node (Check via Email)
            connections["Respond to Frontend"] = {
                "main": [original_next]
            }
            print(f"✅ Added connection: Respond to Frontend -> Check via Email")
    
    # Update the workflow object
    workflow["nodes"] = nodes
    workflow["connections"] = connections
    
    return workflow

def prepare_update_payload(workflow):
    """Prepare the payload for the API update (remove read-only fields)"""
    # Fields that can be updated - based on N8N API docs
    allowed_fields = ["name", "nodes", "connections", "settings"]
    
    payload = {k: v for k, v in workflow.items() if k in allowed_fields}
    
    # Clean up settings - only keep allowed settings fields
    if "settings" in payload and payload["settings"]:
        allowed_settings = ["executionOrder", "saveManualExecutions", "callerPolicy", "errorWorkflow"]
        payload["settings"] = {k: v for k, v in payload["settings"].items() if k in allowed_settings}
    
    return payload

def main():
    print("=" * 60)
    print("Updating Caption Flow V.2 Workflow")
    print("=" * 60)
    
    # Step 1: Fetch current workflow
    print("\n📥 Fetching current workflow...")
    try:
        workflow = get_workflow()
        print(f"   Workflow name: {workflow.get('name')}")
        print(f"   Nodes count: {len(workflow.get('nodes', []))}")
    except Exception as e:
        print(f"❌ Failed to fetch workflow: {e}")
        return
    
    # Step 2: Modify workflow
    print("\n🔧 Modifying workflow...")
    modified_workflow = modify_workflow(workflow)
    
    if not modified_workflow:
        print("❌ Workflow modification failed!")
        return
    
    # Step 3: Prepare update payload
    print("\n📦 Preparing update payload...")
    payload = prepare_update_payload(modified_workflow)
    print(f"   Payload fields: {list(payload.keys())}")
    print(f"   Updated nodes count: {len(payload.get('nodes', []))}")
    
    # Step 4: Update workflow via API
    print("\n📤 Updating workflow via API...")
    try:
        result = update_workflow(payload)
        print(f"✅ Workflow updated successfully!")
        print(f"   Version ID: {result.get('versionId', 'N/A')}")
    except requests.exceptions.HTTPError as e:
        print(f"❌ API Error: {e}")
        if e.response is not None:
            print(f"   Status: {e.response.status_code}")
            print(f"   Response: {e.response.text}")
        return
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return
    
    print("\n" + "=" * 60)
    print("✅ DONE! Workflow has been updated.")
    print("=" * 60)

if __name__ == "__main__":
    main()
