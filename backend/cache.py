from datetime import datetime, timedelta

# in-memory cache to store responses using python dictionary for a limited time 
# period (TTL) to avoid repeated API calls for the same URL
CACHE = {}
TTL_SECONDS = 3600  # 1 hour

def is_recent_response(url: str) -> bool:
    entry = CACHE.get(url)
    if not entry:
        return False
    return (datetime.now() - entry["timestamp"]) < timedelta(seconds=TTL_SECONDS)

def get_cached_response(url: str) -> str:
    return CACHE[url]["response"]

def save_response(url: str, response: str):
    CACHE[url] = {
        "response": response,
        "timestamp": datetime.now()
    }