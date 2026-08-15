import os
import json
import redis
from kiteconnect import KiteTicker
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path='../../.env.example') # Adjust for real .env in production

# Configuration
API_KEY = os.getenv("KITE_API_KEY", "your_api_key_here")
# Normally access_token is fetched dynamically from the DB session.
# For the standalone ticker script, it should be passed securely or read from the database.
ACCESS_TOKEN = os.getenv("KITE_ACCESS_TOKEN", "your_access_token_here") 

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

# Initialize Redis client
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

# Initialize KiteTicker
kws = KiteTicker(API_KEY, ACCESS_TOKEN)

# List of instrument tokens to subscribe to
INSTRUMENT_TOKENS = [738561, 5633] # Example tokens (e.g. Reliance, ACC)

def on_ticks(ws, ticks):
    """Callback to receive ticks."""
    for tick in ticks:
        instrument_token = tick.get('instrument_token')
        # Publish tick data to a Redis channel specific to the instrument
        channel = f"market_data:ticks:{instrument_token}"
        # Convert tick dictionary to JSON string
        tick_json = json.dumps(tick)
        redis_client.publish(channel, tick_json)
        print(f"Published tick for {instrument_token} to {channel}")

def on_connect(ws, response):
    """Callback on successful connect."""
    print("Successfully connected to Kite WebSocket.")
    # Subscribe to a list of instrument_tokens
    ws.subscribe(INSTRUMENT_TOKENS)
    # Set the mode to 'full' for complete market depth, or 'quote'/'ltp'
    ws.set_mode(ws.MODE_FULL, INSTRUMENT_TOKENS)

def on_close(ws, code, reason):
    """Callback on connection close."""
    print(f"Connection closed: {code} - {reason}")

def on_error(ws, code, reason):
    """Callback on connection error."""
    print(f"Connection error: {code} - {reason}")

# Assign callbacks
kws.on_ticks = on_ticks
kws.on_connect = on_connect
kws.on_close = on_close
kws.on_error = on_error

if __name__ == "__main__":
    print("Starting Market Data Service...")
    # Infinite loop to keep connection alive
    # Use kws.connect(threaded=True) if you need to run other tasks in the main thread
    kws.connect()
