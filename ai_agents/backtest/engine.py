import pandas as pd
from typing import Callable, List, Dict
from .costs import calculate_costs, apply_slippage

class BacktestEngine:
    def __init__(self, initial_capital: float = 13000.0, is_intraday: bool = False):
        self.initial_capital = initial_capital
        self.current_capital = initial_capital
        self.is_intraday = is_intraday
        self.positions = {}
        self.trade_journal = []

    def run(self, data: pd.DataFrame, strategy_func: Callable):
        """
        Runs the backtest sequentially row by row to strictly prevent look-ahead bias.
        `strategy_func` should accept (current_row, positions) and return a signal.
        """
        print(f"Starting backtest with capital: ₹{self.initial_capital}")
        
        for i in range(len(data)):
            current_row = data.iloc[i]
            
            # 1. Update Open Positions (e.g., check stop losses or targets)
            self._update_positions(current_row)

            # 2. Generate Signal
            signal = strategy_func(current_row, self.positions)

            # 3. Execute Signal
            if signal:
                self._execute_signal(signal, current_row)

        # Close all positions at end of backtest
        self._close_all_positions(data.iloc[-1])
        
        self._print_summary()

    def _update_positions(self, current_row):
        # Simplified: A real engine checks SL/TP against High/Low here.
        pass

    def _execute_signal(self, signal: dict, current_row):
        symbol = signal.get('symbol')
        action = signal.get('action') # 'BUY' or 'SELL'
        qty = signal.get('quantity')
        
        # Get raw execution price and apply slippage
        raw_price = current_row['Close']
        execution_price = apply_slippage(raw_price, action)

        if action == 'BUY' and symbol not in self.positions:
            cost = execution_price * qty
            if self.current_capital >= cost:
                self.positions[symbol] = {
                    'entry_price': execution_price,
                    'quantity': qty,
                    'entry_time': current_row.name
                }
                self.current_capital -= cost
                
        elif action == 'SELL' and symbol in self.positions:
            pos = self.positions.pop(symbol)
            
            # Calculate P&L and exact transaction costs
            costs_breakdown = calculate_costs(
                buy_price=pos['entry_price'], 
                sell_price=execution_price, 
                quantity=pos['quantity'],
                is_intraday=self.is_intraday
            )
            
            # Update capital with returned capital + net profit
            self.current_capital += (pos['entry_price'] * pos['quantity']) + costs_breakdown['net_pl']
            
            # Record trade
            self.trade_journal.append({
                'symbol': symbol,
                'entry_time': pos['entry_time'],
                'exit_time': current_row.name,
                'entry_price': pos['entry_price'],
                'exit_price': execution_price,
                'quantity': pos['quantity'],
                'net_pl': costs_breakdown['net_pl'],
                'total_charges': costs_breakdown['total_charges']
            })

    def _close_all_positions(self, current_row):
        for symbol in list(self.positions.keys()):
            self._execute_signal({'symbol': symbol, 'action': 'SELL', 'quantity': self.positions[symbol]['quantity']}, current_row)

    def _print_summary(self):
        total_trades = len(self.trade_journal)
        winning_trades = sum(1 for t in self.trade_journal if t['net_pl'] > 0)
        total_profit = sum(t['net_pl'] for t in self.trade_journal)
        total_costs = sum(t['total_charges'] for t in self.trade_journal)
        
        print("\n--- Backtest Summary ---")
        print(f"Total Trades: {total_trades}")
        print(f"Win Rate: {(winning_trades/total_trades)*100:.2f}%" if total_trades > 0 else "Win Rate: N/A")
        print(f"Total Transaction Costs & Slippage: ₹{total_costs:.2f}")
        print(f"Net P&L: ₹{total_profit:.2f}")
        print(f"Final Capital: ₹{self.current_capital:.2f}")

# Example Usage:
# if __name__ == "__main__":
#     engine = BacktestEngine(initial_capital=13000)
#     engine.run(historical_data_df, my_strategy)
