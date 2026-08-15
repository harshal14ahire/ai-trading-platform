# Technical Strategies Overview

## What it is
The Technical Agent is the quantitative core of the AI system. Instead of asking an LLM "should I buy based on this chart?", we deterministically compute mathematical indicators (EMA, RSI, ADX) and map them to a 0-100 score.

## Why it exists
LLMs are notoriously bad at precise math and time-series analysis natively. By using `pandas-ta` to compute the actual mathematical truths, we provide the LLM (and our aggregator) with hard facts rather than relying on its internal hallucination of a chart.

## Indicators Used
1. **EMA 20 & 50**: Determines the primary trend (Bullish if 20 > 50).
2. **RSI (14)**: Measures momentum. Protects the bot from buying when heavily overbought (>70).
3. **ADX (14)**: Measures trend strength. Amplifies the score if a strong trend is present (>25).
