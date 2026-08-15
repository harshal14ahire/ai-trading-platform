# Portfolio Protection Strategy

## What it is
A defense-in-depth security mechanism ensuring the AI algorithmic trading engine never accidentally sells, liquidates, or modifies the user's pre-existing, manual investments (e.g., long-term Mutual Funds or blue-chip stock holdings).

## Why it exists
By default, broker APIs view the user's entire portfolio as a single pool of assets. If an AI agent decides that "RELIANCE" is currently overvalued, it might attempt to sell RELIANCE. If the user already held 500 shares of RELIANCE as a long-term investment, the AI would liquidate it, causing unintended tax events and portfolio disruption.

## How it works
1. **Baseline Snapshot**: Upon first startup (Stage 2), the system connects to the Kite API and downloads all current equity and mutual fund holdings.
2. **Immutability**: These holdings are saved to the `protected_holdings` database table with `portfolioVersion = 1`.
3. **The Risk Firewall**: Later, when the AI agent proposes a SELL order, the Risk Engine checks the `protected_holdings` table. If the symbol exists in that table, the Risk Engine triggers a `PROTECTED_ASSET_GUARD` rejection.

## Alternatives
- Using a completely separate Demat account for the trading bot. While theoretically safer, it is operationally complex and splits available capital. The software-level isolation (as implemented here) allows using a single account safely.
