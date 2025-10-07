// File: src/Processes.jsx

import React, { useState, useEffect, useRef } from 'react';
import './Processes.css';

const processData = [
  { name: 'Injection Molding', description: 'Molten plastic is injected into the mold to form the part. Our ML model provides real-time predictions here.', duration: 2000 },
  { name: 'Degating & Handling', description: 'A robotic arm removes the part and cuts away excess plastic (the runner system).', duration: 1500 },
  { name: 'Cooling & Curing', description: 'The part travels on a conveyor to cool down and solidify, ensuring its structural stability.', duration: 2500 },
  { name: 'Automated Quality Inspection', description: 'A vision system inspects the cooled part for any dimensional errors or visual defects.', duration: 1500 },
  { name: 'Assembly & Finishing', description: 'The part is assembled with other components or printed with logos.', duration: 2000 },
  { name: 'Packaging', description: 'The final, assembled product is packaged for shipping.', duration: 1500 },
];

function Processes() {
  const [activeStep, setActiveStep] = useState(-1);
  const [isRunning, setIsRunning] = useState(false);
  const timeoutRef = useRef(null);

  useEffect(() => {
    if (isRunning && activeStep < processData.length - 1) {
      timeoutRef.current = setTimeout(() => {
        setActiveStep(prevStep => prevStep + 1);
      }, processData[activeStep === -1 ? 0 : activeStep].duration);
    } else if (activeStep >= processData.length - 1) {
      setIsRunning(false);
    }
    return () => clearTimeout(timeoutRef.current);
  }, [isRunning, activeStep]);

  const handleStart = () => {
    if (activeStep >= processData.length - 1) {
      setActiveStep(-1);
    }
    setIsRunning(true);
    if (activeStep === -1) {
      setActiveStep(0);
    }
  };

  const handleReset = () => {
    setIsRunning(false);
    setActiveStep(-1);
    clearTimeout(timeoutRef.current);
  };

  return (
    <>
      <div className="info-panel">
        <h2>Manufacturing Workflow Simulation</h2>
        <div className="simulation-controls">
          <button onClick={handleStart} disabled={isRunning}>
            ▶ Start Simulation
          </button>
          <button onClick={handleReset}>
            ■ Reset
          </button>
        </div>
        
        <div className="timeline-container-horizontal">
          {processData.map((step, index) => (
            <div
              key={step.name}
              className={`timeline-step ${index % 2 === 0 ? 'left' : 'right'} ${index <= activeStep ? 'completed' : ''} ${index === activeStep ? 'active' : ''}`}
            >
              <div className="step-node">{index + 1}</div>
              <div className="step-details">
                <h3>{step.name}</h3>
                <p>{step.description}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </>
  );
}

export default Processes;