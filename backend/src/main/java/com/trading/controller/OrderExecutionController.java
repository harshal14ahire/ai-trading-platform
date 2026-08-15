package com.trading.controller;

import com.trading.service.OrderExecutionService;
import lombok.Data;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/internal/execute")
public class OrderExecutionController {

    private final OrderExecutionService executionService;

    public OrderExecutionController(OrderExecutionService executionService) {
        this.executionService = executionService;
    }

    @PostMapping
    public ResponseEntity<?> executeOrder(@RequestBody ExecutionRequest request) {
        try {
            // Note: In production, this endpoint must be secured (e.g., via internal network policy or API key)
            // to ensure only the Python Orchestrator can call it.
            String kiteOrderId = executionService.executeOrder(
                    request.getSignalId(),
                    request.getSymbol(),
                    request.getAction(),
                    request.getQuantity(),
                    request.getTransactionType()
            );
            return ResponseEntity.ok(new ExecutionResponse("SUCCESS", kiteOrderId, "Order executed successfully."));
        } catch (SecurityException e) {
            return ResponseEntity.status(403).body(new ExecutionResponse("REJECTED", null, e.getMessage()));
        } catch (IllegalStateException e) {
             return ResponseEntity.status(409).body(new ExecutionResponse("DUPLICATE", null, e.getMessage()));
        } catch (Exception e) {
            return ResponseEntity.status(500).body(new ExecutionResponse("ERROR", null, e.getMessage()));
        }
    }

    @Data
    static class ExecutionRequest {
        private String signalId;
        private String symbol;
        private String action;
        private int quantity;
        private String transactionType; // e.g., "BUY" or "SELL"
    }

    @Data
    static class ExecutionResponse {
        private String status;
        private String orderId;
        private String message;

        public ExecutionResponse(String status, String orderId, String message) {
            this.status = status;
            this.orderId = orderId;
            this.message = message;
        }
    }
}
