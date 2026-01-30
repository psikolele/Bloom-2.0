# 🚀 Bloom AI - Setup Flusso Registrazione con Email

Questa guida spiega come configurare il nuovo flusso di registrazione con email di conferma e popup Brand Profile.

## 📋 Modifiche Implementate

### 1. **Email di Conferma Registrazione**
Quando un utente si registra per la prima volta, riceve automaticamente una email di benvenuto con:
- ✅ Nome utente (NO password per sicurezza)
- ✅ Email dell'account
- ✅ Data e ora di registrazione
- ✅ Template HTML professionale con brand guidelines Bloom AI
- ✅ CTA button per accedere alla dashboard
- ✅ Preview delle funzionalità disponibili

### 2. **Popup Brand Profile Post-Registrazione**
Dopo la registrazione, appare un modal elegante che propone:
- **Opzione 1**: "Compila Brand Profile" → redirect a `/brand-profile`
- **Opzione 2**: "Vai alla Dashboard" → redirect a `/`
- Design coerente con lo stile tech/moderno di Bloom AI
- Animazioni smooth e user-friendly

---

## 🔧 Setup N8N Workflow

### Prerequisiti
1. Accesso a N8N Cloud: https://emanueleserra.app.n8n.cloud
2. API Key N8N (Settings → API)
3. Account email SMTP configurato

### Step 1: Configurare Credenziali SMTP

1. Vai su **N8N → Settings → Credentials**
2. Crea nuova credenziale di tipo **"SMTP"**
3. Scegli uno dei servizi consigliati:

#### Opzione A: SendGrid (Raccomandato)
- **Motivo**: 100 email/giorno gratis, alta deliverability, no blocchi
- **SMTP Host**: `smtp.sendgrid.net`
- **Port**: `587`
- **User**: `apikey`
- **Password**: La tua SendGrid API Key
- **Secure Connection**: TLS

**Come ottenere API Key SendGrid:**
1. Crea account su https://sendgrid.com
2. Vai su Settings → API Keys
3. Crea una nuova API Key con permessi "Mail Send"

#### Opzione B: Gmail SMTP (Limitato)
- **SMTP Host**: `smtp.gmail.com`
- **Port**: `587`
- **User**: tua email Gmail
- **Password**: App Password (non la password normale)
- **Secure Connection**: TLS

**⚠️ Attenzione**: Gmail ha limite di ~500 email/giorno e può bloccare l'account

#### Opzione C: Custom SMTP
Usa le credenziali del tuo provider SMTP aziendale.

### Step 2: Deploy Workflow N8N

1. **Configura API Key**:
   ```bash
   # Crea file di configurazione
   nano ~/n8n_config.json
   ```

   Inserisci:
   ```json
   {
     "api_key": "TUA_N8N_API_KEY",
     "base_url": "https://emanueleserra.app.n8n.cloud/api/v1"
   }
   ```

2. **Esegui lo script di deployment**:
   ```bash
   cd /path/to/Bloom-2.0
   python3 deploy_auth_with_email.py
   ```

3. **Configura il nodo Email**:
   - Apri il workflow in N8N UI
   - Trova il nodo "Send Welcome Email"
   - Nella sezione "Credentials", seleziona la credenziale SMTP creata al Step 1
   - Salva il workflow

4. **Testa il workflow**:
   - Attiva il workflow
   - Prova a registrare un nuovo utente
   - Verifica che l'email arrivi correttamente

---

## 🎨 Personalizzazione Email Template

Il template HTML è definito nel workflow JSON. Per modificarlo:

1. Apri il file: `backup_workflows/Bloom_AI_Unified_Auth_WITH_EMAIL.json`
2. Trova il nodo `"send-welcome-email"`
3. Modifica il parametro `"message"` (HTML completo)
4. Re-deploy con `python3 deploy_auth_with_email.py`

### Variabili Disponibili
Nel template puoi usare:
- `{{ $('Webhook').item.json.body.username }}` - Nome utente
- `{{ $('Webhook').item.json.body.email }}` - Email
- `{{ $now.format('DD/MM/YYYY HH:mm') }}` - Data/ora corrente

### Brand Colors
I colori del brand Bloom AI:
- **Accent Orange**: `#FF6B35`
- **Accent Glow**: `#FF9B75`
- **Purple**: `#B349C1`
- **Void (Background)**: `#030303`
- **Surface**: `#0A0A0A`

---

## 🧪 Testing

### Test Registrazione Completa

1. **Frontend Test**:
   ```bash
   npm run dev
   ```
   - Vai su http://localhost:5173/login
   - Clicca su "Non hai un account? Registrati"
   - Compila i campi e invia

2. **Verifica Email**:
   - Controlla la casella email specificata
   - Verifica che l'email arrivi entro 1-2 minuti
   - Controlla spam/promozioni se non arriva

3. **Verifica Popup**:
   - Dopo registrazione, deve apparire il modal Brand Profile
   - Testa entrambi i pulsanti:
     - "Compila Brand Profile" → vai a `/brand-profile`
     - "Vai alla Dashboard" → vai a `/`

### Debug Email

Se l'email non arriva:

1. **Controlla N8N Execution Log**:
   - N8N UI → Executions
   - Trova l'esecuzione del workflow "Bloom AI Unified Auth"
   - Verifica il nodo "Send Welcome Email"
   - Controlla errori

2. **Verifica Credenziali SMTP**:
   - Testa le credenziali SMTP con un tool come https://www.smtper.net/

3. **Controlla Firewall/Network**:
   - Assicurati che N8N possa accedere alla porta SMTP (587/465)

---

## 📁 File Modificati

```
Bloom-2.0/
├── src/pages/Login.tsx                                    # Popup Brand Profile
├── backup_workflows/
│   └── Bloom_AI_Unified_Auth_WITH_EMAIL.json             # Workflow con email
├── deploy_auth_with_email.py                              # Script deployment
└── REGISTRATION_FLOW_SETUP.md                             # Questa guida
```

---

## 🔐 Sicurezza

- ✅ La password **NON** viene inviata via email
- ✅ Email con template HTML professionale (no spam)
- ✅ Link di accesso diretto alla dashboard
- ✅ Credenziali SMTP separate e configurabili
- ✅ TLS/SSL per connessioni SMTP sicure

---

## 🆘 Troubleshooting

### Problema: Email non arriva
**Soluzione**:
1. Verifica spam/promozioni
2. Controlla N8N execution log
3. Testa credenziali SMTP
4. Usa SendGrid invece di Gmail

### Problema: Popup non appare
**Soluzione**:
1. Apri console browser (F12)
2. Verifica errori JavaScript
3. Controlla che `isRegistering` sia true
4. Verifica response del webhook

### Problema: Deployment fallisce
**Soluzione**:
1. Verifica API Key in `~/n8n_config.json`
2. Controlla connessione internet
3. Verifica workflow ID: `uYNin7KcptmBF8Nw`

---

## 📞 Support

Per assistenza:
- Email: support@bloom-ai.app
- N8N Docs: https://docs.n8n.io/
- SendGrid Docs: https://docs.sendgrid.com/

---

**Ultima modifica**: 2026-01-30
**Versione**: 1.0.0
