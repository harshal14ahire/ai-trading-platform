# Market Data Ingestion

## What it is
The Market Data service is responsible for ingesting live price updates (ticks) from the exchange and distributing them to the rest of the application.

## Why it exists
Algorithmic trading requires real-time data. Rather than polling REST APIs (which violates rate limits and is slow), we subscribe to a continuous stream of data. We isolate this into a separate Python service (`ticker.py`) to decouple data fetching from data processing.

## How it works
1. We initialize `KiteTicker` with our `api_key` and `access_token`.
2. We connect to the WebSocket.
3. Upon receiving ticks in the `on_ticks` callback, we immediately serialize the data and publish it to a **Redis channel** (e.g., `market_data:ticks:738561`).
4. Other services (like our AI orchestrator) subscribe to this Redis channel, allowing multiple agents to process the data simultaneously without maintaining their own WebSocket connections.
