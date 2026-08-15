import React, { useState, useEffect } from 'react';
import { getProtectedHoldings } from '../services/api';

const ProtectedHoldings = () => {
  const [holdings, setHoldings] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // In a real scenario, this fetches from Spring Boot backend.
    // We'll mock it if the API is unreachable during frontend dev.
    const fetchHoldings = async () => {
      try {
        const data = await getProtectedHoldings();
        setHoldings(data);
      } catch (error) {
        console.warn("Backend not reachable. Using mock protected holdings data.");
        setHoldings([
          { id: 1, tradingSymbol: 'INFY', quantity: 250, source: 'EQUITY', timestamp: new Date().toISOString() },
          { id: 2, tradingSymbol: 'RELIANCE', quantity: 100, source: 'EQUITY', timestamp: new Date().toISOString() },
          { id: 3, tradingSymbol: 'PARAGPARIKH-FLEXI', quantity: 1543, source: 'MUTUAL_FUND', timestamp: new Date().toISOString() }
        ]);
      } finally {
        setLoading(false);
      }
    };

    fetchHoldings();
  }, []);

  if (loading) return <div style={{ padding: '20px', color: 'var(--text-secondary)' }}>Loading protected baseline...</div>;

  return (
    <div style={{ overflowX: 'auto' }}>
      <table>
        <thead>
          <tr>
            <th>Symbol</th>
            <th>Type</th>
            <th>Baseline Qty</th>
            <th>Protected Since</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          {holdings.map((h) => (
            <tr key={h.id}>
              <td style={{ fontWeight: 600 }}>{h.tradingSymbol}</td>
              <td>{h.source}</td>
              <td>{h.quantity}</td>
              <td style={{ color: 'var(--text-secondary)' }}>{new Date(h.timestamp).toLocaleDateString()}</td>
              <td>
                <span className="status-badge status-protected">PROTECTED</span>
              </td>
            </tr>
          ))}
          {holdings.length === 0 && (
            <tr>
              <td colSpan="5" style={{ textAlign: 'center', color: 'var(--text-secondary)' }}>No protected holdings found.</td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
};

export default ProtectedHoldings;
