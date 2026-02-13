# Istruzioni per Completare il Fix RAG

## 🎯 Problema Identificato

I chunk dell'organigramma esistono in Pinecone MA contengono HTML sporco che rovina gli embeddings:

```html
<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png"...
```

Questo fa sì che i chunk con "Nora Calzolaio" **non siano nemmeno nei top 30** risultati della similarity search!

## ✅ Soluzione

### Opzione 1: File Pulito (RACCOMANDATO)

1. **Elimina il vecchio file** `organigramma-pessina.md` dalla cartella Google Drive (ID: `1McMg9rriVUx6qpkZpfNwhVtd36ht6Nbe`)

2. **Carica il nuovo file pulito** da questo progetto:
   ```
   test_documents/organigramma-pessina.md
   ```

3. **Triggera il workflow** N8N sezione 5 per processare il file

4. **Verifica indicizzazione**:
   ```bash
   python3 check_nora_position.py
   ```
   Dovrebbe trovare "Nora Calzolaio" nei top 10

5. **Test dalla web app**:
   ```
   Query: "chi è il dirigente scolastico del pessina?"
   Risposta attesa: "Nora Calzolaio"
   ```

### Opzione 2: Aumentare topK (WORKAROUND)

Se non vuoi re-indicizzare, puoi aumentare il topK a 50-100 nel nodo "RAG Query Pinecone", ma questo:
- ❌ Consuma più risorse
- ❌ Potrebbe includere chunk non rilevanti
- ❌ Non risolve il problema alla radice

**Script per aumentare topK:**
```python
# TODO: creare script per update topK se necessario
```

### Opzione 3: Pulire Namespace e Re-indicizzare Tutto

Se vuoi pulire completamente:

1. **Elimina tutti i chunk** dal namespace default:
   ```bash
   python3 delete_all_chunks.py  # TODO: creare questo script
   ```

2. **Re-carica tutti i file** su Google Drive

3. **Triggera il workflow** per tutto

## 📊 Verifica Post-Fix

Dopo aver applicato la soluzione, verifica che funzioni:

```bash
# 1. Verifica che Nora Calzolaio sia nei top 10
python3 check_nora_position.py

# 2. Test similarity search
python3 search_nora_calzolaio.py

# 3. Test dalla web app Bloom 2.0
# Query: "chi è il dirigente scolastico del pessina?"
```

## 🔍 Debug se Ancora Non Funziona

Se dopo il fix il RAG ancora non risponde:

1. **Verifica execution N8N**: Controlla che il file sia stato processato senza errori

2. **Verifica chunk in Pinecone**:
   ```bash
   python3 check_nora_position.py
   ```

3. **Verifica score**: Se score < 0.3, potrebbe esserci un problema con l'embedding

4. **Controlla il prompt dell'LLM**: Forse l'LLM sta ignorando i chunk anche se recuperati

## 📁 File Coinvolti

- `test_documents/organigramma-pessina.md` - File pulito da caricare
- `check_nora_position.py` - Verifica ranking di "Nora Calzolaio"
- `search_nora_calzolaio.py` - Search test per debugging
- `scan_all_chunks.py` - Scan completo di tutti i chunk

## ⚠️ Note Importanti

- Il file pulito NON contiene HTML o markdown sporco
- Tutti i tag `[page:1]` sono stati rimossi
- L'informazione sul dirigente è chiara e all'inizio del documento
- Il file è ottimizzato per embedding semantico

---

**Data**: 13 Febbraio 2026
**Session**: claude/fix-n8n-pinecone-error-4Fde4
