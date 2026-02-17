import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Layout, MessageSquare, Briefcase, ExternalLink } from 'lucide-react';
import RAGUpload from '../components/RAGUpload';
import type { DriveFolder } from '../components/RAGUpload';
import RAGChat from '../components/RAGChat';


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
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-void/95 backdrop-blur-sm" style={{ caretColor: 'transparent' }}>
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

const handleLogout = () => {
    localStorage.removeItem('bloom_user');
    window.location.reload(); // Force reload to trigger AuthGuard or clear state
};

export default function Dashboard() {
    const [isLoading, setIsLoading] = useState(true);
    const [folders, setFolders] = useState<DriveFolder[]>([]);
    const [selectedFolderId, setSelectedFolderId] = useState<string>('');
    const [loadingFolders, setLoadingFolders] = useState<boolean>(true);
    const [folderError, setFolderError] = useState<string | null>(null);
    const [currentUser, setCurrentUser] = useState<{ username: string } | null>(null);
    const [isAdmin, setIsAdmin] = useState(false);

    useEffect(() => {
        const timer = setTimeout(() => setIsLoading(false), 1500);
        return () => clearTimeout(timer);
    }, []);

    // Read authenticated user from localStorage
    useEffect(() => {
        const userStr = localStorage.getItem('bloom_user');
        if (userStr) {
            try {
                const user = JSON.parse(userStr);
                const uname = (user.username || '').toLowerCase();
                setCurrentUser({ username: uname });
                setIsAdmin(uname === 'admin');
            } catch (e) {
                console.error('[RAG] Failed to parse bloom_user', e);
                setCurrentUser({ username: '' });
            }
        } else {
            setCurrentUser({ username: '' });
        }
    }, []);

    // Fetch folders once user is known; pass username so n8n can filter per-user
    useEffect(() => {
        if (currentUser === null) return; // Wait for user state to be initialized

        const LIST_FOLDERS_WEBHOOK = 'https://emanueleserra.app.n8n.cloud/webhook/rag-folders';
        const username = currentUser.username;
        const url = username
            ? `${LIST_FOLDERS_WEBHOOK}?username=${encodeURIComponent(username)}`
            : LIST_FOLDERS_WEBHOOK;

        console.log(`[RAG] Fetching folders for user "${username}" from: ${url}`);

        fetch(url)
            .then(res => {
                console.log(`[RAG] Response status: ${res.status} ${res.statusText}`);
                if (!res.ok) throw new Error(`Server returned ${res.status} ${res.statusText}`);
                return res.json();
            })
            .then(data => {
                console.log('[RAG] Data received:', data);
                let items: DriveFolder[] = [];
                if (Array.isArray(data)) items = data;
                else if (Array.isArray((data as any)?.documents)) items = (data as any).documents;
                else items = Object.values(data).find(v => Array.isArray(v)) as DriveFolder[] || [];

                console.log(`[RAG] Parsed ${items.length} folders.`);
                if (items.length === 0) console.warn('[RAG] No folders found in response.');

                setFolders(items);

                // Non-admin: auto-select the single folder returned for their account
                if (username !== 'admin' && items.length > 0) {
                    setSelectedFolderId(items[0].id);
                }

                setLoadingFolders(false);
            })
            .catch(err => {
                console.error("[RAG] Error fetching folders:", err);
                let errorMsg = err.message;
                if (err instanceof TypeError && err.message === 'Failed to fetch') {
                    errorMsg = 'CORS/Network Error (Check Console)';
                }
                setFolderError(errorMsg);
                setLoadingFolders(false);
            });
    }, [currentUser]);

    return (
        <div className="min-h-screen relative font-sans text-gray-200 overflow-x-hidden p-6 md:p-12 flex flex-col">
            {isLoading && <AnimatedLoader />}
            <div className="ambient-light"></div>
            <div className="grid-overlay"></div>

            {/* RAG Upload Widget (Fixed Position or Integrated?) - Let's integrate it nicely in the header area or sidebar if possible, but for now absolute top-right or just below header? 
               Actually, the user asked for a "new box". Let's put it in the main grid for now as a 4th item, OR if it's a utility, maybe in a side panel.
               The user said "crea solo un nuovo box coerente dal punto di vista grafico nella dashboard".
               Let's add it to the main grid.
            */}

            {/* HEADER */}
            <header className="relative z-10 w-full max-w-7xl mx-auto flex flex-col items-center justify-center mb-16 mt-8 animate-reveal">
                <div className="flex items-center gap-3 mb-4">
                    <div className="relative">
                        <img src="/logo.png" alt="Bloom AI" className="h-16 w-auto object-contain drop-shadow-[0_0_30px_rgba(255,107,53,0.5)] animate-[pulse_3s_infinite]" />
                    </div>
                    <h1 className="text-4xl md:text-5xl font-mono font-bold text-white tracking-tighter">
                        Bloom <span className="text-accent">2.0</span>
                    </h1>
                </div>

                <p className="text-gray-400 font-mono text-sm tracking-wide uppercase">Integrated Automation Suite</p>

                <button
                    onClick={handleLogout}
                    className="absolute right-0 top-1/2 -translate-y-1/2 px-4 py-2 text-xs font-mono text-gray-500 hover:text-white border border-transparent hover:border-white/10 rounded-full transition-all flex items-center gap-2 group"
                    title="Logout"
                >
                    <span className="opacity-0 group-hover:opacity-100 transition-opacity">LOGOUT</span>
                    <div className="w-8 h-8 rounded-full bg-white/5 border border-white/10 flex items-center justify-center group-hover:bg-red-500/20 group-hover:border-red-500/30 group-hover:text-red-400 transition-all">
                        <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" /><polyline points="16 17 21 12 16 7" /><line x1="21" y1="12" x2="9" y2="12" /></svg>
                    </div>
                </button>
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

                {/* RAG Section - Upload + Chat side by side */}
                <div className="md:col-span-3 grid grid-cols-1 lg:grid-cols-2 gap-6">
                    <RAGUpload
                        folders={folders}
                        selectedFolderId={selectedFolderId}
                        setSelectedFolderId={isAdmin ? setSelectedFolderId : () => {}}
                        loadingFolders={loadingFolders}
                        folderError={folderError}
                        username={currentUser?.username ?? ''}
                        isAdmin={isAdmin}
                    />
                    <RAGChat
                        folders={folders}
                        selectedFolderId={selectedFolderId}
                        username={currentUser?.username ?? ''}
                        isAdmin={isAdmin}
                    />
                </div>
            </main>

            <footer className="relative z-10 mt-auto pt-20 text-center text-xs text-gray-600 font-mono">
                <p>Bloom Ecosystem 2.0 • Created by BLC • Update version 25.01_08.35</p>
            </footer>
        </div>
    );
}
