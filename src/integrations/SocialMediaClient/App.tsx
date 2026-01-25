
import React, { useState, useEffect } from 'react';
import { Icons } from './components/Icons';
import { SpotlightCard } from './components/SpotlightCard';
// import { Logo } from './components/Logo'; // Removed as replaced by image assets

// --- CONFIG ---
// --- CONFIG ---
// --- CONFIG ---

const COMMUNICATION_TYPES = [
    "Educational",
    "Promozionale",
    "Storytelling",
    "Informativo",
    "Emozionale",
    "Istituzionale"
];

const SOCIAL_PLATFORMS = [
    "Instagram",
    "Facebook",
    "LinkedIn",
    "TikTok",
    "Twitter/X",
    "YouTube"
];

// --- INTERFACES ---
interface Product {
    id: string;
    nome: string;
    descrizione: string;
    link_competitor_1: string;
    link_competitor_2: string;
    link_competitor_3: string;
}

interface ImageFile {
    id: string;
    name: string;
    preview: string;
    data: string; // base64
}

interface FormData {
    // Informazioni Azienda
    nome_azienda: string;
    sito_web: string;
    indirizzo: string;
    email_contatto: string;
    link_facebook: string;
    link_instagram: string;
    link_linkedin: string;
    altri_link: string;

    // Strategia
    strategia_aziendale: string;
    tipologia_comunicazione: string;
    social_platforms: string[];
    prodotti: Product[];
    immagini: ImageFile[];
}

// --- COMPONENTS ---

const AnimatedLoader = () => (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-void/95 backdrop-blur-sm">
        <div className="flex flex-col items-center gap-6">
            {/* Animated Logo */}
            <div className="relative">
                <div className="absolute inset-0 animate-ping">
                    <div className="w-24 h-24 bg-accent/20 rounded-full"></div>
                </div>
                <div className="relative animate-pulse">
                    <img src="/icon.png" alt="Loading" className="w-24 h-24 object-contain drop-shadow-[0_0_40px_rgba(255,107,53,0.6)]" />
                </div>
            </div>

            {/* Loading Bar */}
            <div className="w-64 h-1.5 bg-white/10 rounded-full overflow-hidden">
                <div className="h-full bg-gradient-to-r from-accent to-purple-500 rounded-full animate-[loading_1.5s_ease-in-out_infinite]"></div>
            </div>

            {/* Loading Text */}
            <div className="flex items-center gap-2">
                <span className="text-white font-mono text-sm">Caricamento</span>
                <div className="flex gap-1">
                    <span className="w-1.5 h-1.5 bg-accent rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></span>
                    <span className="w-1.5 h-1.5 bg-accent rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></span>
                    <span className="w-1.5 h-1.5 bg-accent rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></span>
                </div>
            </div>
        </div>

        <style>{`
            @keyframes loading {
                0% { transform: translateX(-100%); }
                50% { transform: translateX(100%); }
                100% { transform: translateX(100%); }
            }
        `}</style>
    </div>
);

const SuccessMessage = ({ onReset }: { onReset: () => void }) => (
    <div className="glass-panel border-emerald-500/20 p-6 rounded-xl text-center animate-reveal">
        <div className="w-12 h-12 bg-emerald-500 rounded-full flex items-center justify-center mb-3 mx-auto text-black">
            <Icons.Check width={24} height={24} />
        </div>
        <h3 className="text-white font-bold font-mono">Dati Inviati con Successo!</h3>
        <p className="text-gray-400 text-sm mt-2">La tua strategia marketing è stata inviata al sistema di automazione.</p>
        <button onClick={onReset} className="mt-4 text-xs text-gray-400 hover:text-white underline font-mono">NUOVA STRATEGIA</button>
    </div>
);

