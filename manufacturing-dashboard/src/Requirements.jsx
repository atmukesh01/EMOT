// File: src/Requirements.jsx

function Requirements() {
  return (
    // --- CHANGE: The className has been removed from this div ---
    <>
      <div className="info-panel">
        <h2>Process Requirements</h2>
        <p>This section details the critical parameters and materials involved in the plastic injection molding process. Each variable directly influences the final product's quality and must be carefully controlled.</p>
        <h3>Material Properties</h3>
        <ul><li><strong>Viscosity (Pa·s):</strong> Measures the raw material's resistance to flow. It dictates how easily the plastic fills the mold. Variations can lead to defects.</li></ul>
        <h3>Machine Parameters</h3>
        <ul><li><strong>Temperature (°C):</strong> The heat of the barrel where plastic is melted. It must be precise to ensure proper material fluidity without causing degradation.</li><li><strong>Pressure (psi):</strong> The force used to inject and hold the plastic in the mold. Essential for creating a complete and properly formed part.</li><li><strong>Speed (rpm):</strong> The rotational speed of the extruder screw, controlling the rate at which material is melted and moved.</li></ul>
        <h3>Operational Factors</h3>
        <ul><li><strong>Hours Since Maintenance (hrs):</strong> Represents the wear and tear on the machine and mold. Older components may perform differently.</li><li><strong>Cycle Time (s):</strong> The total time to produce one part. A key indicator of efficiency and process health.</li></ul>
      </div>
    </>
  );
}
export default Requirements;