#!/usr/bin/env python3
"""
merge_video_to_definitive.py
============================
Aggiunge la sezione "03c. Generazione Video (Ramo Video)" al workflow definitivo
oRYSQ9tk63yPJaqt prelevando i nodi video da t4FjSJFBAlspnVUM.

Operazioni:
  1. Fetch live di ENTRAMBI i workflow via n8n API
  2. Salva backup timestampati in backup_workflows/
  3. Estrae i 12 nodi video da t4FjSJFBAlspnVUM
  4. Aggiunge i nodi al workflow definitivo (senza rimuovere nulla)
  5. Corregge l'espressione Check Format (usa webhook diretto)
  6. Spezza 3c → 4a e inserisce Check Format come branch point
  7. Aggiunge tutte le connessioni video
  8. Ricalcola le posizioni per un layout grafico pulito
  9. Aggiorna sticky notes
 10. PUT del workflow aggiornato su n8n
"""

import json
import os
import sys
import time
import copy
import requests
from datetime import datetime

# ── Configurazione API ─────────────────────────────────────────────────────────
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIwMmRmNzQ5NC1hNjVjLTRjOTAtOTE5MC00NmViOWI4ODg5OGIiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzY4NTEyOTE5fQ.T-W7tlxC7dAA0dPHusS7yuZLpX-qAzuzYCUT653cC0k"
BASE_URL = "https://emanueleserra.app.n8n.cloud/api/v1"
HEADERS  = {"X-N8N-API-KEY": API_KEY, "Content-Type": "application/json"}

ID_DEFINITIVO = "oRYSQ9tk63yPJaqt"   # Caption Flow V.2 (definitivo con RAG avanzato)
ID_FIX_TEST   = "t4FjSJFBAlspnVUM"   # Caption Flow V.2 (Fix Test — ha la sezione video)

BACKUP_DIR = os.path.join(os.path.dirname(__file__), "backup_workflows")

# IDs dei nodi video presenti in t4FjSJFBAlspnVUM che vogliamo portare nel definitivo
VIDEO_NODE_IDS = {
    "5fdf65f1-3cf7-488a-adf0-a7954311a3ed",  # Check Format
    "4d325876-e548-40d8-9381-140416cdc5e3",  # Video Prompt3
    "b35756cb-ce42-4f11-b5e7-fc86008080e5",  # AI Agent
    "73741eaa-2f09-4d8c-8888-03bf3ab5c67c",  # OpenAI Chat Model (sub-node di AI Agent)
    "f989d671-0e76-4d50-beb6-ddfb31820368",  # Text to Video2
    "6ef0a28b-62b2-40e0-9729-d1af2c001469",  # Wait4
    "d78ffbe8-7951-4473-b982-4eedc2a7d253",  # Get Video4
    "cc056014-afc3-4cc4-b130-c503d50ca935",  # If4
    "check-loop-limit",                       # Check Loop Limit
    "email-timeout",                          # Email Timeout
    "f12b53c8-b24f-4f57-8378-fce26b492770",  # Video URL4
    "64870d45-4db1-4039-9dac-8175a46693b8",  # Sticky Note6
}

# Nomi dei nodi video (usato per estrarre connessioni)
VIDEO_NODE_NAMES = {
    "Check Format", "Video Prompt3", "AI Agent", "OpenAI Chat Model",
    "Text to Video2", "Wait4", "Get Video4", "If4",
    "Check Loop Limit", "Email Timeout", "Video URL4", "Sticky Note6",
}

