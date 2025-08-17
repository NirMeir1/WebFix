import redis
import json
from urllib.parse import urlparse, urlunparse

class RedisCacheHandler:
    def __init__(self, host: str, port: int, username: str, password: str):
        self.client = redis.Redis(
            host=host,
            port=port,
            username=username,
            password=password,
            decode_responses=True,
        )
        self.ttl = 86400 * 7  # 7 days

    def _get_base_url(self, url: str) -> str:
        parsed = urlparse(url)
        return urlunparse((parsed.scheme, parsed.netloc, parsed.path, '', '', ''))

    def get_cached_output(self, url: str, report_type: str):
        """
        Returns GPT output if exists in cache, else None.
        """
        try:
            raw = self.client.hget(url, report_type)
            if raw:
                data = json.loads(raw)
                return data.get("gpt_output")
        except json.JSONDecodeError:
            pass
        return None

    def is_cached(self, url: str, report_type: str) -> bool:
        return self.client.hexists(url, report_type)

    def set(self, data: dict):
        url = data.get("url")
        report_type = data.get("report_type")
        if not url or not report_type:
            raise ValueError("Missing 'url' or 'report_type' in data")

        value = json.dumps(data)
        self.client.hset(url, report_type, value)

        if self.client.ttl(url) == -1:
            self.client.expire(url, self.ttl)

        base_url = self._get_base_url(url)
        self.client.sadd("known_base_urls", base_url)
