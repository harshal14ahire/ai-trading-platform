import os
import math
from dotenv import load_dotenv

load_dotenv(dotenv_path='../../.env.example')

class RiskEngine:
    """
    The deterministic Risk Engine for the Python AI strategy layer.
    Vetoes trades and mathematically bounds position sizing.
    """
    def __init__(self):
        # Load risk parameters
        self.initial_capital = float(os.getenv("INITIAL_TRADING_CAPITAL", 13000))
        self.max_risk_per_trade = float(os.getenv("MAX_RISK_PER_TRADE", 0.005)) # 0.5% default
        self.max_capital_per_position = 0.35 # Hard limit: Never put more than 35% of capital into a single trade
        
        self.current_capital = self.initial_capital
        self.daily_realized_loss = 0.0
        self.max_daily_loss = float(os.getenv("MAX_DAILY_LOSS", 0.01)) # 1% default

    def evaluate_signal(self, signal: dict, current_price: float, stop_loss: float) -> dict:
        """
        Evaluates a TRADE_CANDIDATE from the Signal Aggregator.
        Calculates position size and enforces capital constraints.
        """
        if signal['action'] != 'BUY':
            return {"status": "REJECTED", "reason": "Only BUY signals are currently supported."}

        # 1. Global Safety Check
        if self.daily_realized_loss >= (self.initial_capital * self.max_daily_loss):
            return {"status": "REJECTED", "reason": "MAX_DAILY_LOSS limit reached. Trading halted."}

        # 2. Stop Loss Distance
        sl_distance = current_price - stop_loss
        if sl_distance <= 0:
            return {"status": "REJECTED", "reason": "Invalid Stop Loss. Must be below current price for a BUY."}

        # 3. Position Sizing based on Risk
        risk_amount = self.current_capital * self.max_risk_per_trade
        raw_quantity = risk_amount / sl_distance
        quantity = math.floor(raw_quantity)

        if quantity <= 0:
            return {"status": "REJECTED", "reason": f"Risk amount (₹{risk_amount:.2f}) too small for SL distance (₹{sl_distance:.2f}) to buy 1 share."}

        # 4. Maximum Capital Per Position Constraint
        required_capital = quantity * current_price
        max_allowed_capital = self.initial_capital * self.max_capital_per_position

        if required_capital > max_allowed_capital:
            # Scale down the quantity to fit within the max capital constraint
            quantity = math.floor(max_allowed_capital / current_price)
            required_capital = quantity * current_price
            
            if quantity <= 0:
                 return {"status": "REJECTED", "reason": "Price too high. Exceeds MAX_CAPITAL_PER_POSITION limit."}

        # 5. Check if we actually have the available cash
        if required_capital > self.current_capital:
             return {"status": "REJECTED", "reason": f"Insufficient strategy capital. Required: ₹{required_capital:.2f}, Available: ₹{self.current_capital:.2f}"}

        # If all checks pass
        return {
            "status": "APPROVED",
            "quantity": quantity,
            "required_capital": round(required_capital, 2),
            "risk_amount": round(quantity * sl_distance, 2),
            "reason": f"Risk rules passed. Sized for max {self.max_risk_per_trade*100}% risk."
        }
