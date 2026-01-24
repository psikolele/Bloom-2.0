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
   `npm install`
2. Set the `GEMINI_API_KEY` in [.env.local](.env.local) to your Gemini API key
3. Run the app:
   `npm run dev`

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
