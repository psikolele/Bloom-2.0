#!/bin/bash
# Script bash per applicare il fix RAG a n8n
# Usa questo se non hai Python disponibile

set -e

N8N_API_KEY="n8n_api_8f8d3c6e1a5b7d9f2e4c6a8b0d2f4e6a8c0b2d4f6e8a0c2d4f6e8a0c2d4f6e8"
N8N_BASE_URL="https://n8n.bloom-ai.it/api/v1"
WORKFLOW_FILE="backup_workflows/RAG_workflow_FIXED_DATA_LOADER.json"

echo "======================================================================"
echo "APPLYING RAG WORKFLOW FIX TO N8N"
echo "======================================================================"

# Check if workflow file exists
if [ ! -f "$WORKFLOW_FILE" ]; then
    echo "❌ Error: Fixed workflow file not found: $WORKFLOW_FILE"
    echo "   Make sure you're running this from the project root directory"
    exit 1
fi

# 1. Find RAG workflow
echo ""
echo "📋 Step 1: Finding RAG workflow in n8n"
echo "----------------------------------------------------------------------"

workflows=$(curl -s -X GET "$N8N_BASE_URL/workflows" \
    -H "X-N8N-API-KEY: $N8N_API_KEY" \
    -H "Accept: application/json")

if [ $? -ne 0 ]; then
    echo "❌ Error: Could not connect to n8n"
    echo "   Make sure n8n.bloom-ai.it is reachable from this machine"
    exit 1
fi

# Extract workflow ID (basic grep, assumes workflow name contains 'RAG')
workflow_id=$(echo "$workflows" | grep -o '"id":"[^"]*"[^}]*"name":"[^"]*[Rr][Aa][Gg][^"]*"' | grep -o '"id":"[^"]*"' | head -1 | cut -d'"' -f4)

if [ -z "$workflow_id" ]; then
    echo "❌ Error: No RAG workflow found"
    echo "   Available workflows:"
    echo "$workflows" | grep -o '"name":"[^"]*"' | cut -d'"' -f4
    exit 1
fi

echo "✓ Found RAG workflow (ID: $workflow_id)"

# 2. Backup current workflow
echo ""
echo "📥 Step 2: Backing up current workflow"
echo "----------------------------------------------------------------------"

backup_file="workflow_backup_${workflow_id}.json"

curl -s -X GET "$N8N_BASE_URL/workflows/$workflow_id" \
    -H "X-N8N-API-KEY: $N8N_API_KEY" \
    -H "Accept: application/json" \
    -o "$backup_file"

if [ $? -eq 0 ]; then
    echo "✓ Current workflow backed up to: $backup_file"
else
    echo "❌ Error: Could not backup current workflow"
    exit 1
fi

# 3. Prepare fixed workflow
echo ""
echo "🔧 Step 3: Preparing fixed workflow"
echo "----------------------------------------------------------------------"

# Read fixed workflow and update ID (using jq if available, otherwise sed)
if command -v jq &> /dev/null; then
    # Use jq for proper JSON manipulation
    fixed_workflow=$(jq --arg id "$workflow_id" '.id = $id' "$WORKFLOW_FILE")
else
    # Fallback to sed (less reliable but works)
    fixed_workflow=$(sed "s/\"id\":\"[^\"]*\"/\"id\":\"$workflow_id\"/" "$WORKFLOW_FILE")
fi

echo "✓ Fixed workflow prepared"

# 4. Confirm
echo ""
echo "⚠️  This will UPDATE the RAG workflow (ID: $workflow_id)"
echo ""
echo "Changes:"
echo "  1. Auto Data Loader: Added 'dataType: binary'"
echo "  2. Connection: Auto Download → Auto Data Loader → Pinecone"
echo ""
read -p "Continue? [y/N]: " -n 1 -r
echo

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "❌ Aborted by user"
    echo "   Backup saved at: $backup_file"
    exit 0
fi

# 5. Upload fixed workflow
echo ""
echo "🚀 Step 4: Uploading fixed workflow to n8n"
echo "----------------------------------------------------------------------"

response=$(curl -s -w "\n%{http_code}" -X PATCH "$N8N_BASE_URL/workflows/$workflow_id" \
    -H "X-N8N-API-KEY: $N8N_API_KEY" \
    -H "Content-Type: application/json" \
    -d "$fixed_workflow")

http_code=$(echo "$response" | tail -n1)
body=$(echo "$response" | sed '$d')

if [ "$http_code" = "200" ] || [ "$http_code" = "201" ]; then
    echo "✅ Workflow updated successfully!"
else
    echo "❌ Failed to update workflow: HTTP $http_code"
    echo "$body"
    echo ""
    echo "Your backup is safe at: $backup_file"
    exit 1
fi

# 6. Summary
echo ""
echo "======================================================================"
echo "✅ FIX APPLIED SUCCESSFULLY!"
echo "======================================================================"
echo ""
echo "📄 Backup: $backup_file"
echo ""
echo "🔄 NEXT STEPS:"
echo "  1. Re-trigger the workflow:"
echo "     curl -X POST https://n8n.bloom-ai.it/webhook/manual-ingest-trigger-fix"
echo ""
echo "  2. Wait 2-3 minutes for indexing"
echo ""
echo "  3. Verify chunks:"
echo "     python3 scripts/verify_rag_chunks.py"
echo ""
echo "  4. Test the chat"
echo ""
echo "======================================================================"
