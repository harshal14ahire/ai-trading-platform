package com.trading.repository;

import com.trading.entity.ExecutedOrder;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface ExecutedOrderRepository extends MongoRepository<ExecutedOrder, String> {
    boolean existsBySignalId(String signalId);
}
