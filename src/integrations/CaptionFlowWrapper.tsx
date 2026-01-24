import { ArrowLeft } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

export default function CaptionFlowWrapper() {
    const navigate = useNavigate();

    return (
        <div className="w-full h-screen bg-void flex flex-col">
            {/* Floating Back Button */}
            <div className="absolute top-4 right-4 z-50">
                <button
                    onClick={() => navigate('/')}
                    className="flex items-center gap-2 px-4 py-2 bg-black/50 hover:bg-black/80 text-white backdrop-blur-md border border-white/10 rounded-full transition-all text-sm font-mono group"
                >
                    <ArrowLeft size={16} className="group-hover:-translate-x-1 transition-transform" />
                    <span>Back to Hub</span>
                </button>
            </div>

            <iframe
                src="/caption-flow/index.html"
                className="w-full h-full border-none"
                title="Caption Flow"
            />
        </div>
    );
}
