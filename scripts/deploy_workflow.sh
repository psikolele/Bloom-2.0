#!/usr/bin/env bash
# =============================================================================
# deploy_workflow.sh — Deploy N8N workflow to cloud instance
# =============================================================================
#
# Pushes the Caption_Flow_V3_VIDEO_MOD.json workflow to the N8N cloud instance
# using the N8N REST API (PUT /api/v1/workflows/{id}).
#
# USAGE:
#   ./scripts/deploy_workflow.sh                      # uses defaults
#   ./scripts/deploy_workflow.sh --dry-run             # show payload, don't send
#   N8N_API_KEY="your-key" ./scripts/deploy_workflow.sh
#
# CONFIGURATION (in order of precedence):
#   1. Environment variable  N8N_API_KEY
#   2. .env file in project root (same directory as .env.example)
#
# REQUIREMENTS:
#   - bash 4+, curl, python3 (for JSON processing)
#
# =============================================================================

set -euo pipefail

# ---------------------------------------------------------------------------
# Resolve project root (parent of scripts/)
# ---------------------------------------------------------------------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
N8N_BASE_URL="https://emanueleserra.app.n8n.cloud/api/v1"
WORKFLOW_ID="oRYSQ9tk63yPJaqt"
WORKFLOW_FILE="$PROJECT_ROOT/backup_workflows/Caption_Flow_V3_VIDEO_MOD.json"
DRY_RUN=false

# ---------------------------------------------------------------------------
# Color helpers (disabled when not a terminal)
# ---------------------------------------------------------------------------
if [ -t 1 ]; then
    RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
    CYAN='\033[0;36m'; NC='\033[0m'
else
    RED=''; GREEN=''; YELLOW=''; CYAN=''; NC=''
fi

info()  { echo -e "${CYAN}[INFO]${NC}  $*"; }
ok()    { echo -e "${GREEN}[OK]${NC}    $*"; }
warn()  { echo -e "${YELLOW}[WARN]${NC}  $*"; }
err()   { echo -e "${RED}[ERROR]${NC} $*" >&2; }

# ---------------------------------------------------------------------------
# Parse arguments
# ---------------------------------------------------------------------------
for arg in "$@"; do
    case "$arg" in
        --dry-run)  DRY_RUN=true ;;
        --help|-h)
            echo "Usage: $0 [--dry-run] [--help]"
            echo ""
            echo "Deploy Caption_Flow_V3_VIDEO_MOD.json to N8N cloud."
            echo ""
            echo "Options:"
            echo "  --dry-run   Build the payload and print it, but do not send."
            echo "  --help      Show this help message."
            exit 0
            ;;
        *)
            err "Unknown argument: $arg"
            exit 1
            ;;
    esac
done

# ---------------------------------------------------------------------------
# Load .env if N8N_API_KEY is not already set
# ---------------------------------------------------------------------------
if [ -z "${N8N_API_KEY:-}" ]; then
    ENV_FILE="$PROJECT_ROOT/.env"
    if [ -f "$ENV_FILE" ]; then
        info "Loading API key from $ENV_FILE"
        # Source only N8N_API_KEY to avoid polluting the environment
        N8N_API_KEY="$(grep -E '^N8N_API_KEY=' "$ENV_FILE" | head -1 | cut -d'=' -f2-)"
        N8N_API_KEY="${N8N_API_KEY//\"/}"   # strip quotes if present
        N8N_API_KEY="${N8N_API_KEY//\'/}"
    fi
fi

if [ -z "${N8N_API_KEY:-}" ]; then
    err "N8N_API_KEY is not set."
    err "Set it as an environment variable or add it to $PROJECT_ROOT/.env"
    err "See .env.example for the expected format."
    exit 1
fi

ok "N8N_API_KEY loaded (${#N8N_API_KEY} chars)"

# ---------------------------------------------------------------------------
# Validate workflow file exists
# ---------------------------------------------------------------------------
if [ ! -f "$WORKFLOW_FILE" ]; then
    err "Workflow file not found: $WORKFLOW_FILE"
    exit 1
fi

ok "Workflow file found: $WORKFLOW_FILE"

# ---------------------------------------------------------------------------
# Build the API payload using python3 for reliable JSON manipulation
# ---------------------------------------------------------------------------
info "Building API payload..."

