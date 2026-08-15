"""
Transaction Cost Calculator for Indian Equity Markets (Delivery & Intraday)
As per standard 2026 pricing for retail discount brokers (e.g., Zerodha).
"""

def calculate_costs(buy_price, sell_price, quantity, is_intraday=False):
    """
    Calculates the exact transaction costs for a complete trade (buy + sell).
    
    Returns:
        dict containing breakdown of costs and net profit/loss.
    """
    turnover = (buy_price + sell_price) * quantity
    gross_pl = (sell_price - buy_price) * quantity

    # 1. Brokerage
    if is_intraday:
        # Intraday: 0.03% or Rs. 20 per executed order, whichever is lower
        buy_brokerage = min(buy_price * quantity * 0.0003, 20.0)
        sell_brokerage = min(sell_price * quantity * 0.0003, 20.0)
        total_brokerage = buy_brokerage + sell_brokerage
    else:
        # Delivery: Free for equity delivery at discount brokers
        total_brokerage = 0.0

    # 2. STT/CTT (Securities Transaction Tax)
    if is_intraday:
        # Intraday: 0.025% on the sell side
        stt = round(sell_price * quantity * 0.00025)
    else:
        # Delivery: 0.1% on buy and sell side
        stt = round(turnover * 0.001)

    # 3. Transaction Charges (NSE/BSE)
    # Approx 0.00345% on turnover
    transaction_charges = turnover * 0.0000345

    # 4. GST
    # 18% on (brokerage + transaction charges)
    gst = (total_brokerage + transaction_charges) * 0.18

    # 5. SEBI Charges
    # ₹10 per crore (0.0001%)
    sebi_charges = turnover * 0.000001

    # 6. Stamp Duty
    if is_intraday:
        # 0.003% on buy side only
        stamp_duty = buy_price * quantity * 0.00003
    else:
        # 0.015% on buy side only
        stamp_duty = buy_price * quantity * 0.00015

    total_tax_and_charges = total_brokerage + stt + transaction_charges + gst + sebi_charges + stamp_duty
    net_pl = gross_pl - total_tax_and_charges

    return {
        "turnover": turnover,
        "gross_pl": gross_pl,
        "brokerage": total_brokerage,
        "stt": stt,
        "transaction_charges": transaction_charges,
        "gst": gst,
        "sebi_charges": sebi_charges,
        "stamp_duty": stamp_duty,
        "total_charges": total_tax_and_charges,
        "net_pl": net_pl
    }

def apply_slippage(price, side, slippage_percent=0.0005): # 0.05% slippage
    """
    Applies slippage to an execution price to simulate realistic fills.
    """
    if side.upper() == 'BUY':
        return price * (1 + slippage_percent)
    elif side.upper() == 'SELL':
        return price * (1 - slippage_percent)
    return price
