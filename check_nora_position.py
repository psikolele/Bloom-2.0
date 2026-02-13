#!/usr/bin/env python3
import os, requests, sys
from dotenv import load_dotenv
load_dotenv()

print("Getting embedding...")
try:
    resp = requests.post(
        "https://openrouter.ai/api/v1/embeddings",
        headers={
            "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
            "Content-Type": "application/json"
        },
        json={
            "model": "openai/text-embedding-3-small",
            "input": "chi è il dirigente scolastico del pessina?"
        },
        timeout=30
    )

    if resp.status_code != 200:
        print(f"Error from OpenRouter: {resp.status_code}")
        print(resp.text)
        sys.exit(1)

    embedding = resp.json()["data"][0]["embedding"]
    print("✓ Got embedding\n")

except Exception as e:
    print(f"Error getting embedding: {e}")
    sys.exit(1)

print("Searching Pinecone...")
resp2 = requests.post(
    "https://rag-pessina-db-skwro36.svc.aped-4627-b74a.pinecone.io/query",
    headers={
        "Api-Key": os.getenv("PINECONE_API_KEY"),
        "Content-Type": "application/json"
    },
    json={
        "namespace": "",
        "vector": embedding,
        "topK": 30,
        "includeMetadata": True
    }
)

matches = resp2.json().get("matches", [])
print(f"✓ Got {len(matches)} results\n")

print("=" * 70)
print("🔍 POSITION OF 'NORA CALZOLAIO' CHUNKS")
print("=" * 70)

nora_positions = []

for i, m in enumerate(matches, 1):
    text = m.get("metadata", {}).get("text", "").lower()
    if "nora calzolaio" in text:
        nora_positions.append(i)
        print(f"\n✅ FOUND AT POSITION #{i}")
        print(f"   Score: {m['score']:.4f}")
        print(f"   ID: {m['id']}")
        preview = m['metadata']['text'][:200].replace('\n', ' ')
        print(f"   Preview: {preview}...")

print("\n" + "=" * 70)
if nora_positions:
    first_pos = min(nora_positions)
    print(f"📊 FIRST 'Nora Calzolaio' chunk at position #{first_pos}")
    print(f"\n🎯 SOLUTION: Set topK >= {first_pos + 5} in RAG Query node")
else:
    print("❌ 'Nora Calzolaio' NOT found in top 30!")
    print("\n🚨 This is a serious problem - chunks should be ranking higher")
