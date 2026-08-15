import React, { useState, useEffect } from 'react';

// Mock data representing the stream from the Orchestrator
const MOCK_LOGS = [
  { id: 1, time: '09:16:01', symbol: 'RELIANCE', score: 82, action: 'BUY', bull: 'Technical trend is clearly bullish (EMA 20 > EMA 50). | Broader market regime supports long trades.', bear: 'Asset is technically overbought (RSI = 72).' },
  { id: 2, time: '09:17:05', symbol: 'HDFCBANK', score: 45, action: 'HOLD', bull: 'None', bear: 'Technical trend is bearish. Buying is catching a falling knife. | Broader market is HIGH_VOLATILITY.' },
  { id: 3, time: '09:21:30', symbol: 'TCS', score: 90, action: 'BUY', bull: 'Momentum is healthy (RSI = 55). | Broader market regime supports long trades. | Sentiment is Positive.', bear: 'None' },
];

const AIDebateLog = () => {
  const [logs, setLogs] = useState([]);

  useEffect(() => {
    // In production, this would subscribe to a WebSocket or polling endpoint
    // to stream real logs from the Python Orchestrator.
    setLogs(MOCK_LOGS);
  }, []);

  return (
    <div className="log-terminal">
      {logs.map((log) => (
        <div key={log.id} className="log-entry">
          <span className="log-time">[{log.time}]</span>
          <strong>{log.symbol}</strong> — Final Score: <span style={{ color: log.score > 75 ? 'var(--accent-green)' : 'var(--text-secondary)' }}>{log.score}/100</span> — Action: <strong>{log.action}</strong>
          
          <div style={{ paddingLeft: '16px', marginTop: '4px', borderLeft: '2px solid rgba(255,255,255,0.1)' }}>
            <div className="log-bull">▲ Bull Case: {log.bull}</div>
            <div className="log-bear">▼ Bear Case: {log.bear}</div>
          </div>
        </div>
      ))}
      <div className="log-entry">
        <span className="log-time">[{new Date().toLocaleTimeString('en-GB')}]</span>
        <span style={{ color: 'var(--text-secondary)' }}>Waiting for next 1-minute candle...</span>
      </div>
    </div>
  );
};

export default AIDebateLog;
