// File: src/App.jsx

import { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [temperature, setTemperature] = useState(150);
  const [pressure, setPressure] = useState(50);
  const [speed, setSpeed] = useState(1000);
  const [prediction, setPrediction] = useState(null);

  const [targetQuality, setTargetQuality] = useState(98);
  const [optimalParams, setOptimalParams] = useState(null);
  
  const [locks, setLocks] = useState({
    temperature: false,
    pressure: false,
    speed: false,
  });

  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSimulation = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');
    setPrediction(null);
    setOptimalParams(null);

    try {
      const response = await axios.post('http://127.0.0.1:5000/predict', {
        temperature, pressure, speed,
      });
      setPrediction(response.data.predicted_quality);
    } catch (err) {
      setError('Prediction failed. Is the server running?');
    } finally {
      setIsLoading(false);
    }
  };
  
  const handleLockToggle = (param) => {
    setLocks(prevLocks => ({
      ...prevLocks,
      [param]: !prevLocks[param],
    }));
  };

  const handleFindParameters = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');
    setOptimalParams(null);
    setPrediction(null);
    
    const locked_params = {};
    if (locks.temperature) locked_params.temperature = temperature;
    if (locks.pressure) locked_params.pressure = pressure;
    if (locks.speed) locked_params.speed = speed;

    try {
      const response = await axios.post('http://127.0.0.1:5000/find-parameters', {
        target_quality: targetQuality,
        locked_params,
      });
      setOptimalParams(response.data);
    } catch (err) {
      setError('Parameter search failed. Is the server running?');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="dashboard">
      <header><h1>Manufacturing Process Simulator & Optimizer</h1></header>
      <main>
        {/* --- Panel 1: Predict Quality --- */}
        <div className="panel">
          <h2>1. Predict Quality from Parameters</h2>
          <form onSubmit={handleSimulation}>
            <div className="form-group">
              <label>Temperature (°C)</label>
              <input type="number" value={temperature} onChange={(e) => setTemperature(e.target.value)} step="0.1" />
            </div>
            <div className="form-group">
              <label>Pressure (psi)</label>
              <input type="number" value={pressure} onChange={(e) => setPressure(e.target.value)} step="0.1" />
            </div>
            <div className="form-group">
              <label>Speed (rpm)</label>
              <input type="number" value={speed} onChange={(e) => setSpeed(e.target.value)} />
            </div>
            <button type="submit" disabled={isLoading}>{isLoading ? '...' : 'Predict Quality'}</button>
          </form>
          <div className="result-display">
            {isLoading && !optimalParams && <p>Loading...</p>}
            {error && !optimalParams && <p className="error">{error}</p>}
            {prediction !== null && (
              <div className="prediction">
                <p>Predicted Quality Score:</p>
                <span>{prediction.toFixed(2)}</span>
              </div>
            )}
          </div>
        </div>
        
        {/* --- Panel 2: Find Parameters --- */}
        <div className="panel">
          <h2>2. Find Parameters for a Quality Score</h2>
          <form onSubmit={handleFindParameters}>
            <div className="form-group">
              <label>Desired Quality Score</label>
              <input type="number" value={targetQuality} onChange={(e) => setTargetQuality(e.target.value)} step="0.1" />
            </div>
            <div className="form-group-lockable">
              <div className="input-wrapper">
                <label>Temperature (°C)</label>
                <input type="number" value={temperature} onChange={(e) => setTemperature(e.target.value)} step="0.1" disabled={locks.temperature} />
              </div>
              <button type="button" onClick={() => handleLockToggle('temperature')} className={`lock-btn ${locks.temperature ? 'locked' : ''}`}>
                {locks.temperature ? 'Unlock' : 'Lock'}
              </button>
            </div>
            <div className="form-group-lockable">
              <div className="input-wrapper">
                <label>Pressure (psi)</label>
                <input type="number" value={pressure} onChange={(e) => setPressure(e.target.value)} step="0.1" disabled={locks.pressure} />
              </div>
              <button type="button" onClick={() => handleLockToggle('pressure')} className={`lock-btn ${locks.pressure ? 'locked' : ''}`}>
                {locks.pressure ? 'Unlock' : 'Lock'}
              </button>
            </div>
            <div className="form-group-lockable">
              <div className="input-wrapper">
                <label>Speed (rpm)</label>
                <input type="number" value={speed} onChange={(e) => setSpeed(e.target.value)} disabled={locks.speed} />
              </div>
              <button type="button" onClick={() => handleLockToggle('speed')} className={`lock-btn ${locks.speed ? 'locked' : ''}`}>
                {locks.speed ? 'Unlock' : 'Lock'}
              </button>
            </div>
            <button type="submit" disabled={isLoading}>{isLoading ? '...' : 'Find Best Parameters'}</button>
          </form>
        </div>

        {/* --- Panel 3: Dedicated Output Area --- */}
        <div className="output-panel">
            <h2>Optimal Settings Result</h2>
            <div className="result-display">
                {isLoading && !prediction && <p>Searching for parameters...</p>}
                {error && !prediction && <p className="error">{error}</p>}
                {optimalParams && (
                <div className="optimal-params">
                    <p>Found settings for a target of <strong>{targetQuality}</strong></p>
                    <ul>
                    <li><strong>Temp:</strong> {optimalParams.best_parameters.temperature}°C</li>
                    <li><strong>Pressure:</strong> {optimalParams.best_parameters.pressure} psi</li>
                    <li><strong>Speed:</strong> {optimalParams.best_parameters.speed} rpm</li>
                    </ul>
                    <h3>Achieved Quality: <span>{optimalParams.achieved_quality.toFixed(2)}</span></h3>
                </div>
                )}
            </div>
        </div>
      </main>
    </div>
  );
}

export default App;