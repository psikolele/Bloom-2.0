#!/usr/bin/env python3
"""
Scan all chunks in Pinecone to find those containing "Nora Calzolaio" or "dirigente"
"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()

def main():
    pinecone_key = os.getenv("PINECONE_API_KEY")
    host = "rag-pessina-db-skwro36.svc.aped-4627-b74a.pinecone.io"

    print("=" * 70)
    print("🔍 SCANNING ALL CHUNKS FOR 'NORA CALZOLAIO'")
    print("=" * 70)

    headers = {"Api-Key": pinecone_key, "Content-Type": "application/json"}

    # Use a zero vector to get arbitrary results, then scan through batches
    # We'll make multiple queries with different offsets

    all_nora_chunks = []
    all_dirigente_chunks = []

    print("\n📊 Scanning chunks in batches...\n")

    for batch in range(50):  # Scan up to 500 chunks (50 * 10)
        # Use different vectors to get different results
        # This is a hack since Pinecone doesn't have a "list all" API
        import random
        random.seed(batch)
        random_vector = [random.random() * 2 - 1 for _ in range(1536)]

        response = requests.post(
            f"https://{host}/query",
            headers=headers,
            json={
                "namespace": "",
                "vector": random_vector,
                "topK": 10,
                "includeMetadata": True
            }
        )

        matches = response.json().get('matches', [])

        for match in matches:
            chunk_id = match.get('id', '')
            text = match.get('metadata', {}).get('text', '').lower()

            if "nora calzolaio" in text:
                if chunk_id not in [c['id'] for c in all_nora_chunks]:
                    all_nora_chunks.append({
                        'id': chunk_id,
                        'text': match.get('metadata', {}).get('text', ''),
                        'score': match.get('score', 0)
                    })
                    print(f"✅ Found Nora Calzolaio in chunk {chunk_id}")

            if "dirigente" in text and chunk_id not in [c['id'] for c in all_dirigente_chunks]:
                all_dirigente_chunks.append({
                    'id': chunk_id,
                    'text': match.get('metadata', {}).get('text', ''),
                    'has_nora': "nora calzolaio" in text
                })

        if batch % 10 == 0:
            print(f"Scanned {(batch+1)*10} chunks... (Nora: {len(all_nora_chunks)}, Dirigente: {len(all_dirigente_chunks)})")

    print("\n" + "=" * 70)
    print("📊 RESULTS")
    print("=" * 70)

    print(f"\n✅ Chunks with 'Nora Calzolaio': {len(all_nora_chunks)}")
    for chunk in all_nora_chunks:
        print(f"\n  ID: {chunk['id']}")
        print(f"  Text preview: {chunk['text'][:200]}...")

    print(f"\n⚠️  Chunks with 'dirigente' but NO 'Nora Calzolaio': {sum(1 for c in all_dirigente_chunks if not c['has_nora'])}")
    for chunk in all_dirigente_chunks[:5]:  # Show first 5
        if not chunk['has_nora']:
            print(f"\n  ID: {chunk['id']}")
            print(f"  Text preview: {chunk['text'][:150]}...")

    print("\n" + "=" * 70)
    print("🔍 DIAGNOSIS")
    print("=" * 70)

    if len(all_nora_chunks) == 0:
        print("❌ NO chunks found with 'Nora Calzolaio' in the index!")
        print("   This means the organigramma chunk was NOT properly indexed.")
        print("\n🚨 Possible causes:")
        print("   1. File was processed but chunk text was truncated/modified")
        print("   2. Chunk exists but in different namespace")
        print("   3. Text encoding issue during indexing")
    else:
        print(f"✅ Found {len(all_nora_chunks)} chunk(s) with 'Nora Calzolaio'")
        print("❌ BUT they're not ranking high in similarity search!")
        print("\n🚨 This means:")
        print("   1. The embeddings don't match the query well")
        print("   2. The topK parameter might be too low")
        print("   3. Other chunks are ranking higher")

if __name__ == "__main__":
    main()
