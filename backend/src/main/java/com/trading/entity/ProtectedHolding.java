package com.trading.entity;

import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;
import java.time.LocalDateTime;

@Document(collection = "protected_holdings")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class ProtectedHolding {

    @Id
    private String id;

    private String exchange;

    private String tradingSymbol;

    private String isin;

    private Integer baselineQuantity;

    private Double baselineAveragePrice;

    private LocalDateTime timestamp;

    private String source; // "EQUITY" or "MUTUAL_FUND"

    private Integer portfolioVersion;
}
