"""
Fix embedding-001 deprecation in n8n workflows.
Google has deprecated embedding-001 - replace with text-embedding-004.

Usage:
  python fix_embedding_model.py --analyze    # Step 1: Fetch, backup, and analyze (read-only)
  python fix_embedding_model.py --fix        # Step 2: Apply fix and push to n8n
"""

import json
import requests
import sys
import os
from datetime import datetime

# ── Configuration ──────────────────────────────────────────────
N8N_API_KEY = os.environ.get("N8N_API_KEY", "")
N8N_BASE_URL = "https://emanueleserra.app.n8n.cloud/api/v1"
BACKUP_DIR = os.path.join(os.path.dirname(__file__), "backup_workflows")

OLD_MODEL = "embedding-001"
NEW_MODEL = "text-embedding-004"

WORKFLOWS = {
    "7KzNvq6NjRbyQ0j9": "Brand Profile V2 (FIXED)",
    "oRYSQ9tk63yPJaqt": "Caption Flow V.2",
}

TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M")


# ── API Helpers ────────────────────────────────────────────────
def fetch_workflow(workflow_id):
    """Fetch a workflow from n8n API."""
    response = requests.get(
        f"{N8N_BASE_URL}/workflows/{workflow_id}",
        headers={"X-N8N-API-KEY": N8N_API_KEY},
        timeout=30
    )
    response.raise_for_status()
    return response.json()


def push_workflow(workflow_id, payload):
    """Push updated workflow to n8n API."""
    response = requests.put(
        f"{N8N_BASE_URL}/workflows/{workflow_id}",
        headers={
            "X-N8N-API-KEY": N8N_API_KEY,
            "Content-Type": "application/json"
        },
        json=payload,
        timeout=30
    )
    response.raise_for_status()
    return response.json()


def prepare_payload(workflow):
    """Prepare update payload (remove read-only fields)."""
    allowed_fields = ["name", "nodes", "connections", "settings"]
    payload = {k: v for k, v in workflow.items() if k in allowed_fields}
    if "settings" in payload and payload["settings"]:
        allowed_settings = ["executionOrder", "saveManualExecutions", "callerPolicy", "errorWorkflow"]
        payload["settings"] = {k: v for k, v in payload["settings"].items() if k in allowed_settings}
    return payload


# ── Deep Search ────────────────────────────────────────────────
def find_embedding_refs(obj, path=""):
    """Recursively search for embedding-001 in any nested structure."""
    matches = []
    if isinstance(obj, dict):
        for key, value in obj.items():
            current_path = f"{path}.{key}" if path else key
            if isinstance(value, str) and OLD_MODEL in value:
                matches.append({"path": current_path, "value": value})
            else:
                matches.extend(find_embedding_refs(value, current_path))
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            matches.extend(find_embedding_refs(item, f"{path}[{i}]"))
    elif isinstance(obj, str) and OLD_MODEL in obj:
        matches.append({"path": path, "value": obj})
    return matches


def replace_embedding_refs(obj):
    """Recursively replace embedding-001 with text-embedding-004."""
    count = 0
    if isinstance(obj, dict):
        for key in obj:
            if isinstance(obj[key], str) and OLD_MODEL in obj[key]:
                obj[key] = obj[key].replace(OLD_MODEL, NEW_MODEL)
                count += 1
            elif isinstance(obj[key], (dict, list)):
                count += replace_embedding_refs(obj[key])
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            if isinstance(item, str) and OLD_MODEL in item:
                obj[i] = item.replace(OLD_MODEL, NEW_MODEL)
                count += 1
            elif isinstance(item, (dict, list)):
                count += replace_embedding_refs(item)
    return count


