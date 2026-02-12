#!/usr/bin/env python3
"""
Script per verificare che i chunk in Pinecone contengano contenuto reale
e non solo metadati.
"""

import requests
import json
import sys

PINECONE_API_KEY = "pcsk_2LUTsV_Q1CHVucguzS6Hf2v5udstb4V8F3L5umsCcrZDXDUhD3FELjdcE51TeJCn63H4sN"

INDICES = {
    "rag-pessina-db": "https://rag-pessina-db-skwro36.svc.aped-4627-b74a.pinecone.io",
    "rag-jobcourier-db": "https://rag-jobcourier-db-skwro36.svc.aped-4627-b74a.pinecone.io"
}

MIN_CHUNK_SIZE = 500  # Minimum expected chunk size for real content
MAX_METADATA_SIZE = 100  # Maximum size for metadata-only chunks


def check_index(index_name, host):
    """Check if an index has valid chunks with real content"""
    print(f"\n{'='*70}")
    print(f"📊 Checking: {index_name}")
    print(f"{'='*70}")

    # Get stats
    resp_stats = requests.post(
        f"{host}/describe_index_stats",
        headers={
            "Api-Key": PINECONE_API_KEY,
            "Content-Type": "application/json"
        }
    )

    if resp_stats.status_code != 200:
        print(f"❌ Failed to get stats: {resp_stats.status_code}")
        return False

    stats = resp_stats.json()
    total_vectors = stats.get('totalVectorCount', 0)

    print(f"\n📈 Total vectors: {total_vectors}")

    if total_vectors == 0:
        print("⚠️  Index is empty - no vectors found")
        print("   This is expected if you haven't re-triggered the workflow yet.")
        return None  # Not an error, just empty

    # Query sample vectors
    query_payload = {
        "vector": [0.1] * 1536,
        "topK": 10,
        "includeMetadata": True,
        "namespace": ""
    }

    resp_query = requests.post(
        f"{host}/query",
        headers={
            "Api-Key": PINECONE_API_KEY,
            "Content-Type": "application/json"
        },
        json=query_payload
    )

    if resp_query.status_code != 200:
        print(f"❌ Failed to query: {resp_query.status_code}")
        return False

    matches = resp_query.json().get('matches', [])

    if not matches:
        print("⚠️  No matches returned from query")
        return False

    print(f"\n📝 Analyzing {len(matches)} sample chunks:")
    print("-" * 70)

    valid_chunks = 0
    metadata_only_chunks = 0

    for i, match in enumerate(matches, 1):
        metadata = match.get('metadata', {})
        text = metadata.get('text', '')
        text_len = len(text)

        is_valid = text_len >= MIN_CHUNK_SIZE
        is_metadata_only = text_len <= MAX_METADATA_SIZE

        if is_valid:
            valid_chunks += 1
            status = "✅ VALID"
        elif is_metadata_only:
            metadata_only_chunks += 1
            status = "❌ METADATA ONLY"
        else:
            status = "⚠️  TOO SHORT"

        print(f"\n  Chunk {i}: {status}")
        print(f"    Length: {text_len} chars")
        print(f"    Preview: {text[:100]}...")

        if 'source' in metadata:
            print(f"    Source: {metadata.get('source')}")

    # Summary
    print(f"\n{'='*70}")
    print(f"📊 Summary for {index_name}:")
    print(f"{'='*70}")
    print(f"  Total vectors: {total_vectors}")
    print(f"  Valid chunks (>{MIN_CHUNK_SIZE} chars): {valid_chunks}/{len(matches)}")
    print(f"  Metadata-only chunks (<{MAX_METADATA_SIZE} chars): {metadata_only_chunks}/{len(matches)}")

    success = metadata_only_chunks == 0 and valid_chunks >= len(matches) * 0.8

    if success:
        print(f"\n✅ {index_name} is HEALTHY")
        print("   Chunks contain real content from documents")
    else:
        print(f"\n❌ {index_name} has ISSUES")
        print("   Chunks contain metadata instead of real content")
        print("\n🔧 Action needed:")
        print("   1. Make sure the workflow fix has been applied")
        print("   2. Re-trigger the workflow to re-index documents")
        print("   3. Run this script again to verify")

    return success


def main():
    print("="*70)
    print("RAG CHUNKS VERIFICATION SCRIPT")
    print("="*70)
    print("\nThis script checks if Pinecone indices contain real document content")
    print("or just metadata (file names).")

    results = {}

    for index_name, host in INDICES.items():
        result = check_index(index_name, host)
        results[index_name] = result

    # Final summary
    print("\n\n" + "="*70)
    print("FINAL SUMMARY")
    print("="*70)

    for index_name, result in results.items():
        if result is True:
            status = "✅ HEALTHY"
        elif result is False:
            status = "❌ ISSUES FOUND"
        else:
            status = "⚠️  EMPTY"

        print(f"  {index_name}: {status}")

    # Exit code
    if all(r in [True, None] for r in results.values()):
        print("\n✅ All indices are OK (healthy or empty)")
        sys.exit(0)
    else:
        print("\n❌ Some indices have issues - see details above")
        sys.exit(1)


if __name__ == "__main__":
    main()
