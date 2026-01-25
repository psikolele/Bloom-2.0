
import { useState, useEffect } from 'react';
import { Icons } from './components/Icons';
import { SpotlightCard } from './components/SpotlightCard';
import { generateBrandProfile, type BrandProfileData } from './services/gemini';

// --- CONFIG ---
const AVAILABLE_MODELS = [
    { name: "gemini-2.5-flash", displayName: "Gemini 2.5 Flash (Fast)" },
    { name: "gemini-2.5-flash-lite", displayName: "Gemini 2.5 Flash Lite (Ultra Fast)" },
    { name: "gemini-2.5-pro", displayName: "Gemini 2.5 Pro (Advanced Thinking)" },
];

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

const ThinkingBot = () => (
    <div className="flex flex-col items-center justify-center py-12 animate-reveal">
        <div className="relative w-24 h-24 mb-6 animate-float">
            {/* Glow behind */}
            <div className="absolute inset-0 bg-accent/20 rounded-full blur-xl bot-glow"></div>

            <svg viewBox="0 0 100 100" className="w-full h-full relative z-10 drop-shadow-2xl">
                {/* Head */}
                <rect x="20" y="20" width="60" height="50" rx="10" fill="#111" stroke="#333" strokeWidth="2" />
                <rect x="20" y="20" width="60" height="50" rx="10" fill="url(#metalGradient)" opacity="0.5" />

                {/* Antenna */}
                <line x1="50" y1="20" x2="50" y2="10" stroke="#555" strokeWidth="3" />
                <circle cx="50" cy="10" r="4" fill="#FF6B35" className="animate-pulse" />

                {/* Face Screen */}
                <rect x="28" y="30" width="44" height="24" rx="4" fill="#050505" />

                {/* Eyes */}
                <g className="bot-eye">
                    <circle cx="40" cy="42" r="5" fill="#FF6B35" />
                    <circle cx="60" cy="42" r="5" fill="#FF6B35" />
                </g>

                {/* Mouth (Thinking dots) */}
                <g transform="translate(38, 55)">
                    <circle cx="0" cy="0" r="2" fill="#555">
                        <animate attributeName="opacity" values="0;1;0" dur="1.5s" repeatCount="indefinite" begin="0s" />
                    </circle>
                    <circle cx="12" cy="0" r="2" fill="#555">
                        <animate attributeName="opacity" values="0;1;0" dur="1.5s" repeatCount="indefinite" begin="0.2s" />
                    </circle>
                    <circle cx="24" cy="0" r="2" fill="#555">
                        <animate attributeName="opacity" values="0;1;0" dur="1.5s" repeatCount="indefinite" begin="0.4s" />
                    </circle>
                </g>

                <defs>
                    <linearGradient id="metalGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" stopColor="#333" />
                        <stop offset="50%" stopColor="#111" />
                        <stop offset="100%" stopColor="#222" />
                    </linearGradient>
                </defs>
            </svg>
        </div>
        <div className="space-y-2 text-center">
            <h3 className="text-xl font-mono font-bold text-white">AI Processing</h3>
            <p className="text-gray-400 text-xs font-mono tracking-wider animate-pulse">ANALYZING BRAND DNA...</p>
        </div>
    </div>
);

const EditToast = ({ show, onClose }: { show: boolean, onClose: () => void }) => {
    useEffect(() => {
        if (show) {
            const timer = setTimeout(onClose, 4000);
            return () => clearTimeout(timer);
        }
    }, [show, onClose]);

    return (
        <div className={`fixed top-24 left-1/2 -translate-x-1/2 z-[100] transition-all duration-500 transform ${show ? 'translate-y-0 opacity-100' : '-translate-y-8 opacity-0 pointer-events-none'}`}>
            <div className="bg-white/10 backdrop-blur-md border border-white/20 px-6 py-3 rounded-full shadow-[0_0_30px_rgba(255,107,53,0.3)] flex items-center gap-3">
                <div className="w-8 h-8 rounded-full bg-accent/20 flex items-center justify-center text-accent">
                    <Icons.Edit width={16} height={16} />
                </div>
                <div className="flex flex-col">
                    <span className="text-white text-xs font-bold font-mono uppercase tracking-wider">Edit Mode Active</span>
                    <span className="text-gray-300 text-[10px]">Click any text to modify the AI results</span>
                </div>
            </div>
        </div>
    );
};

