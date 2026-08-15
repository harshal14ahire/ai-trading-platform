package com.trading.controller;

import com.trading.entity.BrokerSession;
import com.trading.repository.BrokerSessionRepository;
import com.zerodhatech.kiteconnect.KiteConnect;
import com.zerodhatech.models.User;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.time.LocalDateTime;

@RestController
@RequestMapping("/api/auth")
public class KiteAuthController {

    private final KiteConnect kiteConnect;
    private final BrokerSessionRepository sessionRepository;

    @Value("${kite.api.secret}")
    private String apiSecret;

    public KiteAuthController(KiteConnect kiteConnect, BrokerSessionRepository sessionRepository) {
        this.kiteConnect = kiteConnect;
        this.sessionRepository = sessionRepository;
    }

    @GetMapping("/url")
    public ResponseEntity<String> getLoginUrl() {
        return ResponseEntity.ok(kiteConnect.getLoginURL());
    }

    @GetMapping("/callback")
    public ResponseEntity<String> callback(@RequestParam("request_token") String requestToken) {
        try {
            User user = kiteConnect.generateSession(requestToken, apiSecret);
            kiteConnect.setAccessToken(user.accessToken);
            kiteConnect.setPublicToken(user.publicToken);

            BrokerSession session = new BrokerSession();
            session.setUserId(user.userId);
            session.setAccessToken(user.accessToken);
            session.setPublicToken(user.publicToken);
            session.setLoginTime(LocalDateTime.now());
            session.setActive(true);

            // Invalidate older sessions
            sessionRepository.findTopByActiveTrueOrderByLoginTimeDesc().ifPresent(oldSession -> {
                oldSession.setActive(false);
                sessionRepository.save(oldSession);
            });

            sessionRepository.save(session);
            
            return ResponseEntity.ok("Successfully authenticated. Session generated.");
        } catch (Exception e) {
            return ResponseEntity.status(500).body("Error generating session: " + e.getMessage());
        }
    }
}
