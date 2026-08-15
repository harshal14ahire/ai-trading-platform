package com.trading.entity;

import jakarta.persistence.*;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;

@Entity
@Table(name = "protected_holdings")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class ProtectedHolding {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String exchange;

    @Column(nullable = false)
    private String tradingSymbol;

    @Column(nullable = false)
    private String isin;

    @Column(nullable = false)
    private Integer baselineQuantity;

    private Double baselineAveragePrice;

    @Column(nullable = false)
    private LocalDateTime timestamp;

    @Column(nullable = false)
    private String source; // "EQUITY" or "MUTUAL_FUND"

    @Column(nullable = false)
    private Integer portfolioVersion;
}
