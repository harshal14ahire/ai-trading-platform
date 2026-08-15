import React, { useState } from 'react';
import { PowerOff } from 'lucide-react';
import { triggerKillSwitch } from '../services/api';

const KillSwitch = () => {
  const [status, setStatus] = useState('IDLE'); // IDLE, CONFIRM, EXECUTING, DONE

  const handleTrigger = async () => {
    if (status === 'IDLE') {
      setStatus('CONFIRM');
    } else if (status === 'CONFIRM') {
      setStatus('EXECUTING');
      try {
        await triggerKillSwitch();
        setStatus('DONE');
        setTimeout(() => setStatus('IDLE'), 5000);
      } catch (error) {
        console.error("Kill switch failed:", error);
        alert("CRITICAL ERROR: Failed to reach backend. Manually liquidate via Kite.");
        setStatus('IDLE');
      }
    }
  };

  return (
    <button 
      className="kill-switch" 
      onClick={handleTrigger}
      style={{ 
        background: status === 'CONFIRM' ? '#b91c1c' : status === 'EXECUTING' ? '#fbbf24' : status === 'DONE' ? 'var(--accent-green)' : 'var(--accent-red)',
        color: status === 'EXECUTING' ? '#000' : '#fff'
      }}
    >
      <PowerOff size={24} />
      {status === 'IDLE' && "LIQUIDATE ALL POSITIONS"}
      {status === 'CONFIRM' && "CLICK AGAIN TO CONFIRM LIQUIDATION"}
      {status === 'EXECUTING' && "SENDING MARKET ORDERS..."}
      {status === 'DONE' && "POSITIONS FLATTENED"}
    </button>
  );
};

export default KillSwitch;
