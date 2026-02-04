// Brand Profile Generator v2.0 - Enhanced Targeting & Instagram Discovery
// Uses multi-step AI analysis for accurate persona creation
// Note: OpenRouter API key is handled server-side via Vercel proxy (/api/generate)


// ============================================================================
// SCRAPING UTILITIES
// ============================================================================

/**
 * Scrapes website content using Jina AI Reader API (free service)
 */
async function scrapeWebsite(url: string): Promise<string> {
    try {
        console.log(`🌐 Scraping content from: ${url}`);

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
        const truncatedContent = content.slice(0, 18000); // Increased for better context

        console.log(`✅ Successfully scraped ${truncatedContent.length} characters`);
        return truncatedContent;
    } catch (error: any) {
        console.error("❌ Scraping error:", error.message);
        throw new Error(`Impossibile scrapare il sito web: ${error.message}. Verifica che l'URL sia corretto e accessibile.`);
    }
}

/**
 * Search Google via Jina to find Instagram profile
 * Query: "[brand_name] instagram [location]"
 */
async function searchInstagram(brandName: string, location: string): Promise<{ url: string; handle: string } | null> {
    try {
        const query = `${brandName} instagram ${location}`.trim();
        console.log(`🔍 Searching Instagram via SERP: "${query}"`);

        // Use Jina Search (free Google SERP wrapper)
        const jinaSearchUrl = `https://s.jina.ai/${encodeURIComponent(query)}`;
        const response = await fetch(jinaSearchUrl, {
            headers: { 'Accept': 'text/plain' }
        });

        if (!response.ok) {
            console.warn(`⚠️ Instagram search failed: ${response.status}`);
            return null;
        }

        const searchResults = await response.text();

        // Extract Instagram URL from results
        const igRegex = /https?:\/\/(www\.)?instagram\.com\/([a-zA-Z0-9._]+)/gi;
        const matches = searchResults.matchAll(igRegex);

        for (const match of matches) {
            const handle = match[2];
            // Skip generic Instagram pages
            if (!['p', 'explore', 'reels', 'stories', 'accounts', 'about'].includes(handle.toLowerCase())) {
                console.log(`✅ Found Instagram: @${handle}`);
                return { url: match[0], handle: `@${handle}` };
            }
        }

        console.log(`ℹ️ No Instagram profile found for "${brandName}"`);
        return null;

    } catch (error: any) {
        console.error("❌ Instagram search error:", error.message);
        return null;
    }
}

/**
 * Geocode address using OpenStreetMap Nominatim API
 */
async function getCoordinates(address: string): Promise<{ lat: string, lon: string } | null> {
    try {
        if (!address) return null;
        console.log(`🌍 Geocoding address: "${address}"`);

        const url = `https://nominatim.openstreetmap.org/search?q=${encodeURIComponent(address)}&format=json&limit=1`;

        const response = await fetch(url, {
            headers: {
                'User-Agent': 'BloomAI-BrandProfile/2.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)' // Generic UA to satisfy policy
            }
        });

        if (!response.ok) return null;

        const data = await response.json();
        if (data && data.length > 0) {
            console.log(`📍 Found Coords: ${data[0].lat}, ${data[0].lon}`);
            return {
                lat: data[0].lat,
                lon: data[0].lon
            };
        }
        return null;
    } catch (e) {
        console.error("Geocoding error:", e);
        return null;
    }
}

// ============================================================================
// AI UTILITIES
// ============================================================================

/**
 * Calls OpenRouter Chat Completion API via Vercel Serverless Function
 */
