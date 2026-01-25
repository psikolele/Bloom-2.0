
import { VercelRequest, VercelResponse } from '@vercel/node';

export default async function handler(req: VercelRequest, res: VercelResponse) {
    // 1. Handle CORS
    res.setHeader('Access-Control-Allow-Credentials', 'true');
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET,OPTIONS,PATCH,DELETE,POST,PUT');
    res.setHeader('Access-Control-Allow-Headers', 'X-CSRF-Token, X-Requested-With, Accept, Accept-Version, Content-Length, Content-MD5, Content-Type, Date, X-Api-Version, X-Source');

    // Handle Preflight OPTIONS
    if (req.method === 'OPTIONS') {
        res.status(200).end();
        return;
    }

    if (req.method !== 'POST') {
        return res.status(405).json({ error: 'Method Not Allowed' });
    }

    // 2. Validate API Key (Server-side environment variable)
    const apiKey = process.env.VITE_OPENROUTER_API_KEY;
    // Note: In Vercel, standard env vars are accessed via process.env. 
    // VITE_ prefixed vars are exposed to browser, but we can also read them here if set in Project Settings.
    // Ideally, for security, use a non-VITE prefixed var like OPENROUTER_API_KEY in Vercel Dashboard, 
    // but for now we rely on the existing one which is cleaner than N8N.

    if (!apiKey) {
        return res.status(500).json({ error: 'Server Configuration Error: Missing API Key' });
    }

    try {
        const { model, messages, temperature, provider } = req.body;

        // 3. Call OpenRouter
        const response = await fetch("https://openrouter.ai/api/v1/chat/completions", {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${apiKey}`,
                "HTTP-Referer": "https://bloom-dashboard.com", // Dynamic or fixed
                "X-Title": "Bloom 2.0",
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                model,
                messages,
                temperature,
                provider
            })
        });

        if (!response.ok) {
            const errorText = await response.text();
            return res.status(response.status).json({ error: errorText });
        }

        const data = await response.json();
        return res.status(200).json(data);

    } catch (error: any) {
        console.error("API Proxy Error:", error);
        return res.status(500).json({ error: error.message });
    }
}
