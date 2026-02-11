"""
Add RAG Query Webhook Section to the existing N8N RAG workflow.
Section 6: API: RAG Query (Frontend)

This adds a complete webhook-based RAG query flow that:
1. Receives POST { query, folderId } from the frontend
2. Looks up the folder name from Google Drive
3. Maps folder to the correct Pinecone index
4. Uses an AI Agent (OpenRouter + Pinecone) to generate an answer
5. Returns { answer, sources } to the frontend
"""

import requests
import json
import copy
import sys

API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIwMmRmNzQ5NC1hNjVjLTRjOTAtOTE5MC00NmViOWI4ODg5OGIiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzY4NTEyOTE5fQ.T-W7tlxC7dAA0dPHusS7yuZLpX-qAzuzYCUT653cC0k"
BASE_URL = "https://emanueleserra.app.n8n.cloud/api/v1"
HEADERS = {"X-N8N-API-KEY": API_KEY, "Content-Type": "application/json"}
WF_ID = "XmCaI5Q9MxNf0EP_65UvB"

# ─── New Nodes ───────────────────────────────────────────────────────────────

NEW_NODES = [
    # 1. Sticky Note for the section
    {
        "parameters": {
            "content": "## \ud83d\udd0d 6. API: RAG Query (Frontend)\nEndpoint chiamato dal frontend per effettuare query RAG sui documenti indicizzati.\n\n- **Webhook POST** (`/webhook/rag-query`): Riceve la query e il `folderId` dall\u2019interfaccia chat.\n- **Get Folder Name**: Recupera il nome della cartella da Google Drive tramite API.\n- **Prepare Query**: Mappa la cartella al corretto indice Pinecone e prepara l\u2019input per l\u2019agente.\n- **AI Agent**: Un agente LangChain che cerca nei documenti rilevanti e genera la risposta.\n- **Response**: Restituisce un JSON con `answer` e `sources` al frontend.\n\n> \u26a1 Chiamato da: `RAGChat.tsx` \u2192 `POST /webhook/rag-query`",
            "height": 836,
            "width": 1128,
            "color": 6
        },
        "id": "note-rag-query",
        "name": "Sticky Note RAG Query",
        "type": "n8n-nodes-base.stickyNote",
        "typeVersion": 1,
        "position": [-48, 2050]
    },

    # 2. Webhook RAG Query (POST /webhook/rag-query)
    {
        "parameters": {
            "httpMethod": "POST",
            "path": "rag-query",
            "responseMode": "responseNode",
            "options": {}
        },
        "id": "webhook-rag-query",
        "name": "Webhook RAG Query",
        "type": "n8n-nodes-base.webhook",
        "typeVersion": 2,
        "position": [0, 2300],
        "webhookId": "webhook-rag-query-id"
    },

    # 3. Get Folder Name via Google Drive API
    {
        "parameters": {
            "method": "GET",
            "url": "={{ 'https://www.googleapis.com/drive/v3/files/' + $json.body.folderId + '?fields=id,name' }}",
            "authentication": "predefinedCredentialType",
            "nodeCredentialType": "googleDriveOAuth2Api",
            "options": {}
        },
        "id": "get-rag-folder-name",
        "name": "Get Folder Name",
        "type": "n8n-nodes-base.httpRequest",
        "typeVersion": 4.2,
        "position": [200, 2300],
        "credentials": {
            "googleDriveOAuth2Api": {
                "id": "SJ46HET6LBfzlEsT",
                "name": "Google Drive Didattica BLC"
            }
        }
    },

    # 4. Prepare RAG Query (map folder to Pinecone index + set chatInput)
    {
        "parameters": {
            "jsCode": "const body = $('Webhook RAG Query').first().json.body || {};\nconst query = body.query || '';\nconst folderName = ($json.name || '').toLowerCase();\n\n// Map folder name to Pinecone index\nlet targetIndex = 'rag-pessina-db'; // default\n\nif (folderName.includes('jobcourier') || folderName.includes('job courier')) {\n  targetIndex = 'rag-jobcourier-db';\n} else if (folderName.includes('blc')) {\n  targetIndex = 'rag-blc-db';\n} else if (folderName.includes('walmoss')) {\n  targetIndex = 'rag-walmoss-db';\n} else if (folderName.includes('pessina')) {\n  targetIndex = 'rag-pessina-db';\n} else if (folderName.includes('foot') && folderName.includes('easy')) {\n  targetIndex = 'rag-foot-easy-db';\n}\n\nreturn [{\n  json: {\n    chatInput: query,\n    targetIndex: targetIndex,\n    folderName: $json.name || 'Unknown'\n  }\n}];"
        },
        "id": "prepare-rag-query",
        "name": "Prepare RAG Query",
        "type": "n8n-nodes-base.code",
        "typeVersion": 2,
        "position": [400, 2300]
    },

    # 5. RAG Query Agent
    {
        "parameters": {
            "options": {
                "systemMessage": "You are a helpful RAG assistant. Answer the user's question based on the retrieved documents. Be concise and accurate. If you cannot find relevant information, say so clearly. Always respond in the same language as the user's question."
            }
        },
        "id": "rag-query-agent",
        "name": "RAG Query Agent",
        "type": "@n8n/n8n-nodes-langchain.agent",
        "typeVersion": 3.1,
        "position": [600, 2300]
    },

    # 6. RAG Query LLM (OpenRouter)
    {
        "parameters": {
            "options": {}
        },
        "id": "rag-query-llm",
        "name": "RAG Query LLM",
        "type": "@n8n/n8n-nodes-langchain.lmChatOpenRouter",
        "typeVersion": 1,
        "position": [480, 2524],
        "credentials": {
            "openRouterApi": {
                "id": "bPejUNztelVUXKU1",
                "name": "OpenRouter"
            }
        }
    },

    # 7. RAG Query Pinecone (retrieve-as-tool, dynamic index)
    {
        "parameters": {
            "mode": "retrieve-as-tool",
            "toolDescription": "Use this tool to retrieve information about training courses, professional orientation, and internal company documents based on the user query",
            "pineconeIndex": {
                "__rl": True,
                "value": "={{ $('Prepare RAG Query').first().json.targetIndex }}",
                "mode": "id"
            },
            "options": {}
        },
        "id": "rag-query-pinecone",
        "name": "RAG Query Pinecone",
        "type": "@n8n/n8n-nodes-langchain.vectorStorePinecone",
        "typeVersion": 1.3,
        "position": [700, 2524],
        "credentials": {
            "pineconeApi": {
                "id": "pg8MVmRWeGRWKAH9",
                "name": "PineconeApi account Didattica BLC"
            }
        }
    },

    # 8. RAG Query Embeddings (OpenAI via OpenRouter)
    {
        "parameters": {
            "options": {}
        },
        "id": "rag-query-embeddings",
        "name": "RAG Query Embeddings",
        "type": "@n8n/n8n-nodes-langchain.embeddingsOpenAi",
        "typeVersion": 1.2,
        "position": [780, 2732],
        "credentials": {
            "openAiApi": {
                "id": "kjETjzJF05kUBRFk",
                "name": "OpenRouter_Auto_Fixed"
            }
        }
    },

    # 9. Format RAG Response
    {
        "parameters": {
            "jsCode": "const output = $json.output || $json.text || '';\n\nreturn [{\n  json: {\n    answer: output,\n    sources: []\n  }\n}];"
        },
        "id": "format-rag-response",
        "name": "Format RAG Response",
        "type": "n8n-nodes-base.code",
        "typeVersion": 2,
        "position": [800, 2300]
    },

    # 10. Respond RAG Query (respondToWebhook with CORS headers)
    {
        "parameters": {
            "respondWith": "json",
            "responseBody": "={{ { answer: $json.answer || '', sources: $json.sources || [] } }}",
            "options": {
                "responseHeaders": {
                    "entries": [
                        {
                            "name": "Access-Control-Allow-Origin",
                            "value": "*"
                        },
                        {
                            "name": "Access-Control-Allow-Methods",
                            "value": "GET, POST, OPTIONS"
                        },
                        {
                            "name": "Access-Control-Allow-Headers",
                            "value": "*"
                        }
                    ]
                }
            }
        },
        "id": "respond-rag-query",
        "name": "Respond RAG Query",
        "type": "n8n-nodes-base.respondToWebhook",
        "typeVersion": 1,
        "position": [1000, 2300]
    }
]

