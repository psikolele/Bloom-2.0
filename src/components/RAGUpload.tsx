import React, { useState } from 'react';
import { Upload, Folder, FileUp, Loader2, CheckCircle, AlertCircle } from 'lucide-react';
import './RAGUpload.css';

export interface DriveFolder {
    id: string;
    name: string;
}

interface RAGUploadProps {
    folders: DriveFolder[];
    selectedFolderId: string;
    setSelectedFolderId: (id: string) => void;
    loadingFolders: boolean;
    folderError: string | null;
    username: string;
    isAdmin: boolean;
}

const RAGUpload: React.FC<RAGUploadProps> = ({ folders, selectedFolderId, setSelectedFolderId, loadingFolders, folderError, username, isAdmin }) => {
    const [file, setFile] = useState<File | null>(null);
    const [status, setStatus] = useState<'idle' | 'uploading' | 'success' | 'error'>('idle');
    const [debugError, setDebugError] = useState<string | null>(null);

    const UPLOAD_WEBHOOK = 'https://emanueleserra.app.n8n.cloud/webhook/rag-upload';

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files[0]) {
            setFile(e.target.files[0]);
            setStatus('idle');
        }
    };

    const handleUpload = async () => {
        if (!file || !selectedFolderId) return;

        setStatus('uploading');
        setDebugError(null);

        const formData = new FormData();
        formData.append('file', file);
        formData.append('folderId', selectedFolderId);
        formData.append('username', username);

        try {
            console.log('[RAG] Starting upload to:', UPLOAD_WEBHOOK);
            console.log('[RAG] File:', file.name, 'Folder:', selectedFolderId);

            const res = await fetch(UPLOAD_WEBHOOK, { method: 'POST', body: formData });
            console.log('[RAG] Upload response status:', res.status);

            const responseData = await res.json();
            console.log('[RAG] Upload response data:', responseData);

            // Check for error in response body (N8N may return 200 but with error in body)
            if (!res.ok || responseData.error || responseData.success === false) {
                const errorMsg = responseData.error || responseData.message || `Upload failed (${res.status})`;
                console.error('[RAG] Upload error:', errorMsg);
                setDebugError(errorMsg);
                setStatus('error');
                return;
            }

            console.log('[RAG] Upload successful! FileId:', responseData.fileId);
            setStatus('success');
            setFile(null);
            setTimeout(() => setStatus('idle'), 3000);
        } catch (err: any) {
            console.error("[RAG] Upload exception:", err);
            setDebugError(err.message || 'Network error');
            setStatus('error');
        }
    };


    return (
        <div className="rag-upload-card">
            <div className="rag-header">
                <div className="rag-icon">
                    <FileUp size={20} color="#a78bfa" />
                </div>
                <h3>Quick RAG Upload</h3>
            </div>

            {/* No RAG configured for this non-admin user */}
        {!isAdmin && !selectedFolderId && !loadingFolders && (
            <div style={{ textAlign: 'center', padding: '1.5rem 1rem', color: '#6b7280' }}>
                <Upload size={32} strokeWidth={1} style={{ margin: '0 auto 0.5rem' }} />
                <p style={{ fontSize: '0.8rem' }}>
                    Nessun database RAG configurato per il tuo account.
                </p>
            </div>
        )}

        {(isAdmin || selectedFolderId) && (
        <div className="rag-body">
                {/* Folder Select: admin sees the full dropdown; non-admin sees a read-only label */}
                {isAdmin ? (
                <div className="rag-input-group">
                    <label><Folder size={14} /> Target</label>
                    <select
                        value={selectedFolderId}
                        onChange={(e) => setSelectedFolderId(e.target.value)}
                        disabled={loadingFolders || status === 'uploading'}
                        className="rag-select"
                    >
                        <option value="" disabled>Select Folder</option>
                        {loadingFolders ? <option>Loading...</option> : folders.map(f => (
                            <option key={f.id} value={f.id}>{f.name}</option>
                        ))}
                    </select>
                    {(folderError || debugError) && <p className="text-xs text-red-400 mt-1">Error: {folderError || debugError}</p>}
                </div>
                ) : (
                <div className="rag-input-group">
                    <label><Folder size={14} /> Database</label>
                    <span style={{ fontSize: '0.85rem', color: '#a78bfa', padding: '0.25rem 0', display: 'block' }}>
                        {folders[0]?.name ?? ''}
                    </span>
                </div>
                )}

                {/* File Input - Compact */}
                <div className="rag-input-group">
                    <label><Upload size={14} /> File</label>
                    <div className="rag-file-input" onClick={() => document.getElementById('rag-file-hidden')?.click()}>
                        {file ? <span className="text-white">{file.name}</span> : <span className="text-gray-500">Choose file (PDF, Word, Excel, Images...)</span>}
                        <input id="rag-file-hidden" type="file" hidden onChange={handleFileChange} accept=".pdf,.doc,.docx,.xls,.xlsx,.ppt,.pptx,.png,.jpg,.jpeg,.gif,.mp4,.mov,.md,.txt" />
                    </div>

                </div>

                {/* Action Button */}
                <button
                    className={`rag-confirm-btn ${status}`}
                    onClick={handleUpload}
                    disabled={!file || !selectedFolderId || status === 'uploading'}
                >
                    {status === 'uploading' ? <Loader2 className="animate-spin" size={16} /> :
                        status === 'success' ? <CheckCircle size={16} /> :
                            status === 'error' ? <AlertCircle size={16} /> : 'Upload'}
                </button>
                {debugError && <p className="text-xs text-red-400 mt-1">Error: {debugError}</p>}
            </div>
        )}
        </div>
    );
};

export default RAGUpload;
