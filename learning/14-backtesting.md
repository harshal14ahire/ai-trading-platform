# Backtesting Realities

## What it is
Backtesting is the process of applying a trading strategy to historical data to see how it would have performed.

## The Pitfalls (Why we built a custom engine)
Standard backtesting libraries (like Backtrader) often paint an overly optimistic picture. We built a custom engine to avoid the following issues:

1. **Look-Ahead Bias**: The AI must not accidentally see tomorrow's price when making today's decision. Our `BacktestEngine.run()` method iterates row by row, strictly simulating the flow of time.
2. **Ignored Slippage**: In reality, if the price crosses your buy point, you will get filled slightly higher due to market movement and latency. Our `apply_slippage()` function mathematically enforces this penalty.
3. **Inaccurate Costs**: India has complex transaction costs (Brokerage, STT, Exchange charges, GST, SEBI charges, Stamp duty). Many bots assume a flat 0.1% fee. Our `calculate_costs()` function calculates these down to the rupee based on whether the trade is Delivery or Intraday, heavily impacting the net P&L on a ₹13,000 capital base.

## Rule of Thumb
If a backtest does not explicitly deduct slippage and STT/Brokerage, its results are completely invalid for real-world deployment.
