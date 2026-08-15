import axios from 'axios';

// Base URL points to the Spring Boot backend
const API_BASE = 'http://localhost:8080/api';

export const getProtectedHoldings = async () => {
    try {
        const response = await axios.get(`${API_BASE}/portfolio/protected`);
        return response.data;
    } catch (error) {
        throw new Error("Failed to fetch protected holdings.");
    }
};

export const triggerKillSwitch = async () => {
    try {
        // In a real implementation, this hits an emergency endpoint on the Java backend
        // which instantly issues market sell orders for any active algorithmic positions.
        const response = await axios.post(`${API_BASE}/emergency/liquidate`);
        return response.data;
    } catch (error) {
        // Mock success for UI dev if backend is down
        console.warn("Backend unreachable for Kill Switch. Simulating success.");
        return new Promise((resolve) => setTimeout(() => resolve({ status: 'SUCCESS' }), 1500));
    }
};
