# Market Regimes

## What it is
The Market Regime Agent analyzes a broad benchmark index (e.g., NIFTY 50) rather than the individual stock to determine the overall market "weather".

## Why it exists
A strategy that performs brilliantly in a Bull market will likely suffer heavy drawdowns in a Bear or High-Volatility regime. The system uses the Market Regime Agent's output to scale position sizes or completely halt trading (`ALLOW_TRADING = FALSE`) if conditions are unfavorable. 

## The Four Regimes
1. **BULL**: Price > EMA 20 > EMA 50. High confidence for long trades.
2. **BEAR**: Price < EMA 20 < EMA 50. Long trades are penalized in the aggregator.
3. **SIDEWAYS**: Choppy action. Mean-reversion strategies favored.
4. **HIGH_VOLATILITY**: Detected via ATR. Stop-losses are widened or trading is halted to protect capital from whipsaws.
