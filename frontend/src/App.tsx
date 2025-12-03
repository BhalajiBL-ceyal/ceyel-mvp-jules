import React, { useState } from 'react';
import axios from 'axios';
import './App.css';
import { FileUpload } from './components/FileUpload';
import { ProcessVisualizer } from './components/ProcessVisualizer';

// Define a simple type for the process model for now
interface ProcessModel {
  nodes: Array<{ id: string; label: string; size: number }>;
  edges: Array<{ source: string; target: string; weight: number }>;
}

function App() {
  const [processModel, setProcessModel] = useState<ProcessModel | null>(null);
  const [errorMessage, setErrorMessage] = useState<string>('');

  const handleFileUpload = async (file: File) => {
    const formData = new FormData();
    formData.append('file', file);

    try {
      setErrorMessage('');
      setProcessModel(null);

      // 1. Ingest the CSV to get the event log
      const ingestResponse = await axios.post('/api/v1/ingest/csv', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });

      const eventLog = ingestResponse.data;

      // 2. Discover the process model from the event log
      const discoveryResponse = await axios.post('/api/v1/discover/dfg', eventLog);
      
      setProcessModel(discoveryResponse.data);

    } catch (error: any) {
      setErrorMessage(`Error: ${error.response?.data?.detail || error.message}`);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>CEYEL Process Mining</h1>
      </header>
      <main>
        <FileUpload onUpload={handleFileUpload} />
        {errorMessage && <p style={{ color: 'red' }}>{errorMessage}</p>}
        <ProcessVisualizer model={processModel} />
      </main>
    </div>
  );
}

export default App;
