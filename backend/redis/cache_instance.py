import os
from dotenv import load_dotenv
from backend.redis.cache_manager import CacheManager

load_dotenv()

redis_config = {
    "host": os.getenv("REDIS_HOST"),
    "port": int(os.getenv("REDIS_PORT")),
    "username": os.getenv("REDIS_USERNAME"),
    "password": os.getenv("REDIS_PASSWORD")
}

cache = CacheManager(redis_config)
