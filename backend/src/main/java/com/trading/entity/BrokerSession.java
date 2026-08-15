package com.trading.entity;

import jakarta.persistence.*;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;

@Entity
@Table(name = "broker_sessions")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class BrokerSession {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true)
    private String userId;

    @Column(nullable = false, length = 500)
    private String accessToken;

    @Column(nullable = false)
    private LocalDateTime loginTime;

    private String publicToken;
    
    private boolean active = true;
}
