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

    // Using the same webhooks as before
    const LIST_FOLDERS_WEBHOOK = 'https://emanueleserra.app.n8n.cloud/webhook/rag-folders';
    const UPLOAD_WEBHOOK = 'https://emanueleserra.app.n8n.cloud/webhook/rag-upload';

    useEffect(() => {
        fetch(LIST_FOLDERS_WEBHOOK)
            .then(res => res.json())
            .then(data => {
                let items: DriveFolder[] = [];
                if (Array.isArray(data)) items = data;
                else if (Array.isArray((data as any)?.documents)) items = (data as any).documents;
                else items = Object.values(data).find(v => Array.isArray(v)) as DriveFolder[] || [];

                setFolders(items);
                setLoadingFolders(false);
            })
            .catch(err => {
                console.error("Error fetching folders:", err);
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
        const formData = new FormData();
        formData.append('file', file);
        formData.append('folderId', selectedFolderId);

        try {
            const res = await fetch(UPLOAD_WEBHOOK, { method: 'POST', body: formData });
            if (!res.ok) throw new Error('Upload failed');

            setStatus('success');
            setFile(null);
            setTimeout(() => setStatus('idle'), 3000);
        } catch (err) {
            console.error("Upload error:", err);
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
                </div>

                {/* File Input - Compact */}
                <div className="rag-input-group">
                    <label><Upload size={14} /> File</label>
                    <div className="rag-file-input" onClick={() => document.getElementById('rag-file-hidden')?.click()}>
                        {file ? <span className="text-white">{file.name}</span> : <span className="text-gray-500">Choose PDF...</span>}
                        <input id="rag-file-hidden" type="file" hidden onChange={handleFileChange} />
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
