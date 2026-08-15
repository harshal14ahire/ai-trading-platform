# Implementation Plan & Staged Rollout

## 1. Development Phases
The project will be built in stages to ensure maximum safety and reliability before any live order is placed.

### Stage 1: Core Architecture & Setup
- Project directory setup and repository initialization.
- Documentation scaffolding (`/learning` folder).
- `PAPER_MODE=true` baseline enforcement.

### Stage 2: Kite Authentication & Read-Only Portfolio
- Integrate Kite Connect login flow in the backend.
- Read mutual fund and equity holdings.
- Define and store the immutable `BASELINE_PORTFOLIO_SNAPSHOT`.

### Stage 3: Market Data & Backtesting Engine
- Implement WebSocket client for live data.
- Build the backtesting engine supporting slippage, costs, and realistic fills.

### Stage 4: AI Agents & Strategy Engine
- Develop Technical, Sentiment, and Regime agents.
- Implement the Bull/Bear debate logic.
- Create the deterministic Signal Aggregator.

### Stage 5: Risk Engine & Safety
- Implement the `PROTECTED_ASSET_GUARD`.
- Implement Position Sizing logic.
- Implement Duplicate Order Protection.

### Stage 6: Paper Trading
- Execute signals against live data but route to a simulated ledger.
- Dashboard visualizes simulated P&L.

### Stage 7: Small-Capital Live Execution
- Manual Human Approval mode for all generated orders.
- Only run on a fractional segment of the ₹13,000 strategy capital.

## 2. Learning Documentation
The `/learning` directory will contain markdown files tracking the implementation and technical decisions:
- `01-project-overview.md`
- `02-indian-algo-trading.md`
- `03-kite-connect.md`
- `04-authentication.md`
- ...and subsequent files as features are built.

## 3. Success Criteria
- Existing mutual funds and stocks are 100% protected.
- AI agents provide structured outputs that do NOT bypass the Risk Engine.
- The system achieves positive expected value in backtesting before live deployment.
- The Kill Switch functions correctly.
