# Local Testing Guide

## Prerequisites
Ensure Docker and Docker Compose are installed on your machine.

## Step 1: Configuration
1. Copy the `.env.example` file to `.env` in the root directory.
2. Fill in your real `KITE_API_KEY` and `KITE_API_SECRET`.
3. (Optional) Adjust your `INITIAL_TRADING_CAPITAL` if you want to test the risk engine with a different amount.

## Step 2: Launch
From the root directory (`/lean`), run:
```bash
docker-compose up -d --build
```
This will compile the Java code, install Python dependencies, build the React UI, and start all 5 containers in the background (`-d`).

## Step 3: Monitor
To see the logs of the Python AI Orchestrator:
```bash
docker-compose logs -f ai_orchestrator
```
To see the Java Backend logs:
```bash
docker-compose logs -f backend
```

## Step 4: Access the UI
Open your browser and navigate to:
`http://localhost:3000`

You will see the Premium Glassmorphism Dashboard streaming live logs and displaying your protected portfolio.

## Step 5: Shut Down
To stop the bot and tear down the containers:
```bash
docker-compose down
```
