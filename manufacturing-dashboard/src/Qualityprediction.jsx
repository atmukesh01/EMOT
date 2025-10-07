// File: src/QualityPrediction.jsx

import { useState } from 'react';
import axios from 'axios';

function QualityPrediction() {
  // All state and functions remain the same...
  const [temperature, setTemperature] = useState(150);
  const [pressure, setPressure] = useState(50);
  const [speed, setSpeed] = useState(1000);
  const [viscosity, setViscosity] = useState(15);
  const [maintenance, setMaintenance] = useState(100);
  const [cycle_time, setCycleTime] = useState(30);
  const [prediction, setPrediction] = useState(null);
  const [targetQuality, setTargetQuality] = useState(98);
  const [optimalParams, setOptimalParams] = useState(null);
  const [locks, setLocks] = useState({ temperature: false, pressure: false, speed: false, viscosity: false, maintenance: false, cycle_time: false, });
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSimulation = async (e) => { e.preventDefault(); setIsLoading(true); setError(''); setPrediction(null); setOptimalParams(null); try { const response = await axios.post('http://1227.0.0.1:5000/predict', { temperature, pressure, speed, viscosity, maintenance, cycle_time, }); setPrediction(response.data.predicted_quality); } catch (err) { setError('Prediction failed. Is the server running?'); } finally { setIsLoading(false); } };
  const handleLockToggle = (param) => { setLocks(prevLocks => ({ ...prevLocks, [param]: !prevLocks[param], })); };
  const handleFindParameters = async (e) => { e.preventDefault(); setIsLoading(true); setError(''); setOptimalParams(null); setPrediction(null); const locked_params = {}; if (locks.temperature) locked_params.temperature = temperature; if (locks.pressure) locked_params.pressure = pressure; if (locks.speed) locked_params.speed = speed; if (locks.viscosity) locked_params.viscosity = viscosity; if (locks.maintenance) locked_params.maintenance = maintenance; if (locks.cycle_time) locked_params.cycle_time = cycle_time; try { const response = await axios.post('http://127.0.0.1:5000/find-parameters', { target_quality: targetQuality, locked_params, }); setOptimalParams(response.data); } catch (err) { setError('Parameter search failed. Is the server running?'); } finally { setIsLoading(false); } };

  return (
    // --- CHANGE: The className="main-content" has been removed from this div ---
    // We use a React Fragment <>...</> as a wrapper instead.
    <>
      <div className="panel">
        <h2>1. Predict Quality from Parameters</h2>
        <form onSubmit={handleSimulation}>
          <div className="form-group"><label>Temperature (°C)</label><input type="number" value={temperature} onChange={(e) => setTemperature(e.target.value)} step="0.1" /></div>
          <div className="form-group"><label>Pressure (psi)</label><input type="number" value={pressure} onChange={(e) => setPressure(e.target.value)} step="0.1" /></div>
          <div className="form-group"><label>Speed (rpm)</label><input type="number" value={speed} onChange={(e) => setSpeed(e.target.value)} /></div>
          <div className="form-group"><label>Viscosity (Pa·s)</label><input type="number" value={viscosity} onChange={(e) => setViscosity(e.target.value)} step="0.1" /></div>
          <div className="form-group"><label>Hours Since Maintenance</label><input type="number" value={maintenance} onChange={(e) => setMaintenance(e.target.value)} /></div>
          <div className="form-group"><label>Cycle Time (s)</label><input type="number" value={cycle_time} onChange={(e) => setCycleTime(e.target.value)} step="0.1" /></div>
          <button type="submit" disabled={isLoading}>{isLoading ? '...' : 'Predict Quality'}</button>
        </form>
        <div className="result-display">
          {isLoading && !optimalParams && <p>Loading...</p>}
          {error && !optimalParams && <p className="error">{error}</p>}
          {prediction !== null && <div className="prediction"><p>Predicted Quality Score:</p><span>{prediction.toFixed(2)}</span></div>}
        </div>
      </div>
      
      <div className="panel">
        <h2>2. Find Parameters for a Quality Score</h2>
        <form onSubmit={handleFindParameters}>
          <div className="form-group"><label>Desired Quality Score</label><input type="number" value={targetQuality} onChange={(e) => setTargetQuality(e.target.value)} step="0.1" /></div>
          <div className="form-group-lockable"><div className="input-wrapper"><label>Temperature (°C)</label><input type="number" value={temperature} onChange={(e) => setTemperature(e.target.value)} step="0.1" disabled={locks.temperature} /></div><button type="button" onClick={() => handleLockToggle('temperature')} className={`lock-btn ${locks.temperature ? 'locked' : ''}`}>{locks.temperature ? 'Unlock' : 'Lock'}</button></div>
          <div className="form-group-lockable"><div className="input-wrapper"><label>Pressure (psi)</label><input type="number" value={pressure} onChange={(e) => setPressure(e.target.value)} step="0.1" disabled={locks.pressure} /></div><button type="button" onClick={() => handleLockToggle('pressure')} className={`lock-btn ${locks.pressure ? 'locked' : ''}`}>{locks.pressure ? 'Unlock' : 'Lock'}</button></div>
          <div className="form-group-lockable"><div className="input-wrapper"><label>Speed (rpm)</label><input type="number" value={speed} onChange={(e) => setSpeed(e.target.value)} disabled={locks.speed} /></div><button type="button" onClick={() => handleLockToggle('speed')} className={`lock-btn ${locks.speed ? 'locked' : ''}`}>{locks.speed ? 'Unlock' : 'Lock'}</button></div>
          <div className="form-group-lockable"><div className="input-wrapper"><label>Viscosity (Pa·s)</label><input type="number" value={viscosity} onChange={(e) => setViscosity(e.target.value)} step="0.1" disabled={locks.viscosity} /></div><button type="button" onClick={() => handleLockToggle('viscosity')} className={`lock-btn ${locks.viscosity ? 'locked' : ''}`}>{locks.viscosity ? 'Unlock' : 'Lock'}</button></div>
          <div className="form-group-lockable"><div className="input-wrapper"><label>Hours Since Maintenance</label><input type="number" value={maintenance} onChange={(e) => setMaintenance(e.target.value)} disabled={locks.maintenance} /></div><button type="button" onClick={() => handleLockToggle('maintenance')} className={`lock-btn ${locks.maintenance ? 'locked' : ''}`}>{locks.maintenance ? 'Unlock' : 'Lock'}</button></div>
          <div className="form-group-lockable"><div className="input-wrapper"><label>Cycle Time (s)</label><input type="number" value={cycle_time} onChange={(e) => setCycleTime(e.target.value)} step="0.1" disabled={locks.cycle_time} /></div><button type="button" onClick={() => handleLockToggle('cycle_time')} className={`lock-btn ${locks.cycle_time ? 'locked' : ''}`}>{locks.cycle_time ? 'Unlock' : 'Lock'}</button></div>
          <button type="submit" disabled={isLoading}>{isLoading ? '...' : 'Find Best Parameters'}</button>
        </form>
      </div>

      <div className="output-panel">
          <h2>Optimal Settings Result</h2>
          <div className="result-display">
              {isLoading && !prediction && <p>Searching for parameters...</p>}
              {error && !prediction && <p className="error">{error}</p>}
              {optimalParams && <div className="optimal-params"><p>Found settings for a target of <strong>{targetQuality}</strong></p><ul><li><strong>Temp:</strong> {optimalParams.best_parameters.temperature}°C</li><li><strong>Pressure:</strong> {optimalParams.best_parameters.pressure} psi</li><li><strong>Speed:</strong> {optimalParams.best_parameters.speed} rpm</li><li><strong>Viscosity:</strong> {optimalParams.best_parameters.viscosity} Pa·s</li><li><strong>Maintenance:</strong> {optimalParams.best_parameters.maintenance} hrs</li><li><strong>Cycle Time:</strong> {optimalParams.best_parameters.cycle_time} s</li></ul><h3>Achieved Quality: <span>{optimalParams.achieved_quality.toFixed(2)}</span></h3></div>}
          </div>
      </div>
    </>
  );
}

export default QualityPrediction;