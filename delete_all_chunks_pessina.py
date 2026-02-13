#!/usr/bin/env python3
"""
Delete all chunks from Pinecone rag-pessina-db namespace
"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()

def main():
    api_key = os.getenv("PINECONE_API_KEY")
    host = "rag-pessina-db-skwro36.svc.aped-4627-b74a.pinecone.io"
    namespace = ""  # Default namespace

    print("=" * 70)
    print("🗑️  DELETING ALL CHUNKS FROM PINECONE")
    print("=" * 70)
    print(f"Index: rag-pessina-db")
    print(f"Namespace: '{namespace}' (default)")
    print()

    headers = {"Api-Key": api_key, "Content-Type": "application/json"}

    # Get current stats
    stats_response = requests.post(
        f"https://{host}/describe_index_stats",
        headers=headers,
        json={}
    )
    stats = stats_response.json()

    current_count = stats.get('namespaces', {}).get(namespace, {}).get('vectorCount', 0)
    total_count = stats.get('totalVectorCount', 0)

    print(f"📊 Current state:")
    print(f"   Total vectors in index: {total_count}")
    print(f"   Vectors in namespace '': {current_count}")
    print()

    if current_count == 0:
        print("✅ Namespace already empty, nothing to delete!")
        return

    # Confirm deletion
    print(f"⚠️  WARNING: This will delete ALL {current_count} chunks!")
    print(f"   This includes:")
    print(f"   - PTOF documents")
    print(f"   - Organigramma documents")
    print(f"   - Any other indexed documents")
    print()

    # Delete all vectors in the namespace
    print("🚀 Deleting all vectors...")

    delete_response = requests.post(
        f"https://{host}/vectors/delete",
        headers=headers,
        json={
            "deleteAll": True,
            "namespace": namespace
        }
    )

    if delete_response.status_code == 200:
        print("✅ Delete request successful!")

        # Verify deletion
        print("\n🔍 Verifying deletion...")
        verify_response = requests.post(
            f"https://{host}/describe_index_stats",
            headers=headers,
            json={}
        )

        new_stats = verify_response.json()
        new_count = new_stats.get('namespaces', {}).get(namespace, {}).get('vectorCount', 0)

        print(f"📊 New vector count: {new_count}")

        if new_count == 0:
            print("\n" + "=" * 70)
            print("✅ ALL CHUNKS DELETED SUCCESSFULLY")
            print("=" * 70)
            print("\n🎯 Next steps:")
            print("   1. Upload organigramma-pessina.md to Google Drive")
            print("   2. Trigger workflow to re-index")
            print("   3. Test RAG query")
        else:
            print(f"\n⚠️  Warning: {new_count} vectors still remain")
            print("   Deletion might take a moment to propagate")
    else:
        print(f"❌ Delete failed: {delete_response.status_code}")
        print(f"Response: {delete_response.text}")

if __name__ == "__main__":
    main()
