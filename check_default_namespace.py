#!/usr/bin/env python3
"""
Check what's in the default (empty) namespace
"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()

def main():
    api_key = os.getenv("PINECONE_API_KEY")
    host = "rag-pessina-db-skwro36.svc.aped-4627-b74a.pinecone.io"

    print("=" * 70)
    print("🔍 CHECKING DEFAULT NAMESPACE")
    print("=" * 70)

    headers = {"Api-Key": api_key, "Content-Type": "application/json"}

    # Query with a zero vector to get some results
    query_url = f"https://{host}/query"

    response = requests.post(
        query_url,
        headers=headers,
        json={
            "namespace": "",  # Default namespace
            "vector": [0.0] * 1536,
            "topK": 10,
            "includeMetadata": True
        }
    )

    if response.status_code != 200:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
        return

    results = response.json()
    matches = results.get('matches', [])

    print(f"\n📋 Found {len(matches)} chunks in default namespace:\n")

    for i, match in enumerate(matches, 1):
        metadata = match.get('metadata', {})
        print(f"Chunk #{i}:")
        print(f"  ID: {match.get('id', 'N/A')}")

        # Show all metadata
        for key, value in metadata.items():
            if key == 'text':
                text = str(value)
                preview = text[:150] + "..." if len(text) > 150 else text
                print(f"  {key}: {preview}")
            else:
                print(f"  {key}: {value}")
        print()

    print("=" * 70)

if __name__ == "__main__":
    main()
