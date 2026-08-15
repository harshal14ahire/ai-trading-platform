package com.trading.repository;

import com.trading.entity.ProtectedHolding;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface ProtectedHoldingRepository extends MongoRepository<ProtectedHolding, String> {
    List<ProtectedHolding> findByTradingSymbol(String tradingSymbol);
}
