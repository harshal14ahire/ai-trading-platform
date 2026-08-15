import React from 'react';
import AIDebateLog from './AIDebateLog';
import ProtectedHoldings from './ProtectedHoldings';
import KillSwitch from './KillSwitch';
import { Activity, ShieldCheck, AlertTriangle } from 'lucide-react';

const Dashboard = () => {
  return (
    <div className="dashboard-grid">
      
      {/* Top Row */}
      <div className="glass-panel col-span-8">
        <h2 className="panel-title"><Activity size={20} color="var(--accent-blue)" /> AI Signal & Debate Log</h2>
        <AIDebateLog />
      </div>

      <div className="glass-panel col-span-4" style={{ display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
        <h2 className="panel-title" style={{ color: 'var(--accent-red)' }}><AlertTriangle size={20} /> Emergency Controls</h2>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', marginBottom: '24px' }}>
          Instantly halt the Orchestrator and send market orders to liquidate all currently open AI positions.
        </p>
        <KillSwitch />
      </div>

      {/* Bottom Row */}
      <div className="glass-panel col-span-12">
        <h2 className="panel-title"><ShieldCheck size={20} color="var(--accent-green)" /> Protected Asset Guard (Baseline Portfolio)</h2>
        <ProtectedHoldings />
      </div>

    </div>
  );
};

export default Dashboard;
