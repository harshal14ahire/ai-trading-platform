# Mathematical Position Sizing

## What it is
Position Sizing answers the question: "How many shares should I buy?"

## Why it exists
Most beginner bots arbitrarily say "Buy 10 shares" or "Buy with 20% of my capital". This is mathematically disastrous because it ignores volatility. If you buy ₹5000 of a volatile stock, your risk is much higher than buying ₹5000 of a stable stock.

## How we calculate it
The Python Risk Engine calculates the exact quantity using this formula:

`Quantity = (Total Capital * Max Risk %) / (Entry Price - Stop Loss Price)`

### Example
- Total Capital: ₹13,000
- Max Risk Per Trade: 0.5% (₹65)
- AI Strategy Entry Price: ₹1,000
- AI Strategy Stop Loss: ₹980
- Stop Loss Distance: ₹20

`Quantity = ₹65 / ₹20 = 3.25 shares` (Floored to 3 shares)

If the trade hits the stop loss, the exact loss will be `3 shares * ₹20 = ₹60`. This is mathematically guaranteed to be within the allowed ₹65 limit, regardless of the stock's absolute price.
