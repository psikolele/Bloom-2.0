# Notion Session Creator — Configurazione Guidata

Questo comando va eseguito ogni volta che l'utente chiede di creare una sessione o una pagina nel DB Notion "Sessioni di lavoro".

## Istruzioni per Claude

### Step 1 — Proponi i minuti della sessione

Prima di fare qualsiasi altra cosa, analizza la conversazione corrente e stima la durata della sessione di lavoro. Proponi un valore realistico basato su:
- Numero di messaggi scambiati
- Complessità dei task affrontati
- Tipica durata di sessioni simili (di solito 60–240 minuti)

Comunica all'utente: "Propongo **X minuti** per questa sessione — confermi o modifichi?"

---

### Step 2 — Fetch progetti da Notion (automatico, live)

Esegui il seguente comando per recuperare i progetti disponibili nel workspace Notion:

```bash
python3 -c "
import os, json, requests

key = os.environ.get('NOTION_API_KEY', '')
if not key:
    # Prova dal file .env
    try:
        for line in open(os.path.expanduser('~/Bloom-2.0/.env')):
            if line.startswith('NOTION_API_KEY='):
                key = line.strip().split('=', 1)[1].strip()
    except: pass

if not key:
    print('ERRORE: NOTION_API_KEY non trovata. Impostala nel file .env o come variabile di ambiente.')
    exit(1)

headers = {
    'Authorization': f'Bearer {key}',
    'Notion-Version': '2022-06-28',
    'Content-Type': 'application/json'
}

# Cerca tutte le pagine (progetti)
resp = requests.post('https://api.notion.com/v1/search', json={
    'filter': {'value': 'page', 'property': 'object'},
    'page_size': 100
}, headers=headers)

if resp.status_code != 200:
    print(f'ERRORE API: {resp.status_code} {resp.text[:200]}')
    exit(1)

results = resp.json().get('results', [])
progetti = []
for r in results:
    props = r.get('properties', {})
    title = ''
    for k, v in props.items():
        if v.get('type') == 'title':
            texts = v.get('title', [])
            if texts:
                title = texts[0].get('text', {}).get('content', '').strip()
    if title:
        progetti.append({'id': r['id'], 'nome': title})

# Recupera anche le opzioni di categoria dal DB sessioni
DB_ID = 'c024f662-8528-4572-86bb-8c1809680da2'
db_resp = requests.get(f'https://api.notion.com/v1/databases/{DB_ID}', headers=headers)
categorie = []
if db_resp.status_code == 200:
    db_data = db_resp.json()
    props = db_data.get('properties', {})
    if 'Categoria' in props:
        options = props['Categoria'].get('select', {}).get('options', [])
        categorie = [o['name'] for o in options]

print('=== PROGETTI ===')
for p in sorted(progetti, key=lambda x: x['nome']):
    print(f'  [{p[\"id\"]}] {p[\"nome\"]}')
print()
print('=== CATEGORIE DAL DB ===')
for c in categorie:
    print(f'  - {c}')
"
```

Mostra all'utente la lista dei progetti nel formato:
```
Progetti disponibili su Notion:
1. Nome Progetto A
2. Nome Progetto B
3. ...
(oppure "Nessun progetto correlato")
```

---

### Step 3 — Lista categorie (statica — aggiornata al 2026-03-01)

> **Nota per Claude**: usa questa lista come fallback se il fetch delle categorie fallisce, o se l'utente preferisce vederla subito. Controlla periodicamente se ci sono nuove categorie nel DB e aggiorna questa sezione.

```
CATEGORIE DISPONIBILI:
  1. Sviluppo       → Implementazione features, coding, architettura
  2. Debug          → Risoluzione errori, fix workflow, troubleshooting
  3. Design         → UI/UX, grafica, brand identity, layout
  4. DevOps         → Infrastruttura, deploy, CI/CD, server, N8N workflow
  5. Ricerca        → Analisi, studio tecnologie, documentazione tecnica
  6. Marketing      → Contenuti, social, campagne, caption flow
  7. Meeting        → Riunioni, call, allineamenti con il team/clienti
  8. Manutenzione   → Aggiornamenti dipendenze, backup, cleanup, monitoring
  9. Integrazione   → Collegamento servizi esterni (API, webhook, Notion, ecc.)
 10. Formazione     → Studio, corsi, apprendimento nuovi tool
```

Mostra la lista all'utente e chiedi di scegliere una categoria.

---

