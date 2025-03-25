import json
import logging
from datetime import datetime, timedelta
from typing import Dict
from pydantic import HttpUrl

logger = logging.getLogger(__name__)

BASIC_CACHE_FILE = "basic_report_cache.json"
DEEP_CACHE_FILE = "deep_report_cache.json"
TTL_SECONDS = 86400  # 24 hours

basic_cache = {}
deep_cache = {}

def normalize_url(url: HttpUrl) -> str:
    return str(url).strip().lower()

def load_cache(file_name: str) -> Dict:
    try:
        with open(file_name, "r") as f:
            logger.info(f"Cache loaded from {file_name}")
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        logger.warning(f"Cache file {file_name} not found or empty. Starting new cache.")
        return {}

def save_cache(cache: Dict, file_name: str):
    with open(file_name, "w") as f:
        json.dump(cache, f)
        logger.info(f"Cache saved to {file_name}")

def initialize_caches():
    global basic_cache, deep_cache
    basic_cache = load_cache(BASIC_CACHE_FILE)
    deep_cache = load_cache(DEEP_CACHE_FILE)

def is_recent_response(url: HttpUrl, report_type: str) -> bool:
    """ Choose cache based on report_type """
    cache = basic_cache if report_type == "basic" else deep_cache
    entry = cache.get(normalize_url(url))
    if entry:
        timestamp = datetime.fromisoformat(entry["timestamp"])
        recent = (datetime.now() - timestamp) < timedelta(seconds=TTL_SECONDS)
        logger.info(f"Recent response check for {url}: {recent} (Type: {report_type})")
        return recent
    return False

def is_basic_cached(url: HttpUrl) -> bool:
    """ Check if URL is cached in the basic report cache """
    cached = normalize_url(url) in basic_cache
    logger.info(f"Basic cache existence check for {url}: {cached}")
    return cached

def get_cached_response(url: HttpUrl, report_type: str) -> str:
    """ Retrieve cached response based on report_type """
    cache = basic_cache if report_type == "basic" else deep_cache
    logger.info(f"Fetching cached response for {url} (Type: {report_type})")
    return cache[normalize_url(url)]["response"]

def save_response(url: HttpUrl, report_type: str, response: str):
    """ Save response to the appropriate cache (basic or deep) """
    cache = basic_cache if report_type == "basic" else deep_cache
    cache[normalize_url(url)] = {
        "response": response,
        "timestamp": datetime.now().isoformat()
    }
    save_cache(cache, BASIC_CACHE_FILE if report_type == "basic" else DEEP_CACHE_FILE)