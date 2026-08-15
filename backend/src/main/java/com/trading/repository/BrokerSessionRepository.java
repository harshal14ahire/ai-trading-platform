package com.trading.repository;

import com.trading.entity.BrokerSession;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface BrokerSessionRepository extends MongoRepository<BrokerSession, String> {
    Optional<BrokerSession> findTopByActiveTrueOrderByLoginTimeDesc();
}
