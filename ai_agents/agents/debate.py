class DebateAgent:
    """
    Simulates a multi-agent debate (Bull vs. Bear).
    In Phase 1, it programmatically reviews the signals to identify weak assumptions.
    In production, this would use LLM pipelines for deeper reasoning.
    """
    def __init__(self):
        pass

    def evaluate(self, technical_signal: dict, regime_signal: dict, sentiment_signal: dict) -> dict:
        """
        Takes inputs from other agents and debates the validity of a potential trade.
        """
        bull_arguments = []
        bear_arguments = []

        # Bull Agent logic
        if technical_signal['trend'] == 'BULLISH':
            bull_arguments.append("Technical trend is clearly bullish (EMA 20 > EMA 50).")
        if technical_signal['rsi'] > 40:
            bull_arguments.append(f"Momentum is healthy (RSI = {technical_signal['rsi']}).")
        if regime_signal['regime'] == 'BULL':
            bull_arguments.append("Broader market regime supports long trades.")

        # Bear Agent logic
        if technical_signal['trend'] == 'BEARISH':
            bear_arguments.append("Technical trend is bearish. Buying is catching a falling knife.")
        if technical_signal['rsi'] >= 70:
            bear_arguments.append(f"Asset is technically overbought (RSI = {technical_signal['rsi']}). Prone to pullback.")
        if regime_signal['regime'] == 'BEAR':
            bear_arguments.append("Broader market is bearish. High risk of failure for long trades.")
        if regime_signal['regime'] == 'HIGH_VOLATILITY':
            bear_arguments.append("Market is highly volatile. Stop losses may be hit due to noise.")

        # Debate outcome
        debate_score = 50
        debate_score += len(bull_arguments) * 10
        debate_score -= len(bear_arguments) * 10
        
        debate_score = max(0, min(100, debate_score))

        return {
            "debate_score": debate_score,
            "bull_case": " | ".join(bull_arguments) if bull_arguments else "None",
            "bear_case": " | ".join(bear_arguments) if bear_arguments else "None"
        }
