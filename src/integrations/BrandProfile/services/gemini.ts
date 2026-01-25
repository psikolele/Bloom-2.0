// import { Type } from "@google/genai"; // Removed as unused with OpenRouter implementation

const apiKey = import.meta.env.VITE_OPENROUTER_API_KEY || '';
const siteName = "Bloom 2.0";
const siteUrl = "http://localhost:5173"; // Or your deployed URL

/**
 * Scrapes website content using Jina AI Reader API (free service)
 * Returns clean markdown content of the website
 */
async function scrapeWebsite(url: string): Promise<string> {
    try {
        console.log(`🌐 Scraping content from: ${url}`);

        // Use Jina AI Reader - free service that returns clean markdown
        let targetUrl = url;
        if (!targetUrl.startsWith('http://') && !targetUrl.startsWith('https://')) {
            targetUrl = 'https://' + targetUrl;
        }

        const jinaUrl = `https://r.jina.ai/${targetUrl}`;
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

        // Limit content to ~15000 chars to avoid token limits (standardizing)
        const truncatedContent = content.slice(0, 15000);

        console.log(`✅ Successfully scraped ${truncatedContent.length} characters`);
        return truncatedContent;
    } catch (error: any) {
        console.error("❌ Scraping error:", error.message);
        throw new Error(`Impossibile scrapare il sito web: ${error.message}. Verifica che l'URL sia corretto e accessibile.`);
    }
}

/**
 * Calls OpenRouter Chat Completion API
 */
async function callOpenRouter(model: string, messages: any[], schema?: any) {
    if (!apiKey) {
        throw new Error("API Key mancante (process.env.OPENROUTER_API_KEY).");
    }

    // Default to Gemini Pro via OpenRouter if user selected a 'gemini' model name from the UI,
    // OR map the names.
    // The previous App.tsx used names like 'gemini-2.5-flash'. We need to map these to OpenRouter model IDs.
    // Or just use a versatile model if the specific one isn't on OpenRouter with that exact ID.
    // Mapping:
    // gemini-2.5-flash -> google/gemini-2.0-flash-001 (OpenRouter ID approximation)
    // gemini-2.5-pro -> google/gemini-2.0-pro-exp-02-05:free (or similar)

    // For simplicity, let's map common ones or pass through if already OR compatible
    let orModel = model;
    if (model.includes('flash')) orModel = 'google/gemini-2.0-flash-001';
    else if (model.includes('pro')) orModel = 'google/gemini-2.0-pro-exp-02-05:free'; // Using free tier if available or standard
    else orModel = 'google/gemini-2.0-flash-001'; // Fallback

    console.log(`🤖 Calling OpenRouter with model: ${orModel}`);

    const payload: any = {
        model: orModel,
        messages: messages,
        temperature: 0.7,
    };

    if (schema) {
        payload.response_format = { type: "json_object" }; // Generic JSON enforcement
        // OpenRouter supports 'json_schema' for some models, but 'json_object' is safer globally
    }

    const response = await fetch("https://openrouter.ai/api/v1/chat/completions", {
        method: "POST",
        headers: {
            "Authorization": `Bearer ${apiKey}`,
            "HTTP-Referer": siteUrl,
            "X-Title": siteName,
            "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
    });

    if (!response.ok) {
        const err = await response.text();
        throw new Error(`OpenRouter API Error: ${response.status} - ${err}`);
    }

    const data = await response.json();
    return data.choices[0].message.content;
}


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

    try {
        // STEP 1: Scrape real website content
        console.log("📄 Step 1: Scraping website content...");
        const websiteContent = await scrapeWebsite(websiteUrl);

        if (!websiteContent || websiteContent.length < 100) {
            throw new Error("Il contenuto del sito web è troppo breve o vuoto. Verifica l'URL.");
        }

        // STEP 2: Generate brand profile
        console.log("🤖 Step 2: Analyzing content with AI (OpenRouter)...");

        const systemPrompt = `Sei un analista di brand esperto. Analizza il contenuto del sito web fornito e estrai informazioni strutturate.
        
IMPORTANTE:
1. Restituisci SOLO un oggetto JSON valido.
2. Usa SOLO le informazioni presenti nel testo. Se non trovi qualcosa, usa "Non specificato" o stringa vuota.
3. NON includere markdown format (es. \`\`\`json). Restituisci raw JSON.`;

        const userPrompt = `Analizza questo contenuto web e crea un Brand Profile JSON.

URL: "${websiteUrl}"

CONTENUTO:
${websiteContent}

SCHEMA RICHIESTO (JSON):
{
  "brand_name": "string",
  "settore": "string",
  "target_age": "string",
  "target_job": "string",
  "target_geo": "string",
  "tone_voice": "string",
  "pain_point_1": "string",
  "pain_point_2": "string",
  "pain_point_3": "string",
  "value_prop": "string",
  "competitor_1_name": "string (se presente)",
  "competitor_1_instagram": "string (se presente)",
  "competitor_2_name": "string (se presente)",
  "competitor_2_instagram": "string (se presente)",
  "max_emoji": number (1-5),
  "post_length_min": number,
  "post_length_max": number,
  "confidence_score": number (1-10),
  "scraping_quality": number (1-10),
  "warnings": "string",
  "keywords": ["string", "string"],
  "data_source": "real_content"
}`;

        const content = await callOpenRouter(modelName, [
            { role: "system", content: systemPrompt },
            { role: "user", content: userPrompt }
        ], true);

        if (!content) {
            throw new Error("Nessuna risposta generata dall'AI.");
        }

        // Clean content if it has markdown code blocks (despite instructions)
        let jsonText = content.trim();
        if (jsonText.startsWith('```json')) {
            jsonText = jsonText.replace(/```json\n?/g, '').replace(/```\n?/g, '');
        } else if (jsonText.startsWith('```')) {
            jsonText = jsonText.replace(/```\n?/g, '');
        }

        const result = JSON.parse(jsonText) as BrandProfileData;

        // Ensure data_source is correct
        result.data_source = "real_content";
        result.website = websiteUrl;

        console.log("✅ Brand profile generated successfully!");
        return result;

    } catch (error: any) {
        console.error("❌ OpenRouter/Service Error:", error);
        throw new Error(error.message || "Errore sconosciuto durante la generazione.");
    }
};