import { ArrowLeft } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

export default function CaptionFlowWrapper() {
    const navigate = useNavigate();

    return (
        <div className="w-full h-screen bg-void flex flex-col">
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
                        onClick={() => navigate('/')}
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
