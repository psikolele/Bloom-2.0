import React, { useState, useRef, useEffect } from 'react';
import { MessageSquare, Send, AlertCircle } from 'lucide-react';
import type { DriveFolder } from './RAGUpload';
import './RAGChat.css';

interface ChatMessage {
    role: 'user' | 'bot';
    content: string;
    sources?: string[];
}

interface RAGChatProps {
    folders: DriveFolder[];
    selectedFolderId: string;
}

const QUERY_WEBHOOK = 'https://emanueleserra.app.n8n.cloud/webhook/rag-query';

const RAGChat: React.FC<RAGChatProps> = ({ folders, selectedFolderId }) => {
    const [messages, setMessages] = useState<ChatMessage[]>([]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const messagesEndRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages, isLoading]);

    const selectedFolderName = folders.find(f => f.id === selectedFolderId)?.name;

    const handleSend = async () => {
        const query = input.trim();
        if (!query || !selectedFolderId || isLoading) return;

        setError(null);
        setInput('');

        const userMessage: ChatMessage = { role: 'user', content: query };
        setMessages(prev => [...prev, userMessage]);
        setIsLoading(true);

        try {
            const res = await fetch(QUERY_WEBHOOK, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query, folderId: selectedFolderId }),
            });

            if (!res.ok) {
                throw new Error(`Server returned ${res.status}`);
            }

            const data = await res.json();

            if (data.error) {
                throw new Error(data.error);
            }

            const botMessage: ChatMessage = {
                role: 'bot',
                content: data.answer || 'No response received.',
                sources: data.sources,
            };
            setMessages(prev => [...prev, botMessage]);
        } catch (err: any) {
            setError(err.message || 'Failed to get response');
            const errorMessage: ChatMessage = {
                role: 'bot',
                content: 'Sorry, an error occurred. Please try again.',
            };
            setMessages(prev => [...prev, errorMessage]);
        } finally {
            setIsLoading(false);
        }
    };

    const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSend();
        }
    };

    return (
        <div className="rag-chat-card">
            <div className="rag-chat-header">
                <div className="rag-icon">
                    <MessageSquare size={20} color="#a78bfa" />
                </div>
                <h3>RAG Chat</h3>
                {selectedFolderName && (
                    <span style={{
                        fontSize: '0.7rem',
                        color: '#a78bfa',
                        marginLeft: 'auto',
                        opacity: 0.7,
                    }}>
                        {selectedFolderName}
                    </span>
                )}
            </div>

            {messages.length === 0 && !isLoading ? (
                <div className="rag-chat-empty">
                    <MessageSquare size={32} strokeWidth={1} />
                    <p>Ask questions about your uploaded documents</p>
                    {!selectedFolderId && (
                        <p style={{ color: '#a78bfa', fontSize: '0.75rem' }}>
                            Select a folder first
                        </p>
                    )}
                </div>
            ) : (
                <div className="rag-chat-messages">
                    {messages.map((msg, i) => (
                        <div key={i} className={`rag-chat-bubble ${msg.role}`}>
                            {msg.content}
                            {msg.sources && msg.sources.length > 0 && (
                                <div className="rag-chat-sources">
                                    Sources: {msg.sources.map((s, j) => (
                                        <span key={j}>{s}{j < msg.sources!.length - 1 ? ', ' : ''}</span>
                                    ))}
                                </div>
                            )}
                        </div>
                    ))}
                    {isLoading && (
                        <div className="rag-typing-indicator">
                            <span /><span /><span />
                        </div>
                    )}
                    <div ref={messagesEndRef} />
                </div>
            )}

            {error && (
                <p style={{ fontSize: '0.7rem', color: '#ef4444', marginTop: '0.25rem', display: 'flex', alignItems: 'center', gap: '0.25rem' }}>
                    <AlertCircle size={12} /> {error}
                </p>
            )}

            <div className="rag-chat-input-row">
                <input
                    className="rag-chat-input"
                    type="text"
                    placeholder={selectedFolderId ? 'Ask a question...' : 'Select a folder first'}
                    value={input}
                    onChange={e => setInput(e.target.value)}
                    onKeyDown={handleKeyDown}
                    disabled={!selectedFolderId || isLoading}
                />
                <button
                    className="rag-chat-send-btn"
                    onClick={handleSend}
                    disabled={!input.trim() || !selectedFolderId || isLoading}
                >
                    <Send size={16} />
                </button>
            </div>
        </div>
    );
};

export default RAGChat;
