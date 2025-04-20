import pytest
import fakeredis

from backend.redis.redis_cache import RedisCacheHandler
from backend.redis.cache_manager import CacheManager

# --- Fixtures ---------------------------------------------------------

@pytest.fixture
def redis_handler():
    # Create an instance and replace its client with a fake Redis client.
    handler = RedisCacheHandler(host="localhost", port=6379, username="", password="")
    handler.client = fakeredis.FakeRedis(decode_responses=True)
    return handler

@pytest.fixture
def cache_manager():
    # Create a CacheManager instance and replace its internal Redis client.
    redis_config = {
        "host": "localhost",
        "port": 6379,
        "username": "",
        "password": ""
    }
    cm = CacheManager(redis_config)
    cm.cache.client = fakeredis.FakeRedis(decode_responses=True)
    return cm

# --- Unit Tests for RedisCacheHandler ---------------------------------

def test_set_and_get(redis_handler):
    # Prepare test data
    test_data = {
        "url": "http://example.com/path?query=1",
        "report_type": "basic",
        "email": "test@example.com",
        "gpt_output": "Test output"
    }
    # Set data and then retrieve it.
    redis_handler.set(test_data)
    message, output = redis_handler.get(test_data["url"])
    
    assert message == "Message Type A"
    assert output == "Test output"

def test_classify_url(redis_handler):
    url = "http://example.com/path?query=1"
    
    # Initially, no key or base URL exists.
    classification = redis_handler.classify_url(url)
    assert classification == "Z"
    
    # After setting data, the exact URL key exists.
    test_data = {
        "url": url,
        "report_type": "basic",
        "email": "test@example.com",
        "gpt_output": "Output A"
    }
    redis_handler.set(test_data)
    classification = redis_handler.classify_url(url)
    assert classification == "A"
    
    # Delete the full URL key to simulate only the base URL being known.
    redis_handler.client.delete(url)
    classification = redis_handler.classify_url(url)
    assert classification == "B"

# --- Integration Test for CacheManager -------------------------------

@pytest.mark.asyncio
async def test_cache_manager_run(cache_manager):
    url = "http://example.com/path?query=1"
    report_type = "basic"
    email = "test@example.com"
    
    # Define a dummy async GPT function.
    async def dummy_gpt():
        return "Dummy GPT output"
    
    # First call should invoke the GPT function (cache miss).
    message, output = await cache_manager.run(url, report_type, email, dummy_gpt)
    assert output == "Dummy GPT output"
    # When not cached, classify_url returns "Z" so the returned message is based on that.
    assert message == "Message Type Z"
    
    # Second call should hit the cache.
    message2, output2 = await cache_manager.run(url, report_type, email, dummy_gpt)
    assert output2 == "Dummy GPT output"
    # When retrieved from cache, get() returns "Message Type A".
    assert message2 == "Message Type A"