# ─── New Connections ─────────────────────────────────────────────────────────

NEW_CONNECTIONS = {
    # Main flow: Webhook → Get Folder → Prepare → Agent → Format → Respond
    "Webhook RAG Query": {
        "main": [[
            {"node": "Get Folder Name", "type": "main", "index": 0}
        ]]
    },
    "Get Folder Name": {
        "main": [[
            {"node": "Prepare RAG Query", "type": "main", "index": 0}
        ]]
    },
    "Prepare RAG Query": {
        "main": [[
            {"node": "RAG Query Agent", "type": "main", "index": 0}
        ]]
    },
    "RAG Query Agent": {
        "main": [[
            {"node": "Format RAG Response", "type": "main", "index": 0}
        ]]
    },
    "Format RAG Response": {
        "main": [[
            {"node": "Respond RAG Query", "type": "main", "index": 0}
        ]]
    },
    # AI sub-connections
    "RAG Query LLM": {
        "ai_languageModel": [[
            {"node": "RAG Query Agent", "type": "ai_languageModel", "index": 0}
        ]]
    },
    "RAG Query Pinecone": {
        "ai_tool": [[
            {"node": "RAG Query Agent", "type": "ai_tool", "index": 0}
        ]]
    },
    "RAG Query Embeddings": {
        "ai_embedding": [[
            {"node": "RAG Query Pinecone", "type": "ai_embedding", "index": 0}
        ]]
    }
}


def main():
    # 1. Fetch current workflow
    print("Fetching current workflow...")
    resp = requests.get(f"{BASE_URL}/workflows/{WF_ID}", headers=HEADERS)
    if not resp.ok:
        print(f"ERROR: Failed to fetch workflow: {resp.status_code} - {resp.text}")
        sys.exit(1)

    workflow = resp.json()
    print(f"  Name: {workflow['name']}")
    print(f"  Nodes: {len(workflow['nodes'])}")

    # 2. Save backup
    backup_path = "backup_workflows/RAG_workflow_BEFORE_query_webhook.json"
    with open(backup_path, 'w') as f:
        json.dump(workflow, f, indent=2)
    print(f"  Backup saved: {backup_path}")

    # 3. Check if section already exists
    existing_names = [n['name'] for n in workflow['nodes']]
    if 'Webhook RAG Query' in existing_names:
        print("\n  WARNING: 'Webhook RAG Query' node already exists!")
        print("  Skipping to avoid duplicates.")
        sys.exit(0)

    # 4. Add new nodes
    workflow['nodes'].extend(NEW_NODES)
    print(f"\n  Added {len(NEW_NODES)} new nodes. Total: {len(workflow['nodes'])}")

    # 5. Add new connections
    workflow['connections'].update(NEW_CONNECTIONS)
    print(f"  Added {len(NEW_CONNECTIONS)} new connection entries.")

    # 6. Prepare payload for PUT (only include API-safe settings)
    safe_settings = {
        "executionOrder": "v1"
    }
    payload = {
        "nodes": workflow['nodes'],
        "connections": workflow['connections'],
        "settings": safe_settings,
        "name": workflow['name']
    }

    # 7. Push to N8N
    print("\nPushing updated workflow to N8N...")
    put_resp = requests.put(
        f"{BASE_URL}/workflows/{WF_ID}",
        headers=HEADERS,
        json=payload
    )

    if put_resp.ok:
        result = put_resp.json()
        print(f"  SUCCESS! Workflow updated.")
        print(f"  Name: {result['name']}")
        print(f"  Total nodes: {len(result.get('nodes', []))}")
        print(f"  Updated at: {result.get('updatedAt', 'N/A')}")

        # Save updated version
        with open("backup_workflows/RAG_workflow_WITH_query_webhook.json", 'w') as f:
            json.dump(result, f, indent=2)
        print(f"  Updated workflow saved to backup.")
    else:
        print(f"  ERROR: {put_resp.status_code}")
        print(f"  Response: {put_resp.text[:1000]}")
        sys.exit(1)

    # 8. Print summary
    print("\n" + "=" * 60)
    print("SECTION 6: RAG Query Webhook - ADDED SUCCESSFULLY")
    print("=" * 60)
    print(f"  Webhook URL: https://emanueleserra.app.n8n.cloud/webhook/rag-query")
    print(f"  Method: POST")
    print(f"  Body: {{ query: string, folderId: string }}")
    print(f"  Response: {{ answer: string, sources: string[] }}")
    print(f"\n  New nodes added:")
    for node in NEW_NODES:
        print(f"    - {node['name']} ({node['type']})")
    print(f"\n  Flow: Webhook → Get Folder → Prepare → AI Agent → Format → Respond")
    print(f"  AI Agent sub-nodes: OpenRouter LLM + Pinecone (dynamic index) + Embeddings")


if __name__ == "__main__":
    main()