# Layout pixel per la sezione video nel workflow definitivo
# Sezione video tra y=1080 e y=1500, allineata con il flusso principale
VIDEO_POSITIONS = {
    "Check Format"     : [-640, 1792],   # stesso y di 3c. e 4a. (branch point)
    "Video Prompt3"    : [-900, 1280],
    "AI Agent"         : [-640, 1280],
    "OpenAI Chat Model": [-640, 1480],   # sub-node
    "Text to Video2"   : [-340, 1280],
    "Wait4"            : [-140, 1280],
    "Get Video4"       : [60,   1280],
    "If4"              : [260,  1280],
    "Check Loop Limit" : [460,  1280],
    "Email Timeout"    : [660,  1080],
    "Video URL4"       : [460,  1040],   # sale verso 5. Prepare Data
    "Sticky Note6"     : [-980, 1030],   # background note
}

STICKY_NOTE6_SIZE = {"height": 390, "width": 1720}


# ── Helper ─────────────────────────────────────────────────────────────────────

def fetch_workflow(workflow_id: str) -> dict:
    url = f"{BASE_URL}/workflows/{workflow_id}"
    r = requests.get(url, headers=HEADERS, timeout=30)
    r.raise_for_status()
    return r.json()


def save_backup(workflow: dict, label: str) -> str:
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    fname = f"{label}_LIVE_BACKUP_{ts}.json"
    path = os.path.join(BACKUP_DIR, fname)
    os.makedirs(BACKUP_DIR, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(workflow, f, indent=2, ensure_ascii=False)
    return path


def push_workflow(workflow_id: str, nodes: list, connections: dict, name: str) -> dict:
    url = f"{BASE_URL}/workflows/{workflow_id}"
    payload = {
        "name": name,
        "nodes": nodes,
        "connections": connections,
        "settings": {
            "executionOrder": "v1",
            "saveDataErrorExecution": "all",
            "saveDataSuccessExecution": "all",
            "saveExecutionProgress": True,
            "saveManualExecutions": True,
            "timezone": "Europe/Rome",
        },
    }
    r = requests.put(url, headers=HEADERS, json=payload, timeout=60)
    r.raise_for_status()
    return r.json()


# ── Logica principale ──────────────────────────────────────────────────────────

def main():
    print("=" * 70)
    print("  MERGE VIDEO BRANCH → Caption Flow V.2 Definitivo")
    print("=" * 70)

    # ── 1. Fetch workflow live ───────────────────────────────────────────────
    print("\n[1/7] Fetch workflow live da n8n...")

    print(f"  → GET {ID_DEFINITIVO} (definitivo)...")
    wf_def = fetch_workflow(ID_DEFINITIVO)
    print(f"     OK — '{wf_def['name']}' — {len(wf_def['nodes'])} nodi")

    print(f"  → GET {ID_FIX_TEST} (fix test / video)...")
    wf_vid = fetch_workflow(ID_FIX_TEST)
    print(f"     OK — '{wf_vid['name']}' — {len(wf_vid['nodes'])} nodi")

    # ── 2. Backup ────────────────────────────────────────────────────────────
    print("\n[2/7] Salvataggio backup...")
    p1 = save_backup(wf_def, f"Caption_Flow_V2_{ID_DEFINITIVO}")
    print(f"  ✓ {os.path.basename(p1)}")
    p2 = save_backup(wf_vid, f"Caption_Flow_{ID_FIX_TEST}")
    print(f"  ✓ {os.path.basename(p2)}")

    # ── 3. Estrai nodi video da t4FjSJFBAlspnVUM ────────────────────────────
    print("\n[3/7] Estrazione nodi video da Fix Test...")
    video_nodes_raw = [
        n for n in wf_vid["nodes"]
        if n.get("id") in VIDEO_NODE_IDS or n.get("name") in VIDEO_NODE_NAMES
    ]
    print(f"  Trovati {len(video_nodes_raw)} nodi video:")
    for n in video_nodes_raw:
        print(f"    • {n['name']} (id: {n['id'][:8]}..)")

    # ── 4. Verifica che i nodi video NON siano già nel definitivo ────────────
    print("\n[4/7] Verifica nodi già presenti nel definitivo...")
    existing_ids   = {n["id"]   for n in wf_def["nodes"]}
    existing_names = {n["name"] for n in wf_def["nodes"]}

    video_nodes_to_add = []
    for n in video_nodes_raw:
        if n["id"] in existing_ids:
            print(f"  ! Nodo già presente (id): {n['name']} — skip")
        elif n["name"] in existing_names:
            print(f"  ! Nodo già presente (nome): {n['name']} — skip")
        else:
            video_nodes_to_add.append(copy.deepcopy(n))

    if not video_nodes_to_add:
        print("  Tutti i nodi video sono già presenti. Nulla da aggiungere.")
        return

    print(f"  Nodi da aggiungere: {len(video_nodes_to_add)}")

    # ── 5. Clona il workflow definitivo e aggiungi nodi video ────────────────
    print("\n[5/7] Merge nodi + aggiornamento connessioni...")

    new_nodes = copy.deepcopy(wf_def["nodes"])

    # Applica posizioni video e dimensioni Sticky Note6
    for n in video_nodes_to_add:
        name = n["name"]
        if name in VIDEO_POSITIONS:
            n["position"] = VIDEO_POSITIONS[name]
        if name == "Sticky Note6" and STICKY_NOTE6_SIZE:
            n["parameters"]["height"] = STICKY_NOTE6_SIZE["height"]
            n["parameters"]["width"]  = STICKY_NOTE6_SIZE["width"]
        # Correggi espressione Check Format per usare il webhook diretto
        if name == "Check Format":
            try:
                conds = n["parameters"]["conditions"]["conditions"]
                for c in conds:
                    if "2. Prepare Input Variables" in str(c.get("leftValue", "")):
                        c["leftValue"] = "={{ $('CaptionFlow Webhook').first().json.body.format }}"
                        print(f"    ✓ Check Format espressione corretta → webhook diretto")
            except (KeyError, TypeError):
                pass

        new_nodes.append(n)

    # ── 6. Aggiorna connessioni ──────────────────────────────────────────────
    new_conns = copy.deepcopy(wf_def["connections"])

    NAME_3C = "3c. Generate Post Caption (Gemini)"
    NAME_4A = "4a. Create Image Task (Kie)"
    NAME_CF = "Check Format"
    NAME_VP = "Video Prompt3"
    NAME_AI = "AI Agent"
    NAME_T2 = "Text to Video2"
    NAME_W4 = "Wait4"
    NAME_GV = "Get Video4"
    NAME_I4 = "If4"
    NAME_VU = "Video URL4"
    NAME_CL = "Check Loop Limit"
    NAME_ET = "Email Timeout"
    NAME_5P = "5. Prepare Data for Instagram API"

    # Rimuovi connessione esistente: 3c → 4a (output 0)
    if NAME_3C in new_conns:
        main_outs = new_conns[NAME_3C].get("main", [])
        if main_outs:
            main_outs[0] = [
                c for c in main_outs[0]
                if c.get("node") != NAME_4A
            ]
            print(f"    ✓ Rimossa connessione: {NAME_3C} → {NAME_4A}")

    def add_conn(src, dst, src_out=0, dst_in=0):
        if src not in new_conns:
            new_conns[src] = {"main": []}
        while len(new_conns[src]["main"]) <= src_out:
            new_conns[src]["main"].append([])
        # Evita duplicati
        existing = [c["node"] for c in new_conns[src]["main"][src_out]]
        if dst not in existing:
            new_conns[src]["main"][src_out].append({"node": dst, "type": "main", "index": dst_in})

    # 3c → Check Format (output 0)
    add_conn(NAME_3C, NAME_CF, src_out=0)
    print(f"    ✓ Aggiunta: {NAME_3C} → {NAME_CF}")

    # Check Format → Video Prompt3 (output 0 = True = video)
    add_conn(NAME_CF, NAME_VP, src_out=0)
    print(f"    ✓ Aggiunta: {NAME_CF} [0/video] → {NAME_VP}")

    # Check Format → 4a. Create Image Task (output 1 = False = immagine)
    add_conn(NAME_CF, NAME_4A, src_out=1)
    print(f"    ✓ Aggiunta: {NAME_CF} [1/image] → {NAME_4A}")

    # Catena video interna
    add_conn(NAME_VP, NAME_AI, src_out=0)
    add_conn(NAME_AI, NAME_T2, src_out=0)
    add_conn(NAME_T2, NAME_W4, src_out=0)
    add_conn(NAME_W4, NAME_GV, src_out=0)
    add_conn(NAME_GV, NAME_I4, src_out=0)
    print(f"    ✓ Catena video: {NAME_VP} → {NAME_AI} → {NAME_T2} → {NAME_W4} → {NAME_GV} → {NAME_I4}")

    # If4 → Video URL4 (output 0 = success)
    add_conn(NAME_I4, NAME_VU, src_out=0)
    # If4 → Check Loop Limit (output 1 = not ready yet)
    add_conn(NAME_I4, NAME_CL, src_out=1)
    print(f"    ✓ {NAME_I4} [0] → {NAME_VU} | [1] → {NAME_CL}")

    # Check Loop Limit → Email Timeout (output 0 = over limit)
    add_conn(NAME_CL, NAME_ET, src_out=0)
    # Check Loop Limit → Wait4 (output 1 = loop back)
    add_conn(NAME_CL, NAME_W4, src_out=1)
    print(f"    ✓ {NAME_CL} [0] → {NAME_ET} | [1] → {NAME_W4}")

    # Video URL4 → 5. Prepare Data for Instagram API
    add_conn(NAME_VU, NAME_5P, src_out=0)
    print(f"    ✓ Aggiunta: {NAME_VU} → {NAME_5P}")

    # ── 7. Aggiorna sticky notes nel workflow definitivo ─────────────────────
    print("\n[6/7] Aggiornamento sticky notes...")
    video_section_note = None
    for n in new_nodes:
        if n["name"] == "Sticky Note6":
            video_section_note = n
            break
    if video_section_note:
        # Mantieni il contenuto originale (già ben scritto in t4FjSJFBAlspnVUM)
        print("  ✓ Sticky Note6 (sezione video) presente e posizionata")

    # ── 8. Push su n8n ──────────────────────────────────────────────────────
    print(f"\n[7/7] Push workflow aggiornato su n8n (ID: {ID_DEFINITIVO})...")
    result = push_workflow(
        workflow_id=ID_DEFINITIVO,
        nodes=new_nodes,
        connections=new_conns,
        name=wf_def.get("name", "Caption Flow V.2"),
    )
    print(f"  ✓ Workflow aggiornato: '{result['name']}'")
    print(f"    Nodi totali: {len(result['nodes'])}")
    print(f"    Aggiornato il: {result.get('updatedAt','?')}")

    print("\n" + "=" * 70)
    print("  COMPLETATO CON SUCCESSO")
    print("=" * 70)
    print(f"\n  Backup oRYSQ9: {os.path.basename(p1)}")
    print(f"  Backup t4FjSJ: {os.path.basename(p2)}")
    print(f"\n  Verifica in n8n:")
    print(f"  https://emanueleserra.app.n8n.cloud/workflow/{ID_DEFINITIVO}")
    print()

    print("  TEST RACCOMANDATI:")
    print("  • Ramo VIDEO: POST webhook con body = { ..., 'format': 'video' }")
    print("    → deve eseguire: 3c → Check Format → Video Prompt3 → AI Agent →")
    print("                     Text to Video2 → Wait4 → Get Video4 → If4 → Video URL4 → 5.PrepareData")
    print("  • Ramo IMMAGINE (invariato): POST senza 'format' o con 'format': 'image'")
    print("    → deve eseguire: 3c → Check Format → 4a.CreateImage → ... → Instagram")
    print()


if __name__ == "__main__":
    main()
