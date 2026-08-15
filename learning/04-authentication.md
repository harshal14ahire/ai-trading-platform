# Authentication in Kite Connect

## What it is
Authentication is the process of proving a user's identity to the Kite Connect servers. Kite uses an OAuth 2.0-style flow requiring manual user intervention.

## Why it exists
SEBI regulations mandate that broker APIs cannot support headless, silent logins (such as permanent API keys or infinite refresh tokens) for retail algos. A user must manually authenticate (usually daily via 2FA) to explicitly authorize the algorithm to trade on their behalf for that session.

## How it works
1. **Redirect**: The Spring Boot backend generates a login URL (`kiteSdk.getLoginURL()`) and redirect the user.
2. **Login**: The user logs in at `kite.zerodha.com`.
3. **Callback**: Zerodha redirects the user back to our backend (`/api/auth/callback`) with a `request_token`.
4. **Exchange**: The backend combines the `request_token` with the highly confidential `api_secret` to generate an `access_token`.
5. **Persistence**: The `access_token` is stored in the PostgreSQL database (`broker_sessions` table) and used for all subsequent API calls that day.

## Common Mistakes
- Storing the `api_secret` in the frontend code. It must ALWAYS remain on the backend.
- Failing to handle expired `access_token` exceptions gracefully. The system should halt trading safely if the session expires.
