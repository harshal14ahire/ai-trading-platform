package com.trading.entity;

import jakarta.persistence.*;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;

@Entity
@Table(name = "executed_orders")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class ExecutedOrder {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true)
    private String signalId; // Unique ID from Python orchestrator

    @Column(nullable = false)
    private String kiteOrderId; // Order ID returned by Kite API

    @Column(nullable = false)
    private String symbol;

    @Column(nullable = false)
    private String action; // BUY or SELL

    @Column(nullable = false)
    private Integer quantity;

    @Column(nullable = false)
    private LocalDateTime executionTime;
}
