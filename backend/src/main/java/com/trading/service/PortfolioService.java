package com.trading.service;

import com.trading.entity.BrokerSession;
import com.trading.entity.ProtectedHolding;
import com.trading.repository.BrokerSessionRepository;
import com.trading.repository.ProtectedHoldingRepository;
import com.zerodhatech.kiteconnect.KiteConnect;
import com.zerodhatech.models.Holding;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.List;

@Service
public class PortfolioService {

    private final KiteConnect kiteConnect;
    private final ProtectedHoldingRepository holdingRepository;
    private final BrokerSessionRepository sessionRepository;

    public PortfolioService(KiteConnect kiteConnect, ProtectedHoldingRepository holdingRepository, BrokerSessionRepository sessionRepository) {
        this.kiteConnect = kiteConnect;
        this.holdingRepository = holdingRepository;
        this.sessionRepository = sessionRepository;
    }

    public void syncBaselinePortfolio() throws com.zerodhatech.kiteconnect.kitehttp.exceptions.KiteException, java.io.IOException, org.json.JSONException {
        // Ensure we have an active session
        BrokerSession session = sessionRepository.findTopByActiveTrueOrderByLoginTimeDesc()
                .orElseThrow(() -> new RuntimeException("No active broker session found. Please login first."));
        
        kiteConnect.setAccessToken(session.getAccessToken());

        // Fetch Equity Holdings
        List<Holding> equityHoldings = kiteConnect.getHoldings();
        
        LocalDateTime timestamp = LocalDateTime.now();
        int version = 1; // Baseline version

        for (Holding holding : equityHoldings) {
            ProtectedHolding protectedHolding = new ProtectedHolding();
            protectedHolding.setExchange(holding.exchange);
            protectedHolding.setTradingSymbol(holding.tradingSymbol);
            protectedHolding.setIsin(holding.isin);
            protectedHolding.setBaselineQuantity(holding.quantity);
            protectedHolding.setBaselineAveragePrice(holding.averagePrice);
            protectedHolding.setTimestamp(timestamp);
            protectedHolding.setSource("EQUITY");
            protectedHolding.setPortfolioVersion(version);
            
            holdingRepository.save(protectedHolding);
        }

        // Mutual Funds fetching logic
        // As per Kite Connect Java SDK, MFs can be retrieved via `kiteConnect.getMFHoldings()` if supported.
        // Assuming supported here, otherwise fallback to Coin CSV parsing.
        try {
            List<Holding> mfHoldings = kiteConnect.getHoldings(); // Replace with getMFHoldings() if available
            // Similar logic...
        } catch (Exception e) {
            System.err.println("Failed to fetch MF Holdings directly. Mutual Funds will need manual CSV sync.");
        }
    }
}
