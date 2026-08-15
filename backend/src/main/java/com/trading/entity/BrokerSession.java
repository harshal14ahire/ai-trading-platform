package com.trading.entity;

import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;

@Document(collection = "broker_sessions")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class BrokerSession {

    @Id
    private String id;

    private String userId;

    private String accessToken;

    private LocalDateTime loginTime;

    private String publicToken;
    
    private boolean active = true;
}
