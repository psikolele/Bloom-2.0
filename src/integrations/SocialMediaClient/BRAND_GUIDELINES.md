# MarketingFlow - Brand Guidelines

> Documento completo per la creazione di applicazioni basate sul brand MarketingFlow

---

## 📋 Indice

1. [Brand Identity](#1-brand-identity)
2. [Palette Colori](#2-palette-colori)
3. [Tipografia](#3-tipografia)
4. [Logo e Favicon](#4-logo-e-favicon)
5. [Sistema di Design UI](#5-sistema-di-design-ui)
6. [Stile Visivo e Filosofia](#6-stile-visivo-e-filosofia)
7. [Tone of Voice](#7-tone-of-voice)
8. [Sistema di Icone](#8-sistema-di-icone)
9. [Animazioni e Interazioni](#9-animazioni-e-interazioni)
10. [Layout e Struttura](#10-layout-e-struttura)
11. [Stati e Feedback](#11-stati-e-feedback)
12. [Esempi di Implementazione](#12-esempi-di-implementazione)

---

## 1. Brand Identity

### Nome Brand
- **Brand Principale**: **MarketingFlow**
- **Brand Alternativo**: SocialFlow: Brand Profile AI
- **Tagline**: "Strategia Marketing"

### Naming Conventions
- **Sezioni Features**: Formato numerato con emoji/icone
  - Esempio: "01. Informazioni Azienda", "02. Strategia Aziendale"
- **Stile Label**: MAIUSCOLO con font monospace
- **Naming Tecnico**: Stile tech-forward ("Marketing Configurator", "System Online")
- **Lingua**: Italiano (mercato target italiano)

### Posizionamento Brand
- Professionale e tecnologico
- Orientato all'automazione marketing
- Target: Aziende, Brand, Professionisti
- Settore: Marketing digitale e social media strategy

---

## 2. Palette Colori

### Colori Primari

#### Arancione Accent (Colore Brand Principale)
```css
--accent-primary: #FF6B35
--accent-glow: #FF9B75
```
**Uso**: CTA primari, link, elementi interattivi, focus states

#### Gradiente Logo
```css
Colori gradiente multi-colore:
- #FF9B6B (arancione chiaro)
- #FF7B4D (arancione medio)
- #5B9FE3 (blu)
- #B349C1 (viola/magenta)
```
**Uso**: Logo, heading principali, effetti speciali

### Colori Background

#### Background Primari
```css
--void: #030303       /* Background principale (quasi nero) */
--surface: #0A0A0A    /* Superficie leggermente più chiara */
```

#### Background Glassmorphism
```css
background: rgba(18, 18, 18, 0.6);
backdrop-filter: blur(24px);
```

### Colori Testo

```css
--text-primary: #E0E0E0      /* Testo principale */
--text-secondary: #9CA3AF    /* Testo secondario (gray-400) */
--text-muted: #6B7280        /* Testo disattivato (gray-500) */
```

### Colori Sistema

```css
--success: #34D399    /* Emerald-400 */
--success-dark: #10B981  /* Emerald-500 */
--error: #F87171      /* Red-400 */
--error-medium: #EF4444  /* Red-500 */
--error-dark: #DC2626    /* Red-600 */
```

### Gradiente Bottone Primario
```css
background: linear-gradient(135deg, #FF6B35 0%, #FF8F6B 100%);
```

### Effetti Luce Ambientale
```css
/* Luce arancione */
background: radial-gradient(circle at 20% 30%, rgba(255, 107, 53, 0.06), transparent 50%);

/* Luce blu */
background: radial-gradient(circle at 80% 70%, rgba(59, 130, 246, 0.04), transparent 50%);
```

---

## 3. Tipografia

### Font Families

#### Sans-Serif Primario: Inter
```
Font: Inter
Pesi: 300 (Light), 400 (Regular), 500 (Medium), 600 (Semi-Bold)
Uso: Body text, paragrafi, form fields, contenuto generale
Import: Google Fonts
```

#### Monospace Secondario: Space Grotesk
```
Font: Space Grotesk
Pesi: 300 (Light), 500 (Medium), 700 (Bold)
Uso: Heading, label, testo tecnico, section headers
Import: Google Fonts
```

### Import Google Fonts
```html
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Space+Grotesk:wght@300;500;700&display=swap" rel="stylesheet">
```

### Scala Tipografica

```css
/* Heading Principale */
font-size: 3rem;           /* Mobile: text-4xl */
font-size: 4.5rem;         /* Desktop: text-6xl */
font-family: Space Grotesk;
font-weight: 700;
letter-spacing: -0.025em;  /* tracking-tight */

/* Section Headers */
font-size: 0.875rem;       /* text-sm */
font-family: Space Grotesk;
font-weight: 700;
text-transform: uppercase;
letter-spacing: 0.05em;

/* Body Text */
font-size: 0.875rem;       /* text-sm */
font-family: Inter;
font-weight: 400;

/* Label / Small Text */
font-size: 0.75rem;        /* text-xs */
font-size: 10px;           /* text-[10px] per label mini */
font-family: Space Grotesk;
text-transform: uppercase;
letter-spacing: 0.1em;     /* tracking-widest */
```

### Stili Testo Speciali

#### Gradient Text (Heading)
```css
background: linear-gradient(135deg, #FF9B6B 0%, #FF7B4D 25%, #5B9FE3 50%, #B349C1 100%);
-webkit-background-clip: text;
-webkit-text-fill-color: transparent;
background-clip: text;
animation: gradient-shift 3s ease infinite;
```

#### Glow Text
```css
text-shadow: 0 0 20px rgba(255, 107, 53, 0.5);
animation: text-glow 2s ease-in-out infinite;
```

---

## 4. Logo e Favicon

### Descrizione Logo

Il logo MarketingFlow è un'icona circolare con design tecnico e futuristico:

**Elementi Compositivi:**
1. **Cerchio Esterno**: Raggio 90px, gradiente multi-colore
2. **Simbolo Centrale**: Fulmine/saetta bianco (simbolo di velocità/energia)
3. **Elementi Orbitali**: 4 cerchi bianchi agli angoli (simboleggiano connessione/network)
4. **Linee di Connessione**: Collegano gli elementi orbitali
5. **Effetti**: Drop shadow + glow arancione

### Gradiente Logo
```css
Gradiente radiale dal centro:
- Stop 0%: #FF9B6B (arancione chiaro)
- Stop 40%: #FF7B4D (arancione medio)
- Stop 60%: #5B9FE3 (blu)
- Stop 100%: #B349C1 (viola/magenta)
```

### Simbolo Fulmine (Centrale)
```svg
<path d="M50 20 L35 55 L50 50 L40 80 L65 45 L50 50 Z"
      fill="white" />
```

### Dimensioni Logo

```css
/* Dimensione default */
width: 40px;
height: 40px;

/* Navbar */
width: 48px;
height: 48px;

/* Loader/Splash */
width: 96px;
height: 96px;

/* Favicon */
width: 32px;
height: 32px;
```

### Effetti Logo

#### Glow Effect (Navbar)
```css
filter: drop-shadow(0 0 20px rgba(255, 107, 53, 0.4));
```

#### Animated Glow (Loader)
```css
filter: drop-shadow(0 0 40px rgba(255, 107, 53, 0.6));
animation: pulse 2s ease-in-out infinite;
```

### Favicon
- **Formato**: SVG
- **Design**: Versione ridotta del logo principale
- **Colori**: Stesso gradiente del logo
- **Path**: `/public/favicon.svg`

### Varianti Logo

#### Logo Base (Component Structure)
```tsx
<Logo size={40} />  // Default
<Logo size={48} />  // Navbar
<Logo size={96} />  // Loader
```

**Caratteristiche tecniche:**
- SVG vettoriale scalabile
- Gradiente definito tramite `<defs>` SVG
- Filtri SVG per ombre e glow
- Responsive da 12px a 96px+

---

## 5. Sistema di Design UI

### Glass-Panel (Componente Base)

**Stile principale per cards e pannelli:**

```css
.glass-panel {
  background: rgba(18, 18, 18, 0.6);
  backdrop-filter: blur(24px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 24px;
  box-shadow:
    0 0 0 1px rgba(0, 0, 0, 0.5),
    0 20px 40px -10px rgba(0, 0, 0, 0.5),
    inset 0 0 20px rgba(255, 255, 255, 0.02);
  padding: 2rem;
}
```

**Quando usarlo:**
- Card contenitori
- Form panels
- Section containers
- Modal/Dialog

### Spotlight Card (Variante Interattiva)

```css
.spotlight-card {
  /* Estende glass-panel */
  position: relative;
  overflow: hidden;
  cursor: pointer;
}

.spotlight-card::before {
  content: '';
  position: absolute;
  width: 100px;
  height: 100px;
  background: radial-gradient(
    circle,
    rgba(255, 107, 53, 0.15) 0%,
    transparent 70%
  );
  left: var(--x);
  top: var(--y);
  transform: translate(-50%, -50%);
  pointer-events: none;
  transition: opacity 0.3s;
}

.spotlight-card:hover::before {
  opacity: 1;
}
```

**Quando usarlo:**
- Card cliccabili
- Interactive sections
- Metric cards

### Tech-Input (Form Field)

```css
.tech-input {
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 12px;
  padding: 0.75rem 1rem;
  color: #E0E0E0;
  font-family: Inter, sans-serif;
  font-size: 0.875rem;
  transition: all 0.3s ease;
}

.tech-input:focus {
  outline: none;
  border-color: #FF6B35;
  background: rgba(0, 0, 0, 0.5);
  box-shadow:
    0 0 0 3px rgba(255, 107, 53, 0.1),
    0 0 20px rgba(255, 107, 53, 0.2);
}

.tech-input::placeholder {
  color: rgba(156, 163, 175, 0.5);
}
```

**Stati:**
- **Default**: Background scuro, border sottile
- **Hover**: Background leggermente più chiaro
- **Focus**: Border arancione + glow + background più scuro
- **Error**: Border rosso + messaggio errore
- **Disabled**: Opacity ridotta

### Button Primary (CTA)

```css
.btn-primary {
  background: linear-gradient(135deg, #FF6B35 0%, #FF8F6B 100%);
  color: white;
  font-family: 'Space Grotesk', monospace;
  font-weight: 700;
  font-size: 0.875rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  padding: 1rem 2rem;
  border-radius: 12px;
  border: none;
  box-shadow: 0 0 20px rgba(255, 107, 53, 0.2);
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 0 35px rgba(255, 107, 53, 0.5);
}

.btn-primary:active {
  transform: translateY(0);
}

/* Shimmer effect */
.btn-primary::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.3),
    transparent
  );
  transition: left 0.5s;
}

.btn-primary:hover::before {
  left: 100%;
}
```

### Button Secondary

```css
.btn-secondary {
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: #E0E0E0;
  font-family: 'Space Grotesk', monospace;
  font-weight: 500;
  padding: 0.75rem 1.5rem;
  border-radius: 12px;
  transition: all 0.3s ease;
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.2);
}
```

### Metric Card

```css
.metric-card {
  background: linear-gradient(
    135deg,
    rgba(255, 107, 53, 0.05) 0%,
    rgba(91, 159, 227, 0.05) 100%
  );
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 16px;
  padding: 1.5rem;
  transition: all 0.3s ease;
}

.metric-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 0 30px rgba(255, 107, 53, 0.15);
}
```

### Grid Overlay (Background Pattern)

```css
.grid-overlay {
  background-image:
    linear-gradient(rgba(255, 255, 255, 0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.03) 1px, transparent 1px);
  background-size: 50px 50px;
}
```

---

## 6. Stile Visivo e Filosofia

### Filosofia di Design

**MarketingFlow adotta uno stile "Tech-Forward Glassmorphism":**

1. **Dark Mode First**: Background quasi nero (#030303) per ridurre affaticamento visivo
2. **Glassmorphism**: Superfici semi-trasparenti con blur per profondità
3. **Neon Accents**: Colori vividi (arancione) su sfondo scuro per contrasto drammatico
4. **Minimalismo Funzionale**: Solo elementi essenziali, ma con dettagli curati
5. **Illuminazione Drammatica**: Glow effects e ambient lights per atmosfera futuristica

### Principi Chiave

#### 1. Gerarchia Visiva Chiara
- Heading grandi con gradient
- Section headers con icone
- Contenuto organizzato in card glassmorphism
- CTA prominenti con colore accent

#### 2. Consistenza
- Spacing uniforme (multipli di 8px: 8, 16, 24, 32...)
- Border radius coerenti (8px, 12px, 16px, 24px)
- Transizioni uniformi (0.3s ease per la maggior parte degli elementi)
- Color palette limitata ma espressiva

#### 3. Feedback Visivo
- Hover states sempre presenti
- Loading states animati
- Success/Error states chiari
- Micro-interactions fluide

#### 4. Accessibilità nel Dark
- Contrasto testo/background > 4.5:1
- Focus states visibili
- Colori sistema semantici (verde=success, rosso=error)
- Stati interattivi chiari

### Composizione Layout

```
┌─────────────────────────────────────────┐
│  Navbar (glass-panel, fixed top)       │
│  [Logo] [Title]          [Status]      │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│                                         │
│         Hero Section                    │
│   [Gradient Heading]                    │
│   [Subtitle]                            │
│                                         │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│  Main Content (max-w-4xl, centered)    │
│                                         │
│  ┌───────────────────────────────────┐ │
│  │  Section 1 (glass-panel)          │ │
│  │  [Icon] [Title]                   │ │
│  │  [Form Fields]                    │ │
│  └───────────────────────────────────┘ │
│                                         │
│  ┌───────────────────────────────────┐ │
│  │  Section 2 (glass-panel)          │ │
│  └───────────────────────────────────┘ │
│                                         │
│  [CTA Button - Full Width]             │
│                                         │
└─────────────────────────────────────────┘

[Ambient Lights - Fixed Background]
[Grid Overlay - Fixed Background]
```

---

## 7. Tone of Voice

### Caratteristiche Generali

**Personalità del Brand:**
- Professionale ma accessibile
- Tecnologico e innovativo
- Orientato all'azione
- Chiaro e diretto

**Stile di Scrittura:**
- Frasi concise
- Verbi d'azione
- Terminologia tecnica quando appropriato
- Linguaggio italiano formale ma non eccessivamente burocratico

### Esempi di Copy UI

#### Navigation/Status
```
✓ "System Online" (con indicatore pulsante verde)
✓ "Marketing Strategy Collection"
✓ "Strategia Marketing"
✗ "Il sistema è attualmente online" (troppo verboso)
✗ "Raccolta strategia" (troppo informale)
```

#### Section Headers
```
✓ "01. Informazioni Azienda" [Shield Icon]
✓ "02. Strategia Aziendale" [Target Icon]
✓ "03. Tipologia Comunicazione" [Wand Icon]
✗ "Inserisci le informazioni della tua azienda" (troppo lungo)
✗ "Info Azienda" (troppo abbreviato)
```

#### Success Messages
```
✓ "Dati Inviati con Successo!"
✓ "La tua strategia marketing è stata inviata al sistema di automazione."
✗ "Evviva! I tuoi dati sono stati inviati!" (troppo informale)
✗ "Operazione completata" (troppo generico)
```

#### Error Messages
```
✓ "ERRORE RILEVATO"
✓ "Impossibile inviare i dati. Verifica la connessione e riprova."
✗ "Ops! Qualcosa è andato storto" (troppo informale)
✗ "Error 500" (troppo tecnico senza contesto)
```

#### CTA Buttons
```
✓ "Invia Strategia Marketing"
✓ "Carica Immagini"
✓ "NUOVA STRATEGIA"
✓ "Aggiungi"
✗ "Clicca qui per inviare" (troppo descrittivo)
✗ "OK" (troppo generico)
```

#### Form Placeholders
```
✓ "Nome Azienda / Brand / Professionista *"
✓ "Sito Web (es. https://...) *"
✓ "Descrivi la tua strategia aziendale, obiettivi e vision... *"
✗ "Inserisci nome" (troppo vago)
✗ "Scrivi qui la tua strategia aziendale completa di obiettivi..." (troppo lungo)
```

#### Field Labels
```
✓ "COMPETITOR PRINCIPALI"
✓ "SITO WEB"
✓ "PRODOTTI / SERVIZI"
✗ "Competitor" (manca contesto)
✗ "Qual è il tuo sito web?" (troppo colloquiale)
```

### Linee Guida Tone of Voice

1. **Usa l'imperativo per le azioni**
   - "Carica", "Invia", "Aggiungi", "Seleziona"

2. **Sii specifico nei messaggi di stato**
   - Non "Fatto" → "Dati Inviati con Successo!"
   - Non "Errore" → "ERRORE RILEVATO: [descrizione specifica]"

3. **Mantieni coerenza con asterischi per campi obbligatori**
   - Sempre * alla fine del placeholder/label
   - "Campo Obbligatorio *"

4. **Usa MAIUSCOLO per:**
   - Label importanti (COMPETITOR, SITO WEB)
   - Stati del sistema (ERRORE RILEVATO, NUOVA STRATEGIA)
   - CTA importanti

5. **Formattazione numeri nelle sezioni**
   - Sempre formato "0X." (01., 02., 03...)

6. **Feedback contestuale**
   - Success: Descrivi cosa è successo + cosa succederà dopo
   - Error: Descrivi il problema + suggerisci soluzione

---

## 8. Sistema di Icone

### Libreria Icone

MarketingFlow usa icone SVG custom con stile consistente:

**Specifiche Tecniche:**
- Formato: SVG inline
- Size: 24x24px (default)
- Stroke width: 2px
- Stroke linecap: round
- Stroke linejoin: round
- Color: `currentColor` (eredita dal parent)

### Set Icone Disponibili

```
Upload       - Caricamento file
Zap          - Velocità/energia (logo lightning)
Check        - Conferma/successo
Settings     - Configurazione
Wand         - Creatività/magia
Send         - Invio dati
X            - Chiusura/cancellazione
Alert        - Avvisi/errori
Server       - Sistema/backend
Refresh      - Ricarica/reset
Globe        - Web/online
Users        - Utenti/target
Target       - Obiettivi/targeting
Tag          - Etichette/categorie
Shield       - Sicurezza/protezione
Edit         - Modifica
Info         - Informazioni
```

### Stile Icone

```css
.icon {
  width: 24px;
  height: 24px;
  stroke: currentColor;
  stroke-width: 2px;
  stroke-linecap: round;
  stroke-linejoin: round;
  fill: none;
}
```

### Utilizzo Icone

#### Icone in Section Headers
```jsx
<div className="flex items-center gap-2">
  <Shield className="w-5 h-5 text-orange-500" />
  <span>01. INFORMAZIONI AZIENDA</span>
</div>
```

#### Icone in Buttons
```jsx
<button>
  <Send className="w-4 h-4" />
  <span>Invia Strategia</span>
</button>
```

#### Icone di Stato
```jsx
<div className="flex items-center gap-2">
  <div className="w-2 h-2 bg-emerald-400 rounded-full animate-pulse" />
  <Check className="w-4 h-4 text-emerald-400" />
  <span>System Online</span>
</div>
```

### Color Mapping Icone

```css
/* Accent/Primary */
.text-accent: #FF6B35

/* Success */
.text-success: #34D399 (emerald-400)

/* Error */
.text-error: #F87171 (red-400)

/* Warning */
.text-warning: #FBBF24 (amber-400)

/* Info/Neutral */
.text-info: #60A5FA (blue-400)

/* Muted */
.text-muted: #9CA3AF (gray-400)
```

---

## 9. Animazioni e Interazioni

### Keyframe Animations

#### 1. Reveal (Entry Animation)
```css
@keyframes reveal {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-reveal {
  animation: reveal 0.6s ease-out;
}
```
**Uso**: Entry di componenti, section headers, cards

#### 2. Float (Floating Animation)
```css
@keyframes float {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}

.animate-float {
  animation: float 3s ease-in-out infinite;
}
```
**Uso**: Elementi decorativi, logo splash screen

#### 3. Gradient Shift (Animated Gradient)
```css
@keyframes gradient-shift {
  0%, 100% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
}

.animate-gradient {
  background-size: 200% 200%;
  animation: gradient-shift 3s ease infinite;
}
```
**Uso**: Heading con gradient, elementi hero

#### 4. Text Glow (Pulsing Glow)
```css
@keyframes text-glow {
  0%, 100% {
    text-shadow: 0 0 20px rgba(255, 107, 53, 0.5);
  }
  50% {
    text-shadow: 0 0 30px rgba(255, 107, 53, 0.8);
  }
}

.animate-glow {
  animation: text-glow 2s ease-in-out infinite;
}
```
**Uso**: Testo importante, indicatori di stato

#### 5. Pulse (Indicator Animation)
```css
@keyframes pulse {
  0%, 100% {
    opacity: 1;
    transform: scale(1);
  }
  50% {
    opacity: 0.5;
    transform: scale(1.05);
  }
}

.animate-pulse {
  animation: pulse 2s ease-in-out infinite;
}
```
**Uso**: Indicatori di stato (es. "System Online"), loading states

#### 6. Bounce (Standard Bounce)
```css
@keyframes bounce {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-25%);
  }
}

.animate-bounce {
  animation: bounce 1s infinite;
}
```
**Uso**: Loading dots, indicatori interattivi

#### 7. Spin (Rotation)
```css
@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.animate-spin {
  animation: spin 1s linear infinite;
}
```
**Uso**: Loading spinners, refresh icons

#### 8. Shimmer (Button Effect)
```css
@keyframes shimmer {
  0% {
    left: -100%;
  }
  100% {
    left: 100%;
  }
}

.btn-shimmer::before {
  animation: shimmer 2s infinite;
}
```
**Uso**: Hover effect su bottoni primari

### Transition Standards

```css
/* Transizione Default */
transition: all 0.3s ease;

/* Transizione Veloce */
transition: all 0.15s ease;

/* Transizione Lenta */
transition: all 0.5s ease;

/* Transizione Transform (performance) */
transition: transform 0.3s ease, opacity 0.3s ease;
```

### Micro-Interactions

#### Hover States
```css
/* Card Hover */
.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 0 30px rgba(255, 107, 53, 0.15);
}

/* Button Hover */
.button:hover {
  transform: translateY(-2px);
  box-shadow: 0 0 35px rgba(255, 107, 53, 0.5);
}

/* Link Hover */
.link:hover {
  color: #FF6B35;
  text-decoration: underline;
}
```

#### Focus States
```css
/* Input Focus */
.input:focus {
  outline: none;
  border-color: #FF6B35;
  box-shadow:
    0 0 0 3px rgba(255, 107, 53, 0.1),
    0 0 20px rgba(255, 107, 53, 0.2);
}

/* Button Focus */
.button:focus-visible {
  outline: 2px solid #FF6B35;
  outline-offset: 2px;
}
```

#### Active States
```css
/* Button Active */
.button:active {
  transform: translateY(0);
  box-shadow: 0 0 15px rgba(255, 107, 53, 0.3);
}
```

#### Loading States
```css
/* Spinner Loading */
.loading-spinner {
  animation: spin 1s linear infinite;
}

/* Skeleton Loading */
.skeleton {
  background: linear-gradient(
    90deg,
    rgba(255, 255, 255, 0.05) 0%,
    rgba(255, 255, 255, 0.1) 50%,
    rgba(255, 255, 255, 0.05) 100%
  );
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
}

/* Progress Bar */
.progress-bar {
  background: linear-gradient(90deg, #FF6B35, #FF8F6B);
  animation: progress 2s ease-out;
}
```

### Animation Timing

```css
/* Entrance: Veloce e decisa */
--timing-enter: 0.3s ease-out;

/* Exit: Ancora più veloce */
--timing-exit: 0.2s ease-in;

/* Hover: Responsivo */
--timing-hover: 0.15s ease;

/* Ambient: Lento e fluido */
--timing-ambient: 3s ease-in-out;
```

---

## 10. Layout e Struttura

### Responsive Breakpoints

```css
/* Mobile First Approach */
/* xs: default (< 640px) */
/* sm: 640px */
@media (min-width: 640px) { }

/* md: 768px */
@media (min-width: 768px) { }

/* lg: 1024px */
@media (min-width: 1024px) { }

/* xl: 1280px */
@media (min-width: 1280px) { }

/* 2xl: 1536px */
@media (min-width: 1536px) { }
```

### Container Widths

```css
/* Main Container */
.container-main {
  max-width: 1024px;  /* max-w-4xl */
  margin: 0 auto;
  padding: 0 1rem;    /* px-4 */
}

/* Narrow Container (Forms) */
.container-narrow {
  max-width: 768px;   /* max-w-3xl */
  margin: 0 auto;
}

/* Wide Container (Dashboard) */
.container-wide {
  max-width: 1280px;  /* max-w-6xl */
  margin: 0 auto;
}

/* Full Width */
.container-full {
  width: 100%;
  padding: 0 1rem;
}
```

### Spacing System

```css
/* Scala di Spacing (basata su 4px) */
--space-1: 0.25rem;   /* 4px */
--space-2: 0.5rem;    /* 8px */
--space-3: 0.75rem;   /* 12px */
--space-4: 1rem;      /* 16px */
--space-5: 1.25rem;   /* 20px */
--space-6: 1.5rem;    /* 24px */
--space-8: 2rem;      /* 32px */
--space-10: 2.5rem;   /* 40px */
--space-12: 3rem;     /* 48px */
--space-16: 4rem;     /* 64px */
--space-20: 5rem;     /* 80px */
--space-24: 6rem;     /* 96px */

/* Usage */
padding: var(--space-6);       /* p-6 */
margin: var(--space-8);        /* m-8 */
gap: var(--space-4);           /* gap-4 */
```

### Grid System

```css
/* Form Grid (2 colonne su desktop) */
.form-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
}

@media (min-width: 768px) {
  .form-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 1.5rem;
  }
}

/* Card Grid (3 colonne su desktop) */
.card-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1.5rem;
}

@media (min-width: 768px) {
  .card-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1024px) {
  .card-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}
```

### Z-Index Scale

```css
--z-base: 0;           /* Default */
--z-dropdown: 10;      /* Dropdown menus */
--z-sticky: 20;        /* Sticky headers */
--z-fixed: 30;         /* Fixed elements */
--z-modal-backdrop: 40; /* Modal backgrounds */
--z-modal: 50;         /* Modal content */
--z-popover: 60;       /* Popovers, tooltips */
--z-toast: 70;         /* Toast notifications */
--z-tooltip: 80;       /* Tooltips */
```

### Navbar Structure

```html
<nav class="navbar">
  <div class="navbar-container">
    <div class="navbar-left">
      <Logo size={48} />
      <h1 class="navbar-title">MarketingFlow</h1>
    </div>
    <div class="navbar-right">
      <StatusIndicator />
    </div>
  </div>
</nav>
```

```css
.navbar {
  position: fixed;
  top: 0;
  width: 100%;
  z-index: var(--z-fixed);
  background: rgba(18, 18, 18, 0.8);
  backdrop-filter: blur(24px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}

.navbar-container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 1rem 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
```

### Section Structure

```html
<section class="section">
  <div class="section-header">
    <Icon />
    <h2>01. SECTION TITLE</h2>
  </div>
  <div class="section-content">
    <!-- Content -->
  </div>
</section>
```

```css
.section {
  /* Glass-panel styling */
  padding: 2rem;
  margin-bottom: 1.5rem;
}

.section-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}
```

### Form Layout

```html
<form class="form">
  <div class="form-grid">
    <div class="form-group">
      <label class="form-label">LABEL</label>
      <input class="form-input tech-input" />
    </div>
    <div class="form-group">
      <label class="form-label">LABEL</label>
      <input class="form-input tech-input" />
    </div>
  </div>
  <button class="btn-primary">SUBMIT</button>
</form>
```

```css
.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-label {
  font-family: 'Space Grotesk', monospace;
  font-size: 0.625rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: rgba(224, 224, 224, 0.7);
}
```

---

## 11. Stati e Feedback

### Success State

```jsx
<div className="success-state">
  <div className="success-icon">
    <Check className="w-12 h-12 text-emerald-400" />
  </div>
  <h3 className="success-title">Dati Inviati con Successo!</h3>
  <p className="success-message">
    La tua strategia marketing è stata inviata al sistema di automazione.
  </p>
  <button className="btn-primary">NUOVA STRATEGIA</button>
</div>
```

```css
.success-state {
  text-align: center;
  padding: 3rem 2rem;
}

.success-icon {
  width: 80px;
  height: 80px;
  margin: 0 auto 1.5rem;
  background: radial-gradient(
    circle,
    rgba(52, 211, 153, 0.2) 0%,
    transparent 70%
  );
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  animation: pulse 2s ease-in-out infinite;
}

.success-title {
  font-family: 'Space Grotesk', monospace;
  font-size: 1.5rem;
  font-weight: 700;
  color: #34D399;
  margin-bottom: 0.5rem;
}

.success-message {
  color: #9CA3AF;
  margin-bottom: 2rem;
}
```

### Error State

```jsx
<div className="error-state">
  <div className="error-icon">
    <AlertTriangle className="w-12 h-12 text-red-400" />
  </div>
  <h3 className="error-title">ERRORE RILEVATO</h3>
  <p className="error-message">
    Impossibile inviare i dati. Verifica la connessione e riprova.
  </p>
  <button className="btn-secondary" onClick={retry}>
    <Refresh className="w-4 h-4" />
    RIPROVA
  </button>
</div>
```

```css
.error-state {
  text-align: center;
  padding: 3rem 2rem;
}

.error-icon {
  width: 80px;
  height: 80px;
  margin: 0 auto 1.5rem;
  background: radial-gradient(
    circle,
    rgba(248, 113, 113, 0.2) 0%,
    transparent 70%
  );
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.error-title {
  font-family: 'Space Grotesk', monospace;
  font-size: 1.5rem;
  font-weight: 700;
  color: #F87171;
  margin-bottom: 0.5rem;
}

.error-message {
  color: #9CA3AF;
  margin-bottom: 2rem;
}
```

### Loading State

```jsx
<div className="loading-state">
  <Logo size={96} className="animate-pulse" />
  <div className="progress-bar">
    <div className="progress-fill" style={{width: `${progress}%`}}></div>
  </div>
  <div className="loading-dots">
    <span>Caricamento</span>
    <span className="dot animate-bounce" style={{animationDelay: '0s'}}>.</span>
    <span className="dot animate-bounce" style={{animationDelay: '0.2s'}}>.</span>
    <span className="dot animate-bounce" style={{animationDelay: '0.4s'}}>.</span>
  </div>
</div>
```

```css
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  gap: 2rem;
}

.progress-bar {
  width: 200px;
  height: 4px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 2px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #FF6B35, #FF8F6B);
  transition: width 0.3s ease;
}

.loading-dots {
  display: flex;
  align-items: center;
  font-family: 'Space Grotesk', monospace;
  color: #9CA3AF;
}

.dot {
  display: inline-block;
}
```

### Empty State

```jsx
<div className="empty-state">
  <div className="empty-icon">
    <Inbox className="w-16 h-16 text-gray-600" />
  </div>
  <h3 className="empty-title">Nessun Dato Disponibile</h3>
  <p className="empty-message">
    Inizia compilando il form per creare la tua strategia marketing.
  </p>
</div>
```

```css
.empty-state {
  text-align: center;
  padding: 4rem 2rem;
  color: #6B7280;
}

.empty-icon {
  margin: 0 auto 1.5rem;
  opacity: 0.5;
}

.empty-title {
  font-family: 'Space Grotesk', monospace;
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.empty-message {
  font-size: 0.875rem;
  opacity: 0.7;
}
```

### Status Indicator

```jsx
<div className="status-indicator">
  <div className="status-dot status-online"></div>
  <span className="status-text">System Online</span>
</div>
```

```css
.status-indicator {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: rgba(16, 185, 129, 0.1);
  border: 1px solid rgba(16, 185, 129, 0.3);
  border-radius: 9999px;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.status-online {
  background: #10B981;
  box-shadow: 0 0 10px rgba(16, 185, 129, 0.5);
  animation: pulse 2s ease-in-out infinite;
}

.status-text {
  font-family: 'Space Grotesk', monospace;
  font-size: 0.75rem;
  font-weight: 500;
  color: #10B981;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
```

### Validation States

```css
/* Input Error */
.input-error {
  border-color: #EF4444 !important;
  box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.1) !important;
}

.error-message {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-top: 0.5rem;
  color: #EF4444;
  font-size: 0.75rem;
}

/* Input Success */
.input-success {
  border-color: #10B981 !important;
  box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1) !important;
}

.success-message {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-top: 0.5rem;
  color: #10B981;
  font-size: 0.75rem;
}
```

---

## 12. Esempi di Implementazione

### Esempio 1: Hero Section

```html
<section class="hero">
  <div class="hero-content">
    <h1 class="hero-title">
      Marketing<span class="gradient-text">Flow</span>
    </h1>
    <p class="hero-subtitle">
      Strategia Marketing Automatizzata
    </p>
  </div>
</section>
```

```css
.hero {
  padding: 6rem 1rem 4rem;
  text-align: center;
  position: relative;
}

.hero-content {
  max-width: 800px;
  margin: 0 auto;
}

.hero-title {
  font-family: 'Space Grotesk', monospace;
  font-size: 3rem;
  font-weight: 700;
  line-height: 1.1;
  letter-spacing: -0.025em;
  color: #E0E0E0;
  margin-bottom: 1rem;
}

@media (min-width: 768px) {
  .hero-title {
    font-size: 4.5rem;
  }
}

.gradient-text {
  background: linear-gradient(
    135deg,
    #FF9B6B 0%,
    #FF7B4D 25%,
    #5B9FE3 50%,
    #B349C1 100%
  );
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  background-size: 200% 200%;
  animation: gradient-shift 3s ease infinite;
}

.hero-subtitle {
  font-size: 1.125rem;
  color: #9CA3AF;
  font-weight: 300;
}
```

### Esempio 2: Form Section con Glass Panel

```html
<section class="glass-panel">
  <div class="section-header">
    <Shield class="w-5 h-5 text-orange-500" />
    <h2 class="section-title">01. INFORMAZIONI AZIENDA</h2>
  </div>

  <div class="form-grid">
    <div class="form-group">
      <label class="form-label">NOME AZIENDA *</label>
      <input
        type="text"
        class="tech-input"
        placeholder="Nome Azienda / Brand / Professionista *"
        required
      />
    </div>

    <div class="form-group">
      <label class="form-label">SITO WEB *</label>
      <input
        type="url"
        class="tech-input"
        placeholder="Sito Web (es. https://...) *"
        required
      />
    </div>
  </div>

  <div class="form-group">
    <label class="form-label">DESCRIZIONE *</label>
    <textarea
      class="tech-input"
      rows="4"
      placeholder="Descrivi la tua azienda, prodotti/servizi offerti... *"
      required
    ></textarea>
  </div>
</section>
```

### Esempio 3: CTA Button con Shimmer

```html
<button class="btn-primary btn-shimmer">
  <Send class="w-4 h-4" />
  <span>INVIA STRATEGIA MARKETING</span>
</button>
```

```css
.btn-shimmer {
  position: relative;
  overflow: hidden;
}

.btn-shimmer::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.3),
    transparent
  );
  transition: left 0.5s;
}

.btn-shimmer:hover::before {
  left: 100%;
}
```

### Esempio 4: Spotlight Card

```html
<div class="spotlight-card" data-spotlight>
  <h3 class="card-title">Marketing Automation</h3>
  <p class="card-description">
    Sistema intelligente per la gestione automatizzata delle strategie marketing.
  </p>
</div>
```

```javascript
// JavaScript per spotlight effect
document.querySelectorAll('[data-spotlight]').forEach(card => {
  card.addEventListener('mousemove', (e) => {
    const rect = card.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    card.style.setProperty('--x', `${x}px`);
    card.style.setProperty('--y', `${y}px`);
  });
});
```

### Esempio 5: Success Modal

```html
<div class="modal-backdrop">
  <div class="modal glass-panel">
    <div class="success-state">
      <div class="success-icon">
        <Check class="w-12 h-12" />
      </div>
      <h3 class="success-title">Dati Inviati con Successo!</h3>
      <p class="success-message">
        La tua strategia marketing è stata inviata al sistema di automazione.
      </p>
      <button class="btn-primary">NUOVA STRATEGIA</button>
    </div>
  </div>
</div>
```

```css
.modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: var(--z-modal);
  animation: reveal 0.3s ease-out;
}

.modal {
  max-width: 500px;
  width: 90%;
  animation: reveal 0.4s ease-out 0.1s backwards;
}
```

---

## 📝 Note Finali per l'Implementazione

### Priorità di Implementazione

1. **Fondamenta** (Must-Have):
   - Palette colori esatta
   - Tipografia (Inter + Space Grotesk)
   - Logo con gradiente
   - Glass-panel styling
   - Tech-input styling

2. **Identità Visiva** (Should-Have):
   - Glassmorphism effects
   - Gradient text headings
   - Ambient lighting backgrounds
   - Status indicators
   - Button primary con gradient

3. **Raffinatezze** (Nice-to-Have):
   - Spotlight card effect
   - Shimmer button animation
   - Micro-interactions avanzate
   - Floating animations
   - Glow effects

### Checklist Compatibilità

- ✅ Dark mode nativo
- ✅ Responsive design (mobile-first)
- ✅ Performance ottimizzata (CSS variables, transform per animazioni)
- ✅ Accessibilità (contrasto colori, focus states)
- ✅ Cross-browser (gradients, backdrop-filter con fallback)

### File di Riferimento Principali

```
/components/Logo.tsx          - Logo component
/components/Icons.tsx          - Icon system
/components/SpotlightCard.tsx  - Spotlight effect
/App.tsx                       - Main layout & structure
/index.html                    - Styles & configuration
/public/favicon.svg            - Favicon
```

### Variabili CSS Globali Suggerite

```css
:root {
  /* Colors */
  --accent-primary: #FF6B35;
  --accent-glow: #FF9B75;
  --void: #030303;
  --surface: #0A0A0A;
  --text-primary: #E0E0E0;
  --text-secondary: #9CA3AF;
  --success: #34D399;
  --error: #F87171;

  /* Spacing */
  --space-xs: 0.5rem;
  --space-sm: 1rem;
  --space-md: 1.5rem;
  --space-lg: 2rem;
  --space-xl: 3rem;

  /* Border Radius */
  --radius-sm: 8px;
  --radius-md: 12px;
  --radius-lg: 16px;
  --radius-xl: 24px;

  /* Transitions */
  --transition-fast: 0.15s ease;
  --transition-base: 0.3s ease;
  --transition-slow: 0.5s ease;

  /* Shadows */
  --shadow-glow: 0 0 20px rgba(255, 107, 53, 0.2);
  --shadow-glow-hover: 0 0 35px rgba(255, 107, 53, 0.5);
}
```

---

## 🎯 Obiettivo Finale

Questo documento fornisce tutte le informazioni necessarie per replicare l'identità visiva e l'esperienza utente di **MarketingFlow** in qualsiasi stack tecnologico. L'obiettivo è mantenere:

1. **Consistenza visiva** al 100%
2. **Tone of voice** professionale e tech-forward
3. **User experience** fluida e moderna
4. **Brand recognition** immediato

Ogni elemento di design ha uno scopo funzionale e contribuisce all'identità complessiva del brand MarketingFlow come soluzione premium per l'automazione del marketing digitale.

---

**Versione**: 1.0
**Ultimo aggiornamento**: 2026-01-15
**Brand**: MarketingFlow
**Repository**: psikolele/SocialMediaClient
