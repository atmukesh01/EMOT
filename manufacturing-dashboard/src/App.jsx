// File: src/App.jsx

import { useState } from 'react';
import './App.css';
import Requirements from './Requirements';
import Processes from './Processes';
import QualityPrediction from './Qualityprediction';

function App() {
  const [currentPage, setCurrentPage] = useState(null);

  const renderPage = () => {
    if (!currentPage) return null;
    
    switch (currentPage) {
      case 'requirements':
        return <Requirements />;
      case 'processes':
        return <Processes />;
      case 'prediction':
        return <QualityPrediction />;
      default:
        return null;
    }
  };

  return (
    <div className="dashboard">
      <div className="title-container">
        <h1 className="main-title">Process and Product Optimization Tool</h1>
        <p className="subtitle">Plastic Reuse System</p>
      </div>
      <nav>
        <button onClick={() => setCurrentPage('prediction')} className={currentPage === 'prediction' ? 'active' : ''}>
          Quality Prediction
        </button>
        <button onClick={() => setCurrentPage('requirements')} className={currentPage === 'requirements' ? 'active' : ''}>
          Requirements
        </button>
        <button onClick={() => setCurrentPage('processes')} className={currentPage === 'processes' ? 'active' : ''}>
          Processes
        </button>
      </nav>
      
      {/* --- CHANGE: The className is now here --- */}
      <main className="main-content">
        {renderPage()}
      </main>
    </div>
  );
}

export default App;