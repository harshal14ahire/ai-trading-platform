# Multi-Agent Architecture in Algo Trading

## What it is
Instead of a single monolithic script or a single LLM deciding "BUY" or "SELL", the system is broken into distinct, specialized "Agents".

## Why it exists
LLMs are highly prone to "hallucination" and emotional bias (if prompted with bullish news, they might ignore terrible technicals). By isolating roles, we force a systematic review process similar to a professional quantitative hedge fund.

## How it works in our Platform
1. **Technical Agent**: Only looks at math and price history. Blind to the news.
2. **Sentiment Agent**: Only looks at news and fundamentals. Blind to the chart.
3. **Regime Agent**: Only looks at the macro benchmark (NIFTY 50).
4. **Debate Agent**: Pits the Bull arguments against the Bear arguments.
5. **Signal Aggregator**: The final, deterministic judge. It takes the output of all agents, applies a fixed mathematical weight (e.g., Technical is worth 40%), and only generates a `TRADE_CANDIDATE` if the total score exceeds 75/100.

This architecture ensures the AI acts as a sophisticated data-processing pipeline, while the final execution decision remains strictly mathematically bounded.
