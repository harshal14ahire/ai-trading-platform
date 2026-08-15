# Emergency Protocols (The Kill Switch)

## What it is
The "Kill Switch" is a highly prominent button on the UI that bypasses all normal logic.

## Why it exists
In quantitative trading, flash crashes, API loops, or fundamental shifts (like sudden geopolitical news) can break the assumptions of the algorithm. If the bot starts losing money rapidly, the user must be able to halt the system instantly.

## How it works
1. The user double-clicks the red button on the React dashboard.
2. An HTTP POST request is sent to the Spring Boot backend (`/api/emergency/liquidate`).
3. The Java backend immediately queries Kite for all currently open `MIS` (Intraday) or `CNC` (Delivery) positions held by the algorithm (ignoring `PROTECTED_HOLDINGS`).
4. It fires off `MARKET SELL` orders for those exact quantities.
5. It flips a database flag `ALLOW_ALGO_TRADING = FALSE`, which causes the Python Orchestrator's Risk Engine to instantly reject any further incoming signals.