export WORKFLOW_FILE
PAYLOAD=$(python3 << 'PYEOF'
import json, sys, os

workflow_path = os.environ.get("WORKFLOW_FILE")

try:
    with open(workflow_path, "r", encoding="utf-8") as f:
        wf = json.load(f)
except Exception as e:
    print(f"ERROR: Failed to parse workflow JSON: {e}", file=sys.stderr)
    sys.exit(1)

# Build the payload that N8N API expects for PUT /workflows/{id}
# Keys accepted by the N8N PUT /workflows/{id} API
ALLOWED = {
    "callerPolicy", "errorWorkflow", "executionOrder",
    "saveDataErrorExecution", "saveDataSuccessExecution",
    "saveExecutionProgress", "saveManualExecutions", "timezone",
}

raw_settings = wf.get("settings", {})
settings = {k: v for k, v in raw_settings.items() if k in ALLOWED}

# Merge in safe defaults for settings
defaults = {
    "saveDataErrorExecution": "all",
    "saveDataSuccessExecution": "all",
    "saveExecutionProgress": True,
    "saveManualExecutions": True,
    "timezone": "Europe/Rome",
}
for k, v in defaults.items():
    settings.setdefault(k, v)

payload = {
    "name": wf.get("name", "Caption Flow V.2"),
    "nodes": wf.get("nodes", []),
    "connections": wf.get("connections", {}),
    "settings": settings,
    "staticData": wf.get("staticData", None),
}

print(json.dumps(payload))
PYEOF
)

if [ $? -ne 0 ] || [ -z "$PAYLOAD" ]; then
    err "Failed to build payload from workflow file."
    exit 1
fi

NODE_COUNT=$(echo "$PAYLOAD" | python3 -c "import json,sys; print(len(json.load(sys.stdin).get('nodes',[])))")
WORKFLOW_NAME=$(echo "$PAYLOAD" | python3 -c "import json,sys; print(json.load(sys.stdin).get('name','unknown'))")

ok "Payload built: workflow=\"$WORKFLOW_NAME\", nodes=$NODE_COUNT"

# ---------------------------------------------------------------------------
# Dry-run: print and exit
# ---------------------------------------------------------------------------
if [ "$DRY_RUN" = true ]; then
    warn "DRY RUN -- not sending to N8N. Payload preview:"
    echo "$PAYLOAD" | python3 -m json.tool 2>/dev/null | head -60 || true
    echo "  ... (truncated)"
    info "Target: PUT $N8N_BASE_URL/workflows/$WORKFLOW_ID"
    exit 0
fi

# ---------------------------------------------------------------------------
# Send to N8N via curl
# ---------------------------------------------------------------------------
API_URL="$N8N_BASE_URL/workflows/$WORKFLOW_ID"
info "Deploying to $API_URL ..."

# Write payload to a temp file to avoid argument-length limits
TMPFILE=$(mktemp /tmp/n8n_deploy_XXXXXX.json)
trap "rm -f '$TMPFILE'" EXIT
echo "$PAYLOAD" > "$TMPFILE"

HTTP_RESPONSE=$(curl --silent --write-out "\n%{http_code}" \
    --request PUT \
    --url "$API_URL" \
    --header "Content-Type: application/json" \
    --header "X-N8N-API-KEY: $N8N_API_KEY" \
    --data-binary "@$TMPFILE" \
    --max-time 30 \
    2>&1) || true

# Split response body and status code
HTTP_BODY=$(echo "$HTTP_RESPONSE" | sed '$d')
HTTP_CODE=$(echo "$HTTP_RESPONSE" | tail -1)

# ---------------------------------------------------------------------------
# Handle response
# ---------------------------------------------------------------------------
case "$HTTP_CODE" in
    200)
        ok "Workflow deployed successfully! (HTTP $HTTP_CODE)"
        RESP_NAME=$(echo "$HTTP_BODY" | python3 -c "import json,sys; print(json.load(sys.stdin).get('name',''))" 2>/dev/null || echo "")
        RESP_ID=$(echo "$HTTP_BODY" | python3 -c "import json,sys; print(json.load(sys.stdin).get('id',''))" 2>/dev/null || echo "")
        if [ -n "$RESP_NAME" ]; then
            info "  Name: $RESP_NAME"
            info "  ID:   $RESP_ID"
        fi
        ;;
    401)
        err "Authentication failed (HTTP 401). Check your N8N_API_KEY."
        err "Response: $HTTP_BODY"
        exit 1
        ;;
    403)
        err "Forbidden (HTTP 403). The API key may lack write permissions."
        err "Response: $HTTP_BODY"
        exit 1
        ;;
    404)
        err "Workflow not found (HTTP 404). Check WORKFLOW_ID=$WORKFLOW_ID"
        err "Response: $HTTP_BODY"
        exit 1
        ;;
    "")
        err "No response from server. Check network connectivity and URL."
        err "Target was: $API_URL"
        exit 1
        ;;
    *)
        err "Unexpected response (HTTP $HTTP_CODE)"
        err "Response: $HTTP_BODY"
        exit 1
        ;;
esac

info "Done."