### Step 4 — Raccolta informazioni complete

Fai queste domande in un unico messaggio, ordinato e chiaro:

```
Perfetto! Ho bisogno di questi ultimi dettagli per creare la sessione su Notion:

① MINUTI: Ho proposto [X] minuti — confermi o preferisci un numero diverso?

② PROGETTO COLLEGATO: Quale progetto vuoi collegare?
   [lista recuperata al Step 2]
   (oppure "nessuno")

③ CATEGORIA: Quale categoria descrive meglio questa sessione?
   [lista Step 3]

④ TITOLO BREVE: Un titolo conciso per la sessione (es: "Fix RAG N8N + Pinecone Debug")

⑤ NOTE BREVI: Una riga di contesto rapido da salvare nelle note Notion
```

---

### Step 5 — Crea la pagina Notion con stile HTML/Rich

Una volta raccolte tutte le informazioni, genera e lancia uno script Python che:

1. Usa il `DATABASE_ID = "c024f662-8528-4572-86bb-8c1809680da2"`
2. Crea la pagina con queste **properties**:
   ```python
   properties = {
       "Descrizione Breve": {"title": [{"text": {"content": TITOLO}}]},
       "Data Sessione": {"date": {"start": DATA_OGGI}},  # formato YYYY-MM-DD
       "Minuti Lavorati": {"number": MINUTI},
       "Categoria": {"select": {"name": CATEGORIA}},
       "Note": {"rich_text": [{"text": {"content": NOTE}}]},
       "Progetto Collegato": {"relation": [{"id": PROJECT_ID}]}  # solo se scelto
   }
   ```

3. Costruisce il corpo della pagina con **blocchi Notion** in stile HTML ricco:

   **Struttura obbligatoria dei blocchi:**
   ```
   [callout blu] → Descrizione sintetica della sessione (2-3 righe)

   [heading_1] 📋 Argomenti Trattati
   [heading_2] 1. Titolo Argomento Principale
   [paragraph] Contesto: ...
   [paragraph] Problema identificato: ...
   [bulleted_list] attività svolte
   [paragraph] Risultato: ✅ ...

   [heading_1] 🎯 Decisioni Chiave
   [bulleted_list] decisioni importanti prese durante la sessione

   [divider]

   [heading_1] 📊 Metriche e Risultati (se applicabile)
   [bulleted_list] risultati quantitativi

   [divider]

   [heading_1] 🔗 Riferimenti
   [bulleted_list] tool usati, file modificati, URL, branch git, commit

   [divider]

   [heading_1] 🔮 Prossimi Passi
   [bulleted_list] cosa fare nella prossima sessione
   ```

4. Usa come emoji dell'icona pagina:
   - 💻 per Sviluppo
   - 🐛 per Debug
   - 🎨 per Design
   - ⚙️ per DevOps
   - 🔬 per Ricerca
   - 📣 per Marketing
   - 🤝 per Meeting
   - 🔧 per Manutenzione
   - 🔗 per Integrazione
   - 📚 per Formazione

5. Dopo la creazione, mostra all'utente:
   ```
   ✅ Sessione creata su Notion!
   📄 URL: [url pagina]
   ⏱️  Minuti: X
   📁 Progetto: Nome Progetto
   🏷️  Categoria: Sviluppo
   ```

---

## Regole Generali

- **Chiedi sempre** queste domande prima di creare qualsiasi pagina Notion, senza eccezioni
- **Non creare mai** la pagina senza avere: minuti, categoria, titolo breve, note
- **Il progetto collegato** è opzionale — se l'utente dice "nessuno" o "salta", ometti il campo
- **La descrizione della pagina** deve essere generata da Claude basandosi sulla sessione di chat corrente — non inventare, racconta fedelmente cosa si è fatto
- **Stile rich text**: usa sempre callout, heading gerarchici (h1/h2/h3), bulleted list, divider — mai pagine piatte con solo testo
- **NOTION_API_KEY**: leggi da `$NOTION_API_KEY` (env) oppure da `~/Bloom-2.0/.env`

---

## Aggiornamento Settimanale

Claude deve ricordare di verificare circa ogni 7 giorni se:
1. Ci sono nuovi **progetti** su Notion (il fetch live li recupera automaticamente)
2. Ci sono nuove **categorie** aggiunte al DB (controlla `properties.Categoria.select.options`)
3. Se ci sono nuove categorie, aggiorna la lista statica nello Step 3 di questo file
