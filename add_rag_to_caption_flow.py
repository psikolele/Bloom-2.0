#!/usr/bin/env python3
"""
Add RAG (Pinecone + Embeddings) tool to the AI Agent node in Caption Flow V3.

Generates a new workflow JSON file with:
- Caption RAG Embeddings node (text-embedding-3-small)
- Caption RAG Pinecone node (retrieve-as-tool, index: rag-blc-db)
- Connections: Embeddings -> Pinecone -> AI Agent (ai_tool)
- Updated AI Agent system prompt with RAG instructions

Output: backup_workflows/Caption_Flow_V3_WITH_RAG.json (local only, not published)
"""

import json
import copy
import uuid

INPUT_FILE = "backup_workflows/Caption_Flow_V3_VIDEO_MOD.json"
OUTPUT_FILE = "backup_workflows/Caption_Flow_V3_WITH_RAG.json"

AI_AGENT_NAME = "AI Agent"

# --- New nodes ---

EMBEDDINGS_NODE = {
    "parameters": {
        "model": "text-embedding-3-small",
        "options": {
            "dimensions": 1536
        }
    },
    "id": str(uuid.uuid4()),
    "name": "Caption RAG Embeddings",
    "type": "@n8n/n8n-nodes-langchain.embeddingsOpenAi",
    "typeVersion": 1.2,
    "position": [720, -80],
    "credentials": {
        "openAiApi": {
            "id": "kjETjzJF05kUBRFk",
            "name": "OpenRouter_Auto_Fixed"
        }
    }
}

PINECONE_NODE = {
    "parameters": {
        "mode": "retrieve-as-tool",
        "toolDescription": (
            "Usa questo tool per recuperare informazioni sull'azienda cliente: "
            "tone of voice, prodotti, servizi, brand guidelines, valori e identità visiva. "
            "Chiamalo SEMPRE prima di generare il prompt video, per personalizzare "
            "la scena in base al brand del cliente."
        ),
        "pineconeIndex": {
            "__rl": True,
            "value": "rag-blc-db",
            "mode": "list",
            "cachedResultName": "rag-blc-db"
        },
        "options": {}
    },
    "id": str(uuid.uuid4()),
    "name": "Caption RAG Pinecone",
    "type": "@n8n/n8n-nodes-langchain.vectorStorePinecone",
    "typeVersion": 1.3,
    "position": [720, -200],
    "credentials": {
        "pineconeApi": {
            "id": "pg8MVmRWeGRWKAH9",
            "name": "PineconeApi account Didattica BLC"
        }
    }
}

# --- System prompt addition ---

RAG_SYSTEM_PROMPT_ADDITION = """

---

## Contesto Aziendale (RAG)

PRIMA di generare il prompt video, usa SEMPRE il tool di ricerca RAG per recuperare informazioni sul brand del cliente (tone of voice, prodotti, valori, stile visivo, colori, target audience).

Integra queste informazioni nella scena video in modo naturale e coerente:
- Adatta l'atmosfera e il tono visivo al brand
- Includi riferimenti ai prodotti/servizi se rilevanti
- Rispetta lo stile comunicativo e i valori aziendali
- Se il RAG non restituisce risultati utili, procedi comunque con il prompt basandoti solo sull'input fornito
"""


def main():
    # Load workflow
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        wf = json.load(f)

    wf = copy.deepcopy(wf)

    # 1. Find and update AI Agent node system prompt
    agent_found = False
    for node in wf["nodes"]:
        if node["name"] == AI_AGENT_NAME:
            agent_found = True
            current_prompt = node["parameters"]["options"].get("systemMessage", "")
            node["parameters"]["options"]["systemMessage"] = current_prompt.rstrip() + RAG_SYSTEM_PROMPT_ADDITION
            print(f"[OK] Updated AI Agent system prompt")
            break

    if not agent_found:
        raise RuntimeError(f"Node '{AI_AGENT_NAME}' not found in workflow")

    # 2. Add new nodes
    wf["nodes"].append(EMBEDDINGS_NODE)
    wf["nodes"].append(PINECONE_NODE)
    print(f"[OK] Added 'Caption RAG Embeddings' node (id: {EMBEDDINGS_NODE['id']})")
    print(f"[OK] Added 'Caption RAG Pinecone' node (id: {PINECONE_NODE['id']})")

    # 3. Add connections
    connections = wf.setdefault("connections", {})

    # Embeddings -> Pinecone (ai_embedding)
    connections.setdefault("Caption RAG Embeddings", {})
    connections["Caption RAG Embeddings"]["ai_embedding"] = [
        [
            {
                "node": "Caption RAG Pinecone",
                "type": "ai_embedding",
                "index": 0
            }
        ]
    ]
    print("[OK] Connected: Caption RAG Embeddings --(ai_embedding)--> Caption RAG Pinecone")

    # Pinecone -> AI Agent (ai_tool)
    connections.setdefault("Caption RAG Pinecone", {})
    connections["Caption RAG Pinecone"]["ai_tool"] = [
        [
            {
                "node": AI_AGENT_NAME,
                "type": "ai_tool",
                "index": 0
            }
        ]
    ]
    print(f"[OK] Connected: Caption RAG Pinecone --(ai_tool)--> {AI_AGENT_NAME}")

    # 4. Save output
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(wf, f, indent=4, ensure_ascii=False)

    print(f"\n[DONE] Workflow saved to: {OUTPUT_FILE}")
    print(f"       Import this file in n8n to test before activating.")

    # Verify
    node_names = [n["name"] for n in wf["nodes"]]
    assert "Caption RAG Embeddings" in node_names, "Embeddings node missing"
    assert "Caption RAG Pinecone" in node_names, "Pinecone node missing"
    assert "Caption RAG Embeddings" in connections, "Embeddings connection missing"
    assert "Caption RAG Pinecone" in connections, "Pinecone connection missing"
    print("[OK] Verification passed: all nodes and connections present")


if __name__ == "__main__":
    main()
