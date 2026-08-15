# Event-Driven Orchestration

## What it is
The Orchestrator (`orchestrator.py`) is the central daemon (background process) that runs the algorithmic trading bot. It ties the Python AI logic to the Java Execution logic.

## Why it exists
We need a way to trigger the AI analysis. We could run the AI script on a CRON job every 1 minute, but that causes latency and forces us to reconnect to the database and APIs constantly. 

By using an Event-Driven Architecture (via Redis Pub/Sub), the Orchestrator sits silently in memory. The millisecond the `ticker.py` script receives a market data tick from Zerodha, it publishes it to Redis. The Orchestrator receives this "event" instantly.

## The Execution Pipeline
Every minute (or whenever a candle closes), the Orchestrator runs the pipeline:
1. `Tick` -> `Candle`
2. `Candle` -> `TechnicalAgent` & `RegimeAgent`
3. `Agents` -> `SignalAggregator`
4. `SignalAggregator` (if >75) -> `RiskEngine`
5. `RiskEngine` (if Approved) -> `Java Execution Controller` via REST API.

This completely automates the flow of data from the NSE exchange all the way to a secure, risk-assessed order placement.
