import pandas as pd
import pandas_ta as ta

class TechnicalAgent:
    """
    Computes technical indicators and returns a structured, deterministic signal score.
    """
    def __init__(self):
        pass

    def analyze(self, symbol: str, df: pd.DataFrame) -> dict:
        """
        Expects a DataFrame with 'Open', 'High', 'Low', 'Close', 'Volume'.
        """
        if len(df) < 50:
            return {"symbol": symbol, "trend": "NEUTRAL", "momentum": 0, "score": 50, "reason": "Insufficient data"}

        # Calculate indicators
        df.ta.ema(length=20, append=True)
        df.ta.ema(length=50, append=True)
        df.ta.rsi(length=14, append=True)
        df.ta.adx(length=14, append=True)
        
        latest = df.iloc[-1]
        
        ema_20 = latest['EMA_20']
        ema_50 = latest['EMA_50']
        rsi = latest['RSI_14']
        adx = latest.get('ADX_14', 0)

        score = 50
        trend = "NEUTRAL"
        
        # Trend Analysis
        if ema_20 > ema_50:
            trend = "BULLISH"
            score += 15
        elif ema_20 < ema_50:
            trend = "BEARISH"
            score -= 15

        # Momentum / Overbought / Oversold
        if 40 < rsi < 70:
            score += 10 # Healthy momentum
        elif rsi >= 70:
            score -= 10 # Overbought, penalty for new long entries
        elif rsi <= 30:
            score += 10 # Oversold, potential bounce

        # Trend Strength
        if adx > 25:
            # Strong trend, amplify score
            if trend == "BULLISH":
                score += 10
            elif trend == "BEARISH":
                score -= 10

        # Normalize score between 0 and 100
        score = max(0, min(100, score))

        return {
            "symbol": symbol,
            "trend": trend,
            "rsi": round(rsi, 2),
            "adx": round(adx, 2),
            "score": score,
            "reason": f"Trend: {trend}, RSI: {rsi:.2f}, ADX: {adx:.2f}"
        }