const BloomRedirectLoader = () => (
    <div className="fixed inset-0 z-[100] flex items-center justify-center bg-[#030303]">
        <div className="relative w-32 h-32 flex items-center justify-center animate-[scaleUp_0.6s_ease-out]">
            {/* Glow Ring - Thin Circular with Mask */}
            <div
                className="absolute inset-0 rounded-full bg-[conic-gradient(from_0deg,transparent_0%,transparent_40%,#FF6B35_50%,#B349C1_60%,transparent_70%)] animate-[spin_1s_linear_infinite] z-10 opacity-90"
                style={{ maskImage: 'radial-gradient(transparent 63%, black 65%)', WebkitMaskImage: 'radial-gradient(transparent 63%, black 65%)' }}
            ></div>
            {/* Logo */}
            <div className="relative z-20 transform scale-[0.8]">
                <img src="/icon.png" alt="Loading" className="w-20 h-20 object-contain drop-shadow-[0_0_20px_rgba(255,107,53,0.6)]" />
            </div>
        </div>
        <style>{`
            @keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
            @keyframes scaleUp { from { transform: scale(0.9); opacity: 0; } to { transform: scale(1); opacity: 1; } }
        `}</style>
    </div>
);

// --- MAIN APP ---

export default function App() {
    const [isInitialLoading, setIsInitialLoading] = useState(true);
    const [isLoading, setIsLoading] = useState(false);
    const [isRedirecting, setIsRedirecting] = useState(false);
    const [formData, setFormData] = useState<FormData>({
        nome_azienda: "",
        sito_web: "",
        indirizzo: "",
        email_contatto: "",
        link_facebook: "",
        link_instagram: "",
        link_linkedin: "",
        altri_link: "",
        strategia_aziendale: "",
        tipologia_comunicazione: "",
        social_platforms: [],
        prodotti: [],
        immagini: []
    });

    const [status, setStatus] = useState<"idle" | "publishing" | "success" | "error">("idle");
    const [errorMsg, setErrorMsg] = useState("");

    // Animazione di caricamento iniziale
    useEffect(() => {
        const timer = setTimeout(() => {
            setIsInitialLoading(false);
        }, 1500);
        return () => clearTimeout(timer);
    }, []);

    const updateField = (field: keyof FormData, value: any) => {
        setFormData(prev => ({ ...prev, [field]: value }));
    };

    const toggleArrayItem = (field: 'social_platforms', item: string) => {
        setFormData(prev => {
            const currentArray = prev[field];
            const newArray = currentArray.includes(item)
                ? currentArray.filter(i => i !== item)
                : [...currentArray, item];
            return { ...prev, [field]: newArray };
        });
    };

    const addProduct = () => {
        const newProduct: Product = {
            id: Date.now().toString(),
            nome: "",
            descrizione: "",
            link_competitor_1: "",
            link_competitor_2: "",
            link_competitor_3: ""
        };
        setFormData(prev => ({ ...prev, prodotti: [...prev.prodotti, newProduct] }));
    };

    const updateProduct = (id: string, field: keyof Product, value: string) => {
        setFormData(prev => ({
            ...prev,
            prodotti: prev.prodotti.map(p => p.id === id ? { ...p, [field]: value } : p)
        }));
    };

    const removeProduct = (id: string) => {
        setFormData(prev => ({
            ...prev,
            prodotti: prev.prodotti.filter(p => p.id !== id)
        }));
    };

    const handleImageUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
        const files = e.target.files;
        if (!files) return;

        Array.from(files).forEach(file => {
            if (!file.type.startsWith('image/')) {
                showError('Per favore seleziona solo file immagine.');
                return;
            }

            const reader = new FileReader();
            reader.onloadend = () => {
                const newImage: ImageFile = {
                    id: Date.now().toString() + Math.random(),
                    name: file.name,
                    preview: reader.result as string,
                    data: reader.result as string
                };
                setFormData(prev => ({
                    ...prev,
                    immagini: [...prev.immagini, newImage]
                }));
            };
            reader.readAsDataURL(file);
        });

        // Reset input
        e.target.value = '';
    };

    const removeImage = (id: string) => {
        setFormData(prev => ({
            ...prev,
            immagini: prev.immagini.filter(img => img.id !== id)
        }));
    };

    const handleSubmit = async () => {
        // Validazione base - primi 4 campi obbligatori
        if (!formData.nome_azienda.trim()) {
            return showError("Inserisci il nome dell'azienda o professionista.");
        }
        if (!formData.sito_web.trim()) {
            return showError("Inserisci il sito web.");
        }
        if (!formData.indirizzo.trim()) {
            return showError("Inserisci l'indirizzo fisico.");
        }
        if (!formData.email_contatto.trim()) {
            return showError("Inserisci l'email di contatto.");
        }
        if (!formData.strategia_aziendale.trim()) {
            return showError("Inserisci la strategia aziendale.");
        }
        if (formData.social_platforms.length === 0) {
            return showError("Seleziona almeno un social network.");
        }

        setIsLoading(true);
        setStatus("publishing");
        setErrorMsg("");

        try {
            const payload = {
                ...formData,
                timestamp: new Date().toISOString()
            };

            console.log("📤 Sending payload to N8N:", payload);
            console.log("🔗 Webhook URL:", import.meta.env.VITE_CAPTION_FLOW_WEBHOOK_URL);

            const res = await fetch(import.meta.env.VITE_CAPTION_FLOW_WEBHOOK_URL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            console.log("📥 Response status:", res.status);

            if (res.ok) {
                const responseText = await res.text();
                console.log("✅ Response body:", responseText);
                // Mantieni il loader visibile per almeno 2 secondi
                setTimeout(() => {
                    setIsLoading(false);
                    setStatus("success");
                }, 2000);
            } else {
                const errorText = await res.text();
                console.error("❌ Error response:", errorText);
                throw new Error(`HTTP ${res.status}: ${errorText || 'No error details'}`);
            }
        } catch (e: any) {
            console.error("❌ Full error:", e);
            setIsLoading(false);

            if (e instanceof TypeError && e.message.includes('Failed to fetch')) {
                showError("Errore di rete o CORS. Verifica la connessione al server.");
            } else {
                showError(`Errore Invio: ${e.message || 'Errore sconosciuto'}`);
            }
            setStatus("error");
        }
    };

    const showError = (msg: string) => {
        setErrorMsg(msg);
        setTimeout(() => setErrorMsg(""), 8000);
    };

    const reset = () => {
        setFormData({
            nome_azienda: "",
            sito_web: "",
            indirizzo: "",
            email_contatto: "",
            link_facebook: "",
            link_instagram: "",
            link_linkedin: "",
            altri_link: "",
            strategia_aziendale: "",
            tipologia_comunicazione: "",
            social_platforms: [],
            prodotti: [],
            immagini: []
        });
        setStatus("idle");
        setErrorMsg("");
    };

    const handleReturnToBloom = () => {
        setIsRedirecting(true);
        setTimeout(() => {
            window.location.href = '/';
        }, 2500);
    };

    return (
        <div className="min-h-screen relative font-sans text-gray-200 pb-10 overflow-x-hidden">
            {(isLoading || isInitialLoading) && <AnimatedLoader />}
            {isRedirecting && <BloomRedirectLoader />}

            <div className="ambient-light"></div>
            <div className="grid-overlay"></div>

            <nav className="relative z-50 px-6 py-6 w-full max-w-[90%] mx-auto flex items-center justify-between">
                <div className="flex items-center gap-3">
                    <img src="/logo.png" alt="Bloom AI" className="h-10 w-auto object-contain drop-shadow-[0_0_20px_rgba(255,107,53,0.4)]" />
                    <div className="h-6 w-px bg-white/20 mx-2"></div>
                    <span className="font-mono font-bold text-xl tracking-tighter text-white">SocialFlow</span>
                </div>

                <div className="flex items-center gap-4">
                    <div className="flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-[10px] font-mono uppercase">
                        <div className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></div>
                        <span className="hidden sm:inline">System Online</span>
                    </div>

                    <button
                        onClick={handleReturnToBloom}
                        className="flex items-center gap-2 bg-white/5 border border-white/10 px-4 py-2 rounded-full backdrop-blur-md text-gray-200 font-mono text-xs font-medium hover:bg-white/10 hover:border-white/20 transition-all hover:-translate-y-px hover:shadow-lg group"
                    >
                        <Icons.ArrowLeft width={14} height={14} className="group-hover:-translate-x-1 transition-transform" />
                        <span>Back to Hub</span>
                    </button>
                </div>
            </nav>

            <main className="relative z-10 w-full md:w-[85%] max-w-7xl mx-auto px-4 mt-8 md:mt-12">
                <div className="text-center mb-12 space-y-4 animate-[reveal_0.8s_ease-out]">
                    <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-accent/5 border border-accent/20 mb-2 backdrop-blur-sm">
                        <Icons.Zap width={14} height={14} className="text-accent animate-pulse" />
                        <span className="text-accent text-[10px] font-bold tracking-widest uppercase">Marketing Strategy Collection</span>
                    </div>

                    {/* Animated Title with Loop */}
                    <h1 className="text-4xl md:text-6xl font-bold tracking-tight font-mono">
                        <span className="inline-block text-transparent bg-clip-text bg-gradient-to-r from-accent via-orange-400 to-purple-500 animate-[gradientShift_3s_ease-in-out_infinite,fadeInUp_0.6s_ease-out] bg-[length:200%_auto]">
                            Marketing
                        </span>
                        <br />
                        <span className="inline-block text-transparent bg-clip-text bg-gradient-to-r from-purple-500 via-pink-500 to-accent animate-[gradientShift_3s_ease-in-out_infinite_0.5s,fadeInUp_0.8s_ease-out_0.2s,textGlow_2s_ease-in-out_infinite] bg-[length:200%_auto] opacity-0" style={{ animationFillMode: 'forwards' }}>
                            Configurator.
                        </span>
                    </h1>
                    <p className="text-gray-400 text-sm max-w-2xl mx-auto animate-[fadeIn_1s_ease-out_0.5s] opacity-0" style={{ animationFillMode: 'forwards' }}>
                        Configura la tua strategia di marketing digitale in modo semplice e veloce
                    </p>
                </div>

                {status === 'success' ? (
                    <SuccessMessage onReset={reset} />
                ) : (
                    <SpotlightCard className="p-6 md:p-8 transition-all duration-700 animate-[reveal_1s_ease-out_0.2s_both]">
                        <div className="space-y-8">

                            {/* SEZIONE 1: Informazioni Azienda */}
                            <div className="space-y-4">
                                <label className="text-xs font-bold text-accent uppercase tracking-widest font-mono pl-1 flex items-center gap-2">
                                    <Icons.Shield width={14} height={14} />
                                    01. Informazioni Azienda
                                </label>

                                <div className="grid md:grid-cols-2 gap-4">
                                    <input
                                        type="text"
                                        value={formData.nome_azienda}
                                        onChange={e => updateField('nome_azienda', e.target.value)}
                                        placeholder="Nome Azienda / Brand / Professionista *"
                                        required
                                        className="w-full tech-input rounded-lg py-3 px-4 text-sm font-mono placeholder:text-gray-600"
                                    />
                                    <input
                                        type="url"
                                        value={formData.sito_web}
                                        onChange={e => updateField('sito_web', e.target.value)}
                                        placeholder="Sito Web (es. https://...) *"
                                        required
                                        className="w-full tech-input rounded-lg py-3 px-4 text-sm font-mono placeholder:text-gray-600"
                                    />
                                </div>

                                <div className="grid md:grid-cols-2 gap-4">
                                    <input
                                        type="text"
                                        value={formData.indirizzo}
                                        onChange={e => updateField('indirizzo', e.target.value)}
                                        placeholder="Indirizzo Fisico *"
                                        required
                                        className="w-full tech-input rounded-lg py-3 px-4 text-sm font-mono placeholder:text-gray-600"
                                    />
                                    <input
                                        type="email"
                                        value={formData.email_contatto}
                                        onChange={e => updateField('email_contatto', e.target.value)}
                                        placeholder="Mail di Contatto *"
                                        required
                                        className="w-full tech-input rounded-lg py-3 px-4 text-sm font-mono placeholder:text-gray-600"
                                    />
                                </div>

                                <div className="space-y-2">
                                    <div className="text-[10px] text-gray-400 uppercase font-mono pl-1">Link Social Media</div>
                                    <div className="grid md:grid-cols-2 gap-3">
                                        <input
                                            type="url"
                                            value={formData.link_facebook}
                                            onChange={e => updateField('link_facebook', e.target.value)}
                                            placeholder="Link Facebook"
                                            className="w-full tech-input rounded-lg py-2.5 px-4 text-xs font-mono placeholder:text-gray-600"
                                        />
                                        <input
                                            type="url"
                                            value={formData.link_instagram}
                                            onChange={e => updateField('link_instagram', e.target.value)}
                                            placeholder="Link Instagram"
                                            className="w-full tech-input rounded-lg py-2.5 px-4 text-xs font-mono placeholder:text-gray-600"
                                        />
                                        <input
                                            type="url"
                                            value={formData.link_linkedin}
                                            onChange={e => updateField('link_linkedin', e.target.value)}
                                            placeholder="Link LinkedIn"
                                            className="w-full tech-input rounded-lg py-2.5 px-4 text-xs font-mono placeholder:text-gray-600"
                                        />
                                        <input
                                            type="text"
                                            value={formData.altri_link}
                                            onChange={e => updateField('altri_link', e.target.value)}
                                            placeholder="Altri Link / Piattaforme"
                                            className="w-full tech-input rounded-lg py-2.5 px-4 text-xs font-mono placeholder:text-gray-600"
                                        />
                                    </div>
                                </div>
                            </div>

                            {/* SEZIONE 2: Strategia Aziendale */}
                            <div className="space-y-3">
                                <label className="text-xs font-bold text-accent uppercase tracking-widest font-mono pl-1 flex items-center gap-2">
                                    <Icons.Target width={14} height={14} />
                                    02. Strategia Aziendale
                                </label>
                                <textarea
                                    value={formData.strategia_aziendale}
                                    onChange={e => updateField('strategia_aziendale', e.target.value)}
                                    placeholder="Descrivi la tua strategia aziendale, obiettivi e vision... *"
                                    rows={5}
                                    className="w-full tech-input rounded-xl py-4 px-4 text-sm font-mono placeholder:text-gray-600 resize-none"
                                />
                            </div>

                            {/* SEZIONE 3: Tipologia Comunicazione */}
                            <div className="space-y-3">
                                <label className="text-xs font-bold text-accent uppercase tracking-widest font-mono pl-1 flex items-center gap-2">
                                    <Icons.Send width={14} height={14} />
                                    03. Tipologia Comunicazione
                                </label>
                                <select
                                    value={formData.tipologia_comunicazione}
                                    onChange={e => updateField('tipologia_comunicazione', e.target.value)}
                                    className="w-full tech-input rounded-xl py-4 px-4 text-sm font-mono bg-[#0a0a0a] text-white"
                                >
                                    <option value="">Seleziona una tipologia...</option>
                                    {COMMUNICATION_TYPES.map(type => (
                                        <option key={type} value={type} className="bg-[#0a0a0a] text-white py-3">
                                            {type}
                                        </option>
                                    ))}
                                </select>
                            </div>

                            {/* SEZIONE 4: Scelta Social */}
                            <div className="space-y-3">
                                <label className="text-xs font-bold text-accent uppercase tracking-widest font-mono pl-1 flex items-center gap-2">
                                    <Icons.Zap width={14} height={14} />
                                    04. Piattaforme Social
                                </label>
                                <div className="flex flex-wrap gap-2">
                                    {SOCIAL_PLATFORMS.map(platform => (
                                        <button
                                            key={platform}
                                            onClick={() => toggleArrayItem('social_platforms', platform)}
                                            className={`px-4 py-2.5 rounded-xl text-sm font-mono transition-all border ${formData.social_platforms.includes(platform)
                                                ? 'bg-accent text-white border-accent shadow-[0_0_20px_rgba(255,107,53,0.3)]'
                                                : 'bg-white/5 text-gray-400 border-white/10 hover:border-accent/50'
                                                }`}
                                        >
                                            {platform}
                                        </button>
                                    ))}
                                </div>
                            </div>

                            {/* SEZIONE 5: Prodotti/Servizi con Competitor */}
                            <div className="space-y-4">
                                <div className="flex items-center justify-between">
                                    <label className="text-xs font-bold text-accent uppercase tracking-widest font-mono pl-1 flex items-center gap-2">
                                        <Icons.Tag width={14} height={14} />
                                        05. Prodotti / Servizi & Competitor
                                    </label>
                                    <button
                                        onClick={addProduct}
                                        className="px-4 py-2 rounded-lg bg-accent/10 border border-accent/30 text-accent hover:bg-accent hover:text-white transition-all text-xs font-mono font-bold uppercase flex items-center gap-2"
                                    >
                                        <span className="text-lg leading-none">+</span>
                                        Aggiungi
                                    </button>
                                </div>

                                {formData.prodotti.length === 0 ? (
                                    <div className="bg-white/[0.03] border border-white/10 rounded-xl p-8 text-center">
                                        <Icons.Tag width={32} height={32} className="text-gray-600 mx-auto mb-3" />
                                        <p className="text-gray-500 text-sm font-mono">Nessun prodotto aggiunto. Clicca "Aggiungi" per iniziare.</p>
                                    </div>
                                ) : (
                                    <div className="space-y-4">
                                        {formData.prodotti.map((product, index) => (
                                            <div key={product.id} className="bg-white/[0.03] border border-white/10 rounded-xl p-6 space-y-4 hover:border-accent/30 transition-colors">
                                                <div className="flex items-center justify-between mb-2">
                                                    <span className="text-xs font-bold text-gray-400 uppercase font-mono">Prodotto/Servizio #{index + 1}</span>
                                                    <button
                                                        onClick={() => removeProduct(product.id)}
                                                        className="text-red-400 hover:text-red-300 text-xs font-mono uppercase"
                                                    >
                                                        Rimuovi
                                                    </button>
                                                </div>

                                                <div className="space-y-3">
                                                    <input
                                                        type="text"
                                                        value={product.nome}
                                                        onChange={e => updateProduct(product.id, 'nome', e.target.value)}
                                                        placeholder="Nome prodotto/servizio"
                                                        className="w-full tech-input rounded-lg py-2.5 px-4 text-sm font-mono placeholder:text-gray-600"
                                                    />

                                                    <textarea
                                                        value={product.descrizione}
                                                        onChange={e => updateProduct(product.id, 'descrizione', e.target.value)}
                                                        placeholder="Descrizione del prodotto/servizio..."
                                                        rows={3}
                                                        className="w-full tech-input rounded-lg py-2.5 px-4 text-sm font-mono placeholder:text-gray-600 resize-none"
                                                    />

                                                    <div className="space-y-2">
                                                        <div className="text-[10px] text-gray-400 uppercase font-mono pl-1">Link Competitor (attività simili)</div>
                                                        <div className="grid md:grid-cols-3 gap-3">
                                                            <input
                                                                type="url"
                                                                value={product.link_competitor_1}
                                                                onChange={e => updateProduct(product.id, 'link_competitor_1', e.target.value)}
                                                                placeholder="Competitor 1"
                                                                className="w-full tech-input rounded-lg py-2.5 px-4 text-xs font-mono placeholder:text-gray-600"
                                                            />
                                                            <input
                                                                type="url"
                                                                value={product.link_competitor_2}
                                                                onChange={e => updateProduct(product.id, 'link_competitor_2', e.target.value)}
                                                                placeholder="Competitor 2"
                                                                className="w-full tech-input rounded-lg py-2.5 px-4 text-xs font-mono placeholder:text-gray-600"
                                                            />
                                                            <input
                                                                type="url"
                                                                value={product.link_competitor_3}
                                                                onChange={e => updateProduct(product.id, 'link_competitor_3', e.target.value)}
                                                                placeholder="Competitor 3"
                                                                className="w-full tech-input rounded-lg py-2.5 px-4 text-xs font-mono placeholder:text-gray-600"
                                                            />
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        ))}
                                    </div>
                                )}
                            </div>

                            {/* SEZIONE 6: Upload Immagini */}
                            <div className="space-y-4">
                                <label className="text-xs font-bold text-accent uppercase tracking-widest font-mono pl-1 flex items-center gap-2">
                                    <Icons.Upload width={14} height={14} />
                                    06. Immagini
                                </label>

                                <div className="bg-white/[0.03] border border-white/10 rounded-xl p-6 space-y-4 hover:border-accent/30 transition-colors">
                                    {/* Upload Button */}
                                    <div className="flex items-center justify-center">
                                        <label className="cursor-pointer px-6 py-3 rounded-lg bg-accent/10 border border-accent/30 text-accent hover:bg-accent hover:text-white transition-all text-sm font-mono font-bold uppercase flex items-center gap-2">
                                            <Icons.Upload width={16} height={16} />
                                            Carica Immagini
                                            <input
                                                type="file"
                                                multiple
                                                accept="image/*"
                                                onChange={handleImageUpload}
                                                className="hidden"
                                            />
                                        </label>
                                    </div>

                                    {/* Images Grid */}
                                    {formData.immagini.length > 0 && (
                                        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 mt-4">
                                            {formData.immagini.map((image) => (
                                                <div key={image.id} className="relative group">
                                                    <div className="aspect-square rounded-lg overflow-hidden border border-white/20 hover:border-accent/50 transition-colors">
                                                        <img
                                                            src={image.preview}
                                                            alt={image.name}
                                                            className="w-full h-full object-cover"
                                                        />
                                                    </div>
                                                    {/* Remove Button */}
                                                    <button
                                                        onClick={() => removeImage(image.id)}
                                                        className="absolute top-2 right-2 w-6 h-6 bg-red-500 hover:bg-red-600 rounded-full flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity"
                                                        title="Rimuovi immagine"
                                                    >
                                                        <Icons.X width={14} height={14} className="text-white" />
                                                    </button>
                                                    {/* Image Name */}
                                                    <div className="mt-1 text-[10px] text-gray-400 font-mono truncate px-1">
                                                        {image.name}
                                                    </div>
                                                </div>
                                            ))}
                                        </div>
                                    )}

                                    {formData.immagini.length === 0 && (
                                        <div className="text-center py-4">
                                            <Icons.Upload width={32} height={32} className="text-gray-600 mx-auto mb-2" />
                                            <p className="text-gray-500 text-xs font-mono">Nessuna immagine caricata.</p>
                                        </div>
                                    )}
                                </div>
                            </div>

                        </div>
                    </SpotlightCard>
                )}

                {/* ACTION BUTTON */}
                {status !== 'success' && (
                    <div className="mt-6 animate-[reveal_0.4s_ease-out]">
                        <button
                            onClick={handleSubmit}
                            disabled={status === 'publishing'}
                            className={`w-full py-4 rounded-xl font-bold font-mono tracking-widest uppercase text-white flex items-center justify-center gap-3 btn-primary ${status === 'publishing' ? 'opacity-80' : ''}`}
                        >
                            {status === 'publishing' ? 'Invio in corso...' : 'Invia Strategia Marketing'}
                            {status !== 'publishing' && <Icons.Send width={16} height={16} />}
                        </button>
                    </div>
                )}
            </main>

            <footer className="relative z-10 text-center py-8 text-gray-500 text-xs font-mono tracking-wider">
                <p>MarketingFlow © 2026 — Powered By BLC sa — v.23.01_14.11</p>
            </footer>

            {errorMsg && (
                <div className="fixed bottom-8 left-1/2 -translate-x-1/2 z-50 animate-[reveal_0.3s_ease-out] w-max max-w-[90vw]">
                    <div className="bg-[#1a0505] border border-red-500/30 text-red-200 px-6 py-4 rounded-xl shadow-2xl backdrop-blur flex items-start gap-3">
                        <Icons.Alert width={18} height={18} className="text-red-500 mt-0.5 shrink-0" />
                        <div className="flex flex-col">
                            <span className="font-bold text-xs mb-1 text-red-400">ERRORE RILEVATO</span>
                            <span className="font-mono text-xs font-medium leading-relaxed">{errorMsg}</span>
                        </div>
                    </div>
                </div>
            )}

            <style>{`
                @keyframes fadeInUp {
                    from {
                        opacity: 0;
                        transform: translateY(20px);
                    }
                    to {
                        opacity: 1;
                        transform: translateY(0);
                    }
                }

                @keyframes fadeIn {
                    from {
                        opacity: 0;
                    }
                    to {
                        opacity: 1;
                    }
                }

                @keyframes gradientShift {
                    0%, 100% {
                        background-position: 0% 50%;
                    }
                    50% {
                        background-position: 100% 50%;
                    }
                }

                @keyframes textGlow {
                    0%, 100% {
                        filter: drop-shadow(0 0 8px rgba(255, 107, 53, 0.5));
                    }
                    50% {
                        filter: drop-shadow(0 0 16px rgba(255, 107, 53, 0.8)) drop-shadow(0 0 24px rgba(168, 85, 247, 0.4));
                    }
                }
            `}</style>
        </div>
    );
}
