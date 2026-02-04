import React, { useState, useEffect } from 'react';
import { Upload, Folder, FileUp, Loader2, CheckCircle, AlertCircle } from 'lucide-react';
import './RAGUpload.css';

interface DriveFolder {
    id: string;
    name: string;
}

const RAGUpload: React.FC = () => {
    const [folders, setFolders] = useState<DriveFolder[]>([]);
    const [selectedFolderId, setSelectedFolderId] = useState<string>('');
    const [file, setFile] = useState<File | null>(null);
    const [status, setStatus] = useState<'idle' | 'uploading' | 'success' | 'error'>('idle');
    const [loadingFolders, setLoadingFolders] = useState<boolean>(true);
    const [debugError, setDebugError] = useState<string | null>(null);

    // Using the same webhooks as before
    const LIST_FOLDERS_WEBHOOK = 'https://emanueleserra.app.n8n.cloud/webhook/rag-folders';
    const UPLOAD_WEBHOOK = 'https://emanueleserra.app.n8n.cloud/webhook/rag-upload';

    useEffect(() => {
        console.log(`[RAG] Fetching folders from: ${LIST_FOLDERS_WEBHOOK}`);
        setDebugError(null);

        fetch(LIST_FOLDERS_WEBHOOK)
            .then(res => {
                console.log(`[RAG] Response status: ${res.status} ${res.statusText}`);
                if (!res.ok) {
                    throw new Error(`Server returned ${res.status} ${res.statusText}`);
                }
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
                setLoadingFolders(false);
            })
            .catch(err => {
                console.error("[RAG] Error fetching folders:", err);
                let errorMsg = err.message;
                if (err instanceof TypeError && err.message === 'Failed to fetch') {
                    errorMsg = 'CORS/Network Error (Check Console)';
                    console.error("[RAG] 'Failed to fetch' usually means CORS error or Network unreachable. Verify Webhook URL and N8N Active status.");
                }
                setDebugError(errorMsg);
                setLoadingFolders(false);
            });
    }, []);

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

            <div className="rag-body">
                {/* Folder Select */}
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
                    {debugError && <p className="text-xs text-red-400 mt-1">Error: {debugError}</p>}
                </div>

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
            </div>
        </div>
    );
};

export default RAGUpload;
