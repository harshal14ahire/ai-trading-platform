class SignalAggregator:
    """
    Deterministically aggregates signals from all agents into a final trade score.
    """
    def __init__(self, min_signal_score=75):
        self.min_signal_score = min_signal_score
        
        # Define deterministic weights
        self.weights = {
            "technical": 0.40,
            "regime": 0.20,
            "sentiment": 0.10,
            "debate": 0.30
        }

    def aggregate(self, symbol: str, tech: dict, regime: dict, sentiment: dict, debate: dict) -> dict:
        
        # Calculate weighted score
        final_score = (
            (tech['score'] * self.weights['technical']) +
            # Regime doesn't have a 0-100 score natively yet, so we map it
            (self._regime_to_score(regime['regime']) * self.weights['regime']) +
            (sentiment['score'] * self.weights['sentiment']) +
            (debate['debate_score'] * self.weights['debate'])
        )

        final_score = round(final_score, 2)
        
        action = "HOLD"
        if final_score >= self.min_signal_score:
            action = "BUY"
        elif final_score <= (100 - self.min_signal_score):
            action = "SELL" # Short, though NO_SHORT_SELLING config might block this in the Risk Engine

        return {
            "symbol": symbol,
            "action": action,
            "final_score": final_score,
            "breakdown": {
                "technical": tech['score'],
                "regime_mapped": self._regime_to_score(regime['regime']),
                "sentiment": sentiment['score'],
                "debate": debate['debate_score']
            },
            "bull_case": debate['bull_case'],
            "bear_case": debate['bear_case']
        }

    def _regime_to_score(self, regime: str) -> int:
        mapping = {
            "BULL": 85,
            "BEAR": 15,
            "SIDEWAYS": 50,
            "HIGH_VOLATILITY": 40
        }
        return mapping.get(regime, 50)
