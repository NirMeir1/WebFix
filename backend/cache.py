import json
import logging
from datetime import datetime, timedelta
from typing import Dict

logger = logging.getLogger(__name__)

CACHE_FILE = "cache.json"  # File to store cached responses
TTL_SECONDS = 3600  # 1 hour

# Cache variable, but won't load until explicitly called
CACHE = {}

from pydantic.networks import HttpUrl

def normalize_url(url) -> str:
    # Ensure the URL is of type HttpUrl or string, and convert it to a string if necessary
    if isinstance(url, HttpUrl):
        url = str(url)  # Convert HttpUrl to string
    elif not isinstance(url, str):
        raise ValueError(f"Expected a string or HttpUrl, but got: {type(url)} for URL: {url}")
    return url.strip().lower() 

def load_cache() -> Dict:
    try:
        with open(CACHE_FILE, "r") as f:
            cache = json.load(f)
            logger.info("Cache loaded from file.")
            return cache
    except FileNotFoundError:
        logger.warning("Cache file not found. Starting with empty cache.")
        return {}
    except Exception as e:
        logger.error(f"Error loading cache: {e}")
        return {}

def save_cache():
    try:
        logger.info("Convert all cache dictionary keys to strings before saving to file.")
        cache_with_str_keys = {normalize_url(url): data for url, data in CACHE.items()}
        with open(CACHE_FILE, "w") as f:
            json.dump(cache_with_str_keys, f, default=str)
            logger.info("Cache saved to file.")
    except Exception as e:
        logger.error(f"Error saving cache: {e}")

def initialize_cache():
    global CACHE
    logger.info("Load the cache every time the function is called")
    CACHE = load_cache()

def is_recent_response(url: str) -> bool:
    normalized_url = normalize_url(url)
    entry = CACHE.get(normalized_url)
    if not entry:
        logger.info(f"No cached entry found for URL: {url}")
        return False
    try:
        timestamp = datetime.fromisoformat(entry["timestamp"])
        is_recent = (datetime.now() - timestamp) < timedelta(seconds=TTL_SECONDS)
        logger.info(f"Cache hit for URL: {url} (Recent: {is_recent})")
        return is_recent
    except Exception as e:
        logger.error(f"Invalid timestamp for URL {url}: {e}")
        return False

def get_cached_response(url: str) -> str:
    normalized_url = normalize_url(url)
    logger.info(f"Retrieving cached response for URL: {url}")
    return CACHE[normalized_url]["response"]

def save_response(url: str, response: str):
    normalized_url = normalize_url(url)
    CACHE[normalized_url] = {
        "response": response,
        "timestamp": datetime.now().isoformat()
    }
    logger.info(f"Saved new response to cache for URL: {url}")
    save_cache()