#!/usr/bin/env python3
"""
Search for dirigente info in default namespace
"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()

def main():
    api_key = os.getenv("OPENROUTER_API_KEY")

    # Get embedding for "dirigente"
    print("🔍 Getting embedding for query...")
    response = requests.post(
        "https://openrouter.ai/api/v1/embeddings",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        json={
            "model": "openai/text-embedding-3-small",
            "input": "chi è il dirigente scolastico del pessina nora calzolaio"
        }
    )

    embedding = response.json()["data"][0]["embedding"]

    # Search in default namespace
    pinecone_key = os.getenv("PINECONE_API_KEY")
    host = "rag-pessina-db-skwro36.svc.aped-4627-b74a.pinecone.io"

    print("🔎 Searching in default namespace...\n")

    search_response = requests.post(
        f"https://{host}/query",
        headers={"Api-Key": pinecone_key, "Content-Type": "application/json"},
        json={
            "namespace": "",
            "vector": embedding,
            "topK": 3,
            "includeMetadata": True
        }
    )

    matches = search_response.json().get('matches', [])

    print("=" * 70)
    print("🎯 TOP 3 RESULTS FOR 'CHI È IL DIRIGENTE DEL PESSINA?'")
    print("=" * 70)

    for i, match in enumerate(matches, 1):
        score = match.get('score', 0)
        text = match.get('metadata', {}).get('text', '')

        print(f"\nResult #{i} (similarity: {score:.4f}):")
        print("-" * 70)
        print(text[:400] + "..." if len(text) > 400 else text)

        # Check if contains dirigente info
        if "dirigente" in text.lower():
            print("\n✅ CONTAINS 'DIRIGENTE'!")
        if "nora calzolaio" in text.lower():
            print("✅ CONTAINS 'NORA CALZOLAIO'!")

    print("\n" + "=" * 70)
    print("📊 SUMMARY")
    print("=" * 70)

    # Check if ANY result has the info
    has_dirigente = any("dirigente" in m.get('metadata', {}).get('text', '').lower() for m in matches)
    has_name = any("nora calzolaio" in m.get('metadata', {}).get('text', '').lower() for m in matches)

    if has_dirigente and has_name:
        print("✅ Organigramma chunks EXIST and CONTAIN the dirigente info!")
        print("❌ BUT they're in the WRONG namespace (default '' instead of folder-specific)")
    elif has_dirigente:
        print("⚠️  Chunks mention 'dirigente' but not 'Nora Calzolaio'")
    else:
        print("❌ Chunks don't contain dirigente information")

if __name__ == "__main__":
    main()
