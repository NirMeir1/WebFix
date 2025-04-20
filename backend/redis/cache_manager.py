from backend.redis.redis_cache import RedisCacheHandler

class CacheManager:
    def __init__(self, redis_config: dict):
        self.cache = RedisCacheHandler(**redis_config)

    async def run(self, url: str, report_type: str, email: str, gpt_func):
        if self.cache.is_cached(url, report_type):
            output = self.cache.get_cached_output(url, report_type)
            return True, output  # is_cached = True

        output = await gpt_func()

        self.cache.set({
            "url": url,
            "report_type": report_type,
            "email": email,
            "gpt_output": output
        })

        return False, output  # is_cached = False