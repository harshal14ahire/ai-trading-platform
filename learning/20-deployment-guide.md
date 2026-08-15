# Deployment Guide

This guide explains how to deploy the platform for free (or nearly free).

## 1. Deploying the Frontend to GitHub Pages (Free)
The frontend is a static React Vite application. 
1. The `vite.config.js` is already configured with `base: '/ai-trading-platform/'`.
2. Push your code to your GitHub repo.
3. In GitHub, go to your repository Settings -> Pages.
4. Set the source to GitHub Actions.
5. Create a standard Vite deployment action or manually run `npm run build` and push the `dist` folder to a `gh-pages` branch.

## 2. Deploying the Java Backend (Free Tier vs. Paid)
You can deploy the Spring Boot backend to platforms like **Render**, **Koyeb**, or **Railway**.
- **Koyeb** offers a generous free tier for Docker containers.
- **Render** offers free Web Services.

### WARNING FOR ALGO TRADING
Free tiers will spin down (sleep) your server if there are no HTTP requests for 15 minutes.
**If your server is asleep when the Python Orchestrator finds a trade and sends the API request, the trade will FAIL because the server takes 30-60 seconds to wake up.**
For a live algorithmic bot, you *must* have an "Always On" backend. You should pay the ~$5/month for the basic paid tier on Render, or deploy to an AWS EC2 Nano instance.

## 3. Database Hosting (Free)
Since we have migrated to **MongoDB**, you can use **MongoDB Atlas**.
1. Create a free cluster on MongoDB Atlas.
2. Get the connection URI.
3. Put it in your backend's environment variables (`SPRING_DATA_MONGODB_URI`).

## 4. Deploying the Python Daemon
The Python Orchestrator (`ai_agents/orchestrator.py`) is an infinite loop daemon. It does not respond to HTTP requests, so it cannot be hosted on standard Serverless/Web hosting (like Heroku web dynos).
It must be hosted as a **Worker Process** (Render offers Background Workers) or run inside a Docker container on an EC2 instance.