// Metric Card with optional progress bar
const MetricCard = ({
    label,
    value,
    icon: Icon,
    delay = 0,
    showProgress = false,
    progressValue = 0,
    maxProgress = 10,
    unit = ""
}: {
    label: string,
    value: string | number,
    icon?: any,
    delay?: number,
    showProgress?: boolean,
    progressValue?: number,
    maxProgress?: number,
    unit?: string
}) => {
    const progressPercent = (progressValue / maxProgress) * 100;

    // Calculate color based on progress (0 = red, 10 = green)
    const getProgressColor = (value: number) => {
        const percent = (value / maxProgress) * 100;
        if (percent >= 80) return 'from-emerald-500 to-green-400'; // Green
        if (percent >= 60) return 'from-yellow-500 to-lime-400'; // Yellow-Green
        if (percent >= 40) return 'from-orange-500 to-yellow-400'; // Orange-Yellow
        if (percent >= 20) return 'from-red-500 to-orange-400'; // Red-Orange
        return 'from-red-600 to-red-500'; // Red
    };

    return (
        <div
            className="bg-white/[0.03] border border-white/10 rounded-xl p-4 animate-reveal group cursor-default hover:border-accent/30 hover:bg-white/[0.05] transition-all duration-300 h-full"
            style={{ animationDelay: `${delay}ms` }}
        >
            <div className="flex items-center gap-3 mb-2">
                <div className="p-2 rounded-lg bg-accent/10 text-accent group-hover:scale-110 transition-transform">
                    {Icon && <Icon width={16} height={16} />}
                </div>
                <span className="text-[10px] font-bold text-gray-400 uppercase tracking-wider">{label}</span>
            </div>

            <div className="flex items-baseline gap-2">
                <span className="text-2xl font-bold text-white font-mono">{value}</span>
                {unit && <span className="text-sm text-gray-500">{unit}</span>}
            </div>

            {showProgress && (
                <div className="mt-3 space-y-1">
                    <div className="h-2 bg-white/5 rounded-full overflow-hidden">
                        <div
                            className={`h-full bg-gradient-to-r ${getProgressColor(progressValue)} transition-all duration-700 rounded-full`}
                            style={{ width: `${progressPercent}%` }}
                        />
                    </div>
                    <div className="flex justify-between text-[9px] text-gray-500 font-mono">
                        <span>Low</span>
                        <span>High</span>
                    </div>
                </div>
            )}
        </div>
    );
};

// --- MAIN APP ---

