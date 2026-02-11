
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Lock, User, Mail, ArrowRight, Loader2, Sparkles, LayoutDashboard, X, Target } from 'lucide-react';

export default function Login() {
    const navigate = useNavigate();
    const [isRegistering, setIsRegistering] = useState(false);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState('');
    const [showBrandProfileModal, setShowBrandProfileModal] = useState(false);

    const [formData, setFormData] = useState({
        username: '',
        password: '',
        email: ''
    });

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setFormData(prev => ({ ...prev, [e.target.name]: e.target.value }));
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setIsLoading(true);
        setError('');

        const webhookUrl = import.meta.env.VITE_AUTH_WEBHOOK_URL || 'https://emanueleserra.app.n8n.cloud/webhook/auth';

        try {
            const payload = {
                mode: isRegistering ? 'register' : 'login',
                ...formData
            };

            const response = await fetch(webhookUrl, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            let data;
            try {
                data = await response.json();
            } catch (jsonError) {
                // If JSON parsing fails, we'll handle it using response.status
            }

            if (!response.ok) {
                // Use backend message if available, otherwise fallback based on status
                if (data && data.message) {
                    throw new Error(data.message);
                }

                switch (response.status) {
                    case 401:
                        throw new Error('Nome utente o password errati.');
                    case 409:
                        throw new Error('Email già registrata. Prova ad accedere.');
                    case 404:
                        throw new Error('Servizio di autenticazione non raggiungibile.');
                    case 500:
                        throw new Error('Errore interno del server. Riprova più tardi.');
                    default:
                        throw new Error(`Errore di comunicazione (${response.status}).`);
                }
            }

            if (!data) {
                throw new Error('Risposta non valida dal server.');
            }

            if (data.success) {
                // Save auth state
                localStorage.setItem('bloom_user', JSON.stringify({
                    username: data.username || formData.username,
                    loginName: formData.username,
                    email: data.email || formData.email || '', // Save Email
                    timestamp: new Date().toISOString()
                }));

                if (isRegistering) {
                    setShowBrandProfileModal(true);
                } else {
                    navigate('/');
                }
            } else {
                setError(data.message || 'Credenziali non valide.');
            }
        } catch (err: any) {
            setError(err.message || 'Si è verificato un errore di connessione.');
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="min-h-screen w-full flex items-center justify-center bg-void relative overflow-hidden">
            {/* Brand Profile Onboarding Modal */}
            {showBrandProfileModal && (
                <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-md animate-reveal">
                    <div className="relative w-full max-w-lg mx-4 bg-gradient-to-br from-surface via-void to-surface border border-white/10 rounded-3xl p-8 shadow-[0_0_60px_rgba(255,107,53,0.3)] animate-reveal">
                        {/* Close Button */}
                        <button
                            onClick={() => { setShowBrandProfileModal(false); navigate('/'); }}
                            className="absolute top-4 right-4 p-2 rounded-full bg-white/5 hover:bg-white/10 text-gray-400 hover:text-white transition-all"
                        >
                            <X size={20} />
                        </button>

                        {/* Icon */}
                        <div className="flex justify-center mb-6">
                            <div className="relative">
                                <div className="absolute inset-0 bg-accent/20 blur-2xl rounded-full"></div>
                                <div className="relative w-20 h-20 bg-gradient-to-br from-accent to-accent-glow rounded-2xl flex items-center justify-center shadow-[0_0_40px_rgba(255,107,53,0.5)]">
                                    <Sparkles className="text-white" size={36} />
                                </div>
                            </div>
                        </div>

                        {/* Title */}
                        <div className="text-center mb-4">
                            <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-accent/10 border border-accent/20 mb-4">
                                <span className="text-accent text-[10px] font-bold tracking-widest uppercase">Account Creato</span>
                            </div>
                            <h2 className="text-2xl md:text-3xl font-bold text-white font-mono mb-3">
                                Pronto a far decollare<br />
                                <span className="text-transparent bg-clip-text bg-gradient-to-r from-accent to-accent-glow">il tuo brand?</span>
                            </h2>
                            <p className="text-gray-400 text-sm leading-relaxed">
                                Compila il <span className="text-white font-semibold">Brand Profile</span> e sblocca il potenziale di Bloom AI.<br />
                                Analizza la tua attivita e genera contenuti mirati in pochi click.
                            </p>
                        </div>

                        {/* Features Preview */}
                        <div className="grid grid-cols-2 gap-3 mb-6 mt-6">
                            <div className="bg-white/[0.03] border border-white/10 rounded-xl p-4 text-center">
                                <Target className="mx-auto mb-2 text-accent" size={24} />
                                <div className="text-white text-xs font-semibold mb-1">Target Audience</div>
                                <div className="text-gray-500 text-[10px]">Analisi precisa</div>
                            </div>
                            <div className="bg-white/[0.03] border border-white/10 rounded-xl p-4 text-center">
                                <Sparkles className="mx-auto mb-2 text-accent" size={24} />
                                <div className="text-white text-xs font-semibold mb-1">AI Content</div>
                                <div className="text-gray-500 text-[10px]">Caption su misura</div>
                            </div>
                        </div>

                        {/* CTA Buttons */}
                        <div className="space-y-3">
                            <button
                                onClick={() => navigate('/brand-profile')}
                                className="w-full bg-gradient-to-r from-accent to-accent-glow hover:shadow-[0_0_40px_rgba(255,107,53,0.6)] text-white rounded-xl py-4 font-bold font-mono uppercase tracking-wider text-sm transition-all flex items-center justify-center gap-3 group"
                            >
                                <Sparkles size={18} className="group-hover:rotate-12 transition-transform" />
                                Compila Brand Profile
                                <ArrowRight size={16} className="group-hover:translate-x-1 transition-transform" />
                            </button>
                            <button
                                onClick={() => navigate('/')}
                                className="w-full bg-white/5 hover:bg-white/10 border border-white/10 hover:border-white/20 text-gray-300 hover:text-white rounded-xl py-3 font-medium font-mono text-sm transition-all flex items-center justify-center gap-2"
                            >
                                <LayoutDashboard size={16} />
                                Vai alla Dashboard
                            </button>
                        </div>

                        {/* Helper Text */}
                        <p className="text-center text-gray-600 text-[10px] font-mono mt-4">
                            Potrai compilarlo in qualsiasi momento dalla dashboard
                        </p>
                    </div>
                </div>
            )}

            {/* Background Effects */}
            <div className="absolute inset-0 bg-[url('/grid.svg')] bg-center [mask-image:linear-gradient(180deg,white,rgba(255,255,255,0))] opacity-20"></div>
            <div className="ambient-light"></div>

            <div className="w-full max-w-md p-8 relative z-10">
                <div className="text-center mb-8">
                    <img src="/logo.png" alt="Bloom AI" className="h-16 w-auto mx-auto mb-6 drop-shadow-[0_0_20px_rgba(255,107,53,0.4)]" />
                    <h1 className="text-2xl font-bold font-mono text-white tracking-tight">
                        {isRegistering ? 'Nuovo Account' : 'Accesso Sicuro'}
                    </h1>
                    <p className="text-gray-500 text-sm mt-2 font-mono">
                        {isRegistering ? 'Entra nell\'ecosistema Bloom' : 'Bentornato nel modulo Antigravity'}
                    </p>
                </div>

                <div className="bg-white/[0.03] border border-white/10 rounded-2xl p-8 backdrop-blur-xl shadow-2xl">
                    <form onSubmit={handleSubmit} className="space-y-4">

                        <div className="space-y-1">
                            <label className="text-xs font-bold text-gray-500 uppercase font-mono pl-1">Utente</label>
                            <div className="relative group">
                                <User className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-500 group-focus-within:text-accent transition-colors" size={16} />
                                <input
                                    type="text"
                                    name="username"
                                    value={formData.username}
                                    onChange={handleChange}
                                    required
                                    className="w-full bg-black/20 border border-white/10 rounded-xl py-3 pl-12 pr-4 text-white text-sm font-mono focus:border-accent/50 focus:outline-none focus:ring-1 focus:ring-accent/50 transition-all placeholder:text-gray-700"
                                    placeholder="Username"
                                />
                            </div>
                        </div>

                        {isRegistering && (
                            <div className="space-y-1 animate-reveal">
                                <label className="text-xs font-bold text-gray-500 uppercase font-mono pl-1">Email</label>
                                <div className="relative group">
                                    <Mail className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-500 group-focus-within:text-accent transition-colors" size={16} />
                                    <input
                                        type="email"
                                        name="email"
                                        value={formData.email}
                                        onChange={handleChange}
                                        required
                                        className="w-full bg-black/20 border border-white/10 rounded-xl py-3 pl-12 pr-4 text-white text-sm font-mono focus:border-accent/50 focus:outline-none focus:ring-1 focus:ring-accent/50 transition-all placeholder:text-gray-700"
                                        placeholder="name@company.com"
                                    />
                                </div>
                            </div>
                        )}

                        <div className="space-y-1">
                            <label className="text-xs font-bold text-gray-500 uppercase font-mono pl-1">Password</label>
                            <div className="relative group">
                                <Lock className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-500 group-focus-within:text-accent transition-colors" size={16} />
                                <input
                                    type="password"
                                    name="password"
                                    value={formData.password}
                                    onChange={handleChange}
                                    required
                                    className="w-full bg-black/20 border border-white/10 rounded-xl py-3 pl-12 pr-4 text-white text-sm font-mono focus:border-accent/50 focus:outline-none focus:ring-1 focus:ring-accent/50 transition-all placeholder:text-gray-700"
                                    placeholder="••••••••"
                                />
                            </div>
                        </div>

                        <div className="flex justify-end">
                            <a href="/forgot-password" className="text-[10px] text-gray-500 hover:text-accent transition-colors font-mono">
                                Password dimenticata?
                            </a>
                        </div>

                        {error && (
                            <div className="p-3 rounded-lg bg-red-500/10 border border-red-500/20 text-red-400 text-xs font-mono text-center">
                                {error}
                            </div>
                        )}

                        <button
                            type="submit"
                            disabled={isLoading}
                            className="w-full bg-accent hover:bg-accent-hover text-white rounded-xl py-3 font-bold font-mono uppercase tracking-wider text-sm shadow-[0_0_20px_rgba(255,107,53,0.3)] hover:shadow-[0_0_30px_rgba(255,107,53,0.5)] transition-all flex items-center justify-center gap-2 group disabled:opacity-70 disabled:cursor-not-allowed mt-4"
                        >
                            {isLoading ? <Loader2 className="animate-spin" size={18} /> : (isRegistering ? 'Crea Account' : 'Accedi')}
                            {!isLoading && <ArrowRight size={16} className="group-hover:translate-x-1 transition-transform" />}
                        </button>
                    </form>

                    <div className="mt-6 text-center">
                        <button
                            onClick={() => { setIsRegistering(!isRegistering); setError(''); }}
                            className="text-xs text-gray-500 hover:text-white transition-colors font-mono underline underline-offset-4"
                        >
                            {isRegistering ? 'Hai già un account? Accedi' : 'Non hai un account? Registrati'}
                        </button>
                    </div>
                </div>

                <div className="mt-8 text-center text-[10px] text-gray-600 font-mono">
                    Protected by Bloom Unified Auth Protocol v2.0
                </div>
            </div>
        </div>
    );
}
