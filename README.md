# AI Autonomous Trading Platform

A massive, defense-in-depth, fully autonomous algorithmic trading bot designed for the Indian Stock Market (NSE) using Zerodha's API.

## Architecture

```mermaid
graph TD
    subgraph Frontend [React UI - Hosted on GitHub Pages]
        UI[Glassmorphism Dashboard]
        UI --> |HTTP POST /liquidate| API
        UI --> |HTTP GET /portfolio| API
    end

    subgraph Data Layer [Dockerized]
        Redis[(Redis)]
        Mongo[(MongoDB)]
    end

    subgraph Python AI Daemon [Dockerized - Always On]
        TICKER[ticker.py] --> |Publish| Redis
        ORCH[orchestrator.py] --> |Subscribe| Redis
        
        subgraph Multi-Agent Engine
            TA[Technical Agent]
            RA[Regime Agent]
            DA[Debate Agent]
            AGG[Signal Aggregator]
        end
        
        ORCH --> TA
        ORCH --> RA
        TA & RA --> DA
        DA --> AGG
        AGG --> |Score > 75| RISK[Risk Engine]
    end

    subgraph Java Spring Boot Backend [Hosted on Koyeb/Render]
        API[OrderExecutionController]
        SERVICE[OrderExecutionService]
        GUARD[ProtectedAssetGuard]
        
        API --> SERVICE
        SERVICE --> |Check Idempotency| Mongo
        SERVICE --> GUARD
        GUARD --> |Check Allowed| Mongo
    end

    RISK --> |HTTP POST /execute| API
    SERVICE --> |Order Allowed| ZERODHA(Zerodha Kite API)
```

## Features
- **Deterministic Multi-Agent AI**: Uses Technical and Regime models to debate trades. No LLM hallucination.
- **Risk Firewall**: Mathematical position sizing enforcing max `0.5%` risk per trade.
- **Protected Asset Guard**: The Java backend inherently rejects any sell signals attempting to touch your baseline long-term mutual funds or core equities.
- **Event-Driven**: The system subscribes to live Redis ticks, converting them into 1-minute actionable candles.

## Getting Started

See `learning/19-local-testing-guide.md` to spin up the entire 5-container architecture locally using Docker Compose!
