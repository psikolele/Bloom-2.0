import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Layout, MessageSquare, Briefcase, ExternalLink } from 'lucide-react';

// Reusing global styles from index.css
const Card = ({ title, description, icon: Icon, path, delay }: { title: string, description: string, icon: any, path: string, delay: string }) => {
    const navigate = useNavigate();
    return (
        <div
            className="glass-panel rounded-2xl p-8 hover:border-accent/50 transition-all duration-500 group cursor-pointer hover:-translate-y-2 animate-reveal relative overflow-hidden"
            style={{ animationDelay: delay }}
            onClick={() => navigate(path)}
        >
            <div className="absolute inset-0 bg-gradient-to-br from-accent/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>

            <div className="relative z-10 flex flex-col items-start h-full">
                <div className="p-4 rounded-xl bg-surface border border-white/10 group-hover:border-accent/30 text-accent mb-6 group-hover:scale-110 transition-transform duration-500 shadow-[0_0_20px_rgba(255,107,53,0.1)]">
                    <Icon size={32} />
                </div>

                <h3 className="text-2xl font-mono font-bold text-white mb-3 group-hover:text-accent transition-colors">{title}</h3>
                <p className="text-gray-400 text-sm leading-relaxed mb-8 flex-grow">{description}</p>

                <div className="flex items-center gap-2 text-accent text-xs font-mono font-bold uppercase tracking-widest opacity-80 group-hover:opacity-100 group-hover:translate-x-1 transition-all">
                    Launch App <ExternalLink size={12} />
                </div>
            </div>
        </div>
    );
};

const AnimatedLoader = () => (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-void/95 backdrop-blur-sm">
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

export default function Dashboard() {
    const [isLoading, setIsLoading] = React.useState(true);

    React.useEffect(() => {
        const timer = setTimeout(() => setIsLoading(false), 1500);
        return () => clearTimeout(timer);
    }, []);

    return (
        <div className="min-h-screen relative font-sans text-gray-200 overflow-x-hidden p-6 md:p-12 flex flex-col">
            {isLoading && <AnimatedLoader />}
            <div className="ambient-light"></div>
            <div className="grid-overlay"></div>

            {/* HEADER */}
            <header className="relative z-10 flex flex-col items-center justify-center mb-16 mt-8 animate-reveal">
                <div className="flex items-center gap-3 mb-4">
                    <div className="relative">
                        <img src="/logo.png" alt="Bloom AI" className="h-16 w-auto object-contain drop-shadow-[0_0_30px_rgba(255,107,53,0.5)] animate-[pulse_3s_infinite]" />
                    </div>
                    <h1 className="text-4xl md:text-5xl font-mono font-bold text-white tracking-tighter">
                        Bloom <span className="text-accent">2.0</span>
                    </h1>
                </div>
                <p className="text-gray-400 font-mono text-sm tracking-wide uppercase">Integrated Automation Suite</p>
            </header>

            {/* MAIN GRID */}
            <main className="relative z-10 max-w-7xl mx-auto w-full grid grid-cols-1 md:grid-cols-3 gap-6">
                <Card
                    title="Caption Flow"
                    description="Manage and process your caption workflows effortlessly. The classic tool integrated securely."
                    icon={Layout}
                    path="/caption-flow"
                    delay="0.1s"
                />
                <Card
                    title="Social Client"
                    description="Advanced social media management with AI-powered strategy configuration and analytics."
                    icon={MessageSquare}
                    path="/social-media"
                    delay="0.2s"
                />
                <Card
                    title="Brand Profile"
                    description="Generate comprehensive brand profiles and strategies using Gemini 2.5 AI models."
                    icon={Briefcase}
                    path="/brand-profile"
                    delay="0.3s"
                />
            </main>

            <footer className="relative z-10 mt-auto pt-20 text-center text-xs text-gray-600 font-mono">
                <p>Bloom Ecosystem v2.0 • Antigravity Module</p>
            </footer>
        </div>
    );
}
