import os
import json
import uuid
import time
import redis
import requests
import pandas as pd
from dotenv import load_dotenv

# Import our AI Agents and Risk Engine
from agents.technical import TechnicalAgent
from agents.regime import RegimeAgent
from agents.sentiment import SentimentAgent
from agents.debate import DebateAgent
from strategy.aggregator import SignalAggregator
from risk.engine import RiskEngine

load_dotenv(dotenv_path='../../.env.example')

class Orchestrator:
    def __init__(self):
        # Configuration
        self.redis_host = os.getenv("REDIS_HOST", "localhost")
        self.redis_port = int(os.getenv("REDIS_PORT", 6379))
        self.java_backend_url = os.getenv("JAVA_BACKEND_URL", "http://localhost:8080/api/internal/execute")
        
        self.redis_client = redis.Redis(host=self.redis_host, port=self.redis_port, decode_responses=True)
        self.pubsub = self.redis_client.pubsub()
        self.pubsub.psubscribe("market_data:ticks:*")
        
        # Initialize AI Agents
        self.technical = TechnicalAgent()
        self.regime = RegimeAgent()
        self.sentiment = SentimentAgent()
        self.debate = DebateAgent()
        self.aggregator = SignalAggregator(min_signal_score=75)
        self.risk = RiskEngine()

        # Local storage for mock DataFrame building (in production, fetch historical from DB/Kite)
        self.mock_history = self._generate_mock_history()

    def run(self):
        print("Starting Trading Orchestrator Daemon...")
        print("Listening for ticks on Redis...")
        
        last_eval_time = time.time()
        
        try:
            for message in self.pubsub.listen():
                if message['type'] == 'pmessage':
                    # Parse incoming tick
                    tick_data = json.loads(message['data'])
                    instrument_token = tick_data.get('instrument_token')
                    last_price = tick_data.get('last_price')
                    
                    # Accumulate ticks... (Logic omitted for brevity. We assume we build a 1-minute candle.)
                    
                    # Orchestrator triggers AI evaluation every 60 seconds (1-minute candle close)
                    current_time = time.time()
                    if current_time - last_eval_time >= 60:
                        print(f"\n--- 1-Minute Candle Closed. Triggering AI Pipeline for {instrument_token} ---")
                        self._trigger_ai_pipeline("RELIANCE", last_price) # Hardcoded symbol for example
                        last_eval_time = current_time

        except KeyboardInterrupt:
            print("Orchestrator shutting down.")

    def _trigger_ai_pipeline(self, symbol: str, current_price: float):
        # 1. Gather Data (Mocked for this example)
        df = self.mock_history.copy()
        
        # 2. Run Agents independently
        tech_signal = self.technical.analyze(symbol, df)
        regime_signal = self.regime.determine_regime(df) # Using same DF as benchmark for simplicity
        sent_signal = self.sentiment.analyze(symbol)
        
        # 3. Debate
        debate_outcome = self.debate.evaluate(tech_signal, regime_signal, sent_signal)
        
        # 4. Aggregate
        final_signal = self.aggregator.aggregate(symbol, tech_signal, regime_signal, sent_signal, debate_outcome)
        print(f"Signal Aggregator Result: {final_signal['action']} (Score: {final_signal['final_score']})")

        # 5. Check Threshold
        if final_signal['action'] == 'BUY':
            # 6. Risk Engine Evaluation
            # Mock stop loss 2% below current price
            stop_loss = current_price * 0.98 
            
            risk_clearance = self.risk.evaluate_signal(final_signal, current_price, stop_loss)
            print(f"Risk Engine Status: {risk_clearance['status']}")
            
            if risk_clearance['status'] == 'APPROVED':
                # 7. Execute!
                self._execute_trade(symbol, "BUY", risk_clearance['quantity'])

    def _execute_trade(self, symbol: str, action: str, quantity: int):
        signal_id = str(uuid.uuid4())
        
        payload = {
            "signalId": signal_id,
            "symbol": symbol,
            "action": action,
            "quantity": quantity,
            "transactionType": action # BUY or SELL
        }
        
        print(f"Sending Execution Request to Java Backend: {payload}")
        try:
            response = requests.post(self.java_backend_url, json=payload)
            if response.status_code == 200:
                print(f"SUCCESS: {response.json()}")
            else:
                print(f"EXECUTION FAILED ({response.status_code}): {response.text}")
        except Exception as e:
            print(f"Connection to Java backend failed: {e}")

    def _generate_mock_history(self):
        """Generates 50 rows of dummy data for the pandas-ta indicators."""
        dates = pd.date_range(end=pd.Timestamp.now(), periods=100, freq='1min')
        data = {
            'Open': [1000 + i for i in range(100)],
            'High': [1005 + i for i in range(100)],
            'Low': [995 + i for i in range(100)],
            'Close': [1002 + i for i in range(100)],
            'Volume': [1000 for _ in range(100)]
        }
        df = pd.DataFrame(data, index=dates)
        return df

if __name__ == "__main__":
    orchestrator = Orchestrator()
    orchestrator.run()