async function callOpenRouter(model: string, messages: any[], jsonMode: boolean = false) {
    const proxyUrl = "/api/generate";

    let orModel = model;
    if (model.includes('flash-lite')) orModel = 'google/gemini-2.0-flash-lite-preview-02-05:free';
    else if (model.includes('flash')) orModel = 'google/gemini-2.0-flash-001';
    else if (model.includes('pro')) orModel = 'google/gemini-2.0-pro-exp-02-05:free';
    else orModel = 'google/gemini-2.0-flash-001';

    console.log(`🤖 Calling AI via Vercel Function... (${orModel})`);

    const payload: any = {
        model: orModel,
        messages: messages,
        temperature: 0.6,
        provider: { allow_fallbacks: true }
    };

    if (jsonMode) {
        payload.response_format = { type: "json_object" };
    }

    const response = await fetch(proxyUrl, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-Source": "Bloom-Frontend"
        },
        body: JSON.stringify(payload)
    });

    if (!response.ok) {
        let errText = await response.text();
        try {
            const errJson = JSON.parse(errText);
            if (errJson.error) errText = typeof errJson.error === 'string' ? errJson.error : JSON.stringify(errJson.error);
        } catch (e) { }
        console.error("❌ API Proxy Error:", errText);
        throw new Error(`AI Proxy Error (${response.status}): ${errText}`);
    }

    const data = await response.json();

    if (!data.choices || !data.choices[0] || !data.choices[0].message) {
        throw new Error("Risposta AI non valida (struttura inattesa).");
    }

    return data.choices[0].message.content;
}

/**
 * Parse JSON response, handling markdown code blocks
 */
