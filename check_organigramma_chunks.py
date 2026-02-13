#!/usr/bin/env python3
"""
Script to verify organigramma chunks in Pinecone for folder 1McMg9rriVUx6qpkZpfNwhVtd36ht6Nbe
"""
import os
from pinecone import Pinecone
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def main():
    # Initialize Pinecone
    api_key = os.getenv("PINECONE_API_KEY")
    if not api_key:
        print("❌ PINECONE_API_KEY not found in .env")
        return

    pc = Pinecone(api_key=api_key)

    # Connect to index
    index_name = "rag-pessina-db"
    index = pc.Index(index_name)

    # Folder ID from the query
    folder_id = "1McMg9rriVUx6qpkZpfNwhVtd36ht6Nbe"
    namespace = f"folder-{folder_id}"

    print("=" * 70)
    print(f"🔍 CHECKING ORGANIGRAMMA CHUNKS IN PINECONE")
    print("=" * 70)
    print(f"Index: {index_name}")
    print(f"Namespace: {namespace}")
    print()

    # Get index stats
    stats = index.describe_index_stats()
    print(f"📊 Total vectors in index: {stats.total_vector_count}")

    if namespace in stats.namespaces:
        ns_count = stats.namespaces[namespace].vector_count
        print(f"📊 Vectors in namespace '{namespace}': {ns_count}")
    else:
        print(f"⚠️  Namespace '{namespace}' not found!")
        print(f"Available namespaces: {list(stats.namespaces.keys())}")
        return

    print()
    print("=" * 70)
    print("🔎 SEARCHING FOR ORGANIGRAMMA CONTENT")
    print("=" * 70)

    # Search for "dirigente" content
    query_text = "chi è il dirigente scolastico del pessina?"

    # Create a simple embedding (we'll use the OpenAI-compatible endpoint)
    import openai
    openai.api_base = "https://openrouter.ai/api/v1"
    openai.api_key = os.getenv("OPENROUTER_API_KEY")

    # Get embedding for the query
    try:
        response = openai.embeddings.create(
            model="text-embedding-3-small",
            input=query_text
        )
        query_embedding = response.data[0].embedding

        # Search in Pinecone
        results = index.query(
            namespace=namespace,
            vector=query_embedding,
            top_k=5,
            include_metadata=True
        )

        print(f"\n🎯 Query: '{query_text}'")
        print(f"Found {len(results.matches)} results:\n")

        for i, match in enumerate(results.matches, 1):
            print(f"Result #{i} (score: {match.score:.4f})")
            print(f"  ID: {match.id}")
            metadata = match.metadata

            if 'text' in metadata:
                text = metadata['text']
                # Show first 200 chars
                preview = text[:200] + "..." if len(text) > 200 else text
                print(f"  Text preview: {preview}")
                print(f"  Text length: {len(text)} chars")

                # Check if mentions dirigente
                if "dirigente" in text.lower() or "nora calzolaio" in text.lower():
                    print(f"  ✅ Contains dirigente info!")
                else:
                    print(f"  ⚠️  Does NOT contain dirigente info")

            # Show other metadata
            for key, value in metadata.items():
                if key != 'text':
                    print(f"  {key}: {value}")
            print()

    except Exception as e:
        print(f"❌ Error during search: {e}")
        print("\nTrying direct fetch of vectors...")

        # Try to fetch some vectors directly
        try:
            # Fetch first few vectors from namespace
            results = index.query(
                namespace=namespace,
                vector=[0.0] * 1536,  # Dummy vector
                top_k=10,
                include_metadata=True
            )

            print(f"\n📋 Sample of {len(results.matches)} chunks from namespace:")
            for i, match in enumerate(results.matches[:5], 1):
                metadata = match.metadata
                print(f"\nChunk #{i}:")
                print(f"  ID: {match.id}")

                if 'text' in metadata:
                    text = metadata['text']
                    preview = text[:150] + "..." if len(text) > 150 else text
                    print(f"  Text: {preview}")
                    print(f"  Length: {len(text)} chars")

                # Show filename if available
                if 'source' in metadata:
                    print(f"  Source: {metadata['source']}")
                if 'loc' in metadata:
                    print(f"  Location: {metadata['loc']}")

        except Exception as e2:
            print(f"❌ Error fetching vectors: {e2}")

    print("\n" + "=" * 70)
    print("✅ CHECK COMPLETE")
    print("=" * 70)

if __name__ == "__main__":
    main()
