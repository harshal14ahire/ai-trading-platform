package com.trading.repository;

import com.trading.entity.ProtectedHolding;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface ProtectedHoldingRepository extends JpaRepository<ProtectedHolding, Long> {
    List<ProtectedHolding> findByTradingSymbol(String tradingSymbol);
}