export default function App() {
    // State
    const [webhookUrl, setWebhookUrl] = useState(import.meta.env.VITE_N8N_WEBHOOK_URL || "");
    const [selectedModel, setSelectedModel] = useState(AVAILABLE_MODELS[0].name);
    const [isConfigOpen, setIsConfigOpen] = useState(false);
    const [isInitialLoading, setIsInitialLoading] = useState(true); // Added state
    const [isRedirecting, setIsRedirecting] = useState(false); // Added state

    // Core inputs/outputs
    const [websiteUrl, setWebsiteUrl] = useState("");
    const [profileData, setProfileData] = useState<BrandProfileData | null>(null);

    // Animazione di caricamento iniziale
    useEffect(() => {
        const timer = setTimeout(() => {
            setIsInitialLoading(false);
        }, 1500);
        return () => clearTimeout(timer);
    }, []);

    // Status states
    const [status, setStatus] = useState<"idle" | "generating" | "publishing" | "success" | "error">("idle");
    const [errorMsg, setErrorMsg] = useState("");
    const [showEditToast, setShowEditToast] = useState(false);

    const handleGenerate = async () => {
        if (!websiteUrl) return showError("Inserisci un sito web o nome brand.");

        setStatus("generating");
        setErrorMsg("");
        setProfileData(null);
        setShowEditToast(false);

        try {
            const data = await generateBrandProfile(websiteUrl, selectedModel);
            setProfileData(data);
            setStatus("idle");
            // Show toast after a slight delay for better UX
            setTimeout(() => setShowEditToast(true), 500);
        } catch (e: any) {
            showError(`Errore AI: ${e.message}`);
            setStatus("idle");
        }
    };

    // Generic handler for editable fields
    const handleUpdate = (field: string, value: any) => {
        if (profileData) {
            setProfileData({ ...profileData, [field]: value });
        }
    };

    const removeKeyword = (kwToRemove: string) => {
        if (profileData?.keywords) {
            handleUpdate('keywords', profileData.keywords.filter(k => k !== kwToRemove));
        }
    };

    const handlePublish = async () => {
        if (!profileData) return showError("Genera prima il profilo.");
        setStatus("publishing");
        try {
            const payload = {
                ...profileData,
                website: websiteUrl
            };

            console.log("📤 Sending payload to N8N:", payload);
            console.log("🔗 Webhook URL:", webhookUrl);

            const res = await fetch(webhookUrl, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            console.log("📥 Response status:", res.status);

            if (res.ok) {
                const responseText = await res.text();
                console.log("✅ Response body:", responseText);
                setStatus("success");
            } else {
                const errorText = await res.text();
                console.error("❌ Error response:", errorText);
                throw new Error(`HTTP ${res.status}: ${errorText || 'No error details'}`);
            }
        } catch (e: any) {
            console.error("❌ Full error:", e);

            // Check if it's a network/CORS error
            if (e instanceof TypeError && e.message.includes('Failed to fetch')) {
                showError("Errore di rete o CORS. Verifica che N8N accetti richieste dal browser.");
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
        setWebsiteUrl("");
        setProfileData(null);
        setStatus("idle");
        setShowEditToast(false);
    };

    const handleReturnToBloom = () => {
        setIsRedirecting(true);
        setTimeout(() => {
            window.location.href = '/';
        }, 2500);
    };

    return (
        <div className="min-h-screen relative font-sans text-gray-200 pb-20 overflow-x-hidden">
            {(isInitialLoading) && <AnimatedLoader />}
            {isRedirecting && <BloomRedirectLoader />}

            <div className="ambient-light"></div>
            <div className="grid-overlay"></div>

            <EditToast show={showEditToast} onClose={() => setShowEditToast(false)} />

            <nav className="relative z-50 px-6 py-6 w-full max-w-[90%] mx-auto flex items-center justify-between">
                <div className="flex items-center gap-3">
                    <img src="/logo.png" alt="Bloom AI" className="h-10 w-auto object-contain drop-shadow-[0_0_20px_rgba(255,107,53,0.4)]" />
                    <div className="h-6 w-px bg-white/20 mx-2"></div>
                    <span className="font-mono font-bold text-xl tracking-tighter text-white">BrandProfile</span>
                </div>

                <div className="flex items-center gap-4">
                    <div className="flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-[10px] font-mono uppercase">
                        <div className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></div> System Online
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
                        <Icons.Zap width={14} height={14} className="text-accent" />
                        <span className="text-accent text-[10px] font-bold tracking-widest uppercase">Brand Intelligence Engine</span>
                    </div>
                    <h1 className="text-4xl md:text-6xl font-bold tracking-tight text-white font-mono">
                        Brand Profile <br />
                        <span className="text-transparent bg-clip-text bg-gradient-to-r from-accent via-[#FF9B75] to-purple-500">Generator.</span>
                    </h1>
                </div>

                {/* Added overflow-hidden to force containment of children */}
                <SpotlightCard className="p-6 md:p-8 transition-all duration-700 animate-[reveal_1s_ease-out_0.2s_both] overflow-hidden flex flex-col h-auto">
                    <div className="flex justify-between items-start mb-6 px-2">
                        <div><h2 className="text-lg font-bold text-white font-mono">Strategy Studio</h2></div>
                        <button onClick={() => setIsConfigOpen(!isConfigOpen)} className={`p-2.5 rounded-xl transition-all border ${isConfigOpen ? 'bg-accent text-white border-accent' : 'bg-white/5 text-gray-400 border-transparent hover:text-white'}`}>
                            <Icons.Settings width={18} height={18} />
                        </button>
                    </div>

                    {/* CONFIG PANEL */}
                    <div className={`overflow-hidden transition-all duration-500 ease-in-out ${isConfigOpen ? 'max-h-[600px] mb-8 opacity-100' : 'max-h-0 opacity-0'}`}>
                        <div className="grid gap-4 bg-black/40 p-6 rounded-2xl border border-white/5 mx-2 shadow-inner">
                            <div className="grid md:grid-cols-2 gap-4">
                                <div className="space-y-4">
                                    <div className="space-y-1.5">
                                        <label className="text-[10px] font-bold text-gray-500 uppercase">Webhook Endpoint</label>
                                        <input type="text" value={webhookUrl} onChange={e => setWebhookUrl(e.target.value)} className="w-full tech-input px-4 py-2.5 rounded-lg text-sm font-mono" />
                                    </div>
                                </div>
                                <div className="space-y-4">
                                    <div className="space-y-1.5">
                                        <label className="text-[10px] font-bold text-gray-500 uppercase">Seleziona Modello AI</label>
                                        <div className="flex gap-2">
                                            <select
                                                value={selectedModel}
                                                onChange={e => setSelectedModel(e.target.value)}
                                                className="w-full tech-input px-4 py-2.5 rounded-lg text-sm font-mono bg-[#0a0a0a] text-white"
                                            >
                                                {AVAILABLE_MODELS.map((m, i) => (
                                                    <option
                                                        key={i}
                                                        value={m.name}
                                                        className="bg-[#0a0a0a] text-white hover:bg-accent py-3"
                                                    >
                                                        {m.displayName}
                                                    </option>
                                                ))}
                                            </select>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* MAIN INPUT */}
                    <div className="flex flex-col gap-6 relative min-h-[400px]">

                        {/* INPUT SECTION */}
                        <div className="flex flex-col md:flex-row gap-4 items-end">
                            <div className="flex-1 space-y-2 w-full">
                                <label className="text-xs font-bold text-accent uppercase tracking-widest font-mono pl-1">01. Source Input</label>
                                <div className="relative group">
                                    <Icons.Globe className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-500 group-focus-within:text-accent transition-colors" width={18} height={18} />
                                    <input
                                        type="text"
                                        value={websiteUrl}
                                        onChange={e => setWebsiteUrl(e.target.value)}
                                        placeholder="Costruisci il tuo brand profile partendo dal sito web (es. https://...)"
                                        className="w-full tech-input rounded-xl py-4 pl-12 pr-4 text-sm font-mono placeholder:text-gray-600"
                                        onKeyDown={e => e.key === 'Enter' && handleGenerate()}
                                    />
                                </div>
                            </div>
                            <button
                                onClick={handleGenerate}
                                disabled={status === 'generating' || !websiteUrl}
                                className="w-full md:w-auto h-[54px] px-8 rounded-xl bg-surface border border-white/10 text-white hover:bg-accent hover:text-white transition-all font-mono font-bold uppercase text-sm tracking-wider flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
                            >
                                <Icons.Wand width={18} height={18} />
                                Generate
                            </button>
                        </div>

                        {/* CONTENT AREA */}
                        <div className="relative min-h-[400px] w-full">
                            {status === 'generating' && (
                                <div className="absolute inset-0 z-20 flex items-center justify-center bg-black/50 backdrop-blur-sm rounded-3xl animate-[reveal_0.4s]">
                                    <ThinkingBot />
                                </div>
                            )}

                            {/* RESULTS SECTION INSIDE GLASS */}
                            {/* Increased bottom padding pb-8 to ensure it doesn't touch the edge */}
                            <div className={`transition-all duration-700 w-full ${profileData && status !== 'generating' ? 'opacity-100 translate-y-0 pb-8' : 'opacity-0 translate-y-10 hidden'}`}>

                                {/* METRICS GRID - 4 COLUMNS */}
                                <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4 mb-6 pt-6 border-t border-white/5 w-full">
                                    <MetricCard
                                        label="AI Confidence"
                                        value={profileData?.confidence_score || 0}
                                        icon={Icons.Zap}
                                        delay={0}
                                        showProgress={true}
                                        progressValue={profileData?.confidence_score || 0}
                                        maxProgress={10}
                                        unit="/10"
                                    />
                                    <MetricCard
                                        label="Scraping Quality"
                                        value={profileData?.scraping_quality || 0}
                                        icon={Icons.Check}
                                        delay={100}
                                        showProgress={true}
                                        progressValue={profileData?.scraping_quality || 0}
                                        maxProgress={10}
                                        unit="/10"
                                    />
                                    <MetricCard
                                        label="Max Emoji"
                                        value={profileData?.max_emoji || 0}
                                        icon={Icons.Send}
                                        delay={200}
                                    />
                                    <MetricCard
                                        label="Tone of Voice"
                                        value={profileData?.tone_voice?.split(',')[0].trim() || 'N/A'}
                                        icon={Icons.Shield}
                                        delay={300}
                                    />
                                </div>

                                <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6 w-full">
                                    {/* IDENTITY CARD */}
                                    <div className="bg-white/[0.03] border border-white/10 rounded-2xl p-6 space-y-4 hover:border-accent/30 transition-colors group w-full">
                                        <div className="flex items-center justify-between mb-2">
                                            <div className="flex items-center gap-2">
                                                <div className="p-2 rounded-lg bg-blue-500/20 text-blue-400"><Icons.Shield width={16} height={16} /></div>
                                                <h3 className="font-mono font-bold text-sm text-gray-300 uppercase">Brand Identity</h3>
                                            </div>
                                        </div>
                                        <div className="space-y-4">
                                            <div>
                                                <div className="text-[10px] text-gray-500 uppercase flex items-center gap-1">Brand Name</div>
                                                <input
                                                    className="editable-field w-full text-white font-medium text-lg"
                                                    value={profileData?.brand_name || ''}
                                                    onChange={(e) => handleUpdate('brand_name', e.target.value)}
                                                />
                                            </div>
                                            <div>
                                                <div className="text-[10px] text-gray-500 uppercase flex items-center gap-1">Settore</div>
                                                <input
                                                    className="editable-field w-full text-white font-medium"
                                                    value={profileData?.settore || ''}
                                                    onChange={(e) => handleUpdate('settore', e.target.value)}
                                                />
                                            </div>
                                            <div>
                                                <div className="text-[10px] text-gray-500 uppercase flex items-center gap-1">Tone of Voice</div>
                                                <textarea
                                                    rows={2}
                                                    className="editable-field w-full text-accent font-medium resize-none"
                                                    value={profileData?.tone_voice || ''}
                                                    onChange={(e) => handleUpdate('tone_voice', e.target.value)}
                                                />
                                            </div>
                                        </div>
                                    </div>

                                    {/* TARGET CARD */}
                                    <div className="bg-white/[0.03] border border-white/10 rounded-2xl p-6 space-y-4 hover:border-accent/30 transition-colors group w-full">
                                        <div className="flex items-center justify-between mb-2">
                                            <div className="flex items-center gap-2">
                                                <div className="p-2 rounded-lg bg-purple-500/20 text-purple-400"><Icons.Users width={16} height={16} /></div>
                                                <h3 className="font-mono font-bold text-sm text-gray-300 uppercase">Targeting</h3>
                                            </div>
                                        </div>
                                        <div className="space-y-4">
                                            <div>
                                                <div className="text-[10px] text-gray-500 uppercase flex items-center gap-1">Age Range</div>
                                                <input
                                                    className="editable-field w-full text-white font-medium"
                                                    value={profileData?.target_age || ''}
                                                    onChange={(e) => handleUpdate('target_age', e.target.value)}
                                                />
                                            </div>
                                            <div>
                                                <div className="text-[10px] text-gray-500 uppercase flex items-center gap-1">Geo</div>
                                                <input
                                                    className="editable-field w-full text-white font-medium"
                                                    value={profileData?.target_geo || ''}
                                                    onChange={(e) => handleUpdate('target_geo', e.target.value)}
                                                />
                                            </div>
                                            <div>
                                                <div className="text-[10px] text-gray-500 uppercase flex items-center gap-1">Job/Role</div>
                                                <input
                                                    className="editable-field w-full text-white font-medium"
                                                    value={profileData?.target_job || ''}
                                                    onChange={(e) => handleUpdate('target_job', e.target.value)}
                                                />
                                            </div>
                                        </div>
                                    </div>

                                    {/* STRATEGY CARD */}
                                    <div className="bg-white/[0.03] border border-white/10 rounded-2xl p-6 space-y-4 hover:border-accent/30 transition-colors group w-full">
                                        <div className="flex items-center justify-between mb-2">
                                            <div className="flex items-center gap-2">
                                                <div className="p-2 rounded-lg bg-green-500/20 text-green-400"><Icons.Target width={16} height={16} /></div>
                                                <h3 className="font-mono font-bold text-sm text-gray-300 uppercase">Strategy</h3>
                                            </div>
                                        </div>
                                        <div className="space-y-4">
                                            <div>
                                                <div className="text-[10px] text-gray-500 uppercase flex items-center gap-1">Value Proposition</div>
                                                <textarea
                                                    rows={3}
                                                    className="editable-field w-full text-white text-xs leading-relaxed resize-none"
                                                    value={profileData?.value_prop || ''}
                                                    onChange={(e) => handleUpdate('value_prop', e.target.value)}
                                                />
                                            </div>
                                            <div>
                                                <div className="text-[10px] text-gray-500 uppercase mb-1 flex items-center gap-1">Pain Points</div>
                                                <div className="space-y-2">
                                                    <input className="editable-field w-full text-xs text-gray-400" value={profileData?.pain_point_1 || ''} onChange={e => handleUpdate('pain_point_1', e.target.value)} />
                                                    <input className="editable-field w-full text-xs text-gray-400" value={profileData?.pain_point_2 || ''} onChange={e => handleUpdate('pain_point_2', e.target.value)} />
                                                    <input className="editable-field w-full text-xs text-gray-400" value={profileData?.pain_point_3 || ''} onChange={e => handleUpdate('pain_point_3', e.target.value)} />
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                {/* COMPETITORS & KEYWORDS */}
                                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 w-full">
                                    {/* COMPETITORS */}
                                    <div className="bg-white/[0.03] border border-white/10 rounded-2xl p-6 hover:border-accent/30 transition-colors group w-full">
                                        <h3 className="font-mono font-bold text-sm text-gray-300 uppercase mb-4 flex items-center justify-between">
                                            Competitor Insights
                                        </h3>
                                        <div className="space-y-4">
                                            <div className="p-3 bg-black/20 rounded-lg border border-white/5 space-y-2">
                                                <div className="text-[10px] text-gray-500 uppercase">Competitor 1</div>
                                                <input className="editable-field w-full text-sm font-medium text-white" value={profileData?.competitor_1_name || ''} onChange={e => handleUpdate('competitor_1_name', e.target.value)} placeholder="Name" />
                                                <input className="editable-field w-full text-xs text-gray-500" value={profileData?.competitor_1_instagram || ''} onChange={e => handleUpdate('competitor_1_instagram', e.target.value)} placeholder="@instagram" />
                                            </div>
                                            <div className="p-3 bg-black/20 rounded-lg border border-white/5 space-y-2">
                                                <div className="text-[10px] text-gray-500 uppercase">Competitor 2</div>
                                                <input className="editable-field w-full text-sm font-medium text-white" value={profileData?.competitor_2_name || ''} onChange={e => handleUpdate('competitor_2_name', e.target.value)} placeholder="Name" />
                                                <input className="editable-field w-full text-xs text-gray-500" value={profileData?.competitor_2_instagram || ''} onChange={e => handleUpdate('competitor_2_instagram', e.target.value)} placeholder="@instagram" />
                                            </div>
                                        </div>
                                    </div>

                                    {/* KEYWORDS */}
                                    <div className="bg-white/[0.03] border border-white/10 rounded-2xl p-6 hover:border-accent/30 transition-colors w-full">
                                        <div className="flex items-center gap-2 mb-4">
                                            <Icons.Tag width={16} height={16} className="text-accent" />
                                            <h3 className="font-mono font-bold text-sm text-gray-300 uppercase">Generated Keywords</h3>
                                        </div>
                                        <div className="flex flex-wrap gap-2">
                                            {profileData?.keywords && profileData.keywords.length > 0 ? (
                                                profileData.keywords.map((kw, i) => (
                                                    <span
                                                        key={i}
                                                        onClick={() => removeKeyword(kw)}
                                                        className="px-3 py-1 bg-accent/10 border border-accent/20 rounded-full text-xs text-accent-glow font-mono cursor-pointer hover:bg-red-500/20 hover:text-red-400 hover:border-red-500/30 transition-all"
                                                        title="Click to remove"
                                                    >
                                                        #{kw}
                                                    </span>
                                                ))
                                            ) : (
                                                <p className="text-xs text-gray-500 italic">No keywords generated.</p>
                                            )}
                                        </div>
                                        <p className="text-[10px] text-gray-600 mt-4 italic">Click on a keyword to remove it.</p>
                                    </div>
                                </div>

                            </div>
                        </div>

                    </div>
                </SpotlightCard>

                {/* ACTION BUTTON - OUTSIDE GLASS CARD */}
                {profileData && status !== 'generating' && (
                    <div className="mt-[10px] animate-[reveal_0.4s_ease-out]">
                        {status === 'success' ? (
                            <div className="glass-panel border-emerald-500/20 p-6 rounded-xl text-center">
                                <div className="w-12 h-12 bg-emerald-500 rounded-full flex items-center justify-center mb-3 mx-auto text-black"><Icons.Check width={24} height={24} /></div>
                                <h3 className="text-white font-bold font-mono">Profile Deployed to Webhook</h3>
                                <button onClick={reset} className="mt-4 text-xs text-gray-400 hover:text-white underline font-mono">NEW PROFILE</button>
                            </div>
                        ) : (
                            <button
                                onClick={handlePublish}
                                disabled={status === 'publishing'}
                                className={`w-full py-4 rounded-xl font-bold font-mono tracking-widest uppercase text-white flex items-center justify-center gap-3 btn-primary ${status === 'publishing' ? 'opacity-80' : ''}`}
                            >
                                {status === 'publishing' ? 'Sending Data...' : 'Deploy to Automation'}
                                {!status.includes('pub') && <Icons.Send width={16} height={16} />}
                            </button>
                        )}
                    </div>
                )}
            </main>

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
        </div>
    );
}
