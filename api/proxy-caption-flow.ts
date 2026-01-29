
import { VercelRequest, VercelResponse } from '@vercel/node';

export const config = {
    maxDuration: 60,
};

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

    try {
        const N8N_WEBHOOK_URL = 'https://emanueleserra.app.n8n.cloud/webhook/caption-flow';

        // Setup timeout controller (50s to stay within Vercel 60s limit and handle fallback)
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 50000);

        try {
            const response = await fetch(N8N_WEBHOOK_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(req.body),
                signal: controller.signal
            });

            clearTimeout(timeoutId);

            // Handle Cloudflare Timeouts (524) or Gateway Timeouts (504) as "Success with delay"
            if (response.status === 524 || response.status === 504) {
                console.warn(`N8N Gateway Timeout (${response.status}), returning fallback success`);
                return res.status(200).json({
                    success: true,
                    message: "La generazione sta richiedendo più tempo del previsto. Riceverai il risultato finale via email appena pronto!",
                    data: null
                });
            }

            if (!response.ok) {
                const errorText = await response.text();
                console.error(`N8N Error ${response.status}: ${errorText}`);
                return res.status(response.status).json({
                    success: false,
                    message: `Errore dal server: ${response.status}`,
                    debug: errorText
                });
            }

            const data = await response.json();
            return res.status(200).json(data);

        } catch (fetchError: any) {
            clearTimeout(timeoutId);

            // Handle Client-side Timeout (AbortError)
            if (fetchError.name === 'AbortError' || fetchError.message.includes('timeout')) {
                console.warn("Proxy client timeout, returning fallback success");
                return res.status(200).json({
                    success: true,
                    message: "La generazione è in corso ma richiede tempo. Riceverai il risultato via email!",
                    data: null
                });
            }
            throw fetchError;
        }

    } catch (error: any) {
        console.error("Proxy Internal Error:", error);
        return res.status(500).json({
            success: false,
            message: 'Si è verificato un errore interno nel proxy.',
            error: error.message
        });
    }
}