function parseJsonResponse(content: string): any {
    let jsonText = content.trim();
    if (jsonText.startsWith('```json')) {
        jsonText = jsonText.replace(/```json\n?/g, '').replace(/```\n?$/g, '');
    } else if (jsonText.startsWith('```')) {
        jsonText = jsonText.replace(/```\n?/g, '');
    }
    return JSON.parse(jsonText);
}

// ============================================================================
// BRAND PROFILE INTERFACE
// ============================================================================

export interface BrandProfileData {
    brand_name?: string;
    website?: string;
    settore?: string;
    // Enhanced Targeting
    target_age?: string;
    target_gender?: string;
    target_job?: string;
    target_geo?: string;
    target_interests?: string;
    target_behaviors?: string;
    buyer_persona?: string;
    // Tone & Voice
    tone_voice?: string;
    // Pain Points & Value
    pain_point_1?: string;
    pain_point_2?: string;
    pain_point_3?: string;
    value_prop?: string;
    // Competitors
    competitor_1_name?: string;
    competitor_1_instagram?: string;
    competitor_2_name?: string;
    competitor_2_instagram?: string;
    // Brand Social
    brand_instagram_url?: string;
    brand_instagram_handle?: string;
    // Post Guidelines
    max_emoji?: number;
    post_length_min?: number;
    post_length_max?: number;
    // Metadata
    confidence_score?: number;
    warnings?: string;
    keywords?: string[];
    data_source?: string;
    scraping_quality?: number;
    physical_address?: string;
    latitude?: string;
    longitude?: string;
    [key: string]: any;
}

// ============================================================================
// MAIN GENERATION FUNCTION
// ============================================================================

export const generateBrandProfile = async (websiteUrl: string, modelName: string): Promise<BrandProfileData> => {

    try {
        // =====================================================================
        // STEP 1: Scrape website content
        // =====================================================================
        console.log("📄 Step 1: Scraping website content...");
        const websiteContent = await scrapeWebsite(websiteUrl);

        if (!websiteContent || websiteContent.length < 100) {
            throw new Error("Il contenuto del sito web è troppo breve o vuoto. Verifica l'URL.");
        }

        // =====================================================================
        // STEP 2: Deep Analysis with Enhanced Targeting Prompt
        // =====================================================================
        console.log("🤖 Step 2: Deep brand & targeting analysis...");

        const systemPrompt = `Sei un esperto analista di marketing digitale e brand strategist con 15 anni di esperienza.
Il tuo compito è analizzare il contenuto di un sito web aziendale e creare un profilo brand completo con un'analisi DETTAGLIATA del target audience.

REGOLE CRITICHE:
1. Restituisci SOLO un oggetto JSON valido, senza markdown.
2. Usa ESCLUSIVAMENTE le informazioni presenti nel contenuto. Se non trovi qualcosa, usa "Non specificato".
3. Per il TARGETING, devi fare un'analisi approfondita basata su:
   - Il tipo di prodotti/servizi offerti
   - Il linguaggio e il tono usato nel sito
   - I prezzi (se visibili) per dedurre il potere d'acquisto
   - Le immagini e lo stile visivo descritti
   - I problemi che il brand risolve (per capire chi ha quei problemi)
4. Per la GEOLOCALIZZAZIONE, cerca indirizzi fisici, città, regioni menzionate nel contenuto.
5. Per i PAIN POINTS, identifica i problemi specifici che il target affronta e che il brand risolve.`;

        const targetingPrompt = `Analizza questo contenuto web e crea un Brand Profile con TARGETING AVANZATO.

URL ANALIZZATO: "${websiteUrl}"

CONTENUTO DEL SITO:
${websiteContent}

ISTRUZIONI PER IL TARGETING:
- "target_age": Fascia d'età specifica (es. "25-34 anni", "Millennials 28-40", "Gen Z 18-25")
- "target_gender": Genere prevalente se deducibile (es. "Prevalentemente femminile", "Misto", "Maschile 70%")
- "target_job": Professioni/ruoli specifici (es. "Manager e Dirigenti PMI", "Liberi professionisti del settore creativo")
- "target_geo": Località ESATTA se presente un indirizzo, altrimenti regione/nazione in base al contesto
- "target_interests": Interessi correlati al brand (es. "Sostenibilità, Design, Tecnologia")
- "target_behaviors": Comportamenti d'acquisto (es. "Acquista online, cerca qualità premium, fedele ai brand")
- "buyer_persona": Una descrizione narrativa di 2-3 frasi del cliente ideale tipo

ISTRUZIONI PER L'INDIRIZZO:
- "physical_address": Se trovi un indirizzo fisico completo (via, città, CAP), riportalo esattamente

SCHEMA JSON RICHIESTO:
{
  "brand_name": "string",
  "settore": "string",
  "physical_address": "string (indirizzo completo se presente)",
  "target_age": "string (fascia d'età specifica)",
  "target_gender": "string (distribuzione genere)",
  "target_job": "string (professioni target)",
  "target_geo": "string (località/regione basata su indirizzo o contesto)",
  "target_interests": "string (interessi correlati)",
  "target_behaviors": "string (comportamenti d'acquisto)",
  "buyer_persona": "string (descrizione narrativa cliente ideale)",
  "tone_voice": "string (es. Professionale, Amichevole, Tecnico)",
  "pain_point_1": "string (problema principale del target)",
  "pain_point_2": "string (secondo problema)",
  "pain_point_3": "string (terzo problema)",
  "value_prop": "string (proposta di valore unica)",
  "competitor_1_name": "string",
  "competitor_1_instagram": "string",
  "competitor_2_name": "string",
  "competitor_2_instagram": "string",
  "max_emoji": number (0-5),
  "post_length_min": number,
  "post_length_max": number,
  "confidence_score": number (1-10),
  "scraping_quality": number (1-10),
  "warnings": "string",
  "keywords": ["array", "di", "keywords"]
}`;

        const content = await callOpenRouter(modelName, [
            { role: "system", content: systemPrompt },
            { role: "user", content: targetingPrompt }
        ], true);

        if (!content) {
            throw new Error("Nessuna risposta generata dall'AI.");
        }

        const result = parseJsonResponse(content) as BrandProfileData;

        // =====================================================================
        // STEP 3: Search for Instagram profile via SERP
        // =====================================================================
        console.log("🔍 Step 3: Searching for brand's Instagram...");

        const brandName = result.brand_name || '';
        const location = result.target_geo || result.physical_address || '';

        if (brandName) {
            const instagramResult = await searchInstagram(brandName, location);
            if (instagramResult) {
                result.brand_instagram_url = instagramResult.url;
                result.brand_instagram_handle = instagramResult.handle;
            }
        }

        // =====================================================================
        // STEP 4: Geocoding
        // =====================================================================
        if (location || result.physical_address) {
            const coords = await getCoordinates(result.physical_address || location);
            if (coords) {
                result.latitude = coords.lat;
                result.longitude = coords.lon;
            }
        }

        // =====================================================================
        // STEP 4: Finalize and return
        // =====================================================================
        result.data_source = "real_content";
        result.website = websiteUrl;

        console.log("✅ Brand profile generated successfully!");
        console.log(`   📍 Location: ${result.target_geo}`);
        console.log(`   👥 Target: ${result.target_age} | ${result.target_job}`);
        console.log(`   📸 Instagram: ${result.brand_instagram_handle || 'Non trovato'}`);

        return result;

    } catch (error: any) {
        console.error("❌ OpenRouter/Service Error:", error);
        throw new Error(error.message || "Errore sconosciuto durante la generazione.");
    }
};
