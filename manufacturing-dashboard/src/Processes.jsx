// File: src/Processes.jsx

function Processes() {
  return (
    // --- CHANGE: The className has been removed from this div ---
    <>
      <div className="info-panel">
        <h2>Manufacturing Workflow</h2>
        <p>The journey from raw plastic pellets to a finished product involves several sequential, high-speed processes. Below is a typical timeline.</p>
        <ol className="process-list">
          <li><strong>Injection Molding (30s - 2min):</strong> The core process where molten plastic is injected into a mold to form the part. Our ML model provides real-time predictions during this phase.</li>
          <li><strong>Degating & Handling (5 - 10s):</strong> A robotic arm removes the part from the machine and cuts away excess plastic (the runner system).</li>
          <li><strong>Cooling & Curing (5min - 1hr):</strong> The part travels on a conveyor to cool down and solidify completely, ensuring its structural stability.</li>
          <li><strong>Automated Quality Inspection (1 - 2s):</strong> A vision system inspects the cooled part for any dimensional errors or visual defects.</li>
          <li><strong>Assembly & Finishing (10s - 5min):</strong> The part is assembled with other components, printed with logos, or given its final surface texture.</li>
          <li><strong>Packaging (5 - 10s):</strong> The final, assembled product is packaged for shipping.</li>
        </ol>
      </div>
    </>
  );
}
export default Processes;