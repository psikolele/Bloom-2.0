#!/usr/bin/env python3
"""
fix_cloudinary_video_null.py
============================
Corregge l'errore "Unsupported source URL: null" su Cloudinary
nel workflow Caption Flow V.2 (oRYSQ9tk63yPJaqt).

Causa radice (Execution #7894 — 24/02/2026):
  Il nodo "5. Prepare Data for Instagram API" ha un'espressione ImageURL
  scritta solo per il percorso IMMAGINE:
    JSON.parse($json['data']['resultJson']).resultUrls[0]
  Quando raggiunto dal percorso VIDEO (via "Video URL4"), $json contiene
  solo {video_url: "..."} — non esiste $json.data — risultato: null.
  Cloudinary riceve file=null → 400 "Unsupported source URL: null".

Fix applicati (2 modifiche):
  1. "5. Prepare Data for Instagram API" — ImageURL
       PRIMA: JSON.parse($json['data']['resultJson']).resultUrls[0]
       DOPO:  $json.video_url ? $json.video_url : JSON.parse($json['data']['resultJson']).resultUrls[0]

  2. "Upload Image to Cloudinary" — url endpoint
       PRIMA: .../image/upload  (solo immagini)
       DOPO:  .../auto/upload   (immagini + video, auto-detect)
"""

import json
import os
import copy
import requests
from datetime import datetime

# ── Config ─────────────────────────────────────────────────────────────────────
API_KEY  = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIwMmRmNzQ5NC1hNjVjLTRjOTAtOTE5MC00NmViOWI4ODg5OGIiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzY4NTEyOTE5fQ.T-W7tlxC7dAA0dPHusS7yuZLpX-qAzuzYCUT653cC0k"
BASE_URL = "https://emanueleserra.app.n8n.cloud/api/v1"
HEADERS  = {"X-N8N-API-KEY": API_KEY, "Content-Type": "application/json"}
WF_ID    = "oRYSQ9tk63yPJaqt"
BACKUP_DIR = os.path.join(os.path.dirname(__file__), "backup_workflows")

# Espressione corretta per ImageURL (gestisce sia video che immagine)
NEW_IMAGE_URL_EXPR = (
    "={{ $json.video_url ? $json.video_url "
    ": JSON.parse($json['data']['resultJson']).resultUrls[0] }}"
)

# Nuovo endpoint Cloudinary (auto-detect resource_type)
NEW_CLOUDINARY_URL = "https://api.cloudinary.com/v1_1/dzudfzmx3/auto/upload"


def fetch_workflow(wf_id: str) -> dict:
    r = requests.get(f"{BASE_URL}/workflows/{wf_id}", headers=HEADERS, timeout=30)
    r.raise_for_status()
    return r.json()


def save_backup(workflow: dict, label: str) -> str:
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    os.makedirs(BACKUP_DIR, exist_ok=True)
    path = os.path.join(BACKUP_DIR, f"{label}_LIVE_BACKUP_{ts}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(workflow, f, indent=2, ensure_ascii=False)
    return path


def push_workflow(wf_id: str, wf: dict) -> dict:
    payload = {
        "name":        wf["name"],
        "nodes":       wf["nodes"],
        "connections": wf["connections"],
        "settings": {
            "executionOrder":            "v1",
            "saveDataErrorExecution":    "all",
            "saveDataSuccessExecution":  "all",
            "saveExecutionProgress":     True,
            "saveManualExecutions":      True,
            "timezone":                  "Europe/Rome",
        },
    }
    r = requests.put(f"{BASE_URL}/workflows/{wf_id}", headers=HEADERS,
                     json=payload, timeout=60)
    r.raise_for_status()
    return r.json()


def main():
    print("=" * 65)
    print("  FIX: Cloudinary null URL — Caption Flow V.2")
    print("=" * 65)

    # 1. Fetch live
    print(f"\n[1/4] Fetch workflow live ({WF_ID})...")
    wf = fetch_workflow(WF_ID)
    print(f"  OK — '{wf['name']}' — {len(wf['nodes'])} nodi")

    # 2. Backup
    print("\n[2/4] Backup...")
    bp = save_backup(wf, f"Caption_Flow_V2_{WF_ID}")
    print(f"  ✓ {os.path.basename(bp)}")

    # 3. Applica patch
    print("\n[3/4] Patch nodi...")
    patched = copy.deepcopy(wf)
    fix1_done = False
    fix2_done = False

    for node in patched["nodes"]:
        # ── Fix 1: 5. Prepare Data for Instagram API ──────────────────────
        if node["name"] == "5. Prepare Data for Instagram API":
            assignments = node["parameters"]["assignments"]["assignments"]
            for asgn in assignments:
                if asgn.get("name") == "ImageURL":
                    old_val = asgn["value"]
                    asgn["value"] = NEW_IMAGE_URL_EXPR
                    print(f"  ✓ Fix 1 — ImageURL aggiornato")
                    print(f"       prima: {old_val[:70]}...")
                    print(f"       dopo : {NEW_IMAGE_URL_EXPR[:70]}...")
                    fix1_done = True

        # ── Fix 2: Upload Image to Cloudinary ─────────────────────────────
        if node["name"] == "Upload Image to Cloudinary":
            old_url = node["parameters"].get("url", "")
            if "/image/upload" in old_url:
                node["parameters"]["url"] = NEW_CLOUDINARY_URL
                print(f"  ✓ Fix 2 — Cloudinary URL aggiornato")
                print(f"       prima: {old_url}")
                print(f"       dopo : {NEW_CLOUDINARY_URL}")
                fix2_done = True

    if not fix1_done:
        print("  ⚠  Fix 1 NON applicato — nodo '5. Prepare Data' o campo 'ImageURL' non trovato")
    if not fix2_done:
        print("  ⚠  Fix 2 NON applicato — nodo 'Upload Image to Cloudinary' non trovato")

    if not (fix1_done or fix2_done):
        print("\nNessuna patch applicata. Uscita senza modificare il workflow.")
        return

    # 4. Push
    print(f"\n[4/4] Push su n8n ({WF_ID})...")
    result = push_workflow(WF_ID, patched)
    print(f"  ✓ Workflow aggiornato: '{result['name']}'")
    print(f"    Aggiornato il: {result.get('updatedAt','?')}")

    print("\n" + "=" * 65)
    print("  COMPLETATO")
    print("=" * 65)
    print(f"\n  Backup: {os.path.basename(bp)}")
    print(f"\n  Workflow live: https://emanueleserra.app.n8n.cloud/workflow/{WF_ID}")
    print()
    print("  Verifica fix:")
    print("  • Ramo VIDEO  : POST webhook con 'format':'video'")
    print("    → ImageURL deve essere il video URL da KIE (non null)")
    print("    → Cloudinary /auto/upload accetta video ✓")
    print("  • Ramo IMMAGINE: POST senza 'format' (comportamento invariato)")
    print()


if __name__ == "__main__":
    main()
