<div align="center">
<img width="1200" height="475" alt="GHBanner" src="https://github.com/user-attachments/assets/0aa67016-6eaf-458a-adb2-6e31a0763ed6" />
</div>

# Run and deploy your AI Studio app

Repository: **psikolele/client-app-social**

This contains everything you need to run your app locally.

View your app in AI Studio: https://ai.studio/apps/drive/1uPZ9lskzUeIgqb27cAKT1t9Uw5BdfbzW

## Run Locally

**Prerequisites:**  Node.js


1. Install dependencies:
   ```bash
   npm install
   ```

2. Configure your Gemini API Key:
   - Get a free API key from [Google AI Studio](https://aistudio.google.com/apikey)
   - Copy `.env.local.example` to `.env.local` (if not already created)
   - Open `.env.local` and replace `your_gemini_api_key_here` with your actual API key:
     ```
     GEMINI_API_KEY=AIzaSy...your-actual-key-here
     ```

3. Run the app:
   ```bash
   npm run dev
   ```

The app will be available at `http://localhost:3000`

## Caricare il progetto su GitHub

1. Crea un repository vuoto su GitHub con il nome **psikolele/client-app-social** (senza aggiungere README o altri file).
2. Imposta il nuovo remote nella cartella del progetto:
   ```bash
   git remote add origin https://github.com/psikolele/client-app-social.git
   ```
3. Conferma e invia tutti i file:
   ```bash
   git add .
   git commit -m "Inizializza client-app-social"
   git push -u origin main
   ```
   > Sostituisci `main` con il nome del branch predefinito del tuo repository se diverso.