# ── Save Backup ────────────────────────────────────────────────
def save_backup(workflow, label):
    """Save workflow JSON as a backup file."""
    os.makedirs(BACKUP_DIR, exist_ok=True)
    safe_label = label.replace(" ", "_").replace("(", "").replace(")", "")
    filename = f"{safe_label}_BACKUP_{TIMESTAMP}.json"
    filepath = os.path.join(BACKUP_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(workflow, f, indent=2, ensure_ascii=False)
    return filepath


# ── Phase 1: Analyze ──────────────────────────────────────────
def analyze():
    """Fetch workflows, save backups, and report embedding-001 usage."""
    print("=" * 65)
    print(f"  ANALISI EMBEDDING MODEL - {OLD_MODEL}")
    print("=" * 65)

    all_matches = {}

    for wf_id, wf_name in WORKFLOWS.items():
        print(f"\n{'─' * 65}")
        print(f"  Workflow: {wf_name} ({wf_id})")
        print(f"{'─' * 65}")

        # Fetch
        print(f"  Fetching da n8n API...")
        try:
            workflow = fetch_workflow(wf_id)
        except requests.exceptions.HTTPError as e:
            print(f"  ERRORE: Impossibile scaricare ({e})")
            if e.response is not None:
                print(f"  Status: {e.response.status_code} - {e.response.text[:200]}")
            continue
        except Exception as e:
            print(f"  ERRORE: {e}")
            continue

        nodes = workflow.get("nodes", [])
        print(f"  Scaricato! Nodi totali: {len(nodes)}")

        # Backup
        backup_path = save_backup(workflow, wf_name)
        print(f"  Backup salvato: {backup_path}")

        # List all node types for visibility
        print(f"\n  Tutti i nodi del workflow:")
        for node in nodes:
            node_type = node.get("type", "?")
            node_name = node.get("name", "?")
            # Highlight embedding/vector/pinecone nodes
            flag = ""
            type_lower = node_type.lower()
            name_lower = node_name.lower()
            if any(kw in type_lower or kw in name_lower for kw in ["embed", "vector", "pinecone", "rag"]):
                flag = " <<<< EMBEDDING/VECTOR"
            print(f"    - [{node_type}] {node_name}{flag}")

        # Deep search for embedding-001
        matches = find_embedding_refs(workflow)
        all_matches[wf_id] = matches

        if matches:
            print(f"\n  TROVATE {len(matches)} referenze a '{OLD_MODEL}':")
            for m in matches:
                display_val = m['value'][:100] + "..." if len(m['value']) > 100 else m['value']
                print(f"    Path: {m['path']}")
                print(f"    Value: {display_val}")
                print()
        else:
            print(f"\n  Nessuna referenza a '{OLD_MODEL}' trovata in questo workflow.")

    # Summary
    total = sum(len(v) for v in all_matches.values())
    print(f"\n{'=' * 65}")
    print(f"  RIEPILOGO")
    print(f"{'=' * 65}")
    print(f"  Referenze totali a '{OLD_MODEL}': {total}")
    if total > 0:
        print(f"  Modello sostitutivo: {NEW_MODEL}")
        print(f"\n  Per applicare il fix, esegui:")
        print(f"    python fix_embedding_model.py --fix")
    else:
        print(f"  Nessun fix necessario nei workflow scaricati.")
        print(f"  L'errore potrebbe provenire da un sotto-workflow o un nodo dinamico.")
    print(f"{'=' * 65}")


# ── Phase 2: Fix ──────────────────────────────────────────────
def fix():
    """Apply the embedding model fix and push to n8n."""
    print("=" * 65)
    print(f"  FIX EMBEDDING: {OLD_MODEL} -> {NEW_MODEL}")
    print("=" * 65)

    for wf_id, wf_name in WORKFLOWS.items():
        print(f"\n{'─' * 65}")
        print(f"  Workflow: {wf_name} ({wf_id})")
        print(f"{'─' * 65}")

        # Fetch fresh copy
        print(f"  Fetching workflow...")
        try:
            workflow = fetch_workflow(wf_id)
        except Exception as e:
            print(f"  ERRORE fetch: {e}")
            continue

        # Check if there are matches
        matches = find_embedding_refs(workflow)
        if not matches:
            print(f"  Nessuna referenza a '{OLD_MODEL}' - skip.")
            continue

        print(f"  Trovate {len(matches)} referenze. Applicando fix...")

        # Apply fix
        replaced = replace_embedding_refs(workflow)
        print(f"  Sostituite {replaced} occorrenze: {OLD_MODEL} -> {NEW_MODEL}")

        # Verify no more old references
        remaining = find_embedding_refs(workflow)
        if remaining:
            print(f"  ATTENZIONE: Rimangono {len(remaining)} referenze non sostituite!")
            for r in remaining:
                print(f"    - {r['path']}: {r['value'][:80]}")
            continue

        print(f"  Verifica OK: 0 referenze residue a '{OLD_MODEL}'")

        # Push
        print(f"  Pushing aggiornamento a n8n...")
        try:
            payload = prepare_payload(workflow)
            result = push_workflow(wf_id, payload)
            print(f"  AGGIORNATO! Version: {result.get('versionId', 'N/A')}")
        except requests.exceptions.HTTPError as e:
            print(f"  ERRORE push: {e}")
            if e.response is not None:
                print(f"  Status: {e.response.status_code}")
                print(f"  Body: {e.response.text[:300]}")
        except Exception as e:
            print(f"  ERRORE: {e}")

    print(f"\n{'=' * 65}")
    print(f"  FIX COMPLETATO")
    print(f"  NOTA: I vettori esistenti in Pinecone (BLC) sono stati creati")
    print(f"  con {OLD_MODEL} e sono INCOMPATIBILI con {NEW_MODEL}.")
    print(f"  Ri-esegui Brand Profile V2 per BLC per ricreare i vettori.")
    print(f"{'=' * 65}")


# ── Main ──────────────────────────────────────────────────────
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python fix_embedding_model.py --analyze|--fix")
        print("  --analyze  Scarica, backup e analizza i workflow (read-only)")
        print("  --fix      Applica il fix e aggiorna i workflow su n8n")
        sys.exit(1)

    mode = sys.argv[1]
    if mode == "--analyze":
        analyze()
    elif mode == "--fix":
        fix()
    else:
        print(f"Modalita sconosciuta: {mode}")
        print("Usa --analyze o --fix")
        sys.exit(1)
