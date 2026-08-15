import pandas as pd
import pandas_ta as ta

class RegimeAgent:
    """
    Determines the broader market regime based on a benchmark index (e.g., NIFTY 50).
    """
    def __init__(self):
        pass

    def determine_regime(self, benchmark_df: pd.DataFrame) -> dict:
        """
        Analyzes the benchmark index to return BULL, BEAR, SIDEWAYS, or HIGH_VOLATILITY.
        """
        if len(benchmark_df) < 50:
            return {"regime": "SIDEWAYS", "confidence": 0.5, "reason": "Insufficient benchmark data"}

        # Use SMA 50 and ATR to define regime
        benchmark_df.ta.sma(length=20, append=True)
        benchmark_df.ta.sma(length=50, append=True)
        benchmark_df.ta.atr(length=14, append=True)

        latest = benchmark_df.iloc[-1]
        
        sma_20 = latest['SMA_20']
        sma_50 = latest['SMA_50']
        close = latest['Close']
        atr = latest['ATRr_14']
        
        # Volatility check: if ATR is significantly high relative to price (e.g., > 2% daily)
        volatility_ratio = atr / close
        
        regime = "SIDEWAYS"
        confidence = 0.5

        if volatility_ratio > 0.02:
            regime = "HIGH_VOLATILITY"
            confidence = 0.8
        elif close > sma_20 and sma_20 > sma_50:
            regime = "BULL"
            confidence = 0.8
        elif close < sma_20 and sma_20 < sma_50:
            regime = "BEAR"
            confidence = 0.8

        return {
            "regime": regime,
            "confidence": confidence,
            "volatility_ratio": round(volatility_ratio, 4)
        }
