# CLAUDE.md - Istruzioni per Claude

## Regole di Progetto

### Backup Workflow N8N

**IMPORTANTE**: Prima di modificare qualsiasi file di workflow N8N (`.json`), esegui SEMPRE un backup nella cartella dedicata:

```
/backup-n8n/
```

**Procedura**:
1. Crea la cartella `backup-n8n/` se non esiste
2. Copia il file workflow con nome: `{nome-originale}_backup_{YYYY-MM-DD_HH-mm}.json`
3. Solo dopo il backup, procedi con le modifiche

**Esempio**:
```
n8n-workflow-captionflow.json  →  backup-n8n/n8n-workflow-captionflow_backup_2026-01-22_14-30.json
```

---

## Versioning dell'Applicazione

**IMPORTANTE**: Il footer dell'applicazione deve SEMPRE mostrare la versione corrente nel seguente formato:

```
MarketingFlow © 2026 — Powered By BLC sa — v.DDMM.HHMM
```

**Formato versione**: `v.DDMM.HHMM`
- **DD** = giorno (es. 22)
- **MM** = mese (es. 01)
- **HH** = ora del deploy (es. 14)
- **MM** = minuti del deploy (es. 30)

**Esempio**: `v.2201.1430` (deploy del 22 gennaio alle 14:30)

**Quando aggiornare la versione**:
- Ad ogni deploy dell'applicazione
- Ad ogni modifica del codice HTML, CSS o JavaScript
- Utilizzare sempre data e ora del momento del deploy

**Posizione**: File `index.html`, tag `<footer class="footer">`

---

## Struttura Progetto

- `index.html` - Frontend principale
- `js/app.js` - Logica applicazione e integrazione webhook
- `css/styles.css` - Stili MarketingFlow
- `n8n-workflow-captionflow.json` - Workflow N8N esportato
- `backup-n8n/` - Backup dei workflow prima delle modifiche

## Webhook N8N

- **URL**: `https://emanueleserra.app.n8n.cloud/webhook/caption-flow`
- **Workflow ID**: `#T1faX7EmrumACUVb`
