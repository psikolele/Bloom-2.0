import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Mail, ArrowRight, Loader2, ArrowLeft, XCircle } from 'lucide-react';

export default function ForgotPassword() {
    const [email, setEmail] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [status, setStatus] = useState<'idle' | 'success' | 'error'>('idle');
    const [message, setMessage] = useState('');
    const [showNotFound, setShowNotFound] = useState(false);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setIsLoading(true);
        setStatus('idle');
        setMessage('');

        const webhookUrl = import.meta.env.VITE_AUTH_WEBHOOK_URL || 'https://emanueleserra.app.n8n.cloud/webhook/auth';

        try {
            const response = await fetch(webhookUrl, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    mode: 'forgot_password',
                    email
                })
            });

            const data = await response.json().catch(() => ({}));

            if (data.user_not_found) {
                setShowNotFound(true);
                setTimeout(() => setShowNotFound(false), 4000);
            } else {
                setStatus('success');
                setMessage('Ti abbiamo inviato le istruzioni per reimpostare la password. Controlla la tua casella email.');
            }
        } catch (err: any) {
            setStatus('error');
            setMessage('Errore di connessione. Riprova più tardi.');
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="min-h-screen w-full flex items-center justify-center bg-void relative overflow-hidden">
            {/* User Not Found Popup - same style as registration success */}
            {showNotFound && (
                <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm animate-reveal">
                    <div className="bg-white/[0.05] border border-red-500/30 rounded-2xl p-8 shadow-[0_0_40px_rgba(239,68,68,0.2)] text-center max-w-sm mx-4">
                        <XCircle className="mx-auto mb-4 text-red-500 drop-shadow-[0_0_10px_rgba(239,68,68,0.5)]" size={48} />
                        <h2 className="text-xl font-bold font-mono text-white mb-2">Account non trovato</h2>
                        <p className="text-sm font-mono text-gray-400">Nessun account è associato a questa email. Verifica l'indirizzo o registrati.</p>
                        <Link
                            to="/login"
                            className="inline-flex items-center text-accent hover:text-accent-hover font-mono text-sm mt-6 group"
                        >
                            Vai alla registrazione
                            <ArrowRight size={16} className="ml-2 group-hover:translate-x-1 transition-transform" />
                        </Link>
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
                        Recupero Password
                    </h1>
                    <p className="text-gray-500 text-sm mt-2 font-mono">
                        Inserisci la tua email per ricevere le istruzioni
                    </p>
                </div>

                <div className="bg-white/[0.03] border border-white/10 rounded-2xl p-8 backdrop-blur-xl shadow-2xl">
                    {status === 'success' ? (
                        <div className="text-center space-y-6 animate-reveal">
                            <div className="w-16 h-16 bg-green-500/20 text-green-400 rounded-full flex items-center justify-center mx-auto mb-4">
                                <Mail size={32} />
                            </div>
                            <h3 className="text-xl font-bold text-white">Controlla la tua email</h3>
                            <p className="text-gray-400 text-sm">{message}</p>
                            <Link
                                to="/login"
                                className="inline-flex items-center text-accent hover:text-accent-hover font-mono text-sm mt-4 group"
                            >
                                <ArrowLeft size={16} className="mr-2 group-hover:-translate-x-1 transition-transform" />
                                Torna al login
                            </Link>
                        </div>
                    ) : (
                        <form onSubmit={handleSubmit} className="space-y-6">
                            <div className="space-y-1">
                                <label className="text-xs font-bold text-gray-500 uppercase font-mono pl-1">Email</label>
                                <div className="relative group">
                                    <Mail className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-500 group-focus-within:text-accent transition-colors" size={16} />
                                    <input
                                        type="email"
                                        value={email}
                                        onChange={(e) => setEmail(e.target.value)}
                                        required
                                        className="w-full bg-black/20 border border-white/10 rounded-xl py-3 pl-12 pr-4 text-white text-sm font-mono focus:border-accent/50 focus:outline-none focus:ring-1 focus:ring-accent/50 transition-all placeholder:text-gray-700"
                                        placeholder="name@company.com"
                                    />
                                </div>
                            </div>

                            {status === 'error' && (
                                <div className="p-3 rounded-lg bg-red-500/10 border border-red-500/20 text-red-400 text-xs font-mono text-center">
                                    {message}
                                </div>
                            )}

                            <button
                                type="submit"
                                disabled={isLoading}
                                className="w-full bg-accent hover:bg-accent-hover text-white rounded-xl py-3 font-bold font-mono uppercase tracking-wider text-sm shadow-[0_0_20px_rgba(255,107,53,0.3)] hover:shadow-[0_0_30px_rgba(255,107,53,0.5)] transition-all flex items-center justify-center gap-2 group disabled:opacity-70 disabled:cursor-not-allowed"
                            >
                                {isLoading ? <Loader2 className="animate-spin" size={18} /> : 'Invia Istruzioni'}
                                {!isLoading && <ArrowRight size={16} className="group-hover:translate-x-1 transition-transform" />}
                            </button>

                            <div className="text-center">
                                <Link
                                    to="/login"
                                    className="text-xs text-gray-500 hover:text-white transition-colors font-mono"
                                >
                                    Torna al login
                                </Link>
                            </div>
                        </form>
                    )}
                </div>
            </div>
        </div>
    );
}
