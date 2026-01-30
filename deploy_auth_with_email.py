#!/usr/bin/env python3
"""
Deploy Bloom AI Unified Auth Workflow with Email Support to N8N
This script updates the existing Unified Auth workflow to include welcome email functionality
"""

import json
import requests
import sys
import os
from pathlib import Path

# Configuration
WORKFLOW_PATH = "backup_workflows/Bloom_AI_Unified_Auth_WITH_EMAIL.json"
WORKFLOW_ID = "uYNin7KcptmBF8Nw"  # Existing Unified Auth workflow ID
CONFIG_PATH = os.path.expanduser("~/n8n_config.json")  # Adjust path as needed

def load_config():
    """Load N8N API configuration"""
    if not os.path.exists(CONFIG_PATH):
        print(f"⚠️  Config file not found at {CONFIG_PATH}")
        print("Creating a template config file...")

        template_config = {
            "api_key": "YOUR_N8N_API_KEY_HERE",
            "base_url": "https://emanueleserra.app.n8n.cloud/api/v1"
        }

        with open(CONFIG_PATH, 'w') as f:
            json.dump(template_config, f, indent=2)

        print(f"✅ Template created at {CONFIG_PATH}")
        print("Please edit the file with your N8N credentials and run again.")
        sys.exit(1)

    with open(CONFIG_PATH, 'r') as f:
        return json.load(f)

def load_workflow():
    """Load the workflow JSON file"""
    workflow_path = Path(WORKFLOW_PATH)

    if not workflow_path.exists():
        print(f"❌ Workflow file not found at {WORKFLOW_PATH}")
        sys.exit(1)

    try:
        with open(workflow_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in workflow file: {e}")
        sys.exit(1)

def deploy_workflow(config, workflow_data):
    """Deploy the workflow to N8N"""
    api_key = config.get('api_key')
    base_url = config.get('base_url', 'https://emanueleserra.app.n8n.cloud/api/v1')

    if not api_key or api_key == "YOUR_N8N_API_KEY_HERE":
        print("❌ Please set your N8N API key in the config file")
        sys.exit(1)

    url = f"{base_url}/workflows/{WORKFLOW_ID}"
    headers = {
        "X-N8N-API-KEY": api_key,
        "Content-Type": "application/json"
    }

    # Prepare payload
    payload = {
        "name": workflow_data.get("name", "Bloom AI Unified Auth (With Email)"),
        "nodes": workflow_data["nodes"],
        "connections": workflow_data["connections"],
        "settings": workflow_data.get("settings", {})
    }

    print(f"🚀 Deploying workflow to N8N...")
    print(f"   Workflow ID: {WORKFLOW_ID}")
    print(f"   Endpoint: {url}")

    try:
        response = requests.put(url, json=payload, headers=headers)

        if response.status_code == 200:
            print("✅ Workflow deployed successfully!")
            result = response.json()
            print(f"   Name: {result.get('name', 'N/A')}")
            print(f"   Active: {result.get('active', False)}")
            print(f"   Nodes: {len(result.get('nodes', []))}")
            return True
        else:
            print(f"❌ Deployment failed with status {response.status_code}")
            print(f"   Response: {response.text}")
            return False

    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")
        return False

def activate_workflow(config):
    """Activate the workflow after deployment"""
    api_key = config.get('api_key')
    base_url = config.get('base_url', 'https://emanueleserra.app.n8n.cloud/api/v1')

    url = f"{base_url}/workflows/{WORKFLOW_ID}/activate"
    headers = {
        "X-N8N-API-KEY": api_key,
        "Content-Type": "application/json"
    }

    print(f"🔌 Activating workflow...")

    try:
        response = requests.patch(url, json={"active": True}, headers=headers)

        if response.status_code == 200:
            print("✅ Workflow activated!")
            return True
        else:
            print(f"⚠️  Activation returned status {response.status_code}")
            print(f"   (Workflow may already be active)")
            return False

    except requests.exceptions.RequestException as e:
        print(f"⚠️  Could not activate: {e}")
        return False

def main():
    print("=" * 60)
    print("  Bloom AI - Deploy Unified Auth with Email Workflow")
    print("=" * 60)
    print()

    # Load configuration
    print("📋 Loading configuration...")
    config = load_config()
    print("✅ Config loaded")

    # Load workflow
    print("📦 Loading workflow file...")
    workflow_data = load_workflow()
    print(f"✅ Workflow loaded: {len(workflow_data.get('nodes', []))} nodes")

    # Deploy
    success = deploy_workflow(config, workflow_data)

    if success:
        # Activate
        activate_workflow(config)

        print()
        print("=" * 60)
        print("🎉 Deployment Complete!")
        print("=" * 60)
        print()
        print("⚠️  IMPORTANT: Configure SMTP Credentials in N8N")
        print("   1. Go to N8N Settings → Credentials")
        print("   2. Create a new 'SMTP' credential")
        print("   3. Configure with your email service:")
        print("      - SendGrid (recommended): smtp.sendgrid.net:587")
        print("      - Gmail: smtp.gmail.com:587")
        print("      - Custom SMTP server")
        print("   4. Update the 'Send Welcome Email' node to use your credential")
        print()
        print("📧 Email Template Features:")
        print("   ✓ HTML design with Bloom AI brand guidelines")
        print("   ✓ Username and email in summary (NO password)")
        print("   ✓ CTA button to dashboard")
        print("   ✓ Features preview")
        print()
        print(f"🔗 Webhook URL: https://emanueleserra.app.n8n.cloud/webhook/auth")
        print()
    else:
        print()
        print("=" * 60)
        print("❌ Deployment Failed")
        print("=" * 60)
        sys.exit(1)

if __name__ == "__main__":
    main()
