// File: src/App.jsx

import { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  // State for input fields
  const [temperature, setTemperature] = useState(150);
  const [pressure, setPressure] = useState(50);
  const [speed, setSpeed] = useState(1000);

  // State for the prediction result and loading status
  const [prediction, setPrediction] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSimulation = async (e) => {
    e.preventDefault(); // Prevent form from reloading the page
    setIsLoading(true);
    setError('');
    setPrediction(null);

    try {
      // API endpoint of our Flask back-end
      const apiUrl = 'http://127.0.0.1:5000/predict';
      
      const response = await axios.post(apiUrl, {
        temperature,
        pressure,
        speed,
      });

      setPrediction(response.data.predicted_quality);

    } catch (err) {
      setError('Failed to get a prediction. Is the Python server running?');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="dashboard">
      <header>
        <h1>Manufacturing Process Simulator</h1>
      </header>
      <main>
        <div className="input-panel">
          <h2>Process Parameters</h2>
          <form onSubmit={handleSimulation}>
            <div className="form-group">
              <label>Temperature (°C)</label>
              <input
                type="number"
                value={temperature}
                onChange={(e) => setTemperature(e.target.value)}
                step="0.1"
              />
            </div>
            <div className="form-group">
              <label>Pressure (psi)</label>
              <input
                type="number"
                value={pressure}
                onChange={(e) => setPressure(e.target.value)}
                step="0.1"
              />
            </div>
            <div className="form-group">
              <label>Speed (rpm)</label>
              <input
                type="number"
                value={speed}
                onChange={(e) => setSpeed(e.target.value)}
              />
            </div>
            <button type="submit" disabled={isLoading}>
              {isLoading ? 'Simulating...' : 'Simulate Quality'}
            </button>
          </form>
        </div>

        <div className="output-panel">
          <h2>Predicted Result</h2>
          <div className="result-display">
            {isLoading && <p>Loading...</p>}
            {error && <p className="error">{error}</p>}
            {prediction !== null && (
              <div className="prediction">
                <p>Predicted Quality Score:</p>
                <span>{prediction.toFixed(2)}</span>
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;