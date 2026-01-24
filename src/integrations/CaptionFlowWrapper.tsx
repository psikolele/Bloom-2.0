import React from 'react';
// import { useNavigate } from 'react-router-dom'; // Unused
import { ArrowLeft } from 'lucide-react';

const AnimatedLoader = () => (
    <div className="fixed inset-0 z-[60] flex items-center justify-center bg-void/95 backdrop-blur-sm">
        <div className="flex flex-col items-center gap-6">
            <div className="relative">
                <div className="absolute inset-0 animate-ping">
                    <div className="w-24 h-24 bg-accent/20 rounded-full"></div>
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
        <div className="relative w-32 h-32 flex items-center justify-center animate-[scaleUp_1s_ease-out]">
            {/* Glow Ring - Full Disc */}
            <div className="absolute inset-0 rounded-full bg-[conic-gradient(from_0deg,transparent_0%,transparent_40%,#FF6B35_50%,#B349C1_60%,transparent_70%)] animate-[spin_1.5s_linear_infinite] blur-[8px] z-10"></div>
            {/* Logo */}
            <div className="relative z-20 transform scale-[1.55]">
                <img src="/logo.png" alt="Loading" className="w-20 h-20 object-contain drop-shadow-[0_0_10px_rgba(255,107,53,0.8)]" />
            </div>
        </div>
        <style>{`
            @keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
            @keyframes scaleUp { from { transform: scale(0); } to { transform: scale(1); } }
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
            {isLoading && <AnimatedLoader />}
            {isRedirecting && <BloomRedirectLoader />}

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
