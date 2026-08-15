# Stage 1: Build
FROM maven:3.9.6-eclipse-temurin-21-alpine AS builder
# Note: Using Java 21 as fallback for 25 due to stable Docker image availability. 
# Spring Boot 4 supports Java 21+ natively.
WORKDIR /app
COPY pom.xml .
COPY src ./src
# Build skipping tests for faster local iteration
RUN mvn clean package -DskipTests

# Stage 2: Runtime
FROM eclipse-temurin:21-jre-alpine
WORKDIR /app
COPY --from=builder /app/target/*.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]
