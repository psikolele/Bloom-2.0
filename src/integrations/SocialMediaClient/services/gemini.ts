import { GoogleGenAI, Type } from "@google/genai";

const apiKey = process.env.GEMINI_API_KEY || '';

// Use the new SDK initialization
const ai = new GoogleGenAI({ apiKey });

/**
 * Scrapes website content using Jina AI Reader API (free service)
 * Returns clean markdown content of the website
 */
async function scrapeWebsite(url: string): Promise<string> {
    try {
        console.log(`🌐 Scraping content from: ${url}`);

        // Use Jina AI Reader - free service that returns clean markdown
        const jinaUrl = `https://r.jina.ai/${url}`;
        const response = await fetch(jinaUrl, {
            headers: {
                'Accept': 'text/plain',
                'X-Return-Format': 'markdown'
            }
        });

        if (!response.ok) {
            throw new Error(`Jina AI scraping failed: ${response.status} ${response.statusText}`);
        }

        const content = await response.text();

        // Limit content to ~15000 chars to avoid token limits
        const truncatedContent = content.slice(0, 15000);

        console.log(`✅ Successfully scraped ${truncatedContent.length} characters`);
        return truncatedContent;
    } catch (error: any) {
        console.error("❌ Scraping error:", error.message);
        throw new Error(`Impossibile scrapare il sito web: ${error.message}. Verifica che l'URL sia corretto e accessibile.`);
    }
}

/**
 * Searches for competitors using Google Search Grounding
 * Uses Gemini with Google Search to find real competitors and their Instagram accounts
 */
