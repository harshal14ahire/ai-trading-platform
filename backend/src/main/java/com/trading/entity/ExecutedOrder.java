package com.trading.entity;

import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;

@Document(collection = "executed_orders")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class ExecutedOrder {

    @Id
    private String id;

    private String signalId; // Unique ID from Python orchestrator

    private String kiteOrderId; // Order ID returned by Kite API

    private String symbol;

    private String action; // BUY or SELL

    private Integer quantity;

    private LocalDateTime executionTime;
}
