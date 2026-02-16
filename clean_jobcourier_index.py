#!/usr/bin/env python3
"""
Pulizia dell'index rag-jobcourier-db - rimuove tutti i chunk esistenti
prima del re-indexing con il workflow fixato
"""
import requests
import json

PINECONE_API_KEY = "pcsk_2LUTsV_Q1CHVucguzS6Hf2v5udstb4V8F3L5umsCcrZDXDUhD3FELjdcE51TeJCn63H4sN"
HOST = "https://rag-jobcourier-db-skwro36.svc.aped-4627-b74a.pinecone.io"

def clean_index():
    """Pulisce tutti i vettori dall'index rag-jobcourier-db"""
    print("=" * 70)
    print("🧹 PULIZIA INDEX rag-jobcourier-db")
    print("=" * 70)

    headers = {
        "Api-Key": PINECONE_API_KEY,
        "Content-Type": "application/json"
    }

    # 1. Verifica stato prima della pulizia
    print("\n📊 Stato PRIMA della pulizia:")
    resp_stats = requests.post(
        f"{HOST}/describe_index_stats",
        headers=headers
    )

    if resp_stats.status_code == 200:
        stats = resp_stats.json()
        total_before = stats.get('totalVectorCount', 0)
        print(f"   Total vectors: {total_before}")
        print(f"   Namespaces: {list(stats.get('namespaces', {}).keys())}")
    else:
        print(f"   ❌ Errore get stats: {resp_stats.status_code}")
        return False

    if total_before == 0:
        print("\n✅ Index già vuoto - nessuna pulizia necessaria")
        return True

    # 2. Conferma pulizia
    print(f"\n⚠️  Stai per eliminare {total_before} vettori dall'index rag-jobcourier-db")
    print("   Questa azione è IRREVERSIBILE!")
    print(f"   (Un backup è stato salvato in: backup_jobcourier_chunks_*.json)")

    user_input = input("\n   Procedere con la pulizia? (yes/no): ")

    if user_input.lower() not in ['yes', 'y', 'si', 'sì']:
        print("\n⏸️  Pulizia annullata")
        return False

    # 3. Elimina tutti i vettori nel namespace di default
    print("\n🗑️  Eliminazione in corso...")

    delete_payload = {
        "deleteAll": True,
        "namespace": ""
    }

    resp_delete = requests.post(
        f"{HOST}/vectors/delete",
        headers=headers,
        json=delete_payload
    )

    if resp_delete.status_code not in [200, 202]:
        print(f"\n❌ Errore delete: {resp_delete.status_code}")
        print(resp_delete.text)
        return False

    print("✅ Richiesta di delete inviata")

    # 4. Verifica stato dopo pulizia (attendi un po' per la propagazione)
    import time
    print("\n⏳ Attendo 3 secondi per la propagazione...")
    time.sleep(3)

    resp_stats_after = requests.post(
        f"{HOST}/describe_index_stats",
        headers=headers
    )

    if resp_stats_after.status_code == 200:
        stats_after = resp_stats_after.json()
        total_after = stats_after.get('totalVectorCount', 0)
        print(f"\n📊 Stato DOPO la pulizia:")
        print(f"   Total vectors: {total_after}")

        if total_after == 0:
            print("\n✅ Pulizia completata con successo!")
            print(f"   Eliminati: {total_before} vettori")
        else:
            print(f"\n⚠️  Pulizia parziale: rimangono {total_after} vettori")
            print("   (potrebbe richiedere più tempo per propagare)")
    else:
        print(f"\n⚠️  Impossibile verificare stato finale: {resp_stats_after.status_code}")

    print(f"\n{'='*70}")
    print("📝 PROSSIMI PASSI")
    print(f"{'='*70}")
    print("1. ✅ Index pulito e pronto per re-indexing")
    print("2. 📄 Carica file su Google Drive (cartella RAG Database JobCourier)")
    print("3. 🔄 Triggerare il workflow:")
    print("   - Automatico: attendi il prossimo schedule (ogni 30 min)")
    print("   - Manuale: esegui workflow da N8N UI")
    print("4. ✅ Verifica risultati:")
    print("   python3 scripts/verify_rag_chunks.py")
    print("\n💡 Expected results:")
    print("   - Total vectors: 15-50+ (dipende dalla dimensione dei file)")
    print("   - Tutti i chunk >500 caratteri (tranne eventualmente l'ultimo)")
    print("   - Source = nome file reale (non 'blob')")
    print("   - NO chunk <100 caratteri (metadata-only)")

    return True

if __name__ == "__main__":
    import sys

    success = clean_index()

    if success:
        print("\n✅ Operazione completata")
        sys.exit(0)
    else:
        print("\n❌ Operazione fallita o annullata")
        sys.exit(1)
