#!/usr/bin/env python3
"""
Search for "Nora Calzolaio" in all Pinecone chunks
"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()

def main():
    pinecone_key = os.getenv("PINECONE_API_KEY")
    host = "rag-pessina-db-skwro36.svc.aped-4627-b74a.pinecone.io"

    print("=" * 70)
    print("🔍 SEARCHING FOR 'NORA CALZOLAIO' IN PINECONE")
    print("=" * 70)

    # Get embedding for "Nora Calzolaio dirigente"
    openrouter_key = os.getenv("OPENROUTER_API_KEY")

    response = requests.post(
        "https://openrouter.ai/api/v1/embeddings",
        headers={
            "Authorization": f"Bearer {openrouter_key}",
            "Content-Type": "application/json"
        },
        json={
            "model": "openai/text-embedding-3-small",
            "input": "Nora Calzolaio dirigente scolastico pessina"
        }
    )

    embedding = response.json()["data"][0]["embedding"]

    # Search in Pinecone
    headers = {"Api-Key": pinecone_key, "Content-Type": "application/json"}

    print("\n🎯 Searching with query: 'Nora Calzolaio dirigente scolastico pessina'\n")

    search_response = requests.post(
        f"https://{host}/query",
        headers=headers,
        json={
            "namespace": "",  # Default namespace
            "vector": embedding,
            "topK": 10,
            "includeMetadata": True
        }
    )

    results = search_response.json()
    matches = results.get('matches', [])

    print(f"Found {len(matches)} results:\n")
    print("=" * 70)

    found_nora = False

    for i, match in enumerate(matches, 1):
        score = match.get('score', 0)
        chunk_id = match.get('id', 'N/A')
        text = match.get('metadata', {}).get('text', '')

        print(f"\n#{i} - ID: {chunk_id}")
        print(f"Score: {score:.4f}")

        # Check if contains Nora Calzolaio
        if "nora calzolaio" in text.lower():
            found_nora = True
            print("✅ CONTAINS 'NORA CALZOLAIO'!")
            print(f"\nFull text:")
            print("-" * 70)
            print(text)
            print("-" * 70)
        else:
            # Show preview
            preview = text[:200] + "..." if len(text) > 200 else text
            print(f"Text preview: {preview}")

            # Check for other keywords
            if "dirigente" in text.lower():
                print("⚠️  Contains 'dirigente' but NOT 'Nora Calzolaio'")

    print("\n" + "=" * 70)
    print("📊 SUMMARY")
    print("=" * 70)

    if found_nora:
        print("✅ Found chunks with 'Nora Calzolaio'")
        print("❌ BUT they're not ranking high enough in similarity search!")
        print("\n🔍 Possible issues:")
        print("  1. Embedding model not capturing semantic meaning well")
        print("  2. Query phrasing doesn't match chunk content")
        print("  3. Other chunks have higher similarity scores")
    else:
        print("❌ NO chunks found with 'Nora Calzolaio'")
        print("\n🔍 Checking if chunk exists by ID...")

        # Try to fetch the specific chunk by ID
        fetch_response = requests.post(
            f"https://{host}/fetch",
            headers=headers,
            json={
                "ids": ["78c59f98-a74a-4378-81d9-58759e95aea6"],
                "namespace": ""
            }
        )

        fetch_result = fetch_response.json()
        vectors = fetch_result.get('vectors', {})

        if '78c59f98-a74a-4378-81d9-58759e95aea6' in vectors:
            print("\n✅ Chunk 78c59f98-a74a-4378-81d9-58759e95aea6 EXISTS!")
            chunk_text = vectors['78c59f98-a74a-4378-81d9-58759e95aea6'].get('metadata', {}).get('text', '')
            print(f"\nChunk text:")
            print("-" * 70)
            print(chunk_text)
            print("-" * 70)

            if "nora calzolaio" in chunk_text.lower():
                print("\n✅ This chunk CONTAINS 'Nora Calzolaio'!")
                print("❌ BUT it wasn't returned in top 10 similarity search results!")
                print("\n🚨 ROOT CAUSE: Similarity search is NOT finding the right chunk!")
            else:
                print("\n⚠️  This chunk does NOT contain 'Nora Calzolaio'")
        else:
            print("\n❌ Chunk 78c59f98-a74a-4378-81d9-58759e95aea6 NOT FOUND in Pinecone!")

if __name__ == "__main__":
    main()
