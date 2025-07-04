import redis
import os
import json

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
redis_client = redis.Redis.from_url(REDIS_URL)

def cache_indicator(key: str, value: dict, expire: int = 3600):
    redis_client.set(key, json.dumps(value), ex=expire)

def get_cached_indicator(key: str):
    data = redis_client.get(key)
    if data:
        return json.loads(data)
    return None
