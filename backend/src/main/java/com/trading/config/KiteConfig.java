package com.trading.config;

import com.zerodhatech.kiteconnect.KiteConnect;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class KiteConfig {

    @Value("${kite.api.key}")
    private String apiKey;

    @Bean
    public KiteConnect kiteConnect() {
        KiteConnect kiteConnect = new KiteConnect(apiKey);
        // Additional setup if required
        return kiteConnect;
    }
}
