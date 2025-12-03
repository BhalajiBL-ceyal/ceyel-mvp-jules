import React, { useState } from 'react';

interface FileUploadProps {
    onUpload: (file: File) => void;
}

export const FileUpload: React.FC<FileUploadProps> = ({ onUpload }) => {
    const [file, setFile] = useState<File | null>(null);

    const onFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files) {
            setFile(e.target.files[0]);
        }
    };

    const handleUploadClick = () => {
        if (file) {
            onUpload(file);
        } else {
            alert("Please select a file first.");
        }
    };

    return (
        <div style={{ margin: '20px' }}>
            <h2>Upload Event Log (CSV)</h2>
            <div>
                <input type="file" accept=".csv" onChange={onFileChange} />
                <button onClick={handleUploadClick} disabled={!file}>
                    Discover Process
                </button>
            </div>
        </div>
    );
};
