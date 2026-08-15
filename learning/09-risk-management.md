# Risk Management Strategy

## What it is
The Risk Management system is the most critical component of the algorithmic trading platform. It acts as an impassable firewall between the AI strategy generator and your actual capital.

## Defense-in-Depth Architecture
Risk is managed at two distinct layers to ensure no single point of failure:

### Layer 1: Python Strategy Risk (The Brains)
When the AI Signal Aggregator proposes a trade, it first passes through the `ai_agents/risk/engine.py`. This layer ensures:
1. **Capital Conservation**: Does the strategy have enough allocated capital?
2. **Drawdown Limits**: Have we hit the `MAX_DAILY_LOSS` (e.g., 1% of total capital)? If so, trading is halted.
3. **Position Sizing**: Mathematically derives the quantity of shares based on the stop-loss distance to ensure the trade strictly risks only the permitted fraction of capital (e.g., 0.5%).
4. **Concentration Risk**: Enforces `MAX_CAPITAL_PER_POSITION` (e.g., max 35% of total capital in one trade).

### Layer 2: Java Execution Firewall (The Muscle)
Before an order is physically transmitted to the Zerodha API via `OrderExecutionService.java`, it passes a final set of absolute constraints:
1. **Protected Asset Guard**: The backend directly queries the database. If the AI is trying to `SELL` a symbol that exists in your `portfolioVersion = 1` snapshot (e.g., your long-term Mutual Funds), it throws a `SecurityException` and kills the order instantly.
2. **Idempotency**: Every signal gets a unique ID. The backend verifies this ID has never been executed before, entirely preventing "duplicate order loops" caused by network stutters or bugged AI loops.
