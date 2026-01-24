# Bloom 2.0 - Integrated Automation Suite

Bloom 2.0 is a unified Web Application that integrates **Caption Flow**, **Social Media Client**, and **Brand Profile** into a premium "Collector" Dashboard.

## 🚀 Features

- **Hub Dashboard**: A central landing page to navigate between tools.
- **Visual Integration**: Unified glassmorphism design and "Bloom" branding.
- **Integrated Modules**:
  1. **Caption Flow**: Legacy tool integrated via direct wrapper.
  2. **Social Media Client**: Fully integrated React module.
  3. **Brand Profile**: Fully integrated React module with AI capabilities (OpenRouter / Gemini 2.0).
  4. **UI Refinements**: Standardized "Bloom" branding:
     - **Loaders**: Unified `AnimatedLoader` and `BloomRedirectLoader` with fluid transitions.
     - **Headers**: Standardized Navigation across all modules.
     - **Fixes**: Removed duplicate menus and optimized animations.

## 🛠️ Setup & Configuration

### Prerequisites
- Node.js (v18+)
- N8N Webhook URL (Automatically configured in V.2)
- OpenRouter API Key

### Environment Variables
You must configure the `.env` file in the root directory:
```bash
OPENROUTER_API_KEY=sk-or-v1-...
VITE_N8N_WEBHOOK_URL=https://emanueleserra.app.n8n.cloud/webhook/...
```

### Installation
```bash
cd "Bloom 2.0"
npm install
```

### Running Locally
```bash
npm run dev
```
Open [http://localhost:5173](http://localhost:5173) to view the Hub.

## 📦 Building & Deployment

### Build
To create a production build:
```bash
npm run build
```

### Deploy to GitHub
A script is provided to automate GitHub deployment:
```powershell
./deploy_to_github.ps1
```
This will initialize/push to the `Bloom-2.0` repository.

## 🧩 Architecture

The project is a **Vite + React** Single Page Application.
- `src/pages/Dashboard.tsx`: Main Hub.
- `src/integrations/`: Contains the source code of the integrated apps.
  - `SocialMediaClient/`: Ported React App.
  - `BrandProfile/`: Ported React App.
  - `CaptionFlowWrapper.tsx`: Wrapper for the static Caption Flow app.
- `public/caption-flow/`: Static assets for Caption Flow.

Tailwind CSS v3 is configured to match the original "Bloom AI" theme (`bg-void`, `text-accent`).
