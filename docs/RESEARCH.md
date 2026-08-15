# Deep Technical and Regulatory Research

## 1. Zerodha Kite Connect Capabilities & Limits
*   **Order API Limits:** The maximum allowed limit is 10 orders per second (OPS) per client (trading) account. Requests exceeding this limit receive a HTTP 429 response. There is also an RMS limit of 5,000 orders per day across all segments.
*   **General API Endpoints:** 10 requests per second at the API key level. Quote API is 1 req/sec, Historical Data is 3 req/sec.
*   **WebSocket API:** Supports subscribing to up to 3,000 instruments for live tick data.
*   **Portfolio & Mutual Fund API:** Kite Connect can read holdings, positions, and mutual fund portfolios. However, direct buy/sell order placement for mutual funds is NOT supported via API.
*   **Sandbox Availability:** Zerodha does NOT offer an official sandbox environment for Kite Connect. Workarounds involve placing orders with insufficient balance or implementing internal paper-trading logic.
*   **Sources:**
    *   [Zerodha Rate Limits Documentation](https://kite.trade/docs/connect/v3/exceptions/)
    *   [Zerodha Connect Subscriptions](https://kite.trade/forum/)

## 2. SEBI Retail Algorithmic Trading Framework (2026)
*   **Static IP Requirement:** To comply with SEBI’s 2026 retail algo trading framework, static IP registration is mandatory for all API users. Orders originating from dynamic IPs are rejected.
*   **Authentication:** Continuous refresh-token sessions are deprecated. A fresh 2FA authentication flow is required daily.
*   **Algo Tagging:** All algos must run through exchange-approved broker systems. Retail algo orders are subjected to Market Price Protection (MPP).
*   **Sources:**
    *   [SEBI Circular 2025/2026 Algorithmic Trading Framework](https://www.sebi.gov.in/)
    *   [NSE Retail Algo Guidelines](https://www.nseindia.com/)

## 3. Multi-Agent Trading Architecture
*   **AI-Agent Trading Research (2024-2026):** Recent papers such as *TradingAgents*, *FinRobot*, and *QuantAgent* demonstrate that single-agent LLMs are inadequate. Modern architectures split roles:
    *   **Fundamental/Sentiment Agent:** Processes unstructured news and filings.
    *   **Technical/Quantitative Agent:** Processes structured time-series data.
    *   **Risk/Debate Agent:** Acts as an adversarial network to challenge the signal agent's assumptions.
*   **Transaction Costs & Slippage:** Research indicates that simulated algorithmic returns often fail in production due to insufficient accounting for slippage and exchange charges. Any backtesting engine must model these explicitly.
*   **Sources:**
    *   *FinRobot: An Open-Source AI Agent Platform for Financial Applications (2024)*
    *   *Agentic Trading Surveys 2025/2026*

## 4. Security & Risk Management Best Practices
*   Never expose API credentials in client-side code.
*   The LLM must never have direct API execution privileges; it acts strictly as an advisory/signal layer to a deterministic rule-based execution engine.
*   Idempotency keys must be used to prevent duplicate order executions.
