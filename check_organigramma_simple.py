#!/usr/bin/env python3
"""
Simplified script to check Pinecone chunks using HTTP API
"""
import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

def get_embedding(text):
    """Get embedding from OpenRouter"""
    api_key = os.getenv("OPENROUTER_API_KEY")
    response = requests.post(
        "https://openrouter.ai/api/v1/embeddings",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        json={
            "model": "openai/text-embedding-3-small",
            "input": text
        }
    )
    return response.json()["data"][0]["embedding"]

def main():
    api_key = os.getenv("PINECONE_API_KEY")
    folder_id = "1McMg9rriVUx6qpkZpfNwhVtd36ht6Nbe"
    namespace = f"folder-{folder_id}"

    print("=" * 70)
    print("🔍 CHECKING ORGANIGRAMMA CHUNKS IN PINECONE")
    print("=" * 70)
    print(f"Namespace: {namespace}")
    print()

    # Get index stats
    stats_url = "https://rag-pessina-db-skwro36.svc.aped-4627-b74a.pinecone.io/describe_index_stats"

    headers = {"Api-Key": api_key, "Content-Type": "application/json"}

    stats_response = requests.post(stats_url, headers=headers, json={})
    stats = stats_response.json()

    print(f"📊 Total vectors: {stats.get('totalVectorCount', 0)}")

    namespaces = stats.get('namespaces', {})
    if namespace in namespaces:
        print(f"📊 Vectors in '{namespace}': {namespaces[namespace]['vectorCount']}")
    else:
        print(f"⚠️  Namespace '{namespace}' not found!")
        print(f"Available: {list(namespaces.keys())[:5]}")
        return

    print()
    print("=" * 70)
    print("🔎 SEARCHING FOR 'DIRIGENTE' CONTENT")
    print("=" * 70)

    query_text = "chi è il dirigente scolastico del pessina?"
    print(f"\n🎯 Query: '{query_text}'")

    # Get embedding
    try:
        query_embedding = get_embedding(query_text)

        # Search in Pinecone
        query_url = "https://rag-pessina-db-skwro36.svc.aped-4627-b74a.pinecone.io/query"

        query_response = requests.post(
            query_url,
            headers=headers,
            json={
                "namespace": namespace,
                "vector": query_embedding,
                "topK": 5,
                "includeMetadata": True
            }
        )

        results = query_response.json()
        matches = results.get('matches', [])

        print(f"Found {len(matches)} results:\n")

        for i, match in enumerate(matches, 1):
            score = match.get('score', 0)
            print(f"Result #{i} (score: {score:.4f})")
            print(f"  ID: {match.get('id', 'N/A')}")

            metadata = match.get('metadata', {})
            text = metadata.get('text', '')

            if text:
                preview = text[:200] + "..." if len(text) > 200 else text
                print(f"  Text: {preview}")
                print(f"  Length: {len(text)} chars")

                # Check content
                if "dirigente" in text.lower() or "nora calzolaio" in text.lower():
                    print(f"  ✅ Contains dirigente info!")
                else:
                    print(f"  ⚠️  Missing dirigente info")

            # Other metadata
            for key in ['source', 'loc', 'filename']:
                if key in metadata:
                    print(f"  {key}: {metadata[key]}")
            print()

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

    print("=" * 70)
    print("✅ CHECK COMPLETE")
    print("=" * 70)

if __name__ == "__main__":
    main()
