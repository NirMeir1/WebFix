import redis
import json
from urllib.parse import urlparse, urlunparse

class RedisCacheHandler:
    def __init__(self, host, port, username, password):
        self.client = redis.Redis(
            host=host,
            port=port,
            username=username,
            password=password,
            decode_responses=True,
        )
        self.ttl = 86400  # 24h

    def _get_base_url(self, url: str) -> str:
        parsed = urlparse(url)
        return urlunparse((parsed.scheme, parsed.netloc, parsed.path, '', '', ''))

    def get(self, url: str):
        value = self.client.get(url)
        if value:
            data = json.loads(value)
            return "Message Type A", data["gpt_output"]
        return None, None

    def set(self, data: dict):
        url = data["url"]
        value = json.dumps(data)
        self.client.setex(url, self.ttl, value)
        base_url = self._get_base_url(url)
        self.client.sadd("known_base_urls", base_url)

    def classify_url(self, url: str):
        print(f"Checking Redis key for URL: {url}")
        if not isinstance(url, str) or not url:
            raise ValueError(f"Invalid URL: {url}")
    
        if self.client.get(url):
            return "A"

        base_url = self._get_base_url(url)
        if self.client.sismember("known_base_urls", base_url):
            return "B"

        return "Z"