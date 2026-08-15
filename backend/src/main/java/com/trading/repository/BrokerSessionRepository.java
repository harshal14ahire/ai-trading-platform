package com.trading.repository;

import com.trading.entity.BrokerSession;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface BrokerSessionRepository extends JpaRepository<BrokerSession, Long> {
    Optional<BrokerSession> findTopByActiveTrueOrderByLoginTimeDesc();
}
