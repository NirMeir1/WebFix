import os
from dotenv import load_dotenv
# from backend.redis.cache_manager import CacheManager

load_dotenv()

redis_config = {
    "host": os.getenv("REDIS_HOST"),
    "port": int(os.getenv("REDIS_PORT")),
    "username": os.getenv("REDIS_USERNAME"),
    "password": os.getenv("REDIS_PASSWORD")
}

# Temporarily disable external Redis caching due to connection issues.
class DummyCache:
    async def run(self, url: str, report_type: str, email: str, gpt_func):
        output = await gpt_func()
        return False, output

cache = DummyCache()
