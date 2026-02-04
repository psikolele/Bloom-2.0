import React, { useState, useEffect } from 'react';
import { useNavigate, useSearchParams, Link } from 'react-router-dom';
import { Lock, ArrowRight, Loader2, CheckCircle } from 'lucide-react';

export default function ResetPassword() {
    const [searchParams] = useSearchParams();
    const navigate = useNavigate();

    const [passwords, setPasswords] = useState({
        new: '',
        confirm: ''
    });
    const [isLoading, setIsLoading] = useState(false);
    const [status, setStatus] = useState<'idle' | 'success' | 'error'>('idle');
    const [message, setMessage] = useState('');

    const token = searchParams.get('token');
    const email = searchParams.get('email');

    useEffect(() => {
        if (!token || !email) {
            setStatus('error');
            setMessage('Link non valido o scaduto. Richiedi un nuovo reset password.');
        }
    }, [token, email]);

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setPasswords(prev => ({ ...prev, [e.target.name]: e.target.value }));
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();

        if (passwords.new !== passwords.confirm) {
            setStatus('error');
            setMessage('Le password non corrispondono.');
            return;
        }

        if (passwords.new.length < 8) {
            setStatus('error');
            setMessage('La password deve essere di almeno 8 caratteri.');
            return;
        }

        setIsLoading(true);
        setStatus('idle');
        setMessage('');

        const webhookUrl = import.meta.env.VITE_AUTH_WEBHOOK_URL || 'https://emanueleserra.app.n8n.cloud/webhook/auth';

        try {
            const response = await fetch(webhookUrl, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    mode: 'reset_password',
                    token,
                    email,
                    new_password: passwords.new
                })
            });

            const data = await response.json().catch(() => ({}));

            if (!response.ok) {
                throw new Error(data.message || 'Errore durante il reset della password.');
            }

            if (data.success) {
                setStatus('success');
                setMessage('Password aggiornata con successo!');
                setTimeout(() => navigate('/login'), 3000);
            } else {
                throw new Error(data.message || 'Impossibile resettare la password.');
            }
        } catch (err: any) {
            setStatus('error');
            setMessage(err.message || 'Errore di connessione. Riprova.');
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="min-h-screen w-full flex items-center justify-center bg-void relative overflow-hidden">
            {/* Background Effects */}
            <div className="absolute inset-0 bg-[url('/grid.svg')] bg-center [mask-image:linear-gradient(180deg,white,rgba(255,255,255,0))] opacity-20"></div>
            <div className="ambient-light"></div>

            <div className="w-full max-w-md p-8 relative z-10">
                <div className="text-center mb-8">
                    <img src="/logo.png" alt="Bloom AI" className="h-16 w-auto mx-auto mb-6 drop-shadow-[0_0_20px_rgba(255,107,53,0.4)]" />
                    <h1 className="text-2xl font-bold font-mono text-white tracking-tight">
                        Nuova Password
                    </h1>
                    <p className="text-gray-500 text-sm mt-2 font-mono">
                        Inserisci la tua nuova password sicura
                    </p>
                </div>

                <div className="bg-white/[0.03] border border-white/10 rounded-2xl p-8 backdrop-blur-xl shadow-2xl">
                    {status === 'success' ? (
                        <div className="text-center space-y-6 animate-reveal">
                            <div className="w-16 h-16 bg-green-500/20 text-green-400 rounded-full flex items-center justify-center mx-auto mb-4">
                                <CheckCircle size={32} />
                            </div>
                            <h3 className="text-xl font-bold text-white">Password Aggiornata</h3>
                            <p className="text-gray-400 text-sm">Verrai reindirizzato al login tra pochi secondi...</p>
                            <Link
                                to="/login"
                                className="inline-block bg-accent hover:bg-accent-hover text-white rounded-xl px-6 py-2 font-bold font-mono text-sm transition-all"
                            >
                                Vai al login ora
                            </Link>
                        </div>
                    ) : (
                        <form onSubmit={handleSubmit} className="space-y-4">
                            <div className="space-y-1">
                                <label className="text-xs font-bold text-gray-500 uppercase font-mono pl-1">Nuova Password</label>
                                <div className="relative group">
                                    <Lock className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-500 group-focus-within:text-accent transition-colors" size={16} />
                                    <input
                                        type="password"
                                        name="new"
                                        value={passwords.new}
                                        onChange={handleChange}
                                        required
                                        className="w-full bg-black/20 border border-white/10 rounded-xl py-3 pl-12 pr-4 text-white text-sm font-mono focus:border-accent/50 focus:outline-none focus:ring-1 focus:ring-accent/50 transition-all placeholder:text-gray-700"
                                        placeholder="Nuova password"
                                    />
                                </div>
                            </div>

                            <div className="space-y-1">
                                <label className="text-xs font-bold text-gray-500 uppercase font-mono pl-1">Conferma Password</label>
                                <div className="relative group">
                                    <Lock className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-500 group-focus-within:text-accent transition-colors" size={16} />
                                    <input
                                        type="password"
                                        name="confirm"
                                        value={passwords.confirm}
                                        onChange={handleChange}
                                        required
                                        className="w-full bg-black/20 border border-white/10 rounded-xl py-3 pl-12 pr-4 text-white text-sm font-mono focus:border-accent/50 focus:outline-none focus:ring-1 focus:ring-accent/50 transition-all placeholder:text-gray-700"
                                        placeholder="Conferma password"
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
                                disabled={isLoading || !token}
                                className="w-full bg-accent hover:bg-accent-hover text-white rounded-xl py-3 font-bold font-mono uppercase tracking-wider text-sm shadow-[0_0_20px_rgba(255,107,53,0.3)] hover:shadow-[0_0_30px_rgba(255,107,53,0.5)] transition-all flex items-center justify-center gap-2 group disabled:opacity-70 disabled:cursor-not-allowed mt-4"
                            >
                                {isLoading ? <Loader2 className="animate-spin" size={18} /> : 'Aggiorna Password'}
                                {!isLoading && <ArrowRight size={16} className="group-hover:translate-x-1 transition-transform" />}
                            </button>
                        </form>
                    )}
                </div>
            </div>
        </div>
    );
}
