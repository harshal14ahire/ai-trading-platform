# Docker Orchestration

## What it is
Docker Compose allows us to define and run multi-container applications. With a single configuration file (`docker-compose.yml`), we configure our application's services (Database, Cache, API, AI, UI).

## Why it exists
Without Docker, running this platform would require you to manually install PostgreSQL, Redis, Java 21+, Python 3.11+, and Node 20+ on your machine. You would then need to open 5 separate terminal windows and run start commands for each.

Docker guarantees that the code runs exactly the same way on your laptop as it would on a production AWS server.

## Networking
Docker creates an isolated internal network for these containers.
Notice how the Python Orchestrator connects to the Java backend:
`JAVA_BACKEND_URL=http://backend:8080/api/internal/execute`
Instead of using `localhost`, it uses the service name `backend`. Docker's internal DNS automatically routes the traffic securely.
