# Kite Connect API Overview

## What it is
Kite Connect is a set of REST-like APIs that provide programmatic access to data and execution capabilities on Zerodha's trading platform.

## Why it exists
It allows retail and institutional traders to build algorithmic trading systems, bypassing the manual UI of the Kite web or mobile application.

## How it works
The API provides standard HTTP endpoints for operations like:
- `GET /portfolio/holdings`: Retrieve current stock holdings.
- `GET /portfolio/positions`: Retrieve current intra-day/overnight positions.
- `POST /orders/:variety`: Place a new order.

Responses are returned in JSON format. The Java SDK (`kiteconnect-4.0.1`) wraps these HTTP calls into convenient Java objects.

## Security Considerations
API requests must include authentication headers (`X-Kite-Version` and an `Authorization` token). The most critical security element is ensuring that the `api_secret` is never exposed, as it is used to cryptographically sign the login process.

## Trading Considerations
We must strictly adhere to the 10 orders per second rate limit. Exceeding this will result in HTTP 429 exceptions and could lead to API access revocation.
