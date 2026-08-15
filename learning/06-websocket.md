# WebSocket Architecture

## What it is
A WebSocket is a persistent, bidirectional communication channel over a single TCP connection.

## Why it exists
Standard HTTP requests are unidirectional (client requests, server responds) and have overhead (headers, handshakes). WebSockets allow the Zerodha server to "push" price updates to our application the exact millisecond they happen without us needing to ask.

## Integration in our Platform
We use a **Pub/Sub pattern** with Redis.
- **Publisher**: Our `ticker.py` script receives the WebSocket data.
- **Message Broker**: Redis.
- **Subscribers**: The Technical Agent, Risk Agent, and Market Regime Agent.

This ensures that if the AI Agent takes 100ms to process a signal, it doesn't block the WebSocket thread from receiving the next price tick.
