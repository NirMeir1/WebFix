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
        self.ttl = 86400  # 24 hours

    def _get_base_url(self, url: str) -> str:
        parsed = urlparse(url)
        return urlunparse((parsed.scheme, parsed.netloc, parsed.path, '', '', ''))

    def get(self, url: str, report_type: str):
        value = self.client.hget(url, report_type)
        if value:
            try:
                data = json.loads(value)
                return "Message Type A", data.get("gpt_output")
            except json.JSONDecodeError:
                return None, None
        return None, None

    def set(self, data: dict):
        url = data.get("url")
        report_type = data.get("report_type")
        if not url or not report_type:
            raise ValueError("Missing 'url' or 'report_type' in data")

        key = url
        field = report_type
        value = json.dumps(data)
        self.client.hset(key, field, value)

        # Set TTL only once per hash key (optional: only if key is new)
        if self.client.ttl(key) == -1:
            self.client.expire(key, self.ttl)

        base_url = self._get_base_url(url)
        self.client.sadd("known_base_urls", base_url)

    def classify_url(self, url: str, report_type: str):
        print(f"Checking Redis hash for URL: {url} and report_type: {report_type}")
        if not isinstance(url, str) or not url:
            raise ValueError(f"Invalid URL: {url}")

        if self.client.hget(url, report_type):
            return "A"

        base_url = self._get_base_url(url)
        if self.client.sismember("known_base_urls", base_url):
            return "B"

        return "Z"