async function findCompetitors(brandName: string, sector: string, modelName: string): Promise<{
    competitor_1_name: string;
    competitor_1_instagram: string;
    competitor_2_name: string;
    competitor_2_instagram: string;
}> {
    try {
        console.log(`🔍 Searching for competitors of ${brandName} in ${sector} sector...`);

        // Configure Google Search Grounding tool
        const googleSearchTool = {
            googleSearch: {} // For Gemini 2.0+ models
        };

        const response = await ai.models.generateContent({
            model: modelName,
            contents: `Trova i 2 principali competitor diretti di "${brandName}" nel settore "${sector}" in Italia.

IMPORTANTE: USA Google Search per trovare informazioni REALI e aggiornate.

Per ogni competitor:
1. Trova il nome ufficiale dell'azienda competitor
2. Cerca il loro account Instagram ufficiale (deve esistere e essere verificabile)
3. Verifica che gli account Instagram siano reali

Restituisci la risposta in questo ESATTO formato JSON (e SOLO JSON, nient'altro):
{
  "competitor_1_name": "Nome ufficiale competitor 1",
  "competitor_1_instagram": "@username (o lascia vuoto se non trovato)",
  "competitor_2_name": "Nome ufficiale competitor 2",
  "competitor_2_instagram": "@username (o lascia vuoto se non trovato)"
}

NON aggiungere spiegazioni, SOLO il JSON.`,
            config: {
                tools: [googleSearchTool]
                // NOTA: Non usare responseMimeType con tools - causa conflitti
            }
        });

        const text = response.text;
        if (!text) {
            console.warn("⚠️ No competitors found via Google Search");
            return {
                competitor_1_name: "",
                competitor_1_instagram: "",
                competitor_2_name: "",
                competitor_2_instagram: ""
            };
        }

        console.log("📄 Raw response from Google Search:", text);

        // Try to extract JSON from response (might have markdown formatting)
        let jsonText = text.trim();

        // Remove markdown code blocks if present
        if (jsonText.startsWith('```json')) {
            jsonText = jsonText.replace(/```json\n?/g, '').replace(/```\n?/g, '');
        } else if (jsonText.startsWith('```')) {
            jsonText = jsonText.replace(/```\n?/g, '');
        }

        const competitors = JSON.parse(jsonText.trim());
        console.log(`✅ Found competitors: ${competitors.competitor_1_name}, ${competitors.competitor_2_name}`);

        return {
            competitor_1_name: competitors.competitor_1_name || "",
            competitor_1_instagram: competitors.competitor_1_instagram || "",
            competitor_2_name: competitors.competitor_2_name || "",
            competitor_2_instagram: competitors.competitor_2_instagram || ""
        };
    } catch (error: any) {
        console.error("❌ Competitor search error:", error.message);
        console.error("Full error:", error);
        // Return empty competitors on error - don't fail the entire process
        return {
            competitor_1_name: "",
            competitor_1_instagram: "",
            competitor_2_name: "",
            competitor_2_instagram: ""
        };
    }
}

// Define the schema based on user requirements
const brandProfileSchema = {
    type: Type.OBJECT,
    properties: {
        brand_name: { type: Type.STRING },
        website: { type: Type.STRING },
        settore: { type: Type.STRING },
        target_age: { type: Type.STRING },
        target_job: { type: Type.STRING },
        target_geo: { type: Type.STRING },
        tone_voice: { type: Type.STRING },
        pain_point_1: { type: Type.STRING },
        pain_point_2: { type: Type.STRING },
        pain_point_3: { type: Type.STRING },
        value_prop: { type: Type.STRING },
        competitor_1_name: { type: Type.STRING },
        competitor_1_instagram: { type: Type.STRING },
        competitor_2_name: { type: Type.STRING },
        competitor_2_instagram: { type: Type.STRING },
        max_emoji: { type: Type.NUMBER },
        post_length_min: { type: Type.NUMBER },
        post_length_max: { type: Type.NUMBER },
        confidence_score: { type: Type.NUMBER },
        warnings: { type: Type.STRING },
        keywords: {
            type: Type.ARRAY,
            items: { type: Type.STRING },
            description: "List of SEO and strategic keywords for the brand"
        },
        data_source: {
            type: Type.STRING,
            description: "Indicates if data is from actual website content or inferred"
        },
        scraping_quality: {
            type: Type.NUMBER,
            description: "Quality score of the scraped content (1-10), based on completeness and richness"
        }
    },
    required: ["brand_name", "settore", "keywords", "value_prop", "pain_point_1", "data_source", "scraping_quality"],
};

export interface BrandProfileData {
    brand_name?: string;
    website?: string;
    settore?: string;
    target_age?: string;
    target_job?: string;
    target_geo?: string;
    tone_voice?: string;
    pain_point_1?: string;
    pain_point_2?: string;
    pain_point_3?: string;
    value_prop?: string;
    competitor_1_name?: string;
    competitor_1_instagram?: string;
    competitor_2_name?: string;
    competitor_2_instagram?: string;
    max_emoji?: number;
    post_length_min?: number;
    post_length_max?: number;
    confidence_score?: number;
    warnings?: string;
    keywords?: string[];
    data_source?: string;
    scraping_quality?: number;
    [key: string]: any;
}

export const generateBrandProfile = async (websiteUrl: string, modelName: string): Promise<BrandProfileData> => {
    if (!apiKey || apiKey === 'your_gemini_api_key_here') {
        throw new Error(
            "⚠️ API Key mancante o non configurata!\n\n" +
            "Per risolvere questo problema:\n" +
            "1. Ottieni una API key gratuita da: https://aistudio.google.com/apikey\n" +
            "2. Apri il file .env.local nella cartella del progetto\n" +
            "3. Sostituisci 'your_gemini_api_key_here' con la tua API key\n" +
            "4. Riavvia l'applicazione\n\n" +
            "Esempio: GEMINI_API_KEY=AIzaSy..."
        );
    }

    try {
        // STEP 1: Scrape real website content
        console.log("📄 Step 1: Scraping website content...");
        const websiteContent = await scrapeWebsite(websiteUrl);

        if (!websiteContent || websiteContent.length < 100) {
            throw new Error("Il contenuto del sito web è troppo breve o vuoto. Verifica l'URL.");
        }

        // STEP 2: Generate brand profile based on REAL content
        console.log("🤖 Step 2: Analyzing content with AI...");
        const response = await ai.models.generateContent({
            model: modelName,
            contents: `# ISTRUZIONI CRITICHE - ANTI-ALLUCINAZIONE

Sei un analista di brand ESTREMAMENTE RIGOROSO. Devi analizzare SOLO il contenuto del sito web fornito qui sotto.

⚠️ REGOLE ASSOLUTE:
1. USA SOLO informazioni ESPLICITAMENTE presenti nel contenuto del sito web
2. Se una informazione NON è presente nel contenuto, scrivi "Non specificato" o lascia il campo vuoto
3. NON inventare competitor se non sono menzionati nel sito
4. NON inventare account Instagram se non sono linkati nel sito
5. NON dedurre, NON presumere, NON inventare NULLA
6. Se trovi competitor menzionati, usali. Altrimenti lascia vuoto
7. Il campo "data_source" DEVE essere "real_content"

URL del sito: "${websiteUrl}"

--- INIZIO CONTENUTO REALE DEL SITO WEB ---
${websiteContent}
--- FINE CONTENUTO REALE DEL SITO WEB ---

Analizza SOLO questo contenuto e crea un Brand Profile. Se un'informazione non è presente, NON inventarla.

Restituisci un oggetto JSON con questi campi (snake_case):
- brand_name: nome del brand (dal sito)
- website: "${websiteUrl}"
- settore: settore di business (SOLO se chiaramente identificabile)
- target_age: età del target (SOLO se menzionata, altrimenti "Non specificato")
- target_job: professione target (SOLO se menzionata, altrimenti "Non specificato")
- target_geo: area geografica (SOLO se menzionata, altrimenti "Non specificato")
- tone_voice: tono di voce del brand (es. "Professionale", "Amichevole", "Tecnico", "Creativo", ecc.)
- pain_point_1, pain_point_2, pain_point_3: problemi che il brand risolve (SOLO se espliciti)
- value_prop: proposta di valore (SOLO basata sul contenuto reale)
- competitor_1_name, competitor_1_instagram: competitor SOLO se menzionati nel sito, altrimenti ""
- competitor_2_name, competitor_2_instagram: competitor SOLO se menzionati nel sito, altrimenti ""
- max_emoji: suggerisci un numero (1-5) basato sul tone_voice
- post_length_min: suggerisci (100-300) basato sul settore
- post_length_max: suggerisci (400-800) basato sul settore
- confidence_score: 1-10 (quanto sei sicuro delle informazioni estratte)
- scraping_quality: 1-10 (valuta la qualità del contenuto scrapato: 10=contenuto ricco e completo, 1=contenuto scarso/parziale)
- warnings: segnala se hai dovuto lasciare campi vuoti o se mancano informazioni
- keywords: array di parole chiave REALMENTE presenti nel sito
- data_source: SEMPRE "real_content"`,
            config: {
                responseMimeType: "application/json",
                responseSchema: brandProfileSchema,
            }
        });

        const text = response.text;
        if (!text) {
            throw new Error("Nessuna risposta generata dall'AI.");
        }

        const result = JSON.parse(text) as BrandProfileData;

        // Validate that data_source is correct
        if (result.data_source !== "real_content") {
            result.data_source = "real_content";
        }

        // STEP 3: If competitors are missing, search for them using Google Search Grounding
        const hasCompetitors = result.competitor_1_name && result.competitor_1_name.trim() !== "";

        if (!hasCompetitors && result.brand_name && result.settore) {
            console.log("📊 Step 3: Competitors not found in website. Searching with Google Search...");

            try {
                const competitors = await findCompetitors(
                    result.brand_name,
                    result.settore,
                    modelName
                );

                // Merge competitor data into result
                result.competitor_1_name = competitors.competitor_1_name || "";
                result.competitor_1_instagram = competitors.competitor_1_instagram || "";
                result.competitor_2_name = competitors.competitor_2_name || "";
                result.competitor_2_instagram = competitors.competitor_2_instagram || "";

                // Update warnings to reflect Google Search was used
                if (competitors.competitor_1_name) {
                    result.warnings = (result.warnings || "") + " | Competitor trovati via Google Search";
                }
            } catch (searchError: any) {
                console.warn("⚠️ Could not find competitors via Google Search:", searchError.message);
                // Continue without competitors - don't fail the entire process
            }
        } else if (hasCompetitors) {
            console.log("✅ Competitors found in website content");
        }

        console.log("✅ Brand profile generated successfully!");
        return result;
    } catch (error: any) {
        console.error("❌ Gemini API Error:", error);

        // Check if it's a quota/credit exhausted error
        const errorMsg = error.message || "";
        if (errorMsg.includes("quota") ||
            errorMsg.includes("RESOURCE_EXHAUSTED") ||
            errorMsg.includes("exceeded your current quota")) {
            throw new Error("⚠️ Crediti insufficienti per questo modello AI. Prova con Gemini 2.5 Flash o Flash Lite (gratuiti).");
        }

        throw new Error(error.message || "Errore sconosciuto durante la generazione.");
    }
};