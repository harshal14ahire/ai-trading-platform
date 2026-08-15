package com.trading.service;

import com.trading.entity.BrokerSession;
import com.trading.entity.ExecutedOrder;
import com.trading.entity.ProtectedHolding;
import com.trading.repository.BrokerSessionRepository;
import com.trading.repository.ExecutedOrderRepository;
import com.trading.repository.ProtectedHoldingRepository;
import com.zerodhatech.kiteconnect.KiteConnect;
import com.zerodhatech.kiteconnect.kitehttp.exceptions.KiteException;
import com.zerodhatech.models.Order;
import com.zerodhatech.models.OrderParams;
import org.springframework.stereotype.Service;

import java.io.IOException;
import java.time.LocalDateTime;
import java.util.List;

@Service
public class OrderExecutionService {

    private final KiteConnect kiteConnect;
    private final ProtectedHoldingRepository holdingRepository;
    private final ExecutedOrderRepository executedOrderRepository;
    private final BrokerSessionRepository sessionRepository;

    public OrderExecutionService(KiteConnect kiteConnect, 
                                 ProtectedHoldingRepository holdingRepository, 
                                 ExecutedOrderRepository executedOrderRepository,
                                 BrokerSessionRepository sessionRepository) {
        this.kiteConnect = kiteConnect;
        this.holdingRepository = holdingRepository;
        this.executedOrderRepository = executedOrderRepository;
        this.sessionRepository = sessionRepository;
    }

    /**
     * The final firewall before placing an order on Kite.
     */
    public String executeOrder(String signalId, String symbol, String action, int quantity, String transactionType) throws Exception {
        
        // 1. Idempotency Check
        if (executedOrderRepository.existsBySignalId(signalId)) {
            throw new IllegalStateException("Duplicate Order Detected. Signal ID " + signalId + " has already been executed.");
        }

        // 2. Protected Asset Guard
        if (action.equalsIgnoreCase("SELL")) {
            List<ProtectedHolding> protectedHoldings = holdingRepository.findByTradingSymbol(symbol);
            if (!protectedHoldings.isEmpty()) {
                throw new SecurityException("PROTECTED_ASSET_GUARD: Rejected attempt to sell protected baseline holding: " + symbol);
            }
        }

        // 3. Ensure active session
        BrokerSession session = sessionRepository.findTopByActiveTrueOrderByLoginTimeDesc()
                .orElseThrow(() -> new RuntimeException("No active broker session found."));
        kiteConnect.setAccessToken(session.getAccessToken());

        // 4. Execute to Kite
        OrderParams orderParams = new OrderParams();
        orderParams.exchange = "NSE";
        orderParams.tradingsymbol = symbol;
        orderParams.transactionType = transactionType; // e.g., "BUY" or "SELL"
        orderParams.quantity = quantity;
        orderParams.orderType = "MARKET";
        orderParams.validity = "DAY";
        orderParams.product = "CNC"; // Delivery (Use "MIS" for intraday)

        String kiteOrderId = "SIMULATED_ORDER_ID_FOR_PAPER_MODE";

        try {
            // Uncomment to place live orders
            // Order order = kiteConnect.placeOrder(orderParams, "regular");
            // kiteOrderId = order.orderId;
            System.out.println("Executing " + action + " for " + quantity + " " + symbol);
            
        } catch (Exception e) {
            // Log and rethrow Kite exceptions
            throw new RuntimeException("Kite API Error: " + e.getMessage());
        }

        // 5. Save Idempotency Record
        ExecutedOrder record = new ExecutedOrder();
        record.setSignalId(signalId);
        record.setKiteOrderId(kiteOrderId);
        record.setSymbol(symbol);
        record.setAction(action);
        record.setQuantity(quantity);
        record.setExecutionTime(LocalDateTime.now());
        
        executedOrderRepository.save(record);

        return kiteOrderId;
    }
}
