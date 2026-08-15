package com.trading.repository;

import com.trading.entity.ExecutedOrder;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface ExecutedOrderRepository extends JpaRepository<ExecutedOrder, Long> {
    boolean existsBySignalId(String signalId);
}
