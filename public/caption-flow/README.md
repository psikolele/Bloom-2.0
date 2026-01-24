# CaptionFlow

> Web app per generare caption complete per i social media con AI

## 🚀 Quick Start

1. Apri `index.html` nel browser (o usa un server locale)
2. Inserisci la tua idea/frase
3. Seleziona la piattaforma social
4. Clicca "Genera Caption"

## ⚙️ Configurazione Webhook N8N

Modifica l'URL del webhook in `js/app.js`:

```javascript
const WEBHOOK_URL = 'https://YOUR-N8N-INSTANCE.app.n8n.cloud/webhook/caption-flow';
```

## 📁 Struttura

```
CaptionFlow/
├── index.html          # Pagina principale
├── css/styles.css      # Stile MarketingFlow
├── js/app.js           # Logica applicazione
├── assets/favicon.svg  # Logo/Favicon
└── README.md           # Documentazione
```

## 🎨 Brand

Basato sulle **MarketingFlow Brand Guidelines**:
- Dark glassmorphism design
- Accent color: `#FF6B35`
- Font: Inter + Space Grotesk

## 📤 Dati inviati al Webhook

```json
{
  "idea": "Il testo inserito dall'utente",
  "social_platform": "instagram|facebook|linkedin|tiktok|twitter",
  "timestamp": "2026-01-15T20:30:00.000Z",
  "source": "CaptionFlow Web App"
}
```

---

MarketingFlow © 2026
