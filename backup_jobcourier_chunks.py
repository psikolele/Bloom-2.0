#!/usr/bin/env python3
"""
Backup dei 6 chunk esistenti da rag-jobcourier-db prima della pulizia e re-indexing
"""
import requests
import json
from datetime import datetime

PINECONE_API_KEY = "pcsk_2LUTsV_Q1CHVucguzS6Hf2v5udstb4V8F3L5umsCcrZDXDUhD3FELjdcE51TeJCn63H4sN"
HOST = "https://rag-jobcourier-db-skwro36.svc.aped-4627-b74a.pinecone.io"

def backup_chunks():
    """Backup all chunks from rag-jobcourier-db"""
    print("=" * 70)
    print("🔄 BACKUP CHUNKS da rag-jobcourier-db")
    print("=" * 70)

    headers = {
        "Api-Key": PINECONE_API_KEY,
        "Content-Type": "application/json"
    }

    # Query per ottenere tutti i chunk
    query_payload = {
        "namespace": "",
        "vector": [0.1] * 1536,
        "topK": 10,
        "includeMetadata": True,
        "includeValues": False  # Non serve il vettore per il backup
    }

    response = requests.post(
        f"{HOST}/query",
        headers=headers,
        json=query_payload
    )

    if response.status_code != 200:
        print(f"❌ Errore query Pinecone: {response.status_code}")
        print(response.text)
        return None

    matches = response.json().get('matches', [])

    print(f"\n✅ Trovati {len(matches)} chunk da backuppare")

    # Prepara backup data
    backup_data = {
        "timestamp": datetime.now().isoformat(),
        "index": "rag-jobcourier-db",
        "namespace": "",
        "total_chunks": len(matches),
        "chunks": []
    }

    # Analizza e salva i chunk
    unique_texts = set()
    duplicates_count = 0

    for i, match in enumerate(matches, 1):
        metadata = match.get('metadata', {})
        text = metadata.get('text', '')
        text_len = len(text)
        chunk_id = match.get('id', '')

        chunk_data = {
            "id": chunk_id,
            "score": match.get('score', 0),
            "metadata": metadata,
            "text_length": text_len
        }

        backup_data["chunks"].append(chunk_data)

        # Check duplicati
        if text in unique_texts:
            duplicates_count += 1
            print(f"  🔄 Chunk {i} - DUPLICATO - {text_len} chars - ID: {chunk_id[:20]}...")
        else:
            unique_texts.add(text)
            print(f"  ✅ Chunk {i} - UNICO - {text_len} chars - ID: {chunk_id[:20]}...")
            if text_len < 100:
                print(f"      ⚠️  TROPPO PICCOLO: {text[:80]}...")

    # Salva backup su file
    backup_filename = f"backup_jobcourier_chunks_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(backup_filename, 'w', encoding='utf-8') as f:
        json.dump(backup_data, f, ensure_ascii=False, indent=2)

    print(f"\n{'='*70}")
    print(f"📊 SUMMARY")
    print(f"{'='*70}")
    print(f"  Total chunks: {len(matches)}")
    print(f"  Chunk unici: {len(unique_texts)}")
    print(f"  Duplicati: {duplicates_count}")
    print(f"  Backup salvato: {backup_filename}")

    # Analisi contenuto
    print(f"\n{'='*70}")
    print(f"📄 ANALISI CONTENUTO")
    print(f"{'='*70}")

    for i, text in enumerate(sorted(unique_texts, key=len, reverse=True), 1):
        print(f"\n  Chunk unico #{i} ({len(text)} chars):")
        print(f"  {text[:200]}...")

    return backup_filename

if __name__ == "__main__":
    backup_file = backup_chunks()

    if backup_file:
        print(f"\n✅ Backup completato: {backup_file}")
        print("\n💡 Prossimi passi:")
        print("   1. Connettere Text Splitter al workflow")
        print("   2. Testare con file di esempio")
        print("   3. Pulire index: python3 clean_jobcourier_index.py")
        print("   4. Re-triggerare workflow per re-indexing")
    else:
        print("\n❌ Backup fallito")
