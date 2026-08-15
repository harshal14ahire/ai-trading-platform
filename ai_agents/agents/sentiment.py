class SentimentAgent:
    """
    Parses unstructured news, earnings, and sector developments.
    For Phase 1 (Testing), this returns a neutral score to prevent API costs.
    """
    def __init__(self):
        pass

    def analyze(self, symbol: str) -> dict:
        """
        In production, this would query a News API, pass headlines to an LLM,
        and output a sentiment score between 0 and 100.
        """
        
        # Placeholder / Mock
        return {
            "symbol": symbol,
            "sentiment": "NEUTRAL",
            "score": 50,
            "reason": "Sentiment module running in neutral testing mode."
        }
