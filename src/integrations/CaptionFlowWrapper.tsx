import React from 'react';
// import { useNavigate } from 'react-router-dom'; // Unused
import { ArrowLeft } from 'lucide-react';

const AnimatedLoader = () => (
    <div className="fixed inset-0 z-[60] flex items-center justify-center bg-void/95 backdrop-blur-sm" style={{ caretColor: 'transparent' }}>
        <div className="flex flex-col items-center gap-6">
            <div className="relative w-24 h-24">
                <div className="absolute inset-0 animate-ping rounded-full overflow-hidden">
                    <div className="w-full h-full bg-accent/20 rounded-full"></div>
                </div>
                <div className="relative animate-pulse">
                    <img src="/icon.png" alt="Loading" className="w-24 h-24 object-contain drop-shadow-[0_0_40px_rgba(255,107,53,0.6)]" />
                </div>
            </div>

            <div className="w-64 h-1.5 bg-white/10 rounded-full overflow-hidden">
                <div className="h-full bg-gradient-to-r from-accent to-purple-500 rounded-full animate-[loading_1.5s_ease-in-out_infinite]"></div>
            </div>

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
        <div className="relative w-44 h-44 flex items-center justify-center animate-[scaleUp_0.6s_ease-out]">
            {/* Soft Ambient Glow - Close to logo */}
            <div className="absolute inset-2 rounded-full bg-gradient-radial from-accent/30 via-accent/10 to-transparent blur-xl"></div>
            {/* Glow Ring - Closer and softer */}
            <div
                className="absolute inset-1 rounded-full bg-[conic-gradient(from_0deg,transparent_0%,transparent_30%,#FF6B35_45%,#B349C1_55%,transparent_70%)] animate-[spin_2s_linear_infinite] z-10 opacity-70 blur-[2px]"
                style={{ maskImage: 'radial-gradient(transparent 75%, black 80%)', WebkitMaskImage: 'radial-gradient(transparent 75%, black 80%)' }}
            ></div>
            {/* Logo - Bigger */}
            <div className="relative z-20">
                <img src="/icon.png" alt="Loading" className="w-28 h-28 object-contain drop-shadow-[0_0_30px_rgba(255,107,53,0.5)]" />
            </div>
        </div>
        <style>{`
            @keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
            @keyframes scaleUp { from { transform: scale(0.9); opacity: 0; } to { transform: scale(1); opacity: 1; } }
        `}</style>
    </div>
);

export default function CaptionFlowWrapper() {
    // const navigate = useNavigate(); // Removed unused
    const [isLoading, setIsLoading] = React.useState(true);
    const [isRedirecting, setIsRedirecting] = React.useState(false);

    React.useEffect(() => {
        const timer = setTimeout(() => setIsLoading(false), 1500);
        return () => clearTimeout(timer);
    }, []);

    const handleReturnToBloom = () => {
        setIsRedirecting(true);
        setTimeout(() => {
            window.location.href = '/';
        }, 2500);
    };

    return (
        <div className="w-full h-screen bg-void flex flex-col relative">
            {isLoading && <BloomRedirectLoader />}
            {isRedirecting && <AnimatedLoader />}

            {/* Standard Header */}
            <nav className="relative z-50 px-6 py-6 w-full max-w-[90%] mx-auto flex items-center justify-between">
                <div className="flex items-center gap-3">
                    <img src="/logo.png" alt="Bloom AI" className="h-10 w-auto object-contain drop-shadow-[0_0_20px_rgba(255,107,53,0.4)]" />
                    <div className="h-6 w-px bg-white/20 mx-2"></div>
                    <div className="flex flex-col">
                        <span className="font-mono font-bold text-xl tracking-tighter text-white leading-none">CaptionFlow</span>
                        <span className="text-[10px] text-gray-500 font-mono tracking-widest uppercase leading-none mt-1">Caption AI Generator</span>
                    </div>
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
                        <ArrowLeft size={14} className="group-hover:-translate-x-1 transition-transform" />
                        <span>Back to Hub</span>
                    </button>
                </div>
            </nav>

            <iframe
                src="/caption-flow/index.html"
                className="w-full h-full border-none"
                title="Caption Flow"
            />
        </div>
    );
}
