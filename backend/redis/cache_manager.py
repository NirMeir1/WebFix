from backend.redis.redis_cache import RedisCacheHandler

class CacheManager:
    def __init__(self, redis_config: dict):
        self.cache = RedisCacheHandler(**redis_config)

    async def run(self, url: str, report_type: str, industry: str, email: str, gpt_func):
        classification = self.cache.classify_url(url)

        if classification == "A":
            message, gpt_output = self.cache.get(url)
            return message, gpt_output

        gpt_output = await gpt_func()

        self.cache.set({
            "url": url,
            "report_type": report_type,
            "industry": industry,
            "email": email,
            "gpt_output": gpt_output
        })

        return f"Message Type {classification}", gpt